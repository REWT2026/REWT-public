"""Secret redaction for public diagnostics."""

from __future__ import annotations

import re
from typing import Iterable


_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|secret|password|credential)\s*[=:]\s*\S+"),
    re.compile(r"(?i)Bearer\s+[A-Za-z0-9\-._~+/]+=*"),
)


def redact_secrets(text: str, *, extra_patterns: Iterable[str] | None = None) -> str:
    result = text
    for pattern in _PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    for item in extra_patterns or ():
        if item:
            result = result.replace(item, "[REDACTED]")
    return result
