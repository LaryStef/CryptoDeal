from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgre import db


class CryptocurrencyWallet(db.Model):
    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    ticker: Mapped[str] = mapped_column(
        ForeignKey("CryptoCurrency.ticker", ondelete="CASCADE")
    )
    amount: Mapped[float] = mapped_column(Float, default=0)
    income: Mapped[float] = mapped_column(Float, default=0)
    invested: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("User.uuid", ondelete="CASCADE")
    )

    def __init__(
        self,
        *,
        ID: str,
        ticker: str,
        amount: float,
        income: float,
        invested: float,
        user_id: str
    ) -> None:
        self.ID = ID
        self.ticker = ticker
        self.user_id = user_id
        self.amount = amount
        self.income = income
        self.invested = invested
