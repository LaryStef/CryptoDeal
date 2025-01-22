from random import randint
from time import time

from flask import current_app

from app.config import appConfig
from app.database.redisdb import rediska
from app.tasks.mail import send_register_code, send_restore_code
from app.security.cryptography import hash_password
from app.security.generators import generate_id


class RediskaHandler:
    @staticmethod
    def create_register_request(data: dict[str, str | int]) -> str:
        request_id: str = generate_id(16)
        timestamp: int = int(time()) + appConfig.TIMESTAMP_OFFSET

        data["refresh_attempts"] = 0
        data["verify_attempts"] = 0
        data["creation_time"] = timestamp
        data["deactivation_time"] = timestamp + appConfig.REGISTER_LIFETIME
        data["accept_new_request"] = timestamp + appConfig.MAIL_CODE_COOLDOWN
        data["password_hash"] = hash_password(data["password"])
        data["code"] = "".join([str(randint(0, 9)) for _ in range(6)])
        data["role"] = "user"
        data.pop("password")

        send_register_code.apply_async(
            args=(data["code"], data["email"])
        )

        rediska.json().set("register", request_id, data, nx=True)
        current_app.logger.info(
            "register request created for %s",
            {data['username']}
        )
        return request_id

    @staticmethod
    def refresh_register_code(
        data: dict[str, str | int],
        request_id: str
    ) -> None:
        data["refresh_attempts"] += 1
        data["accept_new_request"] = int(
            time()
        ) + appConfig.TIMESTAMP_OFFSET + appConfig.MAIL_CODE_COOLDOWN

        data["code"] = "".join([str(randint(0, 9)) for _ in range(6)])

        send_register_code.apply_async(
            args=(data["code"], data["email"])
        )

        rediska.json().delete("register", request_id)
        rediska.json().set("register", request_id, data, nx=True)
        current_app.logger.info("created new code for %s", data["username"])

    @staticmethod
    def increase_verify_attempts(
        file: str,
        data: dict[str, str | int],
        request_id: str
    ) -> None:
        data["verify_attempts"] = data["verify_attempts"] + 1

        rediska.json().delete(file, request_id)
        rediska.json().set(file, request_id, data, nx=True)

    @staticmethod
    def create_restore_request(email: str, uuid: str) -> str:
        request_id: str = generate_id(16)
        timestamp: int = int(time()) + appConfig.TIMESTAMP_OFFSET

        data: dict[str, str | int] = dict()
        data["uuid"] = uuid
        data["email"] = email
        data["refresh_attempts"] = 0
        data["verify_attempts"] = 0
        data["creation_time"] = timestamp
        data["deactivation_time"] = timestamp + appConfig.RESTORE_LIFETIME
        data["accept_new_request"] = timestamp + appConfig.MAIL_CODE_COOLDOWN
        data["code"] = "".join([str(randint(0, 9)) for _ in range(6)])

        send_restore_code.apply_async(
            args=(data["code"], email)
        )

        rediska.json().set("password_restore", request_id, data, nx=True)
        current_app.logger.info(
            "created restore request for user with id: %s",
            uuid
        )
        return request_id

    @staticmethod
    def refresh_restore_code(
        data: dict[str, str | int],
        request_id: str
    ) -> None:
        timestamp: int = int(time()) + appConfig.TIMESTAMP_OFFSET

        data["refresh_attempts"] += 1
        data["accept_new_request"] = timestamp + appConfig.MAIL_CODE_COOLDOWN
        data["code"] = "".join([str(randint(0, 9)) for _ in range(6)])
        data["deactivation_time"] = timestamp + appConfig.RESTORE_LIFETIME

        send_restore_code(data["code"], data["email"])
        rediska.json().delete("password_restore", request_id)
        rediska.json().set("password_restore", request_id, data, nx=True)
        current_app.logger.info(
            "created new code for user with id: %s",
            data["uuid"]
        )
