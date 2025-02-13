from time import time
from typing import Any, Literal

from flask import current_app
from jwt import InvalidTokenError, decode, encode

from app.config import appConfig


def generate_tokens(
    payload: dict[str, str | int],
    access_scrf_token: str,
    refresh_scrf_token: str,
    refresh_id: str
) -> tuple[str, str]:

    timestamp = int(time()) + appConfig.TIMESTAMP_OFFSET

    payload.update({
        "exp": timestamp + appConfig.ACCESS_TOKEN_LIFETIME,
        "iat": timestamp,
        "scrf": access_scrf_token
    })

    access: str = encode(
        payload=payload,
        key=appConfig.SECRET_KEY,
        algorithm=appConfig.JWT_ENCODING_ALGORITHM
    )
    refresh: str = encode(
        payload={
            "exp": timestamp + appConfig.REFRESH_TOKEN_LIFETIME,
            "iat": timestamp,
            "jti": refresh_id,
            "scrf": refresh_scrf_token,
            "uuid": payload.get("uuid")
        },
        key=appConfig.SECRET_KEY,
        algorithm=appConfig.JWT_ENCODING_ALGORITHM
    )

    return access, refresh


def validate_token(
    token: str | None,
    type: Literal["access", "refresh"]
) -> Any:
    if token is None:
        return None

    if type == "access":
        token_requirements = [
            "exp",
            "iat",
            "scrf",
            "email",
            "role",
            "uuid",
            "name"
        ]
    elif type == "refresh":
        token_requirements = [
            "exp",
            "iat",
            "jti",
            "scrf",
            "uuid"
        ]

    try:
        return decode(
            token,
            key=appConfig.SECRET_KEY,
            algorithms=[appConfig.JWT_ENCODING_ALGORITHM],
            leeway=appConfig.TIMESTAMP_OFFSET,
            options={
                "verify_exp": True,
                "verify_signature": True,
                "require": token_requirements
            })

    except InvalidTokenError as ex:
        current_app.logger.error(msg=f"decoding exception: {ex}")
        return None
