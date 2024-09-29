from datetime import datetime

from sqlalchemy import ForeignKey, String, Integer, Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgre import db, utcnow


class CryptoTransation(db.Model):
    __tablename__: str = "CryptoTransaction"

    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    ticker: Mapped[str] = mapped_column(ForeignKey("CryptoCurrency.ticker"))
    amount: Mapped[int] = mapped_column(Integer)
    type_: Mapped[str] = mapped_column(String(8))
    time: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=utcnow())
    price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[str] = mapped_column(ForeignKey("User.uuid"))
