# flake8: noqa

import os
from logging.config import dictConfig
from typing import TypeAlias

from celery.schedules import crontab
from dotenv import load_dotenv
from flask import Config
from kombu import Queue


load_dotenv()
_CeleryConf: TypeAlias = dict[str, str | bool | int | list[str] | dict[str, dict[str, str | crontab]] | dict[str, int] | tuple[Queue]]


class AppConfig(Config):
    # app
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://postgres:{os.getenv('DATABASE_PASSWORD')}@localhost:5432/postgres"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")

    # mail
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USE_SSL: bool = True
    MAIL_USERNAME: str | None = os.getenv("MAIL")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: tuple[str, None] = ("CryptoDeal", os.getenv("MAIL"))
    # cooldown and cooldownRec in auth.js must be same or longer
    MAIL_CODE_COOLDOWN: int = 20
    MAIL_CODE_VERIFY_ATTEMPTS: int = 3
    MAIL_CODE_REFRESH_ATTEMTPTS: int = 3

    # user
    START_USD_BALANCE = 10000
    START_RUB_BALANCE = 1000000

    # authentification and authorization
    REGISTER_LIFETIME: int = 1200
    RESTORE_LIFETIME: int = 1200
    # restore_cooldown must be less then restore_lifetime
    ACCESS_TOKEN_LIFETIME: int = 300
    RESTORE_COOLDOWN: int = 2000
    REFRESH_TOKEN_LIFETIME: int = 12000
    JWT_ENCODING_ALGORITHM: str = "HS256"

    # celery
    CELERY: _CeleryConf = {
        "broker_url": "redis://localhost:6379/0",
        "task_ignore_result": True,
        "task_time_limit": 10,
        "imports": (
            "app.tasks.mail",
            "app.tasks.postgre",
            "app.tasks.redis",
        ),
        "task_default_queue": "normal",
        "task_queues": (
            Queue(name="normal", routing_key=".mail_tasks.#"),
            Queue(name="low", routing_key=".db_tasks.#"),
        ),
        "task_routes": {
            "app.tasks.mail.#": {
                "queue": "normal"
            },
            "app.tasks.postgre.#": {
                "queue": "low",
            },
            "app.tasks.redis.#": {
                "queue": "low",
            }
        },
        "worker_max_memory_per_child": 50000,
        "broker_transport_options": {
            "visibility_timeout": 43200
        },
        "timezone": "UTC",
        "worker_logfile": "cryptodeal.log",
        "beat_schedule": {
                "clear-postgre": {
                    "task": "delete_expired_sessions",
                    "schedule": crontab(minute="0", hour="*/12")
                },
                "clear-redis": {
                    "task": "delete_expired_applications",
                    "schedule": crontab(minute="0", hour="*/12")
                }
        },
        "worker_hijack_root_logger": False,
        "worker_redirect_stdouts": True,
        "broker_connection_retry_on_startup": True
    }

    def __init__(self) -> None:
        super().__init__(root_path=os.path)

        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "format": "%(asctime)s %(levelname)s in %(module)s at %(lineno)d line: %(message)s"
                    }
                },
                "handlers": {
                    "stderr": {
                        "class": "logging.StreamHandler",
                        "formatter": "default",
                        "level": "WARNING",
                        "stream": "ext://sys.stderr"
                    },
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "formatter": "default",
                        "level": "INFO",
                        "filename": "cryptodeal.log",
                        "mode": "a",
                        "maxBytes": 1000000,
                        "backupCount": 3
                    }
                },
                "root": {
                    "level": "INFO",
                    "handlers": [
                        "stderr",
                        "file"
                    ]
                }
            }
        )

appConfig: AppConfig = AppConfig()
