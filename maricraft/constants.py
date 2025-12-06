"""Constants for Maricraft Windows automation."""

from __future__ import annotations

from enum import Enum


class ChatKey(Enum):
    """Chat key options for opening Minecraft chat."""
    T = "t"
    SLASH = "/"

    @classmethod
    def from_str(cls, value: str) -> "ChatKey":
        """Convert string to ChatKey, defaulting to T."""
        for member in cls:
            if member.value == value:
                return member
        return cls.T


# Timing Constants (milliseconds)
DELAY_FAST_MS = 50
DELAY_STANDARD_MS = 100
DELAY_BETWEEN_COMMANDS_MS = 150

# Window Dimensions
WINDOW_DEFAULT_WIDTH = 850
WINDOW_DEFAULT_HEIGHT = 700
WINDOW_MIN_WIDTH = 700
WINDOW_MIN_HEIGHT = 500

# Minecraft Window Title Patterns (for pygetwindow)
MINECRAFT_WINDOW_TITLES = ["Minecraft"]

# Log File
DEFAULT_LOG_PATH = "maricraft_log.txt"

# UI Settings
UI_DELAY_MIN_MS = 50
UI_DELAY_MAX_MS = 500
UI_DELAY_DEFAULT_MS = 100

# Button Grid Layout
BUTTONS_PER_ROW = 4
BUTTON_WIDTH = 14
BUTTON_HEIGHT = 2
