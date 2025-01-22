from datetime import datetime

from sqlalchemy import TIMESTAMP, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now

from app.database.postgre import db


class CryptoTransaction(db.Model):
    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    ticker: Mapped[str] = mapped_column(
        ForeignKey("CryptoCurrency.ticker", ondelete="CASCADE")
    )
    amount: Mapped[float] = mapped_column(Float)
    type_: Mapped[str] = mapped_column(String(8))
    time: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=now().op(
        'AT TIME ZONE'
    )('UTC') + text("INTERVAL '3 hours'"))
    price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("User.uuid", ondelete="CASCADE")
    )

    def __init__(
        self,
        *,
        ID: str,
        ticker: str,
        amount: float,
        type_: str,
        price: float,
        user_id: str
    ) -> None:
        self.ID = ID
        self.ticker = ticker
        self.amount = amount
        self.type_ = type_
        self.price = price
        self.user_id = user_id
