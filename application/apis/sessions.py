import typing as t

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

from ..database.postgre import services
from ..database.postgre.models import Session
from ..utils.decorators import authorization_required
from ..utils.JWT import validate_token

api = Namespace("sessions", path="/sessions/")


@api.route("/<string:id_>")
class Sessions(Resource):
    @authorization_required("access")
    def delete(self, id_: str):
        try:
            access_token: str = request.cookies.get("access_token", "")
            access_payload: t.Any = validate_token(token=access_token,
                                                   type="access")

            if access_payload is None:
                raise BadRequest
            uuid: str | None = access_payload.get("uuid")

            if (id_ == "all"):
                refresh_token: str = request.cookies.get("refresh_token", "")
                refresh_payload: t.Any = validate_token(token=refresh_token,
                                                        type="refresh")

                if refresh_payload is None:
                    raise BadRequest

                session_id: str = refresh_payload.get("jti", "")

                services.delete_exclude(
                    table=Session,
                    column=Session.session_id,
                    exclude=[session_id],
                    user_id=uuid
                )
                return "OK", 200

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
