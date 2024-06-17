from datetime import datetime, UTC

from flask_restx import Namespace, Resource
from flask import request, make_response, Response
from werkzeug.exceptions import BadRequest
from redis.exceptions import ResponseError
from bcrypt import checkpw

from ..config import AppConfig
from ..shemas import RegisterSchema, LoginSchema
from ..database.postgre.models import User
from ..database.postgre.services import get, add_user, update_password
from ..database.redisdb import rediska
from ..database.redisdb.services import RediskaHandler


api = Namespace("auth", path="/auth/")


@api.route("/sign-in")
class Sign_in(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            data: dict[str, str] = request.form.to_dict()

            for k, v in data.items():
                data[k] = v.replace(" ", "")

            if LoginSchema().validate(data):
                raise BadRequest
            
            user: User | None = get(User, name=data.get("username"))

            if user is not None and checkpw(data.get("password", "").encode("utf-8"), user.password_hash.encode("utf-8")):
                response: Response = make_response("OK")
                response.status_code = 200
                response.set_cookie("some-cookie", str(int(datetime.now(UTC).timestamp())))
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

            if register_data.get("refresh_attempts") >= AppConfig.MAIL_CODE_REFRESH_ATTEMTPTS:    # type: ignore
                rediska.json().delete("register", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many refresh code requests",
                        "details": "Application for registration has been cancelled"
                    }
                }, 429
            
            if register_data.get("accept_new_request") > int(datetime.now(UTC).timestamp()):    # type: ignore
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
                    "details": "Invalid format of data or no such register ID"
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

            register_data = rediska.json().get("register", request_id)

            if code is None or register_data is None:
                raise BadRequest
            
            if register_data["deactivation_time"] <= int(datetime.now(UTC).timestamp()):
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
            
            add_user(register_data)
            rediska.json().delete("register", request_id)

            response: Response = make_response("OK")
            response.status_code = 200
            response.set_cookie("some-cookie", str(int(datetime.now(UTC).timestamp())))
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

            cooldown: int = user.restore_cooldown - int(datetime.now(UTC).timestamp())
            if cooldown >= 0:
                return {
                    "error": {
                        "code": "Too early",
                        "message": f"Password has been restored recently, try in { cooldown // 60 + 1 } minutes",
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
class RestoreNewCode(Resource):
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

            if restore_data.get("refresh_attempts") >= AppConfig.MAIL_CODE_REFRESH_ATTEMTPTS:    # type: ignore
                rediska.json().delete("password_restore", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many refresh code requests",
                        "details": "Application for password restore has been cancelled"
                    }
                }, 429

            if restore_data.get("accept_new_request") > int(datetime.now(UTC).timestamp()):    # type: ignore
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
                    "details": "Invalid format of data or no such register ID"
                }
            }, 400


@api.route("/restore/verify")
class RestoreVerify(Resource):
    def post(self) -> tuple[dict[str, dict[str, str]], int] | Response:
        try:
            user_data: dict[str, str] | None = request.json

            if user_data is None:
                raise BadRequest
            
            code: str | None = user_data.get("code")
            password: str | None = user_data.get("password")
            request_id: str | None = request.headers.get("Request_Id")

            if password is None or code is None or request_id is None or \
                len(password) < 6 or len(password) > 20:
                raise BadRequest

            request_data = rediska.json().get("password_restore", request_id)

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
            response.set_cookie("some-cookie", str(int(datetime.now(UTC).timestamp())))
            return response

        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such register ID"
                }
            }, 400
