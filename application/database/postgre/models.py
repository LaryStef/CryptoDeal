from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from . import db


class User(db.Model):    # type: ignore[name-defined]
    def __init__(self, user_data: dict[str, str | int]):
        self.uuid = user_data.get("uuid")    # type: ignore[assignment]
        self.name: Mapped[str] = user_data.get("username")    # type: ignore[assignment]
        self.password_hash: int = user_data.get("password_hash")    # type: ignore[assignment]
        self.email: str | None = user_data.get("email")    # type: ignore[assignment]
        self.register_date: int | None = user_data.get("register_date")    # type: ignore[assignment]
        self.restore_cooldown: int | None = user_data.get("restore_cooldown")    # type: ignore[assignment]


    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    register_date: Mapped[int] = mapped_column(Integer)
    restore_cooldown: Mapped[int] = mapped_column(Integer, default=0)
