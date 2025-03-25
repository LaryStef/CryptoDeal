from logging import Formatter, Logger
from typing import Any

from celery import Celery, Task
from celery.signals import after_setup_logger, after_setup_task_logger
from flask import Flask


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app: Celery = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


@after_setup_logger.connect
def setup_celery_logger(
    logger: Logger,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> None:
    formatter: Formatter = Formatter(
        fmt="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",  # noqa: E501
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    for handler in logger.handlers:
        handler.setFormatter(formatter)


@after_setup_task_logger.connect
def setup_celery_task_logger(
    logger: Logger,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> None:
    formatter: Formatter = Formatter(
        fmt="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",  # noqa: E501
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    for handler in logger.handlers:
        handler.setFormatter(formatter)


class TaskConfig():
    def __init__(
        self,
        default_retry_delay: int = 0,
        max_retries: int = 0,
        task_time_limit: int = 10,
        priority: int = 3
    ) -> None:
        self.default_retry_delay = default_retry_delay
        self.max_retries = max_retries
        self.task_time_limit = task_time_limit
        self.priority = priority
