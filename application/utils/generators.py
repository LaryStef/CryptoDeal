from string import ascii_letters, digits
from random import randint


def generate_id(length: int) -> str:
    symbols: str = ascii_letters + digits
    _id: str = ""

    for _ in range(length):
        _id += symbols[randint(0, 61)]
    return _id


def generate_mail_code() -> str:
    return "".join([str(randint(0, 10)) for _ in range(6)])
