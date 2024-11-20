import typing as t
from calendar import monthrange
from datetime import UTC, datetime

from flask import request, url_for
from flask_restx import Namespace, Resource
from sqlalchemy import ScalarResult
from werkzeug.exceptions import BadRequest, NotFound

from app.database.postgre.models import CryptoCourse, CryptoCurrency
from app.database.postgre.services import PostgreHandler
from app.shemas import CryptoTransactionSchema
from app.utils.aliases import RESTError
from app.utils.decorators import authorization_required
from app.utils.JWT import validate_token


api: Namespace = Namespace("crypto", path="/crypto/")

_ListResponse: t.TypeAlias = list[dict[str, str | int]]
_CurrencyResponse: t.TypeAlias = dict[
    str, str | int | float | list[int | float]
]


@api.route("/list")
class List(Resource):
    def get(self) -> tuple[int, dict[str, _ListResponse]]:
        # response example
        # {
        #     "CryptoCurrencyList": [
        #         {
        #             "name": "Bitcoin",
        #             "ticker": "BTC",
        #             "logoUrl": "/static/svg/cryptocurrency/BTC.svg",
        #             "pageUrl": "/crypto/BTC",
        #             "price": 65673.1535301987,
        #             "volume": 28388811901.2917,
        #             "change": 32.8637107645426
        #         },
        #         {
        #             "name": "Ethereum",
        #             "ticker": "ETH",
        #             "logoUrl": "/static/svg/cryptocurrency/ETH.svg",
        #             "pageUrl": "/crypto/ETH",
        #             "price": 2387.54530484819,
        #             "volume": 7865323997.26432,
        #             "change": -1.78983414036351
        #         },
        #         {
        #             "name": "Tether",
        #             "ticker": "USDT",
        #             "logoUrl": "/static/svg/cryptocurrency/USDT.svg",
        #             "pageUrl": "/crypto/USDT",
        #             "price": 1.02090749587501,
        #             "volume": 42177103848.3768,
        #             "change": -3.94483257123361
        #         }
        #     ]
        # }

        currencies: ScalarResult[CryptoCurrency] = PostgreHandler.get(
            table=CryptoCurrency,
            many=True
        )
        currency_list: _ListResponse = []

        for currency in currencies:
            currency_list.append(
                {
                    "name": currency.name,
                    "ticker": currency.ticker,
                    "logoUrl": url_for(
                        "static",
                        filename=f"svg/cryptocurrency/{currency.ticker}.svg"
                    ),
                    "pageUrl": url_for(
                        "main.currency",
                        ticker=currency.ticker
                    ),
                    "price": PostgreHandler.get_crypto_price(
                        PostgreHandler,
                        ticker=currency.ticker
                    ).price,
                    "volume": currency.volume,
                    "change": PostgreHandler.calculate_daily_change(
                        ticker=currency.ticker
                    )
                }
            )

        return {
            "CryptoCurrencyList": currency_list
        }, 200


@api.route("/<string:ticker>/<string:frame>")
class CryptoCurrencyData(Resource):
    def get(
        self, ticker: str, frame: t.Literal["day", "month", "year"]
    ) -> RESTError | dict[str, str | list[int | float]]:
        # response example
        # {
        #     "ticker": "ETH",
        #     "frame": "hour",
        #     "max": 2892.9433335510957,
        #     "min": 2477.3488667840215,
        #     "volume": 7865323997.264321,
        #     "price": 2861.2769881816876,
        #     "change": -0.8153106753556294,
        #     "dataX": [
        #         15,
        #         16,
        #         17,
        #         18,
        #         19,
        #         20,
        #         21,
        #         22,
        #         23,
        #         0,
        #         1,
        #         2,
        #         3,
        #         4,
        #         5,
        #         6,
        #         7,
        #         8,
        #         9,
        #         10,
        #         11,
        #         12,
        #         13,
        #         14
        #     ],
        #     "dataY": [
        #         2884.797046463851,
        #         2581.449498144771,
        #         2867.8517994678778,
        #         2699.494455400336,
        #         2667.566271434009,
        #         2892.9433335510957,
        #         2766.7457729336197,
        #         2834.3491687349238,
        #         2709.4299851672904,
        #         2477.3488667840215,
        #         2717.3481154746414,
        #         2728.0222584743615,
        #         2566.9691755553295,
        #         2775.289778202109,
        #         2792.550468955845,
        #         2636.6031859943855,
        #         2638.3849472857373,
        #         2757.1562940694503,
        #         2784.7968026536614,
        #         2861.7701859540307,
        #         2588.2405829723502,
        #         2650.1253401490467,
        #         2716.5367005266207,
        #         2861.2769881816876
        #     ]
        # }

        currency_data: ScalarResult[CryptoCurrency] = PostgreHandler.get(
            CryptoCurrency,
            ticker=ticker
        )

        if currency_data is None:
            return {
                "error": {
                    "code": "Not Found",
                    "message": "CryptoCurrency not found",
                    "details": "No such cryptocurrency in database"
                }
            }, 404
        if frame not in ["hour", "day", "month"]:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid frame",
                    "details": "No such frame supported by server"
                }
            }, 400

        course_data: ScalarResult[CryptoCourse] = PostgreHandler.get(
            CryptoCourse,
            many=True,
            ticker=ticker,
            type_=frame
        )

        date: datetime = datetime.now(UTC)
        day: int = date.day
        month: int = date.month
        response: _CurrencyResponse = {
            "ticker": ticker,
            "frame": frame,
            "max": 0,
            "min": 0,
            "volume": 0,
            "price": 0,
            "change": 0,
            "dataX": [],
            "dataY": []
        }

        if frame == "hour":
            hour: int = date.hour
            response["dataX"] = [(hour + i + 1) % 24 for i in range(24)]
        elif frame == "day":
            previous_month: int = month - 1 if month > 1 else 12
            last_month_days: int = monthrange(date.year, previous_month)[1]
            response["dataX"] = [
                i for i in range(day + 1, last_month_days + 1)
            ]
            response["dataX"].extend(range(1, day + 1))
        elif frame == "month":
            mid_month: int = 1 if day >= 16 else 0
            response["dataX"] = [i for i in range(month*2+mid_month, 25)]
            response["dataX"].extend(range(1, month*2+mid_month))

        prices: dict[int, float] = {
            raw.number: raw.price for raw in course_data
        }
        response["dataY"] = [prices[num] for num in response["dataX"]]

        current_price: float = PostgreHandler.get(
            CryptoCourse, ticker=ticker, type_="hour", number=date.hour
        ).price

        response["dataY"][-1] = current_price
        response["price"] = current_price
        response["min"] = min(response["dataY"])
        response["max"] = max(response["dataY"])
        response["volume"] = currency_data.volume
        response["change"] = (
            current_price / response["dataY"][0] - 1
        )*100
        return response, 200


