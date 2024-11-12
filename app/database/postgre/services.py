from random import randint
import math
from typing import Any, Literal, TypeAlias
from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Result, delete, select, desc
from sqlalchemy.orm import Mapped
from werkzeug.exceptions import BadRequest

from app.database.postgre import db, utcnow
from app.database.postgre.models import (
    CryptocurrencyWallet, CryptoCourse, FiatWallet, Session, User,
    CryptoTransaction
)
from app.logger import logger
from app.utils.cryptography import hash_password
from app.config import appConfig


_BalanceList: TypeAlias = list[CryptocurrencyWallet | FiatWallet] | None


class PostgreHandler:
    @staticmethod
    def get(
        table: Any = None,
        fields: list[Mapped] = [],
        *,
        many: bool = False,
        **kwargs: Any
    ) -> Any:
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

    @staticmethod
    def remove(table: Any, **kwargs: Any):
        db.session.execute(
            delete(table).filter_by(**kwargs)
        )
        db.session.commit()
        logger.info(msg=f"deleted raw/s with args: {kwargs} in {table}")

    @staticmethod
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

    @staticmethod
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
        usd_balance: FiatWallet = FiatWallet(
            ID=uuid4().__str__(),
            iso="USD",
            amount=appConfig.START_USD_BALANCE,
            user_id=id_
        )

        db.session.add(user)
        db.session.add(usd_balance)
        db.session.commit()
        logger.info(msg=f"added {user_data['role']} {user_data['username']}")

        return id_, alien_number

    @staticmethod
    def update_password(user: User, password: str) -> None:
        user.password_hash = hash_password(password)
        user.restore_date = utcnow()
        db.session.commit()
        logger.info(msg=f"updated password {user.name}")

    @staticmethod
    def add_session(refresh_id: str, user_id: str, device: str) -> None:
        session_raw: Session = Session(
            session_id=refresh_id,
            user_id=user_id,
            device=device
        )
        db.session.add(session_raw)
        db.session.commit()
        logger.info(msg=f"new session added {user_id} on {device}")

    @staticmethod
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

    @classmethod
    def provide_crypto_transaction(
        cls,
        user_id: str,
        *,
        ticker: str,
        amount: float,
        type_: Literal["buy", "sell"]
    ) -> str | None:
        course_row: CryptoCourse | None = cls.get_crypto_price(
            PostgreHandler, ticker
        )

        if course_row is None:
            raise BadRequest(description=f"no such ticker: {ticker}")
        current_price: float = course_row.price

        user: User = db.session.execute(
            select(User).filter_by(uuid=user_id)
        ).scalar()

        usd_balance: FiatWallet | None = None
        for fiat in user.user_fiat_wallet:
            if fiat.iso == "USD":
                usd_balance = fiat
                break

        crypto_balance: CryptocurrencyWallet | None = None
        for crypto in user.user_crypto_wallet:
            if crypto.ticker == ticker:
                crypto_balance = crypto
                break

        if type_ == "buy":
            if usd_balance.amount < amount * current_price:
                shortage: float = math.ceil(
                    (current_price * amount - usd_balance.amount) * 100
                ) / 100
                raise BadRequest(
                    description=(f"you're short of {shortage} USD")
                )

            if crypto_balance is None:
                crypto_balance = CryptocurrencyWallet(
                    ID=uuid4().__str__(),
                    ticker=ticker,
                    amount=0,
                    income=0,
                    invested=0,
                    user_id=user_id
                )
                db.session.add(crypto_balance)

            usd_balance.amount -= amount * current_price
            crypto_balance.invested += amount * current_price
            crypto_balance.amount += amount

        elif type_ == "sell":
            if crypto_balance is None:
                raise BadRequest(description=f"you don't have any {ticker}")

            if crypto_balance.amount < amount:
                shortage: float = math.ceil(
                    (amount - crypto_balance.amount) * 100
                ) / 100
                raise BadRequest(
                    description=f"you're short of {shortage} {ticker}"
                )

            usd_balance.amount += amount * current_price
            crypto_balance.income += amount * current_price
            crypto_balance.amount -= amount

            if crypto_balance.amount == 0:
                db.session.delete(crypto_balance)

        db.session.add(
            CryptoTransaction(
                ID=uuid4().__str__(),
                ticker=ticker,
                amount=amount,
                type_=type_,
                price=current_price,
                user_id=user_id
            )
        )
        db.session.commit()
        logger.info(
            msg=f"transaction made {user_id} {type_} {ticker} {amount}"
        )

    def get_crypto_price(
        cls, ticker: str
    ) -> CryptoCourse | None:
        return db.session.execute(
            select(CryptoCourse).filter_by(
                ticker=ticker).filter_by(
                type_="hour").filter_by(
                number=datetime.now(UTC).hour
            )
        ).scalar()

    def get_crypto_history(user_id: str) -> list[CryptoCourse]:
        transactions: list[CryptoTransaction] | None = db.session.execute(
            select(CryptoTransaction).filter_by(user_id=user_id)
        ).scalar()

        if transactions is None:
            return []
        return transactions

    @staticmethod
    def get_balance(
        ids: list[str],
        *,
        table: CryptocurrencyWallet | FiatWallet,
        user_id: str,
    ) -> list[CryptocurrencyWallet] | list[FiatWallet]:

        if table == CryptocurrencyWallet:
            in_condition: str = CryptocurrencyWallet.ticker.in_(ids)
        elif table == FiatWallet:
            in_condition: str = FiatWallet.iso.in_(ids)

        return db.session.execute(
            select(table).filter(in_condition).filter_by(user_id=user_id)
        ).all()

    @staticmethod
    def get_ordered_wallet(user_id: str) -> list[CryptocurrencyWallet]:
        wallet: list[CryptocurrencyWallet] | None = db.session.execute(
            select(CryptocurrencyWallet).filter_by(user_id=user_id).order_by(
                desc(CryptocurrencyWallet.amount)
            )
        )
        if wallet is None:
            return []
        return wallet

    @staticmethod
    def calculate_daily_change(ticker: str):
        hour: int = datetime.now(UTC).hour

        course_day_ago: CryptoCourse = db.session.execute(
            select(
                CryptoCourse
            ).filter_by(
                ticker=ticker
            ).filter_by(
                type_="hour"
            ).filter_by(
                number=(hour + 1) % 24
            )
        ).scalar_one()
        new_course: CryptoCourse = db.session.execute(
            select(
                CryptoCourse
            ).filter_by(
                ticker=ticker
            ).filter_by(
                type_="hour"
            ).filter_by(
                number=hour
            )
        ).scalar_one()

        if course_day_ago is None or new_course is None:
            return 0
        return (new_course.price / course_day_ago.price - 1) * 100
