from datetime import datetime

from sqlalchemy import TIMESTAMP, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db
from .utc_time import utcnow


class User(db.Model):
    __tablename__ = "user"

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(5), default="user")
    email: Mapped[str] = mapped_column(String(256), unique=True)
    register_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True,
                                                    server_default=utcnow())
    restore_date: Mapped[datetime] = mapped_column(TIMESTAMP,
                                                   server_default=utcnow())
    alien_number: Mapped[int] = mapped_column(Integer, default=0)
    session: Mapped[list["Session"]] = relationship()

    def __init__(
        self,
        uuid: str,
        name: str,
        password_hash: str,
        role: str,
        email: str,
        alien_number: int
    ) -> None:

        self.uuid = uuid
        self.name = name
        self.password_hash = password_hash
        self.role = role
        self.email = email
        self.alien_number = alien_number


class Session(db.Model):
    __tablename__ = "session"

    session_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.uuid"))
    device: Mapped[str] = mapped_column(String(30), default="unknown device")
    last_activity: Mapped[datetime] = mapped_column(TIMESTAMP,
                                                    server_default=utcnow(),
                                                    onupdate=utcnow())

    def __init__(self, session_id: str, user_id: str, device: str):
        self.session_id = session_id,
        self.user_id = user_id,
        self.device = device


class CryptoCurrency(db.Model):
    __tablename__ = "cryptocurrency"

    currency_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    ticker: Mapped[str] = mapped_column(String(8), unique=True)
    time_frame: Mapped[str] = mapped_column(String(16))
    price: Mapped[float] = mapped_column(Float, default=0)
