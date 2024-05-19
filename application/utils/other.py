from string import ascii_letters, digits
from random import randint


def generate_id(length: int) -> str:
    symbols = ascii_letters + digits
    _id = ""

    for _ in range(length):
        _id += symbols[randint(0, 61)]
    return _id
