from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgre import db


class CryptoCourse(db.Model):
    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    ticker: Mapped[str] = mapped_column(
        ForeignKey("CryptoCurrency.ticker", ondelete="CASCADE")
    )
    price: Mapped[float] = mapped_column(Float, default=0)
    type_: Mapped[str] = mapped_column("type", String(8))
    number: Mapped[int] = mapped_column(Integer)

    def __init__(
        self,
        *,
        ID: str,
        ticker: str,
        price: float,
        type_: str,
        number: int,
    ) -> None:
        self.ID = ID
        self.ticker = ticker
        self.price = price
        self.type_ = type_
        self.number = number
