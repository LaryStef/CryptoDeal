import os
from enum import IntEnum
from logging import (
    CRITICAL, DEBUG, ERROR, INFO, WARNING,
    Formatter, Handler, Logger, StreamHandler, getLogger
)
from logging.handlers import RotatingFileHandler

from flask import Flask

from app.config import appConfig


class _Levels(IntEnum):
    DEBUG = DEBUG
    ERROR = ERROR
    INFO = INFO
    WARNING = WARNING
    CRITICAL = CRITICAL


def _setup_file_handler(
    *,
    log_file: str,
    level: int,
    formatter: Formatter
) -> RotatingFileHandler:
    file_handler: RotatingFileHandler = RotatingFileHandler(
        filename=log_file,
        mode="a",
        maxBytes=appConfig.MAX_BYTES_PER_FILE,
        backupCount=appConfig.BACKUP_COUNT
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    return file_handler


def _setup_console_handler(
    *,
    level: int,
    formatter: Formatter
) -> StreamHandler:
    console_handler: StreamHandler = StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    return console_handler


def _setup_logger(
    logger: Logger,
    *,
    level: _Levels,
    handlers: list[Handler]
) -> None:
    logger.setLevel(level)
    logger.handlers = []
    for handler in handlers:
        logger.addHandler(handler)


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

    file_general_handler: RotatingFileHandler = _setup_file_handler(
        log_file=general_log_file,
        level=INFO,
        formatter=formatter
    )
    file_error_handler: RotatingFileHandler = _setup_file_handler(
        log_file=error_log_file,
        level=ERROR,
        formatter=formatter
    )
    file_celery_handler: RotatingFileHandler = _setup_file_handler(
        log_file=celery_log_file,
        level=INFO,
        formatter=formatter
    )
    console_handler: StreamHandler = _setup_console_handler(
        level=WARNING,
        formatter=formatter
    )

    _setup_logger(
        app.logger,
        level=_Levels.INFO,
        handlers=[console_handler, file_error_handler, file_general_handler]
    )
    _setup_logger(
        getLogger("werkzeug"),
        level=_Levels.INFO,
        handlers=[console_handler, file_error_handler, file_general_handler]
    )
    _setup_logger(
        getLogger("celery"),
        level=_Levels.INFO,
        handlers=[file_celery_handler]
    )
    _setup_logger(
        getLogger("celery.task"),
        level=_Levels.INFO,
        handlers=[file_celery_handler]
    )
    _setup_logger(
        getLogger(),
        level=_Levels.DEBUG,
        handlers=[file_error_handler]
    )
