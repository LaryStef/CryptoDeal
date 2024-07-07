from flask_restx import Namespace, Resource


api = Namespace("profile", path="/profile/")

@api.route("/avatar/<uuid:uuid>")
class Avatar(Resource):
    def get(self):
        pass
