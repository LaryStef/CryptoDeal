from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgre import db


class FiatWallet(db.Model):
    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    iso: Mapped[str] = mapped_column(
        ForeignKey("Fiat.iso", ondelete="CASCADE")
    )
    amount: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("User.uuid", ondelete="CASCADE")
    )

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
