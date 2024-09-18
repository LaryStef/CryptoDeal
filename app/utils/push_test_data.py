from random import uniform

from .generators import generate_id
from ..database.postgre import db
from ..database.postgre.models import CryptoCurrency, CryptoCourse


def push_day_course(min_: float, max_: float, ticker: str):
    for hour in range(24):
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                time_frame=f"hour{hour}",
                price=uniform(min_, max_)
            )
        )


def push_month_course(min_: float, max_: float, ticker: str):
    for day in range(1, 32):
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                time_frame=f"day{day}",
                price=uniform(min_, max_)
            )
        )


def push_year_course(min_: float, max_: float, ticker: str):
    for month in range(1, 13):
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                time_frame=f"month{month}fst",
                price=uniform(min_, max_)
            )
        )
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                time_frame=f"month{month}mid",
                price=uniform(min_, max_)
            )
        )


def push_cryptocurrencies():
    db.session.add(
        CryptoCurrency(
            ticker="BTC",
            name="Bitcoin",
            description="""Bitcoin description""",
            volume=28_388_811_901.291_736
        )
    )
    push_day_course(38928.0, 82931.0, "BTC")
    push_month_course(33928.0, 89931.0, "BTC")
    push_year_course(27928.0, 101931.0, "BTC")

    db.session.add(
        CryptoCurrency(
            ticker="ETH",
            name="Ethereum",
            description="""Ethereum description""",
            volume=7_865_323_997.264_321
        )
    )
    push_day_course(2373.0, 2963.0, "ETH")
    push_month_course(2173.0, 3263.0, "ETH")
    push_year_course(1973.0, 3463.0, "ETH")

    db.session.add(
        CryptoCurrency(
            ticker="USDT",
            name="Tether",
            description="""Tether description""",
            volume=42_177_103_848.376_772
        )
    )
    push_day_course(0.993_813, 1.100_362, "USDT")
    push_month_course(0.993_813, 1.100_362, "USDT")
    push_year_course(0.993_813, 1.100_362, "USDT")

    db.session.commit()
