from typing import Any, NoReturn
from time import time
from uuid import uuid4

from . import db
from .models import User
from ...config import AppConfig
from ...utils.cryptography import hash_password


def get(table: db.Model, **kwargs: Any) -> Any | None:
    return db.session.query(table).filter_by(**kwargs).first()


def add_user(user_data: dict[str, str | int]) -> None:
    user_data["uuid"] = uuid4().__str__()
    user_data["register_date"] = int(time())

    row: User = User(user_data)
    db.session.add(row)
    db.session.commit()


def update_password(user: User, password: str) -> None:
    user.restore_cooldown = int(time()) + AppConfig.RESTORE_COOLDOWN
    user.password_hash = hash_password(password)
    db.session.commit()
