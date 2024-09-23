import typing as t
from datetime import datetime, UTC
from calendar import monthrange

from flask import url_for
from flask_restx import Namespace, Resource
from sqlalchemy import ScalarResult

from ..database.postgre.services import get
from ..database.postgre.models import CryptoCurrency, CryptoCourse
from ..utils.aliases import RESTError


api: Namespace = Namespace("crypto", path="/crypto/")

_ListResponse: t.TypeAlias = list[dict[str, str | int]]
_ChartData: t.TypeAlias = dict[
    str, dict[
        str, float | int | bool | dict[int, float]
    ]
]


@api.route("/list")
class List(Resource):
    def get(self) -> tuple[int | dict[str, _ListResponse]]:
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

        currencies: ScalarResult[CryptoCurrency] = get(
            table=CryptoCurrency,
            many=True
        )
        hour: int = datetime.now(UTC).hour
        currency_list: _ListResponse = []

        for currency in currencies:
            # change get for new table model
            course_day_ago: ScalarResult[CryptoCourse] | None = get(
                table=CryptoCourse,
                ticker=currency.ticker,
                type_="hour",
                number=(hour + 1) % 24
            )
            new_course: ScalarResult[CryptoCourse] | None = get(
                table=CryptoCourse,
                ticker=currency.ticker,
                type_="hour",
                number=hour
            )

            if course_day_ago is None or new_course is None:
                return {
                    "CryptoCurrencyList": []
                }, 200

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
                    "price": new_course.price,
                    "volume": currency.volume,
                    "change": (new_course.price / course_day_ago.price - 1)*100
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
        #     "ticker": "BTC",
        #     "frame": "day",
        #     "dataX": [
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
        #         14,
        #         15,
        #         16,
        #         17,
        #         18
        #     ],
        #     "dataY": [
        #         2455.724673,
        #         2482.600027,
        #         2470.579307,
        #         2419.005645,
        #         2423.307852,
        #         2472.691506,
        #         2675.649755,
        #         2542.843266,
        #         2498.632522,
        #         2589.430657,
        #         2699.292851,
        #         2519.367414,
        #         2558.913914,
        #         2576.874516,
        #         2632.828609,
        #         2775.522117,
        #         2771.943085,
        #         2706.550265,
        #         2830.398057,
        #         2790.814923,
        #         2828.539856,
        #         2975.606936,
        #         2969.751264,
        #         2955.923484
        #     ]
        # }

        currency_data: ScalarResult[CryptoCurrency] = get(
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

        course_data: ScalarResult[CryptoCourse] = get(
            CryptoCourse,
            many=True,
            ticker=ticker,
            type_=frame
        )

        date: datetime = datetime.now(UTC)
        day: int = date.day
        month: int = date.month
        response: dict[str, str | int | float | list[int | float]] = {
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

        response["price"] = response["dataY"][-1]
        response["min"] = min(response["dataY"])
        response["max"] = max(response["dataY"])
        response["volume"] = currency_data.volume
        response["change"] = (
            response["dataY"][-1] / response["dataY"][-1] - 1
        )*100
        return response, 200
