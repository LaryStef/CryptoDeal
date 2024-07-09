from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from . import db
from .timestamp import utcnow


class User(db.Model):
    def __init__(
        self,
        uuid: str,
        name: str,
        password_hash: str,
        role: str,
        email: str,
        alien_number: int
    ) -> None:

        self.uuid: Mapped[str] = uuid
        self.name: Mapped[str] = name
        self.password_hash: Mapped[str] = password_hash
        self.role: Mapped[str] = role
        self.email: Mapped[str] = email
        self.alien_number: Mapped[int] = alien_number

    __tablename__ = "user"

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(5), default="user")
    email: Mapped[str] = mapped_column(String(256), unique=True)
    register_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, server_default=utcnow())
    restore_cooldown: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=utcnow(), onupdate=utcnow())
    alien_number: Mapped[int] = mapped_column(Integer, default=0)

    sessions: Mapped[list["Session"]] = relationship(back_populates="user")


class Session(db.Model):
    __tablename__ = "session"

    user_id: Mapped[str] = mapped_column(Integer, ForeignKey("user.uuid"), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36))
    device: Mapped[str] = mapped_column(String(30), default="unknown device")
    last_activity: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=utcnow(), onupdate=utcnow())

    user: Mapped[User] = relationship(back_populates="sessions")
