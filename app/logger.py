import os
from logging import (
    DEBUG, ERROR, INFO, WARNING, Formatter, Logger, StreamHandler, getLogger
)
from logging.handlers import RotatingFileHandler

from flask import Flask

from app.config import appConfig


def setup_logging(app: Flask) -> None:
    log_directory: str = os.path.dirname("logs/")
    os.makedirs(log_directory, exist_ok=True)
    general_log_file: str = os.path.join(log_directory, "app.log")
    error_log_file: str = os.path.join(log_directory, "errors.log")
    celery_log_file: str = os.path.join(log_directory, "celery.log")

    formatter: Formatter = Formatter(
        fmt="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",  # noqa: E501
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_general_handler: RotatingFileHandler = RotatingFileHandler(
        filename=general_log_file,
        mode="a",
        maxBytes=appConfig.MAX_BYTES_PER_FILE,
        backupCount=appConfig.BACKUP_COUNT
    )
    file_general_handler.setLevel(INFO)
    file_general_handler.setFormatter(formatter)

    file_error_handler: RotatingFileHandler = RotatingFileHandler(
        filename=error_log_file,
        mode="a",
        maxBytes=appConfig.MAX_BYTES_PER_FILE,
        backupCount=appConfig.BACKUP_COUNT
    )
    file_error_handler.setLevel(ERROR)
    file_error_handler.setFormatter(formatter)

    file_celery_handler: RotatingFileHandler = RotatingFileHandler(
        filename=celery_log_file,
        mode="a",
        maxBytes=appConfig.MAX_BYTES_PER_FILE,
        backupCount=appConfig.BACKUP_COUNT
    )
    file_celery_handler.setLevel(INFO)
    file_celery_handler.setFormatter(formatter)

    console_handler: StreamHandler = StreamHandler()
    console_handler.setLevel(WARNING)
    console_handler.setFormatter(formatter)

    app.logger.setLevel(INFO)
    app.logger.handlers = []
    app.logger.addHandler(file_error_handler)
    app.logger.addHandler(file_general_handler)
    app.logger.addHandler(console_handler)

    werkzeug_logger: Logger = getLogger("werkzeug")
    werkzeug_logger.setLevel(INFO)
    werkzeug_logger.handlers = []
    werkzeug_logger.addHandler(console_handler)
    werkzeug_logger.addHandler(file_error_handler)
    werkzeug_logger.addHandler(file_general_handler)

    celery_logger: Logger = getLogger("celery")
    celery_logger.setLevel(INFO)
    celery_logger.handlers = []
    celery_logger.addHandler(file_celery_handler)
    celery_logger: Logger = getLogger("celery.task")
    celery_logger.setLevel(INFO)
    celery_logger.handlers = []
    celery_logger.addHandler(file_celery_handler)

    root_logger: Logger = getLogger()
    root_logger.setLevel(DEBUG)
    root_logger.addHandler(file_error_handler)
