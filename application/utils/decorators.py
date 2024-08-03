from typing import Callable, Any
from functools import wraps

from flask import request, Response
from werkzeug.exceptions import Unauthorized

from .JWT import validate_token
from ..mail.senders import send_scrf_attention


def authorization_required(view_func: Callable) -> Callable:
    @wraps(view_func)
    def handler(*args, **kwargs) -> Any:
        scrf_header: str | None = request.headers.get("X-SCRF-TOKEN")
        scrf_cookie: str | None = request.cookies.get("refresh_scrf_token")
        refresh_token: str | None = request.cookies.get("refresh_token")

        payload: dict[str, Any] | None = validate_token(
            token=refresh_token,
            type="refresh"
        )
        if None in [scrf_header, scrf_cookie, payload]:
            raise Unauthorized

        if scrf_cookie != scrf_header or scrf_cookie != payload["scrf"]:
            send_scrf_attention(
                recipient=payload["email"],
                origin=request.headers.get("Origin")
            )
            return {
                "error": {
                    "code": "Forbidden",
                    "message": "Invalid scrf token",
                    "details": """Invalid scrf token. Someone tries to get
                        access from your behalf"""
                }
            }, 403

        return view_func(*args, **kwargs)
    return handler
