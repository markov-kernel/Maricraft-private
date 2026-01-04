"""Logging utilities for Maricraft."""

from __future__ import annotations

import time
from typing import TextIO, Optional, Protocol


class LoggerProtocol(Protocol):
    """Protocol for logger interface used by components."""

    def log(self, msg: str) -> None:
        """Log a message with timestamp."""
        ...


class Logger:
    """File logger with lazy initialization.

    The log file is not opened until the first log() call,
    allowing Logger instances to be created without side effects.
    """

    def __init__(self, path: str = "log.txt") -> None:
        self.path = path
        self._fp: Optional[TextIO] = None

    def _ensure_open(self) -> bool:
        """Lazily open the log file on first write. Returns True if file is open."""
        if self._fp is None:
            try:
                self._fp = open(self.path, "w", encoding="utf-8")
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                self._fp.write(f"[{ts}] === Maricraft run started ===\n")
                self._fp.flush()
            except OSError:
                return False
        return True

    def log(self, msg: str) -> None:
        if not self._ensure_open():
            return
        try:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            self._fp.write(f"[{ts}] {msg}\n")  # type: ignore[union-attr]
            self._fp.flush()
        except OSError:
            pass

    def close(self) -> None:
        if self._fp is None:
            return
        try:
            self.log("=== Maricraft run finished ===")
            self._fp.close()
        except OSError:
            pass
        finally:
            self._fp = None

