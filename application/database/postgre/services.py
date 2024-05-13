from typing import Any

from . import db
from .models import User


def get_all_users() -> list[str]:
    user_names: list[str] = [user.username for user in User.query.all()]

    return user_names


def get(table: Any, **kwargs) -> Any | None:
    row: Any | None = db.session.query(table).filter_by(**kwargs).first()

    return row

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
