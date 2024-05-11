from flask import Blueprint, render_template
from flask_mail import Message

from .database.redisdb import rediska
from .mail import mail


main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", title="Homepage"), 200


@main.route("/send_message/<code>")
def send_message(code):
    message = Message(f"Your secret code: {code}", recipients=["timurkotov1999@gmail.com"])
    mail.send(message)
    return f"i guess message sent with code: {code}", 200


@main.route("/test")
def test():
    rediska.set("23amogusa", "pop4pop")
    return render_template("test.html"), 200
