from time import time
from random import randint

from ...config import AppConfig
from . import rediska
from ...utils.other import generate_id
from ...mail.senders import send_email_code


def create_register_request(data: dict) -> str:
    # TODO password hash

    request_id = generate_id(16)

    data["code"] = "".join([str(randint(0, 10)) for _ in range(5)])
    send_email_code(data["code"], data["email"])

    data["attempts"] = 0
    data["creation_time"] = str(int(time()))
    data["accept_new_request"] = str(int(time()) + AppConfig.MAIL_CODE_COOLDOWN)
    rediska.json().set("register", request_id, data, nx=True)
    return request_id


def refresh_register_code(data: dict, request_id: str):
    data["attempts"] = str(int(data["attempts"]) + 1)
    data["accept_new_request"] = str(int(time()) + AppConfig.MAIL_CODE_COOLDOWN)

    data["code"] = "".join([str(randint(0, 10)) for _ in range(5)])
    send_email_code(data["code"], data["email"])

    rediska.json().delete("register", request_id)
    rediska.json().set("register", request_id, data, nx=True)
