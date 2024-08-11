import typing as t
from time import time

from celery import shared_task

from ..database.redisdb import rediska


class TaskConfig():
    max_retries: int = 0,
    task_time_limit: int = 10,
    priority: int = 3


taskConfig: TaskConfig = TaskConfig()


@shared_task(
    name="delete_expired_applications",
    bind=True,
    max_retries=taskConfig.max_retries,
    task_time_limit=taskConfig.task_time_limit,
    priority=taskConfig.priority
)
def delete_expired_applications(self):
    register_applications: dict[str, t.Any] = rediska.json().get("register")

    for id_, data in register_applications.items():
        if data.get("deactivation_time") < int(time()):
            rediska.json().delete("register", id_)

    restore_applications: dict[str, t.Any] = \
        rediska.json().get("password_restore")

    for id_, data in restore_applications.items():
        if data.get("deactivation_time") < int(time()):
            rediska.json().delete("password_restore", id_)
