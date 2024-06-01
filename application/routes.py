from flask import Blueprint, render_template, request
from werkzeug.exceptions import NotFound
from flask_mail import Message
from .mail import mail

from redis.commands.json.path import Path


main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", title="Homepage"), 200


@main.route("/send_message/<code>")
def send_message(code):
    message = Message(f"Your secret code: {code}", recipients=["timurkotov1999@gmail.com"])
    mail.send(message)
    return f"I guess message sent with code: {code}", 200


@main.route("/test")
def test():
    print(request.remote_addr)
    return render_template("test.html"), 200


@main.app_errorhandler(NotFound)
def handle_not_found(e):
    return render_template("notFound.html", title="Not Found"), 200
