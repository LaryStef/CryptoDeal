from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.expression import text

from app.database.postgre import db


class Session(db.Model):
    session_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("User.uuid", ondelete="CASCADE")
    )
    device: Mapped[str] = mapped_column(String(32), default="unknown device")
    last_activity: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=now().op('AT TIME ZONE')('UTC') + text(
            "INTERVAL '3 hours'"
        ),
        onupdate=now().op('AT TIME ZONE')('UTC') + text(
            "INTERVAL '3 hours'"
        )
    )

    def __init__(self, *, session_id: str, user_id: str, device: str) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.device = device
