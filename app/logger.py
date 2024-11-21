import os
from typing import TypeAlias, Literal
from logging import (
    DEBUG, ERROR, INFO, Formatter, Logger, StreamHandler, getLogger, Handler
)
from logging.handlers import RotatingFileHandler

from flask import Flask

from app.config import appConfig


_Levels: TypeAlias = Literal[10, 20, 30, 40, 50]


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

    file_general_handler: RotatingFileHandler = setup_file_handler(
        log_file=general_log_file,
        level=INFO,
        formatter=formatter
    )
    file_error_handler: RotatingFileHandler = setup_file_handler(
        log_file=error_log_file,
        level=ERROR,
        formatter=formatter
    )
    file_celery_handler: RotatingFileHandler = setup_file_handler(
        log_file=celery_log_file,
        level=INFO,
        formatter=formatter
    )
    console_handler: StreamHandler = setup_console_handler(
        level=INFO,
        formatter=formatter
    )

    setup_logger(
        app.logger,
        level=INFO,
        handlers=[console_handler, file_error_handler, file_general_handler]
    )
    setup_logger(
        getLogger("werkzeug"),
        level=INFO,
        handlers=[console_handler, file_error_handler, file_general_handler]
    )
    setup_logger(
        getLogger("celery"),
        level=INFO,
        handlers=[file_celery_handler]
    )
    setup_logger(
        getLogger("celery.task"),
        level=INFO,
        handlers=[file_celery_handler]
    )
    setup_logger(
        getLogger(),
        level=DEBUG,
        handlers=[file_error_handler]
    )


def setup_file_handler(
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


def setup_console_handler(
    *,
    level: int,
    formatter: Formatter
) -> StreamHandler:
    console_handler: StreamHandler = StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    return console_handler


def setup_logger(
    logger: Logger,
    *,
    level: _Levels,
    handlers: list[Handler]
) -> None:
    logger.setLevel(level)
    logger.handlers = []
    for handler in handlers:
        logger.addHandler(handler)
