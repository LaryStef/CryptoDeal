from typing import Any
from time import time
from uuid import uuid4

from . import db
from .models import User
from ...config import AppConfig
from ...utils.cryptography import hash_password


def get(table: Any, **kwargs) -> Any | None:
    return db.session.query(table).filter_by(**kwargs).first()


def add_user(user_data: dict):
    user_data["uuid"] = uuid4().__str__()
    user_data["register_date"] = int(time())

    row: User = User(user_data)
    db.session.add(row)
    db.session.commit()


def update_after_password_change(user: User, password: str):
    user.restore_cooldown = int(time()) + AppConfig.RESTORE_COOLDOWN
    user.password_hash = hash_password(password)
    db.session.commit()
