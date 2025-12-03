"""Settings and configuration for Maricraft automation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from .constants import DELAY_TURBO_MS, ChatKey

if TYPE_CHECKING:
    from typing import Optional


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

    @classmethod
    def for_run(
        cls,
        chat_key: str = "t",
        delay_ms: int = DELAY_TURBO_MS,
        press_escape_first: bool = True,
        use_quartz_injection: bool = False,
    ) -> "Settings":
        """Create settings optimized for a standard command run.

        Args:
            chat_key: Chat open key ('t' or '/')
            delay_ms: Base delay in milliseconds
            press_escape_first: Press Escape before starting
            use_quartz_injection: Use Quartz for faster input

        Returns:
            Settings configured for turbo mode command execution
        """
        effective_delay = min(delay_ms, DELAY_TURBO_MS)
        return cls(
            chat_key=chat_key,
            delay_ms=effective_delay,
            press_escape_first=press_escape_first,
            type_instead_of_paste=True,
            paste_repeats=1,
            force_ascii_layout=True,
            typing_segment_delay_ms=0,
            turbo_mode=True,
            ultra_mode=False,
            use_quartz_injection=use_quartz_injection,
        )

    @classmethod
    def for_quick_command(
        cls,
        chat_key: str = "t",
        delay_ms: int = DELAY_TURBO_MS,
        press_escape_first: bool = True,
    ) -> "Settings":
        """Create settings optimized for quick single commands (like teleport).

        Args:
            chat_key: Chat open key ('t' or '/')
            delay_ms: Base delay in milliseconds
            press_escape_first: Press Escape before starting

        Returns:
            Settings configured for ultra-fast single command execution
        """
        return cls(
            chat_key=chat_key,
            delay_ms=delay_ms,
            press_escape_first=press_escape_first,
            type_instead_of_paste=True,
            paste_repeats=1,
            force_ascii_layout=True,
            typing_segment_delay_ms=0,
            turbo_mode=True,
            ultra_mode=True,
            use_quartz_injection=False,
        )

    def with_overrides(self, **kwargs: "Optional[object]") -> "Settings":
        """Create a copy with specified fields overridden.

        Args:
            **kwargs: Fields to override

        Returns:
            New Settings instance with overrides applied
        """
        return replace(self, **{k: v for k, v in kwargs.items() if v is not None})

