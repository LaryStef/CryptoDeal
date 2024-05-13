from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import mapped_column, Mapped

from . import db


class User(db.Model):
    uuid: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
