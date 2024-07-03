from datetime import datetime, UTC

from jwt import encode

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
            "scrf": refresh_scrf_token
        },
        key=AppConfig.SECRET_KEY,
        algorithm="HS256"
    )

    return access, refresh
