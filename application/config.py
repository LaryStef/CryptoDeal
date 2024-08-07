import os
from dotenv import load_dotenv

from flask import Config


load_dotenv()


class AppConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://postgres:{os.getenv('DATABASE_PASSWORD')}@localhost:5432/postgres"  # noqa F501
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USE_SSL: bool = True
    MAIL_USERNAME: str | None = os.getenv("MAIL")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: tuple[str, str | None] = ("CryptoDeal",
                                                   os.getenv("MAIL"))
    # cooldown and cooldownRec in auth.js must be same or longer
    MAIL_CODE_COOLDOWN: int = 20
    MAIL_CODE_VERIFY_ATTEMPTS: int = 3
    MAIL_CODE_REFRESH_ATTEMTPTS: int = 3
    REGISTER_LIFETIME: int = 1200
    RESTORE_LIFETIME: int = 1200
    # restore_cooldown must be less then restore_lifetime
    ACCESS_TOKEN_LIFETIME: int = 300
    RESTORE_COOLDOWN: int = 2000
    REFRESH_TOKEN_LIFETIME: int = 12000
    JWT_ENCODING_ALGORITHM: str = "HS256"
