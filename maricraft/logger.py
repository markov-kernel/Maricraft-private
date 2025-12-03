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
    """Simple timestamped file logger.
    
    The log file is overwritten on each run and includes run start/end markers.
    """

    def __init__(self, path: str = "log.txt") -> None:
        self.path = path
        self._fp: Optional[TextIO] = None
        # Overwrite on each run
        self._fp = open(self.path, "w", encoding="utf-8")
        self.log("=== Maricraft run started ===")

    def log(self, msg: str) -> None:
        """Log a message with timestamp."""
        try:
            if self._fp is not None:
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                self._fp.write(f"[{ts}] {msg}\n")
                self._fp.flush()
        except Exception:
            pass

    def close(self) -> None:
        """Close the log file."""
        try:
            self.log("=== Maricraft run finished ===")
            if self._fp is not None:
                self._fp.close()
                self._fp = None
        except Exception:
            pass


def create_log_helper(logger: Optional[LoggerProtocol]) -> callable:
    """Create a log helper function that safely logs to optional logger.
    
    Returns a function that can be called with a message string.
    """
    def _log(msg: str) -> None:
        try:
            if logger is not None:
                logger.log(msg)
        except Exception:
            pass
    return _log

