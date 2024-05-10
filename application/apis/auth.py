from flask_restx import Namespace, Resource


api = Namespace("auth", path="/auth/")


@api.route("/sign-up")
class Sign_up(Resource):
    def post(self):
        return "OK", 200
