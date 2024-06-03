from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from . import db


class User(db.Model):
    def __init__(self, user_data):
        self.uuid = user_data.get("uuid")
        self.name = user_data.get("username")
        self.password_hash = user_data.get("password_hash")
        self.email = user_data.get("email")
        self.register_date = user_data.get("register_date")
        self.restore_cooldown = user_data.get("restore_cooldown")


    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    register_date: Mapped[int] = mapped_column(Integer)
    restore_cooldown: Mapped[int] = mapped_column(Integer, default=0)
