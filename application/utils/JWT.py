from datetime import datetime, UTC
from typing import Any

from jwt import encode, decode, DecodeError

from ..config import AppConfig


def generate_tokens(
        payload: dict[str, str | int],
        access_scrf_token: str,
        refresh_scrf_token: str,
        refresh_id: str
    ) -> tuple[str, str]:

    timestamp = int(datetime.now(UTC).timestamp())

    payload.update({
        "exp": timestamp + AppConfig.ACCESS_TOKEN_LIFETIME,
        "iat": timestamp,
        "scrf": access_scrf_token
    })

    access: bytes = encode(
        payload=payload,
        key=AppConfig.SECRET_KEY,
        algorithm="HS256"
    )
    refresh: bytes = encode(
        payload={
            "exp": timestamp + AppConfig.REFRESH_TOKEN_LIFETIME,
            "iat": timestamp,
            "jti": refresh_id,
            "scrf": refresh_scrf_token,
            "email": payload.get("email"),
            "uuid": payload.get("uuid")
        },
        key=AppConfig.SECRET_KEY,
        algorithm="HS256"
    )

    return access, refresh


def validate_refresh(token: str | None) -> dict[str, Any] | None:
    if token is None:
        return token

    try:
        return decode(
            token,
            key="F1QX6i1XJC5B7GBLYRkroDDLykcb3nTQ",
            algorithms=["HS256"],
            options={
                "verify_exp": True,
                "verify_signature": True,
                "require": [
                    "exp",
                    "iat",
                    "jti",
                    "scrf",
                    "email",
                    "uuid"
                ]
            })
    except DecodeError:
        return None
