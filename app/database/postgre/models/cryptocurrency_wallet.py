from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.postgre import db


if TYPE_CHECKING:
    from .user import User
    from .cryptocurrency import CryptoCurrency


class CryptocurrencyWallet(db.Model):
    __tablename__: str = "CryptocurrencyWallet"

    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    ticker: Mapped[str] = mapped_column(ForeignKey("Cryptocurrency.ticker"))
    user_id: Mapped[str] = mapped_column(ForeignKey("User.uuid"))
    user: Mapped["User"] = relationship(back_populates="cryptocurrency_wallet")
    cryptocurrency: Mapped["CryptoCurrency"] = relationship(
        back_populates="cryptocurrency_wallet"
    )
