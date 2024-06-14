import os
from dotenv import load_dotenv

from flask import Config


load_dotenv()

class AppConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{os.getenv('DATABASE_PASSWORD')}@localhost:5432/postgres"
    REDIS_URL = "redis://localhost:6379/0"
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("CryptoDeal", os.getenv("MAIL"))
    MAIL_CODE_COOLDOWN = 20         # cooldown and cooldownRec in auth.js must be same or longer
    MAIL_CODE_VERIFY_ATTEMPTS = 3
    MAIL_CODE_REFRESH_ATTEMTPTS = 3
    REGISTER_LIFETIME = 1200
    RESTORE_LIFETIME = 1200
    RESTORE_COOLDOWN = 2000         # restore_cooldown must be less then restore_lifetime
