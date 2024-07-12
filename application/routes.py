from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound


main: Blueprint = Blueprint("main", __name__)


@main.route("/")
def index() -> tuple[str, int]:
    return render_template("index.html", title="Homepage"), 200


@main.route("/test")
def test() -> tuple[str, int]:
    from .database.postgre.models import User
    from .database.postgre.services import get
    user = get(User, uuid="be7aad9c-bdeb-449c-9087-fa5f7e62f4e7")
    if user is not None:
        print(user.register_date)
        print(type(user.register_date))
    return render_template("test.html"), 200


@main.app_errorhandler(NotFound)
def handle_not_found(e: NotFound) -> tuple[str, int]:
    return render_template("notFound.html", title="Not Found"), 200
