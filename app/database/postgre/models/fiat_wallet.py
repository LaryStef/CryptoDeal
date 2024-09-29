from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgre import db


from .fiat import Fiat  # type: ignore # noqa F401


class FiatWallet(db.Model):
    __tablename__: str = "FiatWallet"

    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    iso: Mapped[str] = mapped_column(ForeignKey("Fiat.iso"))
    amount: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[str] = mapped_column(ForeignKey("User.uuid"))
