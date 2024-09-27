from celery import Celery
from flask import Flask

from app.apis import api
from app.config import appConfig
from app.database.postgre import db
from app.database.redisdb import rediska
from app.mail import mail
from app.routes import main
from app.taskQueue import celery_init_app
from app.utils.push_test_data import push_cryptocurrencies  # noqa F401


def create_app() -> tuple[Flask, Celery]:
    app: Flask = Flask(__name__)
    app.config.from_object(appConfig)
    app.register_blueprint(main)

    db.init_app(app)
    api.init_app(app)
    mail.init_app(app)
    rediska.init_app(app)

    app.extensions["mail"].debug = 0

    celery: Celery = celery_init_app(app)

    with app.app_context():
        from .database.postgre.models import User  # noqa: F401
        db.create_all()
        push_cryptocurrencies()

    return app, celery
