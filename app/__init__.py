from celery import Celery
from flask import Flask

from app.apis import api
from app.config import appConfig
from app.database.postgre import db
from app.database.redisdb import rediska
from app.logs import setup_logging
from app.mail import mail
from app.routes import main
from app.tasks import celery_init_app


def create_app() -> tuple[Flask, Celery]:
    app: Flask = Flask(__name__)
    app.config.from_object(appConfig)
    app.register_blueprint(main)

    setup_logging(app)
    db.init_app(app)
    api.init_app(app)
    mail.init_app(app)
    rediska.init_app(app)

    app.extensions["mail"].debug = 0

    celery: Celery = celery_init_app(app)

    if rediska.json().get("register") is None:
        rediska.json().set(name="register", path=".", obj={})
    if rediska.json().get("password_restore") is None:
        rediska.json().set(name="password_restore", path=".", obj={})

    # with app.app_context():
    #     from app.utils.push_test_data import push_cryptocurrencies
    #     db.create_all()
    #     push_cryptocurrencies()

    return app, celery
