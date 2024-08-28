from random import randint
from typing import Any
from uuid import uuid4

from sqlalchemy import Result, delete, select
from sqlalchemy.orm import Mapped

from ...logger import logger
from ...utils.cryptography import hash_password
from . import db
from .models import Session, User
from .utc_time import utcnow


def get(
    table: Any = None,
    fields: list[Mapped] = [],
    many: bool = False,
    **kwargs: Any
) -> Any | None:
    if table is not None:
        result: Result = db.session.execute(
            select(table).filter_by(**kwargs)
        )
        if many:
            return result.scalars()
        return result.scalar()

    result: Result = db.session.execute(
        select(*fields).filter_by(**kwargs)
    )

    if many:
        return result.scalars()
    return result.fetchone()


def remove(table: Any, **kwargs: Any):
    db.session.execute(
        delete(table).filter_by(**kwargs)
    )
    db.session.commit()
    logger.info(msg=f"deleted raw/s with args: {kwargs} in {table}")


def delete_exclude(
    table: Any,
    column: Mapped[Any],
    exclude: list[Any],
    **kwargs: Any
):
    db.session.execute(
        delete(table).where(column.not_in(exclude)).filter_by(**kwargs)
    )
    db.session.commit()
    logger.info(msg=f"""
        deleted all raw/s exclude raws: {kwargs} in {column} in {table}
    """)


def add_user(user_data: dict[str, str | int]) -> tuple[str, int]:
    id_: str = uuid4().__str__()
    alien_number: int = randint(1, 5)

    user: User = User(
        uuid=id_,
        name=user_data["username"],
        password_hash=user_data["password_hash"],
        role=user_data["role"],
        email=user_data["email"],
        alien_number=alien_number
    )

    db.session.add(user)
    db.session.commit()
    logger.info(msg=f"added {user_data['role']} {user_data['username']}")
    return id_, alien_number


def update_password(user: User, password: str) -> None:
    user.password_hash = hash_password(password)
    user.restore_date = utcnow()
    db.session.commit()
    logger.info(msg=f"updated password {user.name}")


def add_session(refresh_id: str, user_id: str, device: str) -> None:
    session_raw: Session = Session(
        session_id=refresh_id,
        user_id=user_id,
        device=device
    )
    db.session.add(session_raw)
    db.session.commit()
    logger.info(msg=f"new session added {user_id} on {device}")


def update_session(
        old_refresh_id: str,
        new_refresh_id: str,
        user_id: str,
        device: str
) -> None:
    session_raw: Session | None = db.session.query(Session).filter_by(
        user_id=user_id,
        session_id=old_refresh_id
    ).first()
    if session_raw is None:
        return

    session_raw.session_id = new_refresh_id
    session_raw.device = device
    db.session.commit()
    logger.info(msg=f"session refreshed {user_id}")
