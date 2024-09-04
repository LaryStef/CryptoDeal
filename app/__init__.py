from celery import Celery
from flask import Flask

from .apis import api
from .config import appConfig
from .database.postgre import db
from .database.redisdb import rediska
from .mail import mail
from .routes import main
from .taskQueue import celery_init_app
from .utils.push_test_data import push_cryptocurrencies


def create_app() -> tuple[Flask | Celery]:
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
