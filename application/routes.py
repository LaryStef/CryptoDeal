from flask import Blueprint, render_template
from flask_mail import Message

from .mail import mail
# from .database.services import get_user, insert_user



main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", title="Homepage"), 200


@main.route("/send_message/<code>")
def send_message(code):
    message = Message(f"Your secret code: {code}", recipients=["timurkotov1999@gmail.com"])
    mail.send(message)
    return f"i guess message sent with code: {code}", 200

# @main.route("/test")
# def test():
#     insert_user("lapochka3")
#     data = get_user("lapochka3")
#     return render_template("test.html", id = data["uuid"], name = data["user"], password = data["password"])
