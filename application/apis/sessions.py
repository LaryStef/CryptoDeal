from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

from ..database.postgre import services
from ..database.postgre.models import Session
from ..utils.decorators import authorization_required


api = Namespace("sessions", path="/sessions/")


@api.route("/<string:id_>")
class Sessions(Resource):
    @authorization_required("access")
    def delete(self, id_: str):
        try:
            if len(id_) != 16 or not id_.isalnum():
                raise BadRequest

            services.remove(Session, session_id=id_)
            return "OK", 200

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400
