from flask import Flask

from .routes import main
from .config import appConfig
from .database.postgre import db
from .apis import api
from .mail import mail
from .database.redisdb import rediska


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(appConfig)
    app.register_blueprint(main)

    api.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    rediska.init_app(app)

    app.extensions["mail"].debug = 0

    with app.app_context():
        from .database.postgre.models import User  # noqa: F401
        db.create_all()

    return app
