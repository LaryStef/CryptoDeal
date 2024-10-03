from datetime import datetime, timedelta
from time import time
from typing import Any
from uuid import uuid4

from bcrypt import checkpw
from flask import Response, make_response, request
from flask_restx import Namespace, Resource
from redis.exceptions import ResponseError
from werkzeug.exceptions import BadRequest, Unauthorized

from app.config import appConfig
from app.database.postgre.services import PostgreHandler
from app.database.postgre.models import User
from app.database.redisdb.services import RediskaHandler, rediska
from app.shemas import LoginSchema, RegisterSchema
from app.utils.aliases import RESTError
from app.utils.decorators import authorization_required
from app.utils.generators import generate_id
from app.utils.JWT import generate_tokens, validate_token


api = Namespace("auth", path="/auth/")


def set_auth_cookies(
    response: Response,
    access_scrf: str,
    refresh_scrf: str,
    access_token: str,
    refresh_token: str
) -> Response:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=appConfig.ACCESS_TOKEN_LIFETIME,
        samesite="Strict"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=appConfig.REFRESH_TOKEN_LIFETIME,
        httponly=True,
        samesite="Strict"
    )
    response.set_cookie(
        key="access_scrf_token",
        value=access_scrf,
        max_age=appConfig.ACCESS_TOKEN_LIFETIME,
        samesite="Strict"
    )
    response.set_cookie(
        key="refresh_scrf_token",
        value=refresh_scrf,
        max_age=appConfig.REFRESH_TOKEN_LIFETIME,
        samesite="Strict"
    )
    return response


