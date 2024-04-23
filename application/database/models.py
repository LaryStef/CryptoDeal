from sqlalchemy import Integer, String

from ..database import db


class User(db.Model):
    __tablename__ = "user"
    pass