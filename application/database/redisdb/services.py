from time import time
from random import randint

from ...config import AppConfig
from . import rediska
from ...utils.generators import generate_id
from ...mail.senders import send_email_code


def create_register_request(data: dict) -> str:
    # TODO password hash

    request_id = generate_id(16)

    data["code"] = "".join([str(randint(0, 9)) for _ in range(6)])
    send_email_code(data["code"], data["email"])

    data["refresh_attempts"] = 0
    data["verify_attempts"] = 0
    data["creation_time"] = int(time())
    data["accept_new_request"] = int(time()) + AppConfig.MAIL_CODE_COOLDOWN
    rediska.json().set("register", request_id, data, nx=True)
    return request_id


def refresh_register_code(data: dict, request_id: str):
    data["refresh_attempts"] = data["refresh_attempts"] + 1
    data["accept_new_request"] = int(time()) + AppConfig.MAIL_CODE_COOLDOWN

    data["code"] = "".join([str(randint(0, 9)) for _ in range(6)])
    send_email_code(data["code"], data["email"])

    rediska.json().delete("register", request_id)
    rediska.json().set("register", request_id, data, nx=True)


def increase_verify_attempts(data: dict, request_id: str):
    data["verify_attempts"] = data["verify_attempts"] + 1

    rediska.json().delete("register", request_id)
    rediska.json().set("register", request_id, data, nx=True)
