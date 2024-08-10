from flask import Flask
from celery import Celery

from .routes import main
from .config import appConfig
from .database.postgre import db
from .apis import api
from .mail import mail
from .taskQueue import celery_init_app
from .database.redisdb import rediska


def create_app() -> tuple[Flask, Celery]:
    app: Flask = Flask(__name__)
    app.config.from_object(appConfig)
    app.register_blueprint(main)

    db.init_app(app)
    api.init_app(app)
    mail.init_app(app)
    rediska.init_app(app)

    celery: Celery = celery_init_app(app)

    app.extensions["mail"].debug = 0

    with app.app_context():
        from .database.postgre.models import User  # noqa: F401
        db.create_all()

    return app, celery
