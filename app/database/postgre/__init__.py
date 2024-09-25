from flask_sqlalchemy import SQLAlchemy

from app.database.postgre.utc_time import utcnow
from app.database.postgre.services import PostgreHandler


db: SQLAlchemy = SQLAlchemy()

__all__ = [
    "db",
    "utcnow",
    "PostgreHandler"
]
