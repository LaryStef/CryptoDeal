from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...postgre import db


if TYPE_CHECKING:
    from .user import User


class FiatWallet(db.Model):
    __tablename__: str = "FiatWallet"

    ID: Mapped[str] = mapped_column(String(36), primary_key=True)
    usd: Mapped[float] = mapped_column(Float, default=0)
    rub: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[str] = mapped_column(ForeignKey("User.uuid"))
    user: Mapped["User"] = relationship(back_populates="fiat_wallet")

    def __init__(self, *, ID: str, user_id: str) -> None:
        self.ID = ID
        self.user_id = user_id
