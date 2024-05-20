from time import time
from random import randint
from threading import Thread

from flask_mail import Message

from . import rediska
from ...utils.cryptography import hash_password
from ...utils.other import generate_id
from ...mail import mail


def create_register_request(data: dict) -> str:
    # data["password"] = hash_password(data["password"])
    # TODO password hash

    request_id = generate_id(16)

    data["email"] = "timurkotov1999@gmail.com"  # just for tests

    data["code"] = "".join([str(randint(0, 10)) for _ in range(5)])
    
    thread = Thread(target=lambda message: mail.send, args=[Message(f"Secret code: {data['code']}", recipients=[data["email"]])])
    thread.start()
    # mail.send(message=Message(f"Secret code: {data['code']}", recipients=[data["email"]]))

    data["attemtps"] = 0
    data["creation_time"] = str(int(time()))
    data["last_send_mail_request"] = str(int(time()))
    rediska.json().set("register", request_id, data, nx=True)
    return request_id
