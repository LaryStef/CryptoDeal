from flask import Flask

from .routes import main
from .config import AppConfig
from .database import db
from .database.services import insert_user, get_user


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    app.register_blueprint(main)
    db.init_app(app)
    
    with app.app_context():
        from .database.models import User
        db.create_all()        

    return app
