from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.database.postgre.utc_time import utcnow


__all__ = [
    "db",
    "utcnow",
    "Base"
]


class Base(DeclarativeBase):
    __abstract__: bool = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


db: SQLAlchemy = SQLAlchemy(model_class=Base)
