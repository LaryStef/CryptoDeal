import typing as t
from datetime import datetime, UTC
from calendar import monthrange

from flask import url_for
from flask_restx import Namespace, Resource
from sqlalchemy import ScalarResult

from ..database.postgre.services import get
from ..database.postgre.models import CryptoCurrency, CryptoCourse


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


@api.route("/<string:ticker>")
class CryptoCurrencyData(Resource):
    def get(self, ticker: str):
        # response example
        # {
        #     "ticker": "BTC",
        #     "name": "Bitcion",
        #     "descrption": "the best crypto ever",
        #     "logoUrl": "/static/png/cryptocurrency/BTC",
        #     "volume": 82838219.209291,
        #     "chartData": {
        #         "start": 9,
        #         "end": 8,
        #         "min": 2419.005645,
        #         "max": 2975.606936,
        #         "change": 3.014194591860516859,
        #         "prices": {
        #             "hour0": 2632.828609,
        #             "hour1": 2542.843266,
        #             "hour2": 2576.874516,
        #             "hour3": 2828.539856,
        #             "hour4": 2830.398057,
        #             "hour5": 2558.913914,
        #             "hour6": 2790.814923,
        #             "hour7": 2955.923484,
        #             "hour8": 2675.649755,
        #             "hour9": 2975.606936,
        #             "hour10": 2589.430657,
        #             "hour11": 2455.724670,
        #             "hour12": 2482.600027,
        #             "hour13": 2498.632520,
        #             "hour14": 2775.522117,
        #             "hour15": 2470.579307,
        #             "hour16": 2969.751264,
        #             "hour17": 2706.550265,
        #             "hour18": 2423.307852,
        #             "hour19": 2771.943085,
        #             "hour20": 2472.691506,
        #             "hour21": 2519.367414,
        #             "hour22": 2699.292851,
        #             "hour23": 2419.005645
        #         }
        #     }
        # }

        # currency_data: ScalarResult[CryptoCurrency] = get(
        #     CryptoCurrency,
        #     ticker=ticker
        # )

        # if currency_data is None:
        #     # TODO change error in response
        #     return {
        #         "error": {
        #             "code": "Bad request",
        #             "message": "Invalid data",
        #             "details": "Invalid token or invalid format of data"
        #         }
        #     }, 400

        # course_data: ScalarResult[CryptoCourse] = get(
        #     CryptoCourse,
        #     many=True,
        #     ticker=ticker
        # )
        # hour: int = datetime.now(UTC).hour
        # day: int = datetime.now(UTC).day
        # month: int = datetime.now(UTC).month
        # year: int = datetime.now(UTC).year
        # previous_month: int = (month + 11) % 12 + 1

        # last_month_days: int = monthrange(year, previous_month)[1]

        # max_hour: float = 0
        # min_hour: float = float("inf")
        # max_day: float = 0
        # min_day: float = float("inf")
        # max_month: float = 0
        # min_month: float = float("inf")

        # if day > 24:
        #     month_start: int = day - 24
        # else:
        #     month_start: int = last_month_days + day - 24

        # chartData: _ChartData = {
        #     "day": {
        #         "start": (hour + 1) % 24,
        #         "end": hour,
        #         "prices": {}
        #     },
        #     "month": {
        #         "month_days": last_month_days,
        #         "start": month_start,
        #         "end": day,
        #         "prices": {}
        #     },
        #     "year": {
        #         "isMidOfMonth": True if day < 16 else False,
        #         "start": previous_month,
        #         "end": month,
        #         "prices": {}
        #     }
        # }

        # for row in course_data:
        #     if row.time_frame.startswith("hour"):
        #         chartData["day"]["prices"][row.time_frame[4:]] = row.price
        #         min_hour = min(min_hour, row.price)
        #         max_hour = max(max_hour, row.price)
        #     elif row.time_frame.startswith("day"):
        #         chartData["month"]["prices"][row.time_frame[3:]] = row.price
        #         min_day = min(min_day, row.price)
        #         max_day = max(max_day, row.price)
        #     if row.time_frame.startswith("month"):
        #         chartData["day"]["prices"][row.time_frame[4:5]] = row.price
        #         min_hour = min(min_hour, row.price)
        #         max_hour = max(max_hour, row.price)

        # response: dict[str, str | float | _ChartData] = {
        #     "ticker": ticker,
        #     "name": currency_data.name,
        #     "description": currency_data.description,
        #     "logoUrl": url_for(
        #         "static",
        #         filename=f"svg/cryptocurrency/{ticker}.svg"
        #     ),
        #     "volume": currency_data.volume,
        #     "chartData": chartData
        # }
        pass
