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

    def __init__(
        self,
        *,
        ID: str,
        iso: str,
        amount: float,
        user_id: str
    ) -> None:
        self.ID = ID
        self.iso = iso
        self.amount = amount
        self.user_id = user_id
