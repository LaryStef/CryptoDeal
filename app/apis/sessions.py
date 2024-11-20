import typing as t

from flask import Response, make_response, request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

from app.database.postgre.models import Session
from app.database.postgre.services import PostgreHandler
from app.utils.aliases import RESTError
from app.utils.decorators import authorization_required
from app.utils.JWT import validate_token


api = Namespace("sessions", path="/sessions/")


@api.route("/<string:id_>")
class Sessions(Resource):
    @authorization_required("access")
    def delete(
        self, id_: str
    ) -> RESTError | Response | tuple[str, int]:
        try:
            access_token: str = request.cookies.get("access_token", "")
            access_payload: t.Any = validate_token(
                token=access_token,
                type="access"
            )

            if access_payload is None:
                raise BadRequest
            uuid: str | None = access_payload.get("uuid")

            if id_ not in ["all", "my"]:
                PostgreHandler.remove(Session, user_id=uuid, session_id=id_)
                return "OK", 200

            refresh_token: str = request.cookies.get("refresh_token", "")
            refresh_payload: t.Any = validate_token(
                token=refresh_token,
                type="refresh"
            )

            if refresh_payload is None:
                raise BadRequest

            session_id: str = refresh_payload.get("jti", "")

            if id_ == "all":
                PostgreHandler.delete_exclude(
                    table=Session,
                    column=Session.session_id,
                    exclude=[session_id],
                    user_id=uuid
                )
                return "OK", 200

            PostgreHandler.remove(Session, user_id=uuid, session_id=session_id)

            response: Response = make_response("OK")
            response.status_code = 200
            response.set_cookie(key="access_token", value="")
            response.set_cookie(key="access_scrf_token", value="")
            response.set_cookie(key="refresh_token", value="")
            response.set_cookie(key="refresh_scrf_token", value="")

            return response

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400
