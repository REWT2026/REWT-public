"""Cross-platform advisory lock for public control-plane files."""

from __future__ import annotations

import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path


class FileLockError(OSError):
    pass


@contextmanager
def file_lock(path: Path, *, timeout: float = 10.0, poll_interval: float = 0.05):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 0o600)
    acquired = False
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                _lock(fd)
                acquired = True
                break
            except FileLockError:
                if time.monotonic() >= deadline:
                    raise FileLockError(f"Could not acquire lock on {path}") from None
                time.sleep(poll_interval)
        yield
    finally:
        if acquired:
            _unlock(fd)
        os.close(fd)


def _lock(fd: int) -> None:
    if sys.platform == "win32":
        import msvcrt
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise FileLockError(str(error)) from error
    else:
        import fcntl
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise FileLockError(str(error)) from error


def _unlock(fd: int) -> None:
    if sys.platform == "win32":
        import msvcrt
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN)
