from bcrypt import gensalt, hashpw


def hash_password(password: str) -> str:
    salt: bytes = gensalt()
    hash: bytes = hashpw(password.encode("utf-8"), salt)
    return hash.decode("utf-8")
