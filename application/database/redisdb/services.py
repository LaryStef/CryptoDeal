from . import rediska
from ...utils.cryptography import hash_password



def create_register_request(data: dict) -> None:
    # data["password"] = hash_password(data["password"])
    request_id = data.pop("request_id")
    rediska.json().set("register", request_id, data, nx=True)
