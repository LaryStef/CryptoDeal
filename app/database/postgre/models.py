from datetime import datetime

from sqlalchemy import TIMESTAMP, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db
from .utc_time import utcnow


class User(db.Model):
    __tablename__: str = "User"

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
    wallet: Mapped["Wallet"] = relationship(back_populates="user")

    def __init__(
        self,
        *,
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
    __tablename__: str = "Session"

    # TODO replace session_id UUID
    session_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("User.uuid"))
    device: Mapped[str] = mapped_column(String(30), default="unknown device")
    last_activity: Mapped[datetime] = mapped_column(TIMESTAMP,
                                                    server_default=utcnow(),
                                                    onupdate=utcnow())

    def __init__(self, *, session_id: str, user_id: str, device: str) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.device = device


class CryptoCurrency(db.Model):
    __tablename__: str = "Cryptocurrency"

    ticker: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(4096))
    volume: Mapped[float] = mapped_column(Float, default=0)
    crypto_course: Mapped[list["CryptoCourse"]] = relationship()

    def __init__(
        self,
        *,
        ticker: str,
        name: str,
        description: str,
        volume: float,
    ) -> None:
        self.ticker = ticker
        self.name = name
        self.description = description
        self.volume = volume


class CryptoCourse(db.Model):
    __tablename__: str = "CryptoCourse"

    ID: Mapped[str] = mapped_column(String(16), primary_key=True)
    ticker: Mapped[str] = mapped_column(ForeignKey("Cryptocurrency.ticker"))
    price: Mapped[float] = mapped_column(Float, default=0)
    type_: Mapped[str] = mapped_column("type", String(8))
    number: Mapped[int] = mapped_column(Integer)
    extra: Mapped[str] = mapped_column(String(16), nullable=True)

    def __init__(
        self,
        *,
        ID: str,
        ticker: str,
        price: float,
        type_: str,
        number: int,
        extra: str = None
    ) -> None:
        self.ID = ID
        self.ticker = ticker
        self.price = price
        self.type_ = type_
        self.number = number
        self.extra = extra


class Wallet(db.Model):
    __tablename__: str = "Wallet"

    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    usd: Mapped[float] = mapped_column(Float, default=0)
    rub: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[str] = mapped_column(ForeignKey("User.uuid"))
    user: Mapped["User"] = relationship(back_populates="wallet")

    def __init__(self, *, ID: str, user_id: str) -> None:
        self.ID = ID
        self.user_id = user_id
