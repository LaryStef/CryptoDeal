from flask_mail import Message

from . import mail


def send_register_code(code: str, recipient: str) -> None:
    recipients = ["timurkotov1999@gmail.com"]   # just for tests
  
    message = Message(f"Registration on CryptoDeal", recipients=recipients)
    message.html = f"""
        <h2>Secret code: {code}<h2>
        <p style="font-size: 14px; color: black">Don't reply to this email<p>
        <p style="font-size: 14px; color: black">Support on Support@cryptodeal.com<p>
    """
    mail.send(message)


def send_restore_code(code: str, recipient: str) -> None:
    recipients = ["timurkotov1999@gmail.com"]   # just for tests

    # TODO add ...if it isn't you... to message

    message = Message(f"Password restore on CryptoDeal", recipients=recipients)
    message.html = f"""
        <h2>Secret code: {code}<h2>
        <p style="font-size: 14px; color: black">Don't reply to this email<p>
        <p style="font-size: 14px; color: black">Support on Support@cryptodeal.com<p>
    """
    mail.send(message)
