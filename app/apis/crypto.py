import typing as t
from datetime import datetime, UTC

from flask import url_for
from flask_restx import Namespace, Resource
from sqlalchemy import ScalarResult

from ..database.postgre.services import get
from ..database.postgre.models import CryptoCurrency, CryptoCourse


api: Namespace = Namespace("crypto", path="/crypto/")

CurrencyData: t.TypeAlias = list[dict[str, str | int]]


@api.route("/list")
class List(Resource):
    def get(self) -> tuple[int | dict[str, CurrencyData]]:
        currencies: ScalarResult[CryptoCurrency] = get(
            table=CryptoCurrency,
            many=True
        )
        hour: int = datetime.now(UTC).hour
        currency_list: CurrencyData = []

        for currency in currencies:
            course_day_ago: ScalarResult[CryptoCourse] = get(
                table=CryptoCourse,
                ticker=currency.ticker,
                time_frame="hour" + str(hour + 1)
            )
            last_course: ScalarResult[CryptoCourse] = get(
                table=CryptoCourse,
                ticker=currency.ticker,
                time_frame="hour" + str(hour)
            )
            change: float = (last_course.price / course_day_ago.price - 1)*100

            currency_list.append(
                {
                    "name": currency.name,
                    "ticker": currency.ticker,
                    "logo": url_for(
                        "static",
                        filename=f"png/cryptocurrency/{currency.name}"
                    ),
                    "price": last_course.price,
                    "volume": currency.volume,
                    "change": "+" if change >= 0 else "" + change,
                    "posTrend": change >= 0
                }
            )

        return {
            "CryptoCurrencyList": currency_list
        }, 200


# data = {
#     "CryptoCurrencyList": [
#         {
#             "name": "",
#             "ticker": "",
#             "logo": "",
#             "price": 0,
#             "volume": 0,
#             "change": 0
#         }
#     ]
# }


# lst = list(range(9))
# new_lst = [lst[i] if i % 2 == 0 else lst[-i] for i in range(len(lst))]
# print(new_lst)
