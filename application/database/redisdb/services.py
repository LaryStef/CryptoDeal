from time import time

from . import rediska
from ...utils.cryptography import hash_password
from ...utils.other import generate_id


def create_register_request(data: dict) -> str:
    # data["password"] = hash_password(data["password"])
    request_id = generate_id(16)
    data["attemtps"] = 0
    data["creation_time"] = str(int(time()))
    rediska.json().set("register", request_id, data, nx=True)
    return request_id
