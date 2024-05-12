import os
from dotenv import load_dotenv

from flask import Config


load_dotenv()

class AppConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{os.getenv('DATABASE_PASSWORD')}@localhost:5432/postgres"
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL")
    REDIS_URL = "redis://localhost:6379/0"
