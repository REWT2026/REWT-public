"""Public security control-plane port."""

from __future__ import annotations

from enum import Enum
from typing import Protocol


class KillSwitch(str, Enum):
    GLOBAL_STOP = "GLOBAL_STOP"
    INTERNET_STOP = "INTERNET_STOP"
    EXTERNAL_ACTION_STOP = "EXTERNAL_ACTION_STOP"
    TASK_STOP = "TASK_STOP"
    DEPLOYMENT_STOP = "DEPLOYMENT_STOP"


class SecurityViolation(Exception):
    def __init__(self, control: KillSwitch, message: str) -> None:
        self.control = control
        super().__init__(message)


class SecurityPort(Protocol):
    def is_engaged(self, control: KillSwitch) -> bool: ...
    def assert_allowed(self, *controls: KillSwitch) -> None: ...
    def assert_internet_allowed(self) -> None: ...
