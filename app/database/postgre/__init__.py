from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, declared_attr

__all__ = [
    "db",
]


class _Base(DeclarativeBase):
    __abstract__: bool = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


db: SQLAlchemy = SQLAlchemy(model_class=_Base)
