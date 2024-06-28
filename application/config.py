import os
from dotenv import load_dotenv

from flask import Config


load_dotenv()

class AppConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://postgres:{os.getenv('DATABASE_PASSWORD')}@localhost:5432/postgres"
    REDIS_URL: str = "redis://localhost:6380/0"
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USE_SSL: bool = True
    MAIL_USERNAME: str | None = os.getenv("MAIL")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: tuple[str, str | None] = ("CryptoDeal", os.getenv("MAIL"))
    MAIL_CODE_COOLDOWN: int = 20         # cooldown and cooldownRec in auth.js must be same or longer
    MAIL_CODE_VERIFY_ATTEMPTS: int = 3
    MAIL_CODE_REFRESH_ATTEMTPTS: int = 3
    REGISTER_LIFETIME: int = 1200
    RESTORE_LIFETIME: int = 1200
    RESTORE_COOLDOWN: int = 2000         # restore_cooldown must be less then restore_lifetime
