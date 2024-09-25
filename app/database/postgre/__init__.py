from flask_sqlalchemy import SQLAlchemy

from .models.user import User
from .models.session import Session
from .models.cryptocurrency import CryptoCurrency
from .models.cryptocourse import CryptoCourse
from .models.fiat_wallet import FiatWallet
from .models.cryptocurrency_wallet import CryptocurrencyWallet


db: SQLAlchemy = SQLAlchemy()


__all__ = [
    "User",
    "Session",
    "CryptoCurrency",
    "CryptoCourse",
    "FiatWallet",
    "CryptocurrencyWallet"
]
