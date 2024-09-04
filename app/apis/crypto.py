import typing as t
from datetime import datetime, UTC

from flask import url_for
from flask_restx import Namespace, Resource
from sqlalchemy import ScalarResult

from ..database.postgre.services import get
from ..database.postgre.models import CryptoCurrency, CryptoCourse


api: Namespace = Namespace("crypto", path="/crypto/")

_CurrencyData: t.TypeAlias = list[dict[str, str | int]]


@api.route("/list")
class List(Resource):
    def get(self) -> tuple[int | dict[str, _CurrencyData]]:
        # response example
        # {
        #     "CryptoCurrencyList": [
        #         {
        #             "name": "Ethereum",
        #             "ticker": "ETH",
        #             "logo": "/static/png/cryptocurrency/Ethereum",
        #             "price": 2682.823913,
        #             "volume": 7433271729.333189,
        #             "change": -6.240546710846617
        #         },
        #         {
        #             "name": "Bitcoin",
        #             "ticker": "BTC",
        #             "logo": "/static/png/cryptocurrency/Bitcoin",
        #             "price": 72916.728154,
        #             "volume": 28821829110.47828,
        #             "change": 8.263753024401588
        #         },
        #         {
        #             "name": "Tether",
        #             "ticker": "USDT",
        #             "logo": "/static/png/cryptocurrency/Tether",
        #             "price": 1.000523,
        #             "volume": 91738219.0,
        #             "change": 0.014194591860516859
        #         }
        #     ]
        # }

        currencies: ScalarResult[CryptoCurrency] = get(
            table=CryptoCurrency,
            many=True
        )
        hour: int = datetime.now(UTC).hour
        currency_list: _CurrencyData = []

        for currency in currencies:
            course_day_ago: ScalarResult[CryptoCourse] = get(
                table=CryptoCourse,
                ticker=currency.ticker,
                time_frame="hour" + str(hour + 1)
            )
            new_course: ScalarResult[CryptoCourse] = get(
                table=CryptoCourse,
                ticker=currency.ticker,
                time_frame="hour" + str(hour)
            )

            currency_list.append(
                {
                    "name": currency.name,
                    "ticker": currency.ticker,
                    "logo": url_for(
                        "static",
                        filename=f"png/cryptocurrency/{currency.name}"
                    ),
                    "price": new_course.price,
                    "volume": currency.volume,
                    "change": (new_course.price / course_day_ago.price - 1)*100
                }
            )

        return {
            "CryptoCurrencyList": currency_list
        }, 200
