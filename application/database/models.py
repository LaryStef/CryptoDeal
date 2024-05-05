from sqlalchemy import Integer, String, Column

from ..database import db


class User(db.Model):
    
    uuid = Column(Integer, primary_key=True, unique=True, nullable=False)
    user = Column(String(30), nullable=False)
    password = Column(String(64), nullable=False)

    def __str__(self):
        print("11")
