from typing import Any
from time import time
from random import randint
from uuid import uuid4

from . import db
from .models import User, Session
from ...config import AppConfig
from ...utils.cryptography import hash_password


def get(table: db.Model, **kwargs: Any) -> Any | None:
    return db.session.query(table).filter_by(**kwargs).first()


def add_user(user_data: dict[str, str | int]) -> tuple[str, int]:
    _id: str = uuid4().__str__()
    alien_number: int = randint(1, 6)

    user: User = User(
        uuid=_id,
        name=user_data["username"],
        password_hash=user_data["password_hash"],
        role="user",
        email=user_data["email"],
        register_date=int(time()),
        restore_cooldown=0,
        alien_number=alien_number
    )

    db.session.add(user)
    session: Session = Session(uuid=_id)
    db.session.add(session)

    db.session.commit()
    return _id, alien_number


def update_password(user: User, password: str) -> None:
    user.restore_cooldown = int(time()) + AppConfig.RESTORE_COOLDOWN
    user.password_hash = hash_password(password)
    db.session.commit()


def add_session(refresh_id: str, user_id: str, device: str | None) -> bool:
    sessions_raw: Session | None = get(Session, uuid=user_id)
    if sessions_raw is None:
        return False
    
    sessions_data: dict[str, str | int] = sessions_raw.__dict__
    
    earlier_activity: float = float("inf")
    for key, value in sessions_data.items():
        if key.startswith("activity") and value < earlier_activity:
            earlier_activity: int = value
            oldest_session: str = key.replace("activity", "")
    
    setattr(sessions_raw, "session" + oldest_session, refresh_id)
    setattr(sessions_raw, "activity" + oldest_session, int(time()))

    if device is None:
        device = "unknown device"
    setattr(sessions_raw, "device" + oldest_session, device)

    db.session.commit()
    return True


def update_session(old_refresh_id: str, new_refresh_id: str, user_id: str, device: str) -> bool:
    sessions_raw: Session | None = get(Session, uuid=user_id)
    if sessions_raw is None:
        return False
    
    sessions_data: dict[str, str] = sessions_raw.__dict__
    for key, value in sessions_data.items():
        if key.startswith("session") and value == old_refresh_id:
            session_num: str = key.replace("session", "")
            setattr(sessions_raw, "session" + session_num, new_refresh_id)
            setattr(sessions_raw, "activity" + session_num, int(time()))
            setattr(sessions_raw, "device" + session_num, device)
            db.session.commit()
            return True

    return False
