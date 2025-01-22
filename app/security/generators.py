from random import randint
from string import ascii_letters, digits


def generate_id(length: int) -> str:
    symbols: str = ascii_letters + digits
    _id: str = ""

    for _ in range(length):
        _id += symbols[randint(0, 61)]
    return _id
