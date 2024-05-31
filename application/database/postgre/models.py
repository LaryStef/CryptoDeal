from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from . import db


class User(db.Model):
    def __init__(self, user_data):
        self.uuid = user_data["uuid"]
        self.name = user_data["username"]
        self.password_hash = user_data["password_hash"]
        self.email = user_data["email"]
        self.register_date = user_data["register_date"]


    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    register_date: Mapped[int] = mapped_column(Integer, nullable=False)
