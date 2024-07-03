from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from . import db

# TODO change datatype for timestamps in db to suitable datatype
class User(db.Model):
    def __init__(
            self,
            uuid: str,
            name: str,
            password_hash: str,
            role: str,
            email: str,
            register_date: int,
            restore_cooldown: int
        ):

        self.uuid: str = uuid
        self.name: str = name
        self.password_hash: str = password_hash
        self.role: str = role
        self.email: str = email
        self.register_date: int = register_date
        self.restore_cooldown: int = restore_cooldown

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(5), default="user")
    email: Mapped[str] = mapped_column(String(256), unique=True)
    register_date: Mapped[int] = mapped_column(Integer)
    restore_cooldown: Mapped[int] = mapped_column(Integer, default=0)


class Session(db.Model):
    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True) # TODO foreign key
    
    session1: Mapped[str] = mapped_column(String(16), nullable=True)
    session2: Mapped[str] = mapped_column(String(16), nullable=True)
    session3: Mapped[str] = mapped_column(String(16), nullable=True)
    session4: Mapped[str] = mapped_column(String(16), nullable=True)
    session5: Mapped[str] = mapped_column(String(16), nullable=True)

    device1: Mapped[str] = mapped_column(String(30), default="unnkown device")
    device2: Mapped[str] = mapped_column(String(30), default="unnkown device")
    device3: Mapped[str] = mapped_column(String(30), default="unnkown device")
    device4: Mapped[str] = mapped_column(String(30), default="unnkown device")
    device5: Mapped[str] = mapped_column(String(30), default="unnkown device")

    activity1: Mapped[int] = mapped_column(Integer, default=0)
    activity2: Mapped[int] = mapped_column(Integer, default=0)
    activity3: Mapped[int] = mapped_column(Integer, default=0)
    activity4: Mapped[int] = mapped_column(Integer, default=0)
    activity5: Mapped[int] = mapped_column(Integer, default=0)
