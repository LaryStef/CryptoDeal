from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound, Unauthorized


main: Blueprint = Blueprint("main", __name__)


@main.route("/")
def index() -> tuple[str, int]:
    return render_template("index.html", title="Homepage"), 200


@main.route("/profile")
def profile() -> tuple[str, int]:
    return render_template("profile.html", title="Profile"), 200


# from .database.postgre import services
# from .database.postgre.models import User, Session
# from pprint import pprint
# @main.route("/test")
# def test() -> tuple[str, int]:
#     uuid = "21c89744-ec1c-48ae-b255-f02dbd330f51"

#     u: User = services.get(User, uuid=uuid)

#     user: User = services.get(fields=[
#         User.alien_number,
#         User.name,
#         User.email,
#         User.role,
#         User.register_date
#     ], uuid=uuid)
#     sessions: list[Session] = services.get(Session, fields=[
#         Session.session_id,
#         Session.device,
#         Session.last_activity
#     ], many=True, user_id=uuid)

#     print(u)
#     print(user)
#     print(sessions)

#     user_data: dict[str, str | dict[str, str | int] |
#                     list[dict[str, str]]] = {
#         "id": uuid,
#         "profile": {
#             "name": user.name,
#             "alienNumber": user.alien_number,
#             "role": user.role,
#             "email": user.email,
#             "registerDate": str(user.register_date)
#         },
#         "sessions": []
#     }

#     for session in sessions:
#         user_data.get("sessions").append(
#             {
#                 "sessionId": session.session_id,
#                 "device": session.device,
#                 "lastActivity": session.last_activity
#             }
#         )

#     pprint(user_data)
#     return render_template("test.html"), 200


@main.app_errorhandler(NotFound)
def handle_not_found(e: NotFound) -> tuple[str, int]:
    return render_template("notFound.html", title="Not Found"), 200


@main.app_errorhandler(Unauthorized)
def handle_unauthorized(e: Unauthorized) -> tuple[str, int]:
    return render_template("unauthorized.html", title="Unauthorized"), 200
