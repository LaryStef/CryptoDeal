import typing as t

from flask import request, url_for
from flask_restx import Namespace, Resource
from sqlalchemy import Sequence
from werkzeug.exceptions import BadRequest

from app.database.postgre.models import (
    CryptoCurrency, CryptocurrencyWallet, FiatWallet, Session, User
)
from app.database.postgre.services import PostgreHandler
from app.utils.aliases import RESTError
from app.utils.decorators import authorization_required
from app.utils.JWT import validate_token


api = Namespace("user", path="/user/")

_UserData: t.TypeAlias = dict[
    str, str | dict[str, str | int] | list[dict[str, str | bool]]
]


@api.route("/")
class Profile(Resource):
    @authorization_required("access")
    def get(self) -> tuple[dict[str, _UserData] | RESTError, int]:
        try:
            # response example
            # {
            #     "userData": {
            #         "uuid": "uuid",
            #         "profile": {
            #             "name": "Chirill",
            #             "alienNumber": 1,
            #             "role": "user",
            #             "email": "poopka06@gmail.com",
            #             "registerDate": "2024-07-09 20:52:41.792133"
            #         },
            #         "sessions": [
            #             {
            #                 "sessionId": "5ZB7k7c7hxr9KcX2",
            #                 "device": "Chrome, Windows10",
            #                 "lastActivity": "2024-07-30 19:56:41.192498",
            #                 "isCurrent": false
            #             },
            #             {
            #                 "sessionId": "vLEiYUtkmK8DHZWg",
            #                 "device": "Chrome, Linux",
            #                 "lastActivity": "2024-08-04 20:27:41.80115",
            #                 "isCurrent": true
            #             }
            #         ]
            #     }
            # }

            refresh_token: str | None = request.cookies.get("refresh_token")
            refresh_payload: t.Any = validate_token(
                token=refresh_token,
                type="refresh"
            )
            access_token: str | None = request.cookies.get("access_token")
            access_payload: t.Any = validate_token(
                token=access_token,
                type="access"
            )

            if access_payload is None or refresh_payload is None:
                raise BadRequest

            current_session_id: str = refresh_payload.get("jti", "")
            uuid: str = access_payload.get("uuid", "")

            user: User = PostgreHandler.get(fields=[
                User.alien_number,
                User.name,
                User.email,
                User.role,
                User.register_date
            ], uuid=uuid)
            sessions: list[Session] = PostgreHandler.get(Session, fields=[
                Session.session_id,
                Session.device,
                Session.last_activity
            ], many=True, user_id=uuid)

            user_data: _UserData = {
                "id": uuid,
                "profile": {
                    "name": user.name,
                    "alienNumber": user.alien_number,
                    "role": user.role,
                    "email": user.email,
                    "registerDate": str(user.register_date)
                },
                "sessions": []
            }

            for session in sessions:
                user_data.get("sessions").append(
                    {
                        "sessionId": session.session_id,
                        "device": session.device,
                        # TODO: display last activity in user's timezone
                        "lastActivity": session.last_activity.strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        "isCurrent": session.session_id == current_session_id
                    }
                )

            return {
                "userData": user_data
            }, 200

        except BadRequest:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid data",
                    "details": "Invalid format of data"
                }
            }, 400


@api.route("/balance/<string:asset>/ids")
class Balance(Resource):
    @authorization_required("access")
    def get(
        self, asset: str
    ) -> tuple[dict[str, dict[str, float]], int] | RESTError:
        # request /api/user/balance/currency/ids?id=USD&id=RUR
        # response example
        # {
        #     "type": "currency",
        #     "balance": {
        #         "USD": 20.383631,
        #         "RUR": 38381.389311
        #     }
        # }

        availible_assets: list[str] = ["cryptocurrency", "currency"]

        try:
            if asset not in availible_assets:
                raise BadRequest(description=f"Type not in {availible_assets}")

            ids: list[str] = request.args.getlist("id")
            access_token: str | None = request.cookies.get("access_token")
            access_payload: t.Any = validate_token(
                token=access_token,
                type="access"
            )

            if access_payload is None:
                raise BadRequest("Access token is not valid")
            user_id: str = access_payload.get("uuid", "")
            balance: dict[str, float] = {}

            if asset == "cryptocurrency":
                wallet: Sequence = PostgreHandler.get_balance(
                    ids,
                    table=CryptocurrencyWallet,
                    user_id=user_id,
                )
                for crypto in wallet:
                    balance[crypto[0].ticker] = crypto[0].amount

            elif asset == "currency":
                wallet: list[FiatWallet] = PostgreHandler.get_balance(
                    ids,
                    table=FiatWallet,
                    user_id=user_id,
                )
                for currency in wallet:
                    balance[currency[0].iso] = currency[0].amount

            return {
                "type": asset,
                "balance": balance
            }, 200

        except BadRequest as error:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Can't recognize request",
                    "details": error.description
                }
            }, 400


