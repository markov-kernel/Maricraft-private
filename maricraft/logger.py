"""Logging utilities for Maricraft."""

from __future__ import annotations

import time
from typing import TextIO, Protocol


class LoggerProtocol(Protocol):
    """Protocol for logger interface used by components."""

    def log(self, msg: str) -> None:
        """Log a message with timestamp."""
        ...


class Logger:
    def __init__(self, path: str = "log.txt") -> None:
        self.path = path
        self._fp: TextIO = open(self.path, "w", encoding="utf-8")
        self.log("=== Maricraft run started ===")

    def log(self, msg: str) -> None:
        try:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            self._fp.write(f"[{ts}] {msg}\n")
            self._fp.flush()
        except OSError:
            pass

    def close(self) -> None:
        try:
            self.log("=== Maricraft run finished ===")
            self._fp.close()
        except OSError:
            pass

