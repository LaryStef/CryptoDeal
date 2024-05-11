from signal import SIG_DFL
from . import db
# from ..database.models import User

from random import randint


# def insert_user(username: str):
#     print("here")
#     uuid = randint(1, 1000000)
#     password = "123"
#     row = User(uuid = uuid, username = username, password = password) # type: ignore
#     print("here2")
#     db.session.add(row)
#     db.session.commit()

# def get_user(username: str):
#     data = User.query.filter_by(user = username).first()
#     return data.__dict__