@api.route("/price/<string:ticker>")
class CryptoCurrencyPrice(Resource):
    def get(self, ticker: str) -> RESTError | dict[str, float | str]:
        # response example
        # {
        #     "ticker": "ETH",
        #     "price": 2861.2769881816876
        # }

        currency: ScalarResult[CryptoCurrency] = PostgreHandler.get(
            CryptoCurrency,
            ticker=ticker
        )

        if currency is None:
            return {
                "error": {
                    "code": "Not Found",
                    "message": "CryptoCurrency not found",
                    "details": "No such cryptocurrency in database"
                }
            }, 404

        price: float = PostgreHandler.get(
            CryptoCourse,
            ticker=ticker,
            type_="hour",
            number=datetime.now(UTC).hour
        ).price

        return {
            "ticker": ticker,
            "price": price
        }, 200


@api.route("/overview/<string:ticker>")
class CryptoCurrencyOverview(Resource):
    def get(self, ticker: str) -> RESTError:
        # response example
        # {
        #     "ticker": "ETH",
        #     "name": "Ethereum",
        #     "description": "Ethereum is...",
        #     "logoUrl": "/static/svg/cryptocurrency/ETH.svg"
        # }

        currency: ScalarResult[CryptoCurrency] = PostgreHandler.get(
            CryptoCurrency,
            ticker=ticker
        )

        if currency is None:
            return {
                "error": {
                    "code": "Not Found",
                    "message": "CryptoCurrency not found",
                    "details": "No such cryptocurrency in database"
                }
            }, 404

        return {
            "ticker": ticker,
            "name": currency.name,
            "description": currency.description,
            "logoUrl": url_for(
                "static",
                filename=f"svg/cryptocurrency/{ticker}.svg"
            ),
        }, 200


@api.route("/transaction")
class Transaction(Resource):
    @authorization_required("access")
    def post(self) -> RESTError | tuple[str, int]:
        try:
            transaction_data: dict[str, str] = request.json

            access_token: str | None = request.cookies.get("access_token")
            access_payload: t.Any = validate_token(
                token=access_token,
                type="access"
            )
            user_id: str = access_payload.get("uuid", "")

            if CryptoTransactionSchema().validate(transaction_data):
                raise BadRequest(description="Invalid format of data")

            PostgreHandler.provide_crypto_transaction(
                user_id,
                ticker=transaction_data["ticker"],
                amount=round(float(transaction_data["amount"]), ndigits=2),
                type_=transaction_data["type"]
            )
            return "OK", 200

        except (BadRequest, NotFound) as error:
            return {
                "error": {
                    "code": "Bad request",
                    "message": "Invalid request",
                    "details": error.description
                }
            }, 400


@api.route("/transaction/history")
class Histoty(Resource):
    @authorization_required("access")
    def get(self) -> RESTError | dict[str, list[dict[str, str | int]]]:
        access_token: str | None = request.cookies.get("access_token")
        access_payload: t.Any = validate_token(
            token=access_token,
            type="access"
        )

        return {
            "history": PostgreHandler.get_crypto_history(
                access_payload.get("uuid", "")
            )
        }, 200
