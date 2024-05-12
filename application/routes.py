from flask import Blueprint, render_template
from flask_mail import Message
from marshmallow import pre_dump
from redis.commands.json.path import Path
from .database.redisdb import rediska
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


@main.route("/test/<_id>")
def test(_id):
    res = rediska.json().get("register", Path("$.000000000001"))
    print(res)
    
    return render_template("test.html"), 200
