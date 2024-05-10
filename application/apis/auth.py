from flask_restx import Namespace, Resource
from flask import request, make_response, jsonify


api = Namespace("auth", path="/auth/")


@api.route("/sign-up")
class Sign_up(Resource):
    def post(self):
        data = request.form
        return make_response(jsonify(data), 200)


@api.route("/sign-in")
class Sign_in(Resource):
    def post(self):
        data = request.form
        return make_response(jsonify(data), 200)
