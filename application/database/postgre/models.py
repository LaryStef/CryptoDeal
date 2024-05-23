from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from . import db


class User(db.Model):
    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    salt: Mapped[str] = mapped_column(String(29), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    register_date: Mapped[int] = mapped_column(Integer, nullable=False)
