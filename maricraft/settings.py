"""Simplified settings for Maricraft Windows app."""

from __future__ import annotations

from dataclasses import dataclass

from .constants import UI_DELAY_DEFAULT_MS


@dataclass
class Settings:
    """Configuration for command automation."""
    chat_key: str = "t"
    delay_ms: int = UI_DELAY_DEFAULT_MS
    press_escape_first: bool = True

    @classmethod
    def default(cls) -> "Settings":
        """Create default settings."""
        return cls()
