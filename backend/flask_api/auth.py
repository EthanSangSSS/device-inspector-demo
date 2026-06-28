"""JWT helper for the demo API."""

from __future__ import annotations

import datetime as dt
import os
from functools import wraps
from typing import Any, Callable, TypeVar, cast

import jwt
from flask import g, jsonify, request

F = TypeVar("F", bound=Callable[..., Any])


def _jwt_secret() -> str:
    """Return a local demo secret.

    The fallback is intentionally a non-production placeholder. Production would require
    a managed secret store and key rotation policy.
    """

    return os.getenv("DEVICE_INSPECTOR_JWT_SECRET", "local-demo-only-jwt-placeholder")


def issue_token(subject: str, role: str = "engineer") -> str:
    now = dt.datetime.now(tz=dt.timezone.utc)
    payload = {
        "sub": subject,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + dt.timedelta(hours=1)).timestamp()),
        "scope": "diagnostic-demo",
    }
    return jwt.encode(payload, _jwt_secret(), algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
    return cast(dict[str, Any], jwt.decode(token, _jwt_secret(), algorithms=["HS256"]))


def require_auth(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "missing bearer token"}), 401
        token = header.removeprefix("Bearer ").strip()
        try:
            g.claims = decode_token(token)
        except jwt.PyJWTError:
            return jsonify({"error": "invalid bearer token"}), 401
        return func(*args, **kwargs)

    return cast(F, wrapper)
