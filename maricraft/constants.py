"""Constants for Maricraft automation."""

from __future__ import annotations

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

