from time import time

from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify
from werkzeug.exceptions import BadRequest

from ..config import AppConfig
from ..shemas import RegisterSchema
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
                return "Email already exists", 403
            
            if data.get("username") in rediska.json().get("register", "$..username") or get(User, username=data.get("username")):
                return "Username already exists", 403
            
            response = make_response("OK")
            response.status_code = 201
            response.headers["Request-Id"] = create_register_request(data)

            return response
        except BadRequest:
            return "Invalid data", 400


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
                return "Too many requests", 429
            
            if register_data.get("accept_new_request") > int(time()):
                return "Too early", 425

            refresh_register_code(register_data, request_id)

            response = make_response("OK")
            response.status_code = 200
            return response

        except BadRequest:
            return "Invalid data", 400


@api.route("/verify-code")
class Verify_code(Resource):
    def post(self):
        try:
            code = request.json.get("code")
            request_id = request.headers.get("Request-Id")

            register_data = rediska.json().get("register", request_id)

            if register_data is None: # or register_data["deactivation_time"] <= int(time())
                raise BadRequest

            if register_data.get("verify_attempts") >= AppConfig.MAIL_CODE_VERIFY_ATTEMPTS:
                rediska.json().delete("register", request_id)
                return "Too many requests", 429

            if register_data.get("code") != code:
                increase_verify_attempts(register_data, request_id)
                return "Invalid code", 400

            add_user(register_data)
            rediska.json().delete("register", request_id)

            response = make_response("OK")
            response.status_code = 200
            response.set_cookie("some-cookie", "123")
            return response

        except BadRequest:
            return "Invalid data", 400


@api.route("/sign-in")
class Sign_in(Resource):
    def post(self):
        data = request.form        
        return make_response(jsonify(data), 200)
