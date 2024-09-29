from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgre import db


class CryptocurrencyWallet(db.Model):
    __tablename__: str = "CryptocurrencyWallet"

    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    ticker: Mapped[str] = mapped_column(ForeignKey("CryptoCurrency.ticker"))
    amount: Mapped[int] = mapped_column(Integer, default=0)
    income: Mapped[float] = mapped_column(Float, default=0)
    invested: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[str] = mapped_column(ForeignKey("User.uuid"))

    def __init__(
        self,
        ID: str,
        ticker: str,
        amount: int,
        income: float,
        invested: float,
        user_id: str
    ) -> None:
        self.ID = ID
        self.ticker = ticker
        self.amount = amount
        self.income = income
        self.invested = invested
        self.user_id = user_id
