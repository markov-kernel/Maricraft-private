"""Settings and configuration for Maricraft automation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .constants import DELAY_TURBO_MS


class ChatKey(Enum):
    """Chat opening key for Minecraft."""
    T = "t"
    SLASH = "/"


@dataclass
class Settings:
    """Configuration for command automation.
    
    Attributes:
        chat_key: Key to open chat ('t' or '/')
        delay_ms: Base delay between operations in milliseconds
        press_escape_first: Whether to press Escape before starting (resumes game)
        type_instead_of_paste: Use keystroke typing instead of clipboard paste
        paste_repeats: Number of times to repeat paste operation (for reliability)
        force_ascii_layout: Switch to ASCII-friendly keyboard layout before typing
        typing_segment_delay_ms: Delay between typed segments
        use_quartz_injection: Use Quartz text injection (faster but may not work on all setups)
        turbo_mode: Enable faster timing (reduces delays to ~40ms)
        ultra_mode: Enable aggressive timing (reduces delays to ~5ms)
    """
    chat_key: str = "t"
    delay_ms: int = DELAY_TURBO_MS
    press_escape_first: bool = True
    type_instead_of_paste: bool = True
    paste_repeats: int = 2
    force_ascii_layout: bool = True
    typing_segment_delay_ms: int = 0
    use_quartz_injection: bool = False
    turbo_mode: bool = True
    ultra_mode: bool = True

