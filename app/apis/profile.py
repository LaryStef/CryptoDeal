import typing as t

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

from ..database.postgre import services
from ..database.postgre.models import Session, User
from ..utils.decorators import authorization_required
from ..utils.JWT import validate_token
from ..utils.aliases import RESTError


api = Namespace("profile", path="/profile/")

_UserData: t.TypeAlias = dict[
    str, str | dict[str, str | int] | list[dict[str, str | bool]]
]


@api.route("/")
class Profile(Resource):
    @authorization_required("access")
    def get(self) -> _UserData | RESTError:
        try:
            # response example
            # {
            #     "userData": {
            #         "uuid": "uuid",
            #         "profile": {
            #             "name": "Chirill",
            #             "alienNumber": 1,
            #             "role": "user",
            #             "email": "poopka06@gmail.com",
            #             "registerDate": "2024-07-09 20:52:41.792133"
            #         },
            #         "sessions": [
            #             {
            #                 "sessionId": "5ZB7k7c7hxr9KcX2",
            #                 "device": "Chrome, Windows10",
            #                 "lastActivity": "2024-07-30 19:56:41.192498",
            #                 "isCurrent": false
            #             },
            #             {
            #                 "sessionId": "vLEiYUtkmK8DHZWg",
            #                 "device": "Chrome, Linux",
            #                 "lastActivity": "2024-08-04 20:27:41.80115",
            #                 "isCurrent": true
            #             }
            #         ]
            #     }
            # }

            refresh_token: str | None = request.cookies.get("refresh_token")
            refresh_payload: t.Any = validate_token(token=refresh_token,
                                                    type="refresh")
            access_token: str | None = request.cookies.get("access_token")
            access_payload: t.Any = validate_token(token=access_token,
                                                   type="access")

            if access_payload is None or refresh_payload is None:
                raise BadRequest

            current_session_id: str = refresh_payload.get("jti", "")
            uuid: str = access_payload.get("uuid", "")

            user: User = services.get(fields=[
                User.alien_number,
                User.name,
                User.email,
                User.role,
                User.register_date
            ], uuid=uuid)
            sessions: list[Session] = services.get(Session, fields=[
                Session.session_id,
                Session.device,
                Session.last_activity
            ], many=True, user_id=uuid)

            user_data: _UserData = {
                "id": uuid,
                "profile": {
                    "name": user.name,
                    "alienNumber": user.alien_number,
                    "role": user.role,
                    "email": user.email,
                    "registerDate": str(user.register_date)
                },
                "sessions": []
            }

            for session in sessions:
                user_data.get("sessions").append(
                    {
                        "sessionId": session.session_id,
                        "device": session.device,
                        "lastActivity": session.last_activity.strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        "isCurrent": session.session_id == current_session_id
                    }
                )

            return {
                "userData": user_data
            }, 200

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400
