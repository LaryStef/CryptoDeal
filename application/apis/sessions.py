import typing as t

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

from ..database.postgre import services
from ..database.postgre.models import Session
from ..utils.JWT import validate_token
from ..utils.decorators import authorization_required


api = Namespace("sessions", path="/sessions/")


@api.route("/<string:id_>")
class Sessions(Resource):
    @authorization_required("access")
    def delete(self, id_: str):
        try:
            access_token: str | None = request.cookies.get("access_token")
            payload: t.Any = validate_token(token=access_token, type="access")

            if payload is None:
                raise BadRequest
            uuid: str | None = payload.get("uuid")

            if (id_ == "all"):
                services.remove(Session, user_id=uuid)

            services.remove(Session, user_id=uuid, session_id=id_)
            return "OK", 200

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400