@api.route("/statistics/<string:asset>")
class Statistics(Resource):
    @staticmethod
    def _calculate_profit(
        invested: float,
        income: float,
        worth: float
    ) -> float:
        return (worth - invested + income) / invested * 100

    @authorization_required("access")
    def get(self, asset: str) -> tuple[dict[str, t.Any], int] | RESTError:
        # request /api/user/statistics/cryptocurrency
        # response example
        # {
        #     "type": "cryptocurrency",
        #     "spent": 238392.392,
        #     "derived": 2999990.281,
        #     "cryptocurrencies": [
        #         {
        #             "place": 1,
        #             "ticker": "BTC",
        #             "name": "Bitcoin",
        #             "logoUrl": "/static/svg/cryptocurrency/BTC.svg",
        #             "amount": 0.839832,
        #             "price": 238392.392,
        #             "volume": 5848323932.888,
        #             "profit": -84.21,
        #             "change": 10.04
        #         },
        #         {
        #             "place": 2,
        #             "ticker": "ETH",
        #             "name": "Ethereum",
        #             "logoUrl": "/static/svg/cryptocurrency/ETH.svg",
        #             "amount": 46.438,
        #             "price": 2849.442,
        #             "volume": 1882351134.882,
        #             "profit": 20.78,
        #             "change": -4.91
        #         }
        #     ]
        # }

        availible_assets: list[str] = ["cryptocurrency"]

        try:
            if asset not in availible_assets:
                raise BadRequest(description=f"Type not in {availible_assets}")

            access_token: str | None = request.cookies.get("access_token")
            access_payload: t.Any = validate_token(
                token=access_token,
                type="access"
            )

            if access_payload is None:
                raise BadRequest("Access token is not valid")
            user_id: str = access_payload.get("uuid", "")
            cryptocurrencies: list[dict[str, str | int]] = []

            if asset == "cryptocurrency":

                total_invested: float = 0
                total_derived: float = 0
                total_worth: float = 0
                wallet: list[FiatWallet] = PostgreHandler.get_ordered_wallet(
                    user_id=user_id,
                )

                for index, currency in enumerate(wallet):
                    ticker: str = currency[0].ticker
                    price: float = PostgreHandler.get_crypto_price(
                        PostgreHandler,
                        ticker
                    ).price
                    general_currency_info: CryptoCurrency = PostgreHandler.get(
                        CryptoCurrency, ticker=ticker
                    )

                    cryptocurrencies.append(
                        {
                            "place": index + 1,
                            "ticker": ticker,
                            "name": general_currency_info.name,
                            "logoUrl": url_for(
                                "static",
                                filename=f"/svg/cryptocurrency/{ticker}.svg"
                            ),
                            "amount": currency[0].amount,
                            "price": price,
                            "volume": general_currency_info.volume,
                            "profit": self._calculate_profit(
                                invested=currency[0].invested,
                                income=currency[0].income,
                                worth=currency[0].amount * price
                            ),
                            "change": PostgreHandler.calculate_daily_change(
                                ticker=ticker
                            )
                        }
                    )
                    total_invested += currency[0].invested
                    total_derived += currency[0].income
                    total_worth += currency[0].amount * price

                user: User = PostgreHandler.get(User, uuid=user_id)
                change = 0 if total_invested == 0 else (
                    total_worth - total_invested + total_derived
                ) / total_invested * 100

                return {
                    "type": asset,
                    "worth": total_worth,
                    "change": change,
                    "spent": user.crypto_spent,
                    "derived": user.crypto_derived,
                    "cryptocurrencies": cryptocurrencies
                }

        except BadRequest as error:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Can't recognize request",
                    "details": error.description
                }
            }, 400
