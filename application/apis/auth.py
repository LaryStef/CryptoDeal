from datetime import datetime, timedelta
from time import time
from typing import Any

from flask_restx import Namespace, Resource
from flask import request, make_response, Response
from werkzeug.exceptions import BadRequest
from redis.exceptions import ResponseError
from bcrypt import checkpw

from ..mail.senders import send_scrf_attention
from ..config import AppConfig
from ..utils.generators import generate_id
from ..utils.JWT import generate_tokens, validate_token
from ..shemas import RegisterSchema, LoginSchema
from ..database.postgre.models import User
from ..database.postgre.services import get, add_user, update_password, add_session, update_session
from ..database.redisdb import rediska
from ..database.redisdb.services import RediskaHandler


api = Namespace("auth", path="/auth/")


@api.route("/sign-in")
class Sign_in(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            data: dict[str, str] = request.form.to_dict()

            for k, v in data.items():
                if k == "device":
                    continue
                data[k] = v.replace(" ", "")

            if LoginSchema().validate(data):
                raise BadRequest
            
            user: User | None = get(User, name=data.get("username"))

            if user is not None and checkpw(data.get("password", "").encode("utf-8"), user.password_hash.encode("utf-8")):
                response: Response = make_response("OK")
                response.status_code = 200

                refresh_token_id: str = generate_id(16)
                access_scrf_token: str = generate_id(32)
                refresh_scrf_token: str = generate_id(32)

                add_session(
                    refresh_id=refresh_token_id,
                    user_id=user.uuid,
                    device=data.get("device")
                )
                access_token, refresh_token = generate_tokens(
                    payload={
                        "uuid": user.uuid,
                        "role": user.role,
                        "email": user.email,
                        "name": user.name,
                        "alien_number": user.alien_number
                    },
                    access_scrf_token=access_scrf_token,
                    refresh_scrf_token=refresh_scrf_token,
                    refresh_id=refresh_token_id
                )

                response.set_cookie(
                    key="access_token",
                    value=access_token
                )
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token
                )
                response.set_cookie(
                    key="access_scrf_token",
                    value=access_scrf_token
                )
                response.set_cookie(
                    key="refresh_scrf_token",
                    value=refresh_scrf_token
                )

                return response
            
            return {
                "error": {
                    "code": "Unauthorized",
                    "message": "Invalid login or password",
                    "details": "Try one more time or restore password"
                }
            }, 401               
            
        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400


@api.route("/register/apply")
class Sign_up(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            data: dict[str, str] = request.form.to_dict()
            
            for k, v in data.items():
                data[k] = v.replace(" ", "")

            if RegisterSchema().validate(data):
                raise BadRequest

            if data.get("email") in rediska.json().get("register", "$..email") or get(User, email=data.get("email")): 
                return {
                    "error": {
                        "code": "Conflict",
                        "message": "Email already taken",
                        "details": "User with this email already exists or he is being registered now"
                    }
                }, 409
            
            if data.get("username") in rediska.json().get("register", "$..username") or get(User, name=data.get("username")):
                return {
                    "error": {
                        "code": "Conflict",
                        "message": "Username already taken",
                        "details": "User with this username already exists or he is being registered now"
                    }
                }, 409
            
            response: Response = make_response("OK")
            response.status_code = 201
            response.headers["Request-Id"] = RediskaHandler.create_register_request(data)

            return response
        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400


@api.route("/register/new-code")
class Refresh_code(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            user_data: dict[str, str] | None = request.json

            if user_data is None:
                raise BadRequest

            email: str = user_data.get("email", "")
            request_id: str | None = request.headers.get("Request-Id")
            register_data: dict[str, str | int] = rediska.json().get("register", request_id)

            if request_id is None or register_data.get("email") != email:
                raise BadRequest

            if register_data.get("refresh_attempts") >= AppConfig.MAIL_CODE_REFRESH_ATTEMTPTS:
                rediska.json().delete("register", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many refresh code requests",
                        "details": "Application for registration has been cancelled"
                    }
                }, 429
            
            if register_data.get("accept_new_request") > int(time()):
                return {
                    "error": {
                        "code": "Too early",
                        "message": "Too frequent refresh code requests",
                        "details": "Try later"
                    }
                }, 425

            RediskaHandler.refresh_register_code(register_data, request_id)

            response: Response = make_response("OK")
            response.status_code = 200
            return response

        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such request ID"
                }
            }, 400


