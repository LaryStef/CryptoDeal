import typing as t
from time import time

from celery import shared_task

from ..database.redisdb import rediska


tasks_config: dict[str, int | bool] = {
    "bind": True,
    "default_retry_delay": 60,
    "max_retries": 3,
    "task_time_limit": 15,
    "priority": 8
}


@shared_task(name="delete_expired_applications", options=tasks_config)
def delete_expired_applications():
    register_applications: dict[str, t.Any] = rediska.json().get("register")

    for id_, data in register_applications.items():
        if data.get("deactivation_time") < int(time()):
            rediska.json().delete("register", id_)

    restore_applications: dict[str, t.Any] = \
        rediska.json().get("password_restore")

    for id_, data in restore_applications.items():
        if data.get("deactivation_time") < int(time()):
            rediska.json().delete("password_restore", id_)
