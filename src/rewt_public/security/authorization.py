"""Draft single-operator authorisation for public control mutations."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path


class AuthorizationError(PermissionError):
    pass


@dataclass(frozen=True)
class ControlAuthorization:
    token: str

    def verify(self, expected: str) -> None:
        if not expected or not secrets.compare_digest(self.token, expected):
            raise AuthorizationError("Control operation not authorised")


def _token_file(data_dir: Path) -> Path:
    return data_dir / "control_plane" / ".control_token"


def ensure_control_token(data_dir: Path) -> str:
    path = _token_file(data_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    token = secrets.token_urlsafe(32)
    path.write_text(token, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return token


def authorize_control_operation(data_dir: Path) -> None:
    expected = ensure_control_token(data_dir)
    supplied = os.environ.get("REWT_PUBLIC_CONTROL_TOKEN", "").strip() or expected
    ControlAuthorization(supplied).verify(expected)