@api.route("/register/verify")
class Verify_code(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            user_data: dict[str, str] | None = request.json
            request_id: str | None = request.headers.get("Request-Id")

            if user_data is None or request_id is None:
                raise BadRequest

            code: str | None = user_data.get("code")

            register_data: dict[str, str | int] = rediska.json().get("register", request_id)

            if code is None or register_data is None:
                raise BadRequest
            
            if register_data["deactivation_time"] <= int(time()):
                return {
                    "error": {
                        "code": "Bad Request",
                        "message": "Application registreation has been cancelled",
                        "details": "It's too many time since you applied for registration"
                    }
                }, 400

            if register_data.get("verify_attempts") >= AppConfig.MAIL_CODE_VERIFY_ATTEMPTS:
                rediska.json().delete("register", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many verify code requests",
                        "details": "Application for registration has been cancelled"
                    }
                }, 429
            
            if register_data.get("code") != code:
                RediskaHandler.increase_verify_attempts("register", register_data, request_id)
                return {
                    "error": {
                        "code": "Bad request",
                        "message": "Invalid code",
                        "details": "Try one more time or get new code"
                    }
                }, 400
            
            id_, alien_number = add_user(register_data)
            rediska.json().delete("register", request_id)

            response: Response = make_response("OK")
            response.status_code = 200

            refresh_token_id: str = generate_id(16)
            access_scrf_token: str = generate_id(32)
            refresh_scrf_token: str = generate_id(32)

            add_session(
                refresh_id=refresh_token_id,
                user_id=id_,
                device=user_data.get("device")
            )
            access_token, refresh_token = generate_tokens(
                payload={
                    "uuid": id_,
                    "role": register_data["role"],
                    "email": register_data["email"],
                    "name": register_data["username"],
                    "alien_number": alien_number
                },
                access_scrf_token=access_scrf_token,
                refresh_scrf_token=refresh_scrf_token,
                refresh_id=refresh_token_id
            )

            response.set_cookie(
                key="access_token",
                value=access_token
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token
            )
            response.set_cookie(
                key="access_scrf_token",
                value=access_scrf_token
            )
            response.set_cookie(
                key="refresh_scrf_token",
                value=refresh_scrf_token
            )

            return response

        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such register ID"
                }
            }, 400


@api.route("/restore/apply")
class Restore(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            user_data: dict[str, str] | None = request.json
            if user_data is None:
                raise BadRequest

            email: str | None = user_data.get("email", "")
            if email is None:
                raise BadRequest

            user: User | None = get(User, email=email)
            if user is None:
                return {
                    "error": {
                        "code": "Not found",
                        "message": "Email not found",
                        "details": "No user with this email"
                    }
                }, 404

            cooldown: int = int(datetime.now().timestamp()) - int(user.restore_date.timestamp() + int(timedelta(hours=3.0).total_seconds()))
            if cooldown < AppConfig.RESTORE_COOLDOWN:
                return {
                    "error": {
                        "code": "Too early",
                        "message": f"Password has been restored recently, try in {(AppConfig.RESTORE_COOLDOWN - cooldown) // 60 + 1} minutes",
                        "details": "Password restore procedure has 10 minutes cooldown"
                    }
                }, 425

            response: Response = make_response("OK")
            response.status_code = 201             
            response.headers["Request-Id"] = RediskaHandler.create_restore_request(email)
            return response

        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400


@api.route("/restore/new-code")
class Restore_new_code(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            user_data: dict[str, str] | None = request.json
            request_id: str | None = request.headers.get("Request-Id")

            if user_data is None or request_id is None:
                raise BadRequest

            email: str | None = user_data.get("email", "")
            
            restore_data: dict[str, str | int] | None = rediska.json().get("password_restore", request_id)

            if restore_data is None or restore_data.get("email") != email:
                raise BadRequest

            if restore_data.get("refresh_attempts") >= AppConfig.MAIL_CODE_REFRESH_ATTEMTPTS:
                rediska.json().delete("password_restore", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many refresh code requests",
                        "details": "Application for password restore has been cancelled"
                    }
                }, 429

            if restore_data.get("accept_new_request") > int(time()):
                return {
                    "error": {
                        "code": "Too early",
                        "message": "Too frequent refresh code requests",
                        "details": "Try later"
                    }
                }, 425

            RediskaHandler.refresh_restore_code(restore_data, request_id)
            response = make_response("OK")
            response.status_code = 200
            return response

        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such request ID"
                }
            }, 400


