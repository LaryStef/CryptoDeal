from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgre import db, utcnow


class Session(db.Model):
    __tablename__: str = "Session"

    # TODO replace session_id UUID
    session_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("User.uuid", ondelete="CASCADE")
    )
    device: Mapped[str] = mapped_column(String(30), default="unknown device")
    last_activity: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=utcnow(),
        onupdate=utcnow()
    )

    def __init__(self, *, session_id: str, user_id: str, device: str) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.device = device
