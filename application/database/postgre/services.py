from typing import Any
from time import time
from uuid import uuid4

from . import db
from .models import User
from ...utils.cryptography import hash_password


def get(table: Any, **kwargs) -> Any | None:
    return db.session.query(table).filter_by(**kwargs).first()


def add_user(user_data: dict):
    user_data["uuid"] = uuid4().__str__()
    user_data["register_date"] = int(time())

    row: User = User(user_data)
    db.session.add(row)
    db.session.commit()


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