@api.route("/restore/verify")
class Restore_verify(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            user_data: dict[str, str] | None = request.json

            if user_data is None:
                raise BadRequest
            

            code: str | None = user_data.get("code")
            password: str | None = user_data.get("password")
            request_id: str | None = request.headers.get("Request_Id")

            if not all([code, password, request_id]) or len(password) < 6 or len(password) > 20:
                raise BadRequest

            request_data: dict[str, str | int] = rediska.json().get("password_restore", request_id)

            if request_data is None:
                raise BadRequest
            
            if request_data.get("verify_attempts") >= AppConfig.MAIL_CODE_VERIFY_ATTEMPTS:
                rediska.json().delete("password_restore", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many verify code requests",
                        "details": "Application for registration has been cancelled"
                    }
                }, 429
            
            if request_data.get("code") != code:
                RediskaHandler.increase_verify_attempts("password_restore", request_data, request_id) 
                return {
                    "error": {
                        "code": "Bad request",
                        "message": "Invalid code",
                        "details": "Try one more time or get new code"
                    }
                }, 400

            user: User | None = get(User, email=request_data.get("email"))

            if user is None:
                raise BadRequest
            
            update_password(user, password)
            rediska.json().delete("password_restore", request_id)

            response = make_response("OK")
            response.status_code = 200

            refresh_token_id: str = generate_id(16)
            access_scrf_token: str = generate_id(32)
            refresh_scrf_token: str = generate_id(32)

            add_session(
                refresh_id=refresh_token_id,
                user_id=user.uuid,
                device=user_data.get("device")
            )
            access_token, refresh_token = generate_tokens(
                payload={
                    "uuid": user.uuid,
                    "role": user.role,
                    "email": user.email,
                    "name": user.name,
                    "alien_number": user.alien_number
                },
                access_scrf_token=access_scrf_token,
                refresh_scrf_token=refresh_scrf_token,
                refresh_id=refresh_token_id
            )

            response.set_cookie(
                key="access_token",
                value=access_token
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token
            )
            response.set_cookie(
                key="access_scrf_token",
                value=access_scrf_token
            )
            response.set_cookie(
                key="refresh_scrf_token",
                value=refresh_scrf_token
            )

            return response

        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such request ID"
                }
            }, 400


@api.route("/refresh-tokens")
class Refresh_access(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            scrf_cookie: str | None = request.cookies.get("refresh_scrf_token")
            refresh_token: str | None = request.cookies.get("refresh_token")
            device: str = request.headers.get("Device", "unknown device")
            scrf_header: str | None = request.headers.get("X-SCRF-TOKEN")

            payload: dict[str, Any] | None = validate_token(refresh_token, "refresh")
            if not all([scrf_cookie, scrf_header, payload]):
                raise BadRequest

            if scrf_cookie != scrf_header or scrf_cookie != payload["scrf"]:
                send_scrf_attention(recipient=payload.get("email"), origin=request.headers.get("Origin"))
                return {
                    "error": {
                        "code": "Forbidden",
                        "message": "Invalid scrf token",
                        "details": "Invalid scrf token. Someone tries to get access from your behalf"   
                    }
                }, 403

            user: User | None = get(User, uuid=payload.get("uuid"))
            if user is None:
                raise BadRequest

            refresh_token_id: str = generate_id(16)
            access_scrf_token: str = generate_id(32)
            refresh_scrf_token: str = generate_id(32)

            update_session(
                old_refresh_id=payload.get("jti", ""),
                new_refresh_id=refresh_token_id,
                user_id=payload.get("uuid", ""),
                device=device
            )
            access_token, refresh_token = generate_tokens(
                payload={
                    "uuid": user.uuid,
                    "role": user.role,
                    "email": user.email,
                    "name": user.name,
                    "alien_number": user.alien_number
                },
                access_scrf_token=access_scrf_token,
                refresh_scrf_token=refresh_scrf_token,
                refresh_id=refresh_token_id
            )

            response = make_response("OK")
            response.status_code = 200

            response.set_cookie(
                key="access_token",
                value=access_token
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token
            )
            response.set_cookie(
                key="access_scrf_token",
                value=access_scrf_token
            )
            response.set_cookie(
                key="refresh_scrf_token",
                value=refresh_scrf_token
            )

            return response

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid token or invalid format of data"
                }
            }, 400
