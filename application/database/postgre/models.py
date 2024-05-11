from sqlalchemy import Integer, String, Column

from . import db


# class User(db.Model):

#     uuid = Column(Integer, primary_key=True, unique=True, nullable=False)
#     user = Column(String(30), nullable=False)
#     password = Column(String(64), nullable=False)

#     def __init__(self, uuid: int, username: str, password: str) -> None:
#         self.uuid = uuid
#         self.user = username
#         self.password = password
