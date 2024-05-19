from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from ..shemas import RegisterSchema
from ..database.redisdb import rediska
from ..database.postgre.models import User
from ..database.postgre.services import get
from ..database.redisdb.services import create_register_request


api = Namespace("auth", path="/auth/")


@api.route("/sign-up")
class Sign_up(Resource):
    def post(self):
        try:
            data = request.form.to_dict()

            # TODO empty password defence

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
            return "Bad request", 400


@api.route("/sign-in")
class Sign_in(Resource):
    def post(self):
        data = request.form        
        return make_response(jsonify(data), 200)
