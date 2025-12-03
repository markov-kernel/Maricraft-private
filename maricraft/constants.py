"""Constants for Maricraft automation."""

from __future__ import annotations

from enum import Enum


# === Enums for Type Safety ===

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


class AIMode(Enum):
    """AI assistant mode."""
    CREATE = "create"
    DEBUG = "debug"

    @classmethod
    def from_str(cls, value: str) -> "AIMode":
        """Convert string to AIMode, defaulting to CREATE."""
        for member in cls:
            if member.value == value:
                return member
        return cls.CREATE


# macOS Key Codes (virtual key codes for AppleScript/Quartz)
KEY_ENTER = 36
KEY_ESCAPE = 53
KEY_DELETE = 51
KEY_SPACE = 49
KEY_N = 45
KEY_V = 9

# Timing Constants (milliseconds)
DELAY_ULTRA_MS = 5
DELAY_TURBO_MS = 40
DELAY_STANDARD_MS = 120
DELAY_SETTLE_MS = 100
DELAY_PASTE_WAIT_MS = 160
DELAY_VERIFY_MS = 80
VERIFY_TIMEOUT_MS = 5000  # Maximum time for input verification

# Window Dimensions
WINDOW_DEFAULT_WIDTH = 900
WINDOW_DEFAULT_HEIGHT = 680
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 520

# Process Names for Minecraft Detection
MINECRAFT_PROCESS_NAMES = ("java", "javaw")

# Text Injection Chunk Size
QUARTZ_INJECT_CHUNK_SIZE = 256

# Log File
DEFAULT_LOG_PATH = "log.txt"

# Keyboard Layout Candidates (for ASCII input forcing)
KEYBOARD_LAYOUT_CANDIDATES = ("ABC", "U.S.", "ABC - QWERTZ", "ABC QWERTZ")

# Sentinel Pattern Prefix (for clipboard verification)
SENTINEL_PREFIX = "__MARICRAFT_SENTINEL__"

# Teleport Command
TELEPORT_BACK_COMMAND = "/tp @s ^ ^ ^-75"
TELEPORT_BACK_DISTANCE = 75

# AI Model Options
AI_MODEL_OPTIONS = (
    "openrouter/openai/gpt-4o-mini",
    "openrouter/openai/gpt-4o",
    "openrouter/meta-llama/llama-3.1-70b-instruct",
    "openrouter/mistralai/mistral-large",
)
AI_DEFAULT_MODEL = "openrouter/openai/gpt-4o-mini"

# UI Delay Limits
UI_DELAY_MIN_MS = 30
UI_DELAY_MAX_MS = 1000
UI_DELAY_INCREMENT = 5

