from flask_sqlalchemy import SQLAlchemy

from .models.cryptocourse import CryptoCourse
from .models.cryptocurrency import CryptoCurrency
from .models.cryptocurrency_wallet import CryptocurrencyWallet
from .models.fiat_wallet import FiatWallet
from .models.session import Session
from .models.user import User


db: SQLAlchemy = SQLAlchemy()


__all__ = [
    "User",
    "Session",
    "CryptoCurrency",
    "CryptoCourse",
    "FiatWallet",
    "CryptocurrencyWallet"
]
