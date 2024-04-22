from flask import Flask

from .routes import main
from .config import AppConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    app.register_blueprint(main)
    
    return app
