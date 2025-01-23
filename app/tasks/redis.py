import typing as t
from logging import Logger, getLogger
from time import time

from celery import shared_task

from app.config import appConfig
from app.database.redisdb import rediska
from app.tasks import TaskConfig as TaskConfig


taskConfig: TaskConfig = TaskConfig()
logger: Logger = getLogger("celery")


@shared_task(
    name="delete_expired_applications",
    bind=True,
    max_retries=taskConfig.max_retries,
    task_time_limit=taskConfig.task_time_limit,
    priority=taskConfig.priority
)
def delete_expired_applications(self) -> None:
    register_applications: dict[str, t.Any] = rediska.json().get("register")

    for id_, data in register_applications.items():
        if data.get("deactivation_time") < int(
            time()
        ) + appConfig.TIMESTAMP_OFFSET:
            rediska.json().delete("register", id_)

    restore_applications: dict[str, t.Any] = rediska.json().get(
        "password_restore"
    )

    for id_, data in restore_applications.items():
        if data.get("deactivation_time") < int(
            time()
        ) + appConfig.TIMESTAMP_OFFSET:
            rediska.json().delete("password_restore", id_)
    logger.info(msg="expired applications in redis deleted")
