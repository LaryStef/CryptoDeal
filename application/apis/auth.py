from time import time

from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from ..config import AppConfig
from ..shemas import RegisterSchema
from ..database.redisdb import rediska
from ..database.postgre.models import User
from ..database.postgre.services import get
from ..database.redisdb.services import create_register_request, refresh_register_code


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

            if data.get("email") in rediska.json().get("register", "$..email"): 
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

            if (register_data.get("email") != email):
                raise BadRequest

            if int(register_data.get("attempts")) >= 10:
                rediska.json().delete("register", request_id)
                return "Too many requests", 429
            
            if int(register_data.get("accept_new_request")) > int(time()):
                return "Too early", 425

            refresh_register_code(register_data, request_id)

            response = make_response("OK")
            response.status_code = 200
            return response

        except BadRequest:
            return "Invalid data", 400


@api.route("/sign-in")
class Sign_in(Resource):
    def post(self):
        data = request.form        
        return make_response(jsonify(data), 200)
