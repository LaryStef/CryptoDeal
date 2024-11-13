from functools import wraps
from typing import Any, Callable, Literal

from flask import request
from werkzeug.exceptions import Unauthorized

from app.tasks.mail import send_scrf_attention
from app.utils.JWT import validate_token


def authorization_required(
    token_type: Literal["access", "refresh"],
    scrf_header_requied: bool = True
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def wrap(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def handler(*args: Any, **kwargs: Any) -> Any:
            scrf_header: str | None = request.headers.get("X-SCRF-TOKEN")
            scrf_cookie: str | None = request.cookies.get(
                f"{token_type}_scrf_token"
            )
            token: str | None = request.cookies.get(f"{token_type}_token")

            payload: dict[str, Any] | None = validate_token(
                token=token,
                type=token_type
            )
            if not scrf_header_requied:
                scrf_header = scrf_cookie

            if None in [scrf_header, scrf_cookie, payload]:
                if token_type == "refresh":
                    return {
                        "error": {
                            "code": "Unauthorized",
                            "message": "Authorization failed",
                            "details": """Your token or scrf header are
                                invalid or missing. Try one more time or
                                logout and sign in again"""
                        }
                    }, 401
                raise Unauthorized

            if scrf_cookie != scrf_header or scrf_cookie != payload["scrf"]:

                send_scrf_attention.apply_async(
                    args=(payload["email"], request.headers.get("Origin"))
                )

                return {
                    "error": {
                        "code": "Forbidden",
                        "message": "Invalid scrf token",
                        "details": """Invalid scrf token. Someone tries to get
                            access from your behalf"""
                    }
                }, 403

            return func(*args, **kwargs)
        return handler
    return wrap
