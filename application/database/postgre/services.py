from typing import Any
from time import time

from . import db
from .models import User
from ...utils.cryptography import hash_password


def get(table: Any, **kwargs) -> Any | None:
    return db.session.query(table).filter_by(**kwargs).first()


def add_user(user_data: dict):
    hash, salt = hash_password(user_data["password"])
    row: User = User(
        uuid = "12383a",
        username = user_data["username"],
        password_hash = hash,
        salt = salt,
        email = user_data["email"],
        register_date = int(time())
    )
    db.session.add(row)
    db.session.commit()


# def get_all_users() -> list[str]:
#     user_names: list[str] = [user.username for user in User.query.all()]

#     return user_names

# def insert_user(username: str):
#     print("here")
#     uuid = randint(1, 1000000)
#     password = "123"
#     row = User(uuid = uuid, username = username, password = password)
#     db.session.add(row)
#     db.session.commit()

# def get_user(username: str):
#     data = User.query.filter_by(user = username).first()
#     return data.__dict__
