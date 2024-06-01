from time import time

from flask_restx import Namespace, Resource
from flask import request, make_response
from werkzeug.exceptions import BadRequest
from bcrypt import checkpw

from ..config import AppConfig
from ..shemas import RegisterSchema, LoginSchema
from ..database.postgre.models import User
from ..database.postgre.services import get, add_user
from ..database.redisdb import rediska
from ..database.redisdb.services import create_register_request, refresh_register_code, increase_verify_attempts



api = Namespace("auth", path="/auth/")


@api.route("/sign-up")
class Sign_up(Resource):
    def post(self):
        try:
            data = request.form.to_dict()
            
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
            
            response = make_response("OK")
            response.status_code = 201
            response.headers["Request-Id"] = create_register_request(data)

            return response
        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such register ID"
                }
            }, 400


@api.route("/refresh-code")
class Refresh_code(Resource):
    def post(self):
        try:
            email = request.json.get("email")
            request_id = request.headers.get("Request-Id")

            register_data = rediska.json().get("register", request_id)

            if register_data is None or register_data.get("email") != email:
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

            refresh_register_code(register_data, request_id)

            response = make_response("OK")
            response.status_code = 200
            return response

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such register ID"
                }
            }, 400


@api.route("/verify-code")
class Verify_code(Resource):
    def post(self):
        try:
            code = request.json.get("code")
            request_id = request.headers.get("Request-Id")

            register_data = rediska.json().get("register", request_id)

            if register_data is None or register_data["deactivation_time"] <= int(time()): 
                raise BadRequest

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
                increase_verify_attempts(register_data, request_id)
                return "Invalid code", 400
                return {
                    "error": {
                        "code": "Bad request",
                        "message": "Invalid code",
                        "details": "Try one more time or get new code"
                    }
                }, 400
            
            add_user(register_data)
            rediska.json().delete("register", request_id)

            response = make_response("OK")
            response.status_code = 200
            response.set_cookie("some-cookie", str(int(time())))
            return response

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data or no such register ID"
                }
            }, 400


@api.route("/sign-in")
class Sign_in(Resource):
    def post(self):
        try:
            data = request.form.to_dict()

            for k, v in data.items():
                data[k] = v.replace(" ", "")

            if LoginSchema().validate(data):
                raise BadRequest
            
            user = get(User, name=data.get("username"))

            if user is not None and checkpw(data.get("password").encode("utf-8"), user.password_hash.encode("utf-8")):
                response = make_response("OK")
                response.status_code = 200
                response.set_cookie("some-cookie", str(int(time())))
                return response
            
            return {
                "error": {
                    "code": "Unauthorized",
                    "message": "Invalid login or password",
                    "details": "Try one more time or restore password"
                }
            }, 401               
            
        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400
