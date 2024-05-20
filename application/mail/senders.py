from threading import Thread

from flask_mail import Message

from . import mail


def send_email_code(code: str, recipient: str) -> None:
    recipient = "timurkotov1999@gmail.com"  # just for tests

    mail.send(message=Message(f"Secret code: {code}", recipients=[recipient]))
