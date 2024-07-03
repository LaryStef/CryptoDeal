from flask import Blueprint, render_template, request
from werkzeug.exceptions import NotFound
from flask_mail import Message

from .mail import mail


main: Blueprint = Blueprint("main", __name__)

@main.route("/")
def index() -> tuple[str, int]:
    return render_template("index.html", title="Homepage"), 200


@main.route("/send_message/<code>")
def send_message(code: int) -> tuple[str, int]:
    message: Message = Message(f"Your secret code: {code}", recipients=["timurkotov1999@gmail.com"])
    mail.send(message)
    return f"I guess message sent with code: {code}", 200




@main.route("/test")
def test() -> tuple[str, int]:
    from .database.postgre.models import Session
    from pprint import pprint
    from .database.postgre.services import get
    id = "23874892"
    sessions_raw: Session = get(Session, uuid=id)
    sessions_data: dict[str, str] = sessions_raw.__dict__
    

    earlier_activity = float("inf")
    for key, value in sessions_data.items():
        if key.startswith("activity") and value < earlier_activity:
            earlier_activity = value
            oldest_session = int(key.replace("activity", ""))
    return render_template("test.html"), 200


@main.app_errorhandler(NotFound)
def handle_not_found(e: NotFound) -> tuple[str, int]:
    return render_template("notFound.html", title="Not Found"), 200
