from flask import Config


class AppConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:^Q06Rmt{@localhost:5432/PostgreSQL 16"