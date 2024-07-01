from datetime import datetime, UTC

from jwt import encode

from ..config import AppConfig


def generate_tokens(
        payload: dict[str, str | int],
        access_scrf_token: str,
        refersh_scrf_token: str,
        refresh_id: str
    ) -> (str, str):

    timestamp = int(datetime.now(UTC).timestamp())

    payload.update({
        "scrf": access_scrf_token,
        "exp": AppConfig.ACCESS_TOKEN_LIFETIME,
        "iat": timestamp
    })

    access: bytes = encode(
        payload=payload,
        key=AppConfig.SECRET_KEY,
        algorithm="HS256"
    )
    refresh: bytes = encode(
        payload={
            "scrf": refersh_scrf_token,
            "exp": AppConfig.REFRESH_TOKEN_LIFETIME,
            "iat": timestamp,
            "jti": refresh_id
        },
        key=AppConfig.SECRET_KEY,
        algorithm="HS256"
    )

    return access, refresh
