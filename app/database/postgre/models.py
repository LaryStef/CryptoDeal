from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Float
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

        self.uuid: Mapped[str] = uuid
        self.name: Mapped[str] = name
        self.password_hash: Mapped[str] = password_hash
        self.role: Mapped[str] = role
        self.email: Mapped[str] = email
        self.alien_number: Mapped[int] = alien_number


class Session(db.Model):
    __tablename__ = "session"

    session_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.uuid"))
    device: Mapped[str] = mapped_column(String(30), default="unknown device")
    last_activity: Mapped[datetime] = mapped_column(TIMESTAMP,
                                                    server_default=utcnow(),
                                                    onupdate=utcnow())

    def __init__(self, session_id: str, user_id: str, device: str):
        self.session_id: Mapped[str] = session_id,
        self.user_id: Mapped[str] = user_id,
        self.device: Mapped[str] = device


class CryptoCurrency(db.Model):
    __tablename__ = "cryptocurrency"

    currency_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    # january_fst: Mapped[float] = mapped_column(Float, default=0)
    # january_mid: Mapped[float] = mapped_column(Float, default=0)
    # february_fst: Mapped[float] = mapped_column(Float, default=0)
    # february_mid: Mapped[float] = mapped_column(Float, default=0)
    # march_fst: Mapped[float] = mapped_column(Float, default=0)
    # march_mid: Mapped[float] = mapped_column(Float, default=0)
    # april_fst: Mapped[float] = mapped_column(Float, default=0)
    # april_mid: Mapped[float] = mapped_column(Float, default=0)
    # may_fst: Mapped[float] = mapped_column(Float, default=0)
    # may_mid: Mapped[float] = mapped_column(Float, default=0)
    # june_fst: Mapped[float] = mapped_column(Float, default=0)
    # june_mid: Mapped[float] = mapped_column(Float, default=0)
    # july_fst: Mapped[float] = mapped_column(Float, default=0)
    # july_mid: Mapped[float] = mapped_column(Float, default=0)
    # august_fst: Mapped[float] = mapped_column(Float, default=0)
    # august_mid: Mapped[float] = mapped_column(Float, default=0)
    # september_fst: Mapped[float] = mapped_column(Float, default=0)
    # september_mid: Mapped[float] = mapped_column(Float, default=0)
    # october_fst: Mapped[float] = mapped_column(Float, default=0)
    # october_mid: Mapped[float] = mapped_column(Float, default=0)
    # november_fst: Mapped[float] = mapped_column(Float, default=0)
    # november_mid: Mapped[float] = mapped_column(Float, default=0)
    # december_fst: Mapped[float] = mapped_column(Float, default=0)
    # december_mid: Mapped[float] = mapped_column(Float, default=0)

    hour0: Mapped[float] = mapped_column(Float, default=0)
    hour1: Mapped[float] = mapped_column(Float, default=0)
    hour2: Mapped[float] = mapped_column(Float, default=0)
    hour3: Mapped[float] = mapped_column(Float, default=0)
    hour4: Mapped[float] = mapped_column(Float, default=0)
    hour5: Mapped[float] = mapped_column(Float, default=0)
    hour6: Mapped[float] = mapped_column(Float, default=0)
    hour7: Mapped[float] = mapped_column(Float, default=0)
    hour8: Mapped[float] = mapped_column(Float, default=0)
    hour9: Mapped[float] = mapped_column(Float, default=0)
    hour10: Mapped[float] = mapped_column(Float, default=0)
    hour11: Mapped[float] = mapped_column(Float, default=0)
    hour12: Mapped[float] = mapped_column(Float, default=0)
    hour13: Mapped[float] = mapped_column(Float, default=0)
    hour14: Mapped[float] = mapped_column(Float, default=0)
    hour15: Mapped[float] = mapped_column(Float, default=0)
    hour16: Mapped[float] = mapped_column(Float, default=0)
    hour17: Mapped[float] = mapped_column(Float, default=0)
    hour18: Mapped[float] = mapped_column(Float, default=0)
    hour19: Mapped[float] = mapped_column(Float, default=0)
    hour20: Mapped[float] = mapped_column(Float, default=0)
    hour21: Mapped[float] = mapped_column(Float, default=0)
    hour22: Mapped[float] = mapped_column(Float, default=0)
    hour23: Mapped[float] = mapped_column(Float, default=0)
