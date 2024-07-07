from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from flask_mail import Message

from .mail import mail


main: Blueprint = Blueprint("main", __name__)


@main.route("/")
def index() -> tuple[str, int]:
    return render_template("index.html", title="Homepage"), 200 # Text return


@main.route("/test")
def test() -> tuple[str, int]:
    from .mail.senders import send_scrf_attention
    send_scrf_attention("", origin="no origin")
    return render_template("test.html"), 200


@main.app_errorhandler(NotFound)
def handle_not_found(e: NotFound) -> tuple[str, int]:
    return render_template("notFound.html", title="Not Found"), 200
