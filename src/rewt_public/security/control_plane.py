"""Independent file-backed, fail-closed public control plane."""

from __future__ import annotations

import json
from pathlib import Path

from rewt_public.security.authorization import authorize_control_operation
from rewt_public.security.file_lock import file_lock
from rewt_public.security.port import KillSwitch, SecurityViolation


class ControlPlaneStore:
    def __init__(self, state_file: Path, *, data_dir: Path | None = None, require_authorization: bool = True) -> None:
        self._state_file = state_file
        self._data_dir = data_dir or state_file.parent.parent
        self._require_authorization = require_authorization
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        if not self._state_file.exists():
            self._write_unsafe({item.value: False for item in KillSwitch})

    def _lock_path(self) -> Path:
        return self._state_file.with_suffix(".lock")

    def _read_unsafe(self) -> dict[str, bool]:
        if not self._state_file.is_file():
            raise SecurityViolation(KillSwitch.GLOBAL_STOP, "Control state unavailable")
        try:
            data = json.loads(self._state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as error:
            raise SecurityViolation(KillSwitch.GLOBAL_STOP, "Control state unreadable") from error
        return {str(key): bool(value) for key, value in data.items()}

    def _write_unsafe(self, state: dict[str, bool]) -> None:
        self._state_file.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")

    def engage(self, control: KillSwitch) -> None:
        if self._require_authorization:
            authorize_control_operation(self._data_dir)
        with file_lock(self._lock_path()):
            state = self._read_unsafe()
            state[control.value] = True
            self._write_unsafe(state)

    def release(self, control: KillSwitch) -> None:
        if self._require_authorization:
            authorize_control_operation(self._data_dir)
        with file_lock(self._lock_path()):
            state = self._read_unsafe()
            state[control.value] = False
            self._write_unsafe(state)


class FileBackedSecurityPort:
    def __init__(self, state_file: Path) -> None:
        self._state_file = state_file
        self._lock_path = state_file.with_suffix(".lock")

    def _read_state(self) -> dict[str, bool]:
        if not self._state_file.is_file():
            raise SecurityViolation(KillSwitch.GLOBAL_STOP, "Control state unavailable")
        try:
            data = json.loads(self._state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as error:
            raise SecurityViolation(KillSwitch.GLOBAL_STOP, "Control state unreadable") from error
        return {str(key): bool(value) for key, value in data.items()}

    def is_engaged(self, control: KillSwitch) -> bool:
        with file_lock(self._lock_path):
            return self._read_state().get(control.value, True)

    def assert_allowed(self, *controls: KillSwitch) -> None:
        for control in controls:
            if self.is_engaged(control):
                raise SecurityViolation(control, f"{control.value} is engaged")

    def assert_internet_allowed(self) -> None:
        self.assert_allowed(KillSwitch.GLOBAL_STOP, KillSwitch.INTERNET_STOP)
