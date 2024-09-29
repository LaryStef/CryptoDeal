from typing import TYPE_CHECKING

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.postgre import db


if TYPE_CHECKING:
    from .fiat_wallet import FiatWallet


class Fiat(db.Model):
    __tablename__: str = "Fiat"

    iso: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(4096))
    volume: Mapped[float] = mapped_column(Float, default=0)
    fiat_wallet: Mapped[list["FiatWallet"]] = relationship()
