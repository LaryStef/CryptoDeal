from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.postgre import db, utcnow


if TYPE_CHECKING:
    from .cryptocurrency_wallet import CryptocurrencyWallet
    from .crypto_transaction import CryptoTransaction
    from .fiat_wallet import FiatWallet
    from .session import Session


class User(db.Model):
    # __tablename__: str = "User"

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(5), default="user")
    email: Mapped[str] = mapped_column(String(256), unique=True)
    register_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=utcnow()
    )
    restore_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=utcnow()
    )
    alien_number: Mapped[int] = mapped_column(Integer, default=0)

    session: Mapped[list["Session"]] = relationship(cascade="all, delete")
    user_fiat_wallet: Mapped[list["FiatWallet"]] = relationship(
        cascade="all, delete"
    )
    user_crypto_wallet: Mapped[list["CryptocurrencyWallet"]] = relationship(
        cascade="all, delete"
    )
    crypto_transaction: Mapped[list["CryptoTransaction"]] = relationship(
        cascade="all, delete"
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
