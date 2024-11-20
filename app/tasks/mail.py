from celery import shared_task
from flask_mail import Message

from app.logger import logger
from app.mail import mail


class _TaskConfig():
    default_retry_delay: int = 60
    max_retries: int = 3
    task_time_limit: int = 20
    priority: int = 8


taskConfig: _TaskConfig = _TaskConfig()


@shared_task(
    name="send_register_code",
    bind=True,
    default_retry_delay=taskConfig.default_retry_delay,
    max_retries=taskConfig.max_retries,
    task_time_limit=taskConfig.task_time_limit,
    priority=taskConfig.priority
)
def send_register_code(code: str, recipient: str) -> None:
    recipient = "timurkotov1999@gmail.com"    # just for tests

    message: Message = Message("Registration on CryptoDeal",
                               recipients=[recipient])
    message.html = f"""
        <h2>Secret code: {code}<h2>
        <p style="font-size: 12px; color: black">Don't reply to this email<p>
        <p style="font-size: 12px; color: black">Support on
        Support@cryptodeal.com<p>
    """
    mail.send(message)
    logger.info(msg=f"registaration code sent to {recipient}")


@shared_task(
    name="send_restore_code",
    bind=True,
    default_retry_delay=taskConfig.default_retry_delay,
    max_retries=taskConfig.max_retries,
    task_time_limit=taskConfig.task_time_limit,
    priority=taskConfig.priority
)
def send_restore_code(code: str, recipient: str) -> None:
    recipient = "timurkotov1999@gmail.com"    # just for tests

    message: Message = Message("Password restore on CryptoDeal",
                               recipients=[recipient])
    message.html = f"""
        <h2>Secret code: {code}<h2>
        <p style="font-size: 16px; color: black">Warning: If it isn't you,
        immediately change password<p>
        <p style="font-size: 12px; color: black">Don't reply to this email<p>
        <p style="font-size: 12px; color: black">Support on
        Support@cryptodeal.com<p>
    """
    mail.send(message)
    logger.info(msg=f"password restore code sent to {recipient}")


@shared_task(
    name="send_scrf_attention",
    bind=True,
    default_retry_delay=taskConfig.default_retry_delay,
    max_retries=taskConfig.max_retries,
    task_time_limit=taskConfig.task_time_limit,
    priority=taskConfig.priority
)
def send_scrf_attention(recipient: str, origin: str | None) -> None:
    recipient: str = "timurkotov1999@gmail.com"    # just for tests

    message: Message = Message("SCRF attack attention", recipients=[recipient])
    message.html = f"""
        <h2 style="color: black">Attention: your account is under attack!</h2>
        <p style="display: inline; font-size: 14px; color: black">    We are
        aware that your account is currently under SCRF attack (Cross-site
        request forgery)</p>
        <span style="display: inline; font-size: 14px; font-weight: 700;
        color: black">{" " if origin is None else " from " + origin + " "}
        </span>
        <p style="display: inline; font-size: 14px; color: black">and we are
        taking immediate action to secure your account. Please, be careful:
        avoid clicking on links from suspicious or unknown sources, as they
        may lead to malicious websites designed to send requests from your
        behalf.</p>
        <div>
            <p style="font-size: 14px; color: black">If you have any concerns
            or questions, please feel free to reach out to our customer
            support team for assistance. Your security and privacy are our top
            priorities and we are committed to ensuring the safety of your
            account. Thank you for your cooperation and understanding in this
            matter.</p>
        </div>
        <p style="font-size: 14px; color: black">Sincerely,</p>
        <p style="font-size: 14px; color: black">CryptoDeal Security Team</p>

        <p style="font-size: 12px; color: black; padding-top: 5%">Don't reply
        to this email<p>
        <p style="font-size: 12px; color: black">Support on
        Support@cryptodeal.com<p>
    """
    mail.send(message)
    logger.warning(msg=f"scrf attention sent to {recipient}")
