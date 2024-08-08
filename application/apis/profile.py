import typing as t

from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest

from ..database.postgre import services
from ..database.postgre.models import Session, User
from ..utils.JWT import validate_token
from ..utils.decorators import authorization_required


api = Namespace("profile", path="/profile/")


@api.route("/")
class Profile(Resource):
    @authorization_required("access")
    def get(self):
        try:
            # response example
            # {
            #     "userData": {
            #         "uuid": 123,
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
            #                 "lastActivity": "2024-07-30 19:56:41.192498"
            #             },
            #             {
            #                 "sessionId": "vLEiYUtkmK8DHZWg",
            #                 "device": "Chrome, Linux",
            #                 "lastActivity": "2024-08-04 20:27:41.80115"
            #             }
            #         ]
            #     }
            # }

            access_token: str | None = request.cookies.get("access_token")
            payload: t.Any = validate_token(token=access_token, type="access")

            if payload is None:
                raise BadRequest
            uuid: str | None = payload.get("uuid")

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

            user_data: dict[str, str | dict[str, str | int] |
                            list[dict[str, str]]] = {
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
                        "lastActivity": str(session.last_activity)
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
