from typing import Any
from datetime import datetime, UTC
from uuid import uuid4

from . import db
from .models import User, Session
from ...config import AppConfig
from ...utils.cryptography import hash_password


def get(table: db.Model, **kwargs: Any) -> Any | None:
    return db.session.query(table).filter_by(**kwargs).first()


def add_user(user_data: dict[str, str | int]) -> None:
    _id = uuid4().__str__()

    user: User = User(
        uuid=_id,
        name=user_data["username"],
        password_hash=user_data["password_hash"],
        role="user",
        email=user_data["email"],
        register_date=int(datetime.now(UTC).timestamp()),
        restore_cooldown=0
    )

    db.session.add(user)
    session: Session = Session(uuid=_id)
    db.session.add(session)

    db.session.commit()
    return _id


def update_password(user: User, password: str) -> None:
    user.restore_cooldown = int(datetime.now(UTC).timestamp()) + AppConfig.RESTORE_COOLDOWN
    user.password_hash = hash_password(password)
    db.session.commit()


def add_session(refresh_id: str, user_id: str, device: str) -> None:
    sessions_raw: Session | None = get(Session, uuid=user_id)
    if sessions_raw is None:
        return
    
    sessions_data: dict[str, str] = sessions_raw.__dict__
    
    earlier_activity: float = float("inf")
    for key, value in sessions_data.items():
        if key.startswith("activity") and value < earlier_activity:
            earlier_activity: int = value
            oldest_session: str = key.replace("activity", "")
    
    setattr(sessions_raw, "session" + oldest_session, refresh_id)
    setattr(sessions_raw, "activity" + oldest_session, datetime.now(UTC).timestamp())

    if device is None:
        setattr(sessions_raw, "device" + oldest_session, "unnkown device")
    else:
        setattr(sessions_raw, "device" + oldest_session, device)

    db.session.commit()
