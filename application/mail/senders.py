from flask_mail import Message

from . import mail


def send_register_code(code: str, recipient: str) -> None:
    recipients: list[str] = ["timurkotov1999@gmail.com"]   # just for tests
  
    message: Message = Message(f"Registration on CryptoDeal", recipients=recipients)
    message.html = f"""
        <h2>Secret code: {code}<h2>
        <p style="font-size: 14px; color: black">Don't reply to this email<p>
        <p style="font-size: 14px; color: black">Support on Support@cryptodeal.com<p>
    """
    mail.send(message)


def send_restore_code(code: str, recipient: str) -> None:
    recipients: list[str] = ["timurkotov1999@gmail.com"]   # just for tests

    message: Message = Message(f"Password restore on CryptoDeal", recipients=recipients)
    message.html = f"""
        <h2>Secret code: {code}<h2>
        <p style="font-size: 16px; color: black">Warning: If it isn't you, immediately change password<p>
        <p style="font-size: 14px; color: black">Don't reply to this email<p>
        <p style="font-size: 14px; color: black">Support on Support@cryptodeal.com<p>
    """
    mail.send(message)
