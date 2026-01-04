"""Debug logging utilities for datapack/behavior pack troubleshooting."""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Optional


# Module-level state for debug logging
_DEBUG_LOG_PATH: Optional[Path] = None


def set_debug_log_path(path: Path) -> None:
    """Set the path for debug logging.

    Args:
        path: Path to the debug log file.
    """
    global _DEBUG_LOG_PATH
    _DEBUG_LOG_PATH = path
    # Clear existing log
    if path.exists():
        path.unlink()
    debug_log("=== Bedrock Debug Log Started ===")


def debug_log(message: str) -> None:
    """Write a debug message to log file and console.

    Args:
        message: The message to log.
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(f"DEBUG: {message}")
    if _DEBUG_LOG_PATH:
        try:
            with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except Exception as e:
            print(f"DEBUG LOG ERROR: {e}")


def reset_debug_log() -> None:
    """Reset the debug log path (useful for testing)."""
    global _DEBUG_LOG_PATH
    _DEBUG_LOG_PATH = None
