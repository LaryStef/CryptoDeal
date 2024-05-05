import os
from dotenv import load_dotenv

from flask import Config


load_dotenv()

class AppConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:^Q06Rmt{@localhost:5432/postgres"
    SECRET_KEY = os.getenv("SECRET_KEY")
