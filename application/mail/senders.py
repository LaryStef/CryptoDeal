from threading import Thread

from flask_mail import Message

from . import mail


def send_email_code(code: str, recipient: str) -> None:
    recipient = "timurkotov1999@gmail.com"  # just for tests
    
    message = Message(f"Registration on CryptoDeal", recipients=[recipient])
    message.html = f"""
        <h2 style>Secret code: {code}<h2>
        <p style="font-size: 14px; color: black">Don't reply to this email<p>
        <p style="font-size: 14px; color: black">Support on Support@cryptodeal.com<p>
    """
    mail.send(message)
