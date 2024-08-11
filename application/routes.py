from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound, Unauthorized


main: Blueprint = Blueprint("main", __name__)


@main.route("/")
def index() -> tuple[str, int]:
    return render_template("index.html", title="Homepage"), 200


@main.route("/profile")
def profile() -> tuple[str, int]:
    return render_template("profile.html", title="Profile"), 200


# from .database.postgre import db
# from .database.postgre.models import Session
# from datetime import datetime, timedelta
# from .config import appConfig
# from sqlalchemy import delete, select
# from pprint import pprint
# @main.route("/test")
# def test() -> tuple[str, int]:

#     print(expire)

#     res = db.session.execute(
#         select(Session).filter(Session.last_activity < expire)
#     )

#     db.session.execute(
#         delete(Session).filter(Session.last_activity < expire)
#     )
#     db.session.commit()

#     for s in res.fetchall():
#         pprint(s[0].__dict__)
#     return render_template("test.html"), 200


@main.app_errorhandler(NotFound)
def handle_not_found(e: NotFound) -> tuple[str, int]:
    return render_template("notFound.html", title="Not Found"), 200


@main.app_errorhandler(Unauthorized)
def handle_unauthorized(e: Unauthorized) -> tuple[str, int]:
    return render_template("unauthorized.html", title="Unauthorized"), 200
