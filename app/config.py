
import os
from typing import TypeAlias

from celery.schedules import crontab
from dotenv import load_dotenv
from flask import Config
from kombu import Queue


load_dotenv()

_CeleryConf: TypeAlias = dict[
    str, str | int | bool | tuple[Queue] | tuple[str] | dict[str, int] | dict[
        str, dict[str, str | crontab]
    ]
]


class AppConfig(Config):
    # app
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('HOST_NETWORK')}:5432/{os.getenv('POSTGRES_NAME')}"  # noqa: E501
    REDIS_URL: str = f"redis://{os.getenv('REDIS_USER')}:{os.getenv('REDIS_PASSWORD')}@{os.getenv('HOST_NETWORK')}:6379/0"  # noqa: E501
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    # logging
    BACKUP_COUNT: int = 3
    MAX_BYTES_PER_FILE: int = 4 * 1024 * 1024

    # mail
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USE_SSL: bool = True
    MAIL_USERNAME: str | None = os.getenv("MAIL")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: tuple[str, str | None] = (
        "CryptoDeal", os.getenv("MAIL")
    )

    # cooldown and cooldownRec in js files must be same or longer
    MAIL_CODE_COOLDOWN: int = 20
    MAIL_CODE_VERIFY_ATTEMPTS: int = 3
    MAIL_CODE_REFRESH_ATTEMTPTS: int = 3

    # user
    START_USD_BALANCE = 10000
    START_RUB_BALANCE = 1000000

    # authentification and authorization
    REGISTER_LIFETIME: int = 1200
    # restore_cooldown must be more then restore_lifetime
    RESTORE_LIFETIME: int = 1200
    ACCESS_TOKEN_LIFETIME: int = 10000
    RESTORE_COOLDOWN: int = 20000
    REFRESH_TOKEN_LIFETIME: int = 12000
    JWT_ENCODING_ALGORITHM: str = "HS256"
    LOGIN_COOLDOWN: int = 2
    LOGIN_FAST_ATTEMPTS: int = 10

    # celery
    CELERY: _CeleryConf = {
        "broker_url": REDIS_URL,
        "task_ignore_result": True,
        "task_time_limit": 10,
        "imports": (
            "app.tasks.mail",
            "app.tasks.postgre",
            "app.tasks.redis",
        ),
        "task_default_queue": "normal",
        "task_queues": (
            Queue(name="normal"),
            Queue(name="low"),
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
            },
        },
        "worker_max_memory_per_child": 50000,
        "broker_transport_options": {
            "visibility_timeout": 43200
        },
        "timezone": "UTC",
        "beat_schedule": {
            "clear-postgre": {
                "task": "delete_expired_sessions",
                "schedule": crontab(minute="0", hour="*/12")
            },
            "clear-redis": {
                "task": "delete_expired_applications",
                "schedule": crontab(minute="0", hour="*/12")
            },
        },
        "worker_hijack_root_logger": False,
        "worker_redirect_stdouts": True,
        "broker_connection_retry_on_startup": True
    }


appConfig: AppConfig = AppConfig(os.path.dirname(__file__))
