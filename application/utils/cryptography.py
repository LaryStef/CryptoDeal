from bcrypt import gensalt, hashpw


def hash_password(password: str) -> (str, str):
    salt = gensalt()
    hash = hashpw(password.encode("utf-8"), salt)
    return hash.decode("utf-8"), salt.decode("utf-8")