@api.route("/sign-in")
class SignIn(Resource):
    def post(self) -> RESTError | Response:
        try:
            data: dict[str, str] = request.form.to_dict()

            for k, v in data.items():
                if k in ["password", "username"]:
                    data[k] = v.replace(" ", "")

            if LoginSchema().validate(data):
                raise BadRequest

            user: User | None = PostgreHandler.get(
                User,
                name=data.get("username")
            )

            if user is not None and checkpw(
                data.get("password", "").encode("utf-8"),
                user.password_hash.encode("utf-8")
            ):
                response: Response = make_response("OK")
                response.status_code = 200

                refresh_token_id: str = uuid4().__str__()
                access_scrf_token: str = generate_id(32)
                refresh_scrf_token: str = generate_id(32)

                PostgreHandler.add_session(
                    refresh_id=refresh_token_id,
                    user_id=user.uuid,
                    device=request.headers.get("Device", "unknown device")
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

                return set_auth_cookies(
                    response,
                    access_scrf_token,
                    refresh_scrf_token,
                    access_token,
                    refresh_token
                )

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
class SignUp(Resource):
    def post(self) -> RESTError | Response:
        try:
            data: dict[str, str] = request.form.to_dict()

            for k, v in data.items():
                data[k] = v.replace(" ", "")

            if RegisterSchema().validate(data):
                raise BadRequest

            is_email_in_redis: bool = data.get("email") in rediska.json().get(
                "register",
                "$..email"
            )
            is_email_in_postgre: bool = PostgreHandler.get(
                User,
                email=data.get("email")
            )
            if is_email_in_redis or is_email_in_postgre:
                return {
                    "error": {
                        "code": "Conflict",
                        "message": "Email already taken",
                        "details": """
                            User with this email already exists or he is being
                            registered now
                        """
                    }
                }, 409

            usernames_in_redis: list[str] = rediska.json().get(
                "register",
                "$..username"
            )
            is_name_in_redis: bool = data.get("username") in usernames_in_redis
            is_name_in_postgre: bool = PostgreHandler.get(
                User,
                name=data.get("username")
            )
            if is_name_in_redis or is_name_in_postgre:
                return {
                    "error": {
                        "code": "Conflict",
                        "message": "Username already taken",
                        "details": """User with this username already exists
                            or he is being registered now
                        """
                    }
                }, 409

            response: Response = make_response("OK")
            response.status_code = 201
            response.headers["Request-Id"] = \
                RediskaHandler.create_register_request(data)

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
class RefreshCode(Resource):
    def patch(self) -> RESTError | Response:
        try:
            user_data: dict[str, str] | None = request.json

            if user_data is None:
                raise BadRequest

            email: str = user_data.get("email", "")
            request_id: str | None = request.headers.get("Request-Id")
            register_data: dict[str, str | int] = rediska.json().get(
                "register", request_id
            )

            if request_id is None or register_data.get("email") != email:
                raise BadRequest

            if register_data.get("refresh_attempts") >= \
                    appConfig.MAIL_CODE_REFRESH_ATTEMTPTS:
                rediska.json().delete("register", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many refresh code requests",
                        "details": """Application for registration has been
                            cancelled
                        """
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
class VerifyCode(Resource):
    def post(self) -> RESTError | Response:
        try:
            user_data: dict[str, str] | None = request.json
            request_id: str | None = request.headers.get("Request-Id")

            if user_data is None or request_id is None:
                raise BadRequest

            code: str | None = user_data.get("code")

            register_data: dict[str, str | int] = rediska.json().get(
                "register", request_id
            )

            if code is None or register_data is None:
                raise BadRequest

            if register_data["deactivation_time"] <= int(time()):
                return {
                    "error": {
                        "code": "Bad Request",
                        "message": """Application registreation has been
                            cancelled""",
                        "details": """It's too many time since you applied for
                            registration"""
                    }
                }, 400

            if register_data.get("verify_attempts") >= \
                    appConfig.MAIL_CODE_VERIFY_ATTEMPTS:
                rediska.json().delete("register", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many verify code requests",
                        "details": """Application for registration has been
                            cancelled"""
                    }
                }, 429

            if register_data.get("code") != code:
                RediskaHandler.increase_verify_attempts(
                    file="register",
                    data=register_data,
                    request_id=request_id
                )
                return {
                    "error": {
                        "code": "Bad request",
                        "message": "Invalid code",
                        "details": "Try one more time or get new code"
                    }
                }, 400

            id_, alien_number = PostgreHandler.add_user(register_data)
            rediska.json().delete("register", request_id)

            response: Response = make_response("OK")
            response.status_code = 200

            refresh_token_id: str = uuid4().__str__()
            access_scrf_token: str = generate_id(32)
            refresh_scrf_token: str = generate_id(32)

            PostgreHandler.add_session(
                refresh_id=refresh_token_id,
                user_id=id_,
                device=request.headers.get("Device", "unknown device")
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

            return set_auth_cookies(
                response,
                access_scrf_token,
                refresh_scrf_token,
                access_token,
                refresh_token
            )

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
    def post(self) -> RESTError | Response:
        try:
            user_data: dict[str, str] | None = request.json
            if user_data is None:
                raise BadRequest

            email: str | None = user_data.get("email")
            if email is None:
                raise BadRequest

            user: User | None = PostgreHandler.get(User, email=email)
            if user is None:
                return {
                    "error": {
                        "code": "Not found",
                        "message": "Email not found",
                        "details": "No user with this email"
                    }
                }, 404

            cooldown: int = int(datetime.now().timestamp()) \
                - int(user.restore_date.timestamp()) \
                + int(timedelta(hours=3.0).total_seconds())  # because of utc((

            if cooldown < appConfig.RESTORE_COOLDOWN:
                return {
                    "error": {
                        "code": "Too early",
                        "message": f"""Password has been restored recently,
                            try in
                            {(appConfig.RESTORE_COOLDOWN - cooldown) // 60 + 1}
                            minutes
                        """,
                        "details": """Password restore procedure has 10
                            minutes cooldown"""
                    }
                }, 425

            response: Response = make_response("OK")
            response.status_code = 201
            response.headers["Request-Id"] = \
                RediskaHandler.create_restore_request(email)
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
    def patch(self) -> RESTError | Response:
        try:
            user_data: dict[str, str] | None = request.json
            request_id: str | None = request.headers.get("Request-Id")

            if user_data is None or request_id is None:
                raise BadRequest

            email: str | None = user_data.get("email", "")

            restore_data: dict[str, str | int] | None = rediska.json().get(
                "password_restore", request_id
            )

            if restore_data is None or restore_data.get("email") != email:
                raise BadRequest

            if restore_data.get("refresh_attempts") >= \
                    appConfig.MAIL_CODE_REFRESH_ATTEMTPTS:
                rediska.json().delete("password_restore", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many refresh code requests",
                        "details": """Application for password restore has
                            been cancelled"""
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
class RestoreVerify(Resource):
    def post(self) -> RESTError | Response:
        try:
            user_data: dict[str, str] | None = request.json

            if user_data is None:
                raise BadRequest

            code: str | None = user_data.get("code")
            password: str | None = user_data.get("password")
            request_id: str | None = request.headers.get("Request_Id")

            if not all([code, password, request_id]) \
                    or len(password) < 6 \
                    or len(password) > 20:
                raise BadRequest

            request_data: dict[str, str | int] = rediska.json().get(
                "password_restore", request_id
            )

            if request_data is None:
                raise BadRequest

            if request_data.get("verify_attempts") >= \
                    appConfig.MAIL_CODE_VERIFY_ATTEMPTS:
                rediska.json().delete("password_restore", request_id)
                return {
                    "error": {
                        "code": "Too many requests",
                        "message": "Too many verify code requests",
                        "details": """Application for registration has been
                            cancelled"""
                    }
                }, 429

            if request_data.get("code") != code:
                RediskaHandler.increase_verify_attempts(
                    file="password_restore",
                    data=request_data,
                    request_id=request_id
                )
                return {
                    "error": {
                        "code": "Bad request",
                        "message": "Invalid code",
                        "details": "Try one more time or get new code"
                    }
                }, 400

            user: User | None = PostgreHandler.get(
                User,
                email=request_data.get("email")
            )

            if user is None:
                raise BadRequest

            PostgreHandler.update_password(user, password)
            rediska.json().delete("password_restore", request_id)

            response = make_response("OK")
            response.status_code = 200

            refresh_token_id: str = uuid4().__str__()
            access_scrf_token: str = generate_id(32)
            refresh_scrf_token: str = generate_id(32)

            PostgreHandler.add_session(
                refresh_id=refresh_token_id,
                user_id=user.uuid,
                device=request.headers.get("Device", "unknown device")
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

            return set_auth_cookies(
                response,
                access_scrf_token,
                refresh_scrf_token,
                access_token,
                refresh_token
            )

        except (BadRequest, ResponseError):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such request ID"
                }
            }, 400


@api.route("/refresh-tokens")
class RefreshAccess(Resource):
    @authorization_required("refresh")
    def post(self) -> RESTError | Response:
        try:
            refresh_token: str | None = request.cookies.get("refresh_token")
            payload: dict[str, Any] | None = validate_token(
                token=refresh_token,
                type="refresh"
            )

            user: User | None = PostgreHandler.get(
                User,
                uuid=payload.get("uuid")
            )
            if user is None:
                raise BadRequest

            refresh_token_id: str = uuid4().__str__()
            access_scrf_token: str = generate_id(32)
            refresh_scrf_token: str = generate_id(32)

            PostgreHandler.update_session(
                old_refresh_id=payload.get("jti", ""),
                new_refresh_id=refresh_token_id,
                user_id=payload.get("uuid", ""),
                device=request.headers.get("Device", "unknown device")
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

            return set_auth_cookies(
                response,
                access_scrf_token,
                refresh_scrf_token,
                access_token,
                refresh_token
            )

        except (BadRequest, Unauthorized):
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid token or invalid format of data"
                }
            }, 400
