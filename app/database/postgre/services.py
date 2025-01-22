from datetime import datetime, timedelta
from random import randint
from typing import Any, Literal
from uuid import uuid4

from flask import current_app, url_for
from sqlalchemy import BinaryExpression, Result, Sequence, delete, desc, select
from sqlalchemy.orm import Mapped
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.expression import text

from app.config import appConfig
from app.database.postgre import db
from app.database.postgre.models import (
    CryptoCourse, CryptocurrencyWallet, CryptoTransaction, FiatWallet, Session,
    User, CryptoCurrency
)
from app.security import hash_password


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
    def remove(table: Any, **kwargs: Any) -> None:
        db.session.execute(
            delete(table).filter_by(**kwargs)
        )
        db.session.commit()
        current_app.logger.info(
            "deleted raw/s with args: %s in %s",
            kwargs,
            table
        )

    @staticmethod
    def delete_exclude(
        table: Any,
        column: Mapped[Any],
        exclude: list[Any],
        **kwargs: Any
    ) -> None:
        db.session.execute(
            delete(table).where(column.not_in(exclude)).filter_by(**kwargs)
        )
        db.session.commit()
        current_app.logger.info(
            "deleted all raw/s exclude raws: %s in %s in %s",
            kwargs,
            column,
            table
        )

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
        current_app.logger.info(
            "added %s %s",
            user_data['role'],
            user_data['username']
        )

        return id_, alien_number

    @staticmethod
    def update_password(user: User, password: str) -> None:
        user.password_hash = hash_password(password)
        user.restore_date = now().op('AT TIME ZONE')('UTC') + text(
            "INTERVAL '3 hours'"
        )
        db.session.commit()
        current_app.logger.info("updated password %s", user.name)

    @staticmethod
    def add_session(refresh_id: str, user_id: str, device: str) -> None:
        user: User = db.session.execute(
            select(User).filter_by(uuid=user_id)
        ).scalar()
        user.login_attempts = 0
        user.login_mode = "fast"

        session_raw: Session = Session(
            session_id=refresh_id,
            user_id=user_id,
            device=device
        )
        db.session.add(session_raw)
        db.session.commit()
        current_app.logger.info("new session added %s on %s", user_id, device)

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
        current_app.logger.info("session refreshed %s", user_id)

    @classmethod
    def provide_crypto_transaction(
        cls,
        user_id: str,
        *,
        ticker: str,
        amount: float,
        type_: Literal["buy", "sell"]
    ) -> None:
        course_row: CryptoCourse | None = cls.get_crypto_price(
            PostgreHandler, ticker
        )

        if course_row is None:
            raise BadRequest(description=f"No such ticker: {ticker}")
        current_price: float = course_row.price

        user: User | None = db.session.execute(
            select(User).filter_by(uuid=user_id)
        ).scalar()

        if user is None:
            raise NotFound(description=f"No such ticker: {ticker}")

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
                shortage: float = round(
                    current_price * amount - usd_balance.amount,
                    ndigits=2
                )
                current_app.logger.info(
                    "buy failed %s %s %s not enough %s",
                    user_id,
                    ticker,
                    amount,
                    shortage
                )
                raise BadRequest(
                    description=(f"You're short of {shortage} USD")
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

            usd_balance.amount -= round(amount * current_price, ndigits=2)
            crypto_balance.amount += amount
            crypto_balance.invested += round(amount * current_price, ndigits=2)
            user.crypto_spent += round(amount * current_price, ndigits=2)

        elif type_ == "sell":
            if crypto_balance is None:
                raise BadRequest(description=f"You don't have any {ticker}")

            if crypto_balance.amount < amount:
                shortage = round(
                    amount - crypto_balance.amount,
                    ndigits=2
                )
                current_app.logger.info(
                    "sell failed %s %s %s not enough %s",
                    user_id,
                    ticker,
                    amount,
                    shortage
                )
                raise BadRequest(
                    description=f"You're short of {shortage} {ticker}"
                )

            usd_balance.amount += round(amount * current_price, ndigits=2)
            crypto_balance.amount -= amount
            crypto_balance.income += round(amount * current_price, ndigits=2)
            user.crypto_derived += round(amount * current_price, ndigits=2)

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
        current_app.logger.info(
            "transaction made %s %s %s %s", user_id, type_, ticker, amount
        )

    def get_crypto_price(
        cls, ticker: str
    ) -> CryptoCourse | None:
        return db.session.execute(
            select(CryptoCourse).filter_by(
                ticker=ticker).filter_by(
                type_="hour").filter_by(
                number=datetime.now().hour
            )
        ).scalar()

    @staticmethod
    def get_crypto_history(user_id: str) -> list[CryptoCourse]:
        transactions: tuple[
            str | None, CryptoTransaction | None
        ] = db.session.execute(
            select(CryptoCurrency.name, CryptoTransaction).join_from(
                CryptoCurrency, CryptoTransaction
            ).filter_by(user_id=user_id)
        ).all()

        if transactions is None:
            return []
        return [{
            "name": transaction[0],
            "ticker": transaction[1].ticker,
            "price": transaction[1].price,
            "amount": transaction[1].amount,
            "type": transaction[1].type_,
            "date": transaction[1].time.strftime("%d.%m.%Y %H:%M"),
            "logoUrl": url_for(
                "static",
                filename=f"svg/cryptocurrency/{transaction[1].ticker}.svg"
            ),
        } for transaction in transactions]

    @staticmethod
    def get_balance(
        ids: list[str],
        *,
        table: CryptocurrencyWallet | FiatWallet,
        user_id: str,
    ) -> Sequence:

        if table == CryptocurrencyWallet:
            in_cond: BinaryExpression[bool] = CryptocurrencyWallet.ticker.in_(
                ids
            )
        elif table == FiatWallet:
            in_cond: BinaryExpression[bool] = FiatWallet.iso.in_(ids)

        return db.session.execute(
            select(table).filter(in_cond).filter_by(user_id=user_id)
        ).all()

    @staticmethod
    def get_ordered_wallet(
        user_id: str
    ) -> Result[tuple[CryptocurrencyWallet]]:
        wallet: Result[tuple[CryptocurrencyWallet]] = db.session.execute(
            select(CryptocurrencyWallet).filter_by(user_id=user_id).order_by(
                desc(CryptocurrencyWallet.amount)
            )
        )
        if wallet is None:
            return []
        return wallet

    @staticmethod
    def calculate_daily_change(ticker: str) -> float:
        hour: int = datetime.now().hour

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

    @staticmethod
    def increase_login_attempts(user: User) -> None:
        user.login_attempts += 1
        if user.login_attempts >= appConfig.LOGIN_FAST_ATTEMPTS:
            user.login_mode = "slow"
            user.login_cooldown_end = datetime.now() + timedelta(
                seconds=appConfig.LOGIN_COOLDOWN
            )
        db.session.commit()
