from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import String, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...postgre import db
from ..utc_time import utcnow


if TYPE_CHECKING:
    from .session import Session
    from .fiat_wallet import FiatWallet
    from .cryptocurrency_wallet import CryptocurrencyWallet


class User(db.Model):
    __tablename__: str = "User"

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(5), default="user")
    email: Mapped[str] = mapped_column(String(256), unique=True)
    register_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=True,
        server_default=utcnow()
    )
    restore_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=utcnow()
    )
    alien_number: Mapped[int] = mapped_column(Integer, default=0)
    session: Mapped[list["Session"]] = relationship()
    fiat_wallet: Mapped["FiatWallet"] = relationship(back_populates="user")
    cryptocurrency_wallet: Mapped["CryptocurrencyWallet"] = relationship(
        back_populates="user"
    )

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
