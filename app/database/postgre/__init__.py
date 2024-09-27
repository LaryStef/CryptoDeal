from flask_sqlalchemy import SQLAlchemy

from app.database.postgre.utc_time import utcnow


db: SQLAlchemy = SQLAlchemy()

__all__ = [
    "db",
    "utcnow"
]
