"""Global hotkey watcher for emergency stop functionality."""

from __future__ import annotations

import threading
import time
from typing import Any, Optional

from .constants import KEY_SPACE, KEY_ESCAPE
from .logger import LoggerProtocol

_HOTKEYS_IMPORT_ERROR: Optional[str] = None
try:
    from Quartz import (
        CGEventTapCreate,
        CGEventMaskBit,
        kCGHIDEventTap,
        kCGHeadInsertEventTap,
        kCGEventKeyDown,
        kCGEventKeyUp,
        CGEventGetIntegerValueField,
        kCGKeyboardEventKeycode,
        CFMachPortCreateRunLoopSource,
        CFRunLoopAddSource,
        CFRunLoopRun,
        CFRunLoopStop,
        CFRunLoopGetCurrent,
    )
    HAVE_HOTKEYS = True
except ImportError as e:
    HAVE_HOTKEYS = False
    _HOTKEYS_IMPORT_ERROR = f"ImportError: {e}"
    # Define stubs for type checking
    kCGEventKeyDown = None
    kCGKeyboardEventKeycode = None
except Exception as e:
    HAVE_HOTKEYS = False
    _HOTKEYS_IMPORT_ERROR = f"{type(e).__name__}: {e}"
    kCGEventKeyDown = None
    kCGKeyboardEventKeycode = None


class HotkeyWatcher:
    """Global hotkey watcher for Space+Escape combo (stop signal).

    Uses a Quartz event tap when available. If unavailable, acts as a no-op.
    The stop signal is triggered when Space and Escape are pressed within
    the specified window (default 500ms).
    """

    def __init__(
        self,
        stop_event: threading.Event,
        logger: Optional[LoggerProtocol] = None,
        window_ms: int = 500,
    ) -> None:
        """Initialize the hotkey watcher.

        Args:
            stop_event: Event to set when hotkey combo is detected
            logger: Optional logger for status messages
            window_ms: Time window in ms for detecting the key combo
        """
        self.stop_event = stop_event
        self.logger = logger
        self.window_ms = window_ms
        self._thread: Optional[threading.Thread] = None
        self._runloop: Any = None
        self._port: Any = None
        self._last_space: float = 0.0
        self._last_esc: float = 0.0

    def log(self, msg: str) -> None:
        """Log a message if logger is available."""
        try:
            if self.logger:
                self.logger.log(msg)
        except Exception as e:
            # Fallback: print to stderr if logging fails
            import sys
            print(f"Hotkeys log error: {e}", file=sys.stderr)

    def start(self) -> None:
        """Start the hotkey watcher thread."""
        if not HAVE_HOTKEYS:
            msg = "Hotkeys: Quartz not available; global stop disabled"
            if _HOTKEYS_IMPORT_ERROR:
                msg += f" ({_HOTKEYS_IMPORT_ERROR})"
            self.log(msg)
            return
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the hotkey watcher."""
        if not HAVE_HOTKEYS:
            return
        try:
            if self._runloop is not None:
                CFRunLoopStop(self._runloop)
        except Exception as e:
            self.log(f"Error stopping runloop: {e}")

    # === internals ===
    def _tap_callback(self, proxy: Any, etype: int, event: Any, refcon: Any) -> Any:
        """Callback for Quartz event tap."""
        try:
            if etype == kCGEventKeyDown:
                code = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
                now = time.monotonic()
                if code == KEY_SPACE:
                    self._last_space = now
                    if (now - self._last_esc) * 1000.0 <= self.window_ms:
                        self.log("Hotkeys: Space+Esc detected -> stop")
                        self.stop_event.set()
                elif code == KEY_ESCAPE:
                    self._last_esc = now
                    if (now - self._last_space) * 1000.0 <= self.window_ms:
                        self.log("Hotkeys: Space+Esc detected -> stop")
                        self.stop_event.set()
        except Exception as e:
            # Log but don't crash - this is a callback from the system
            self.log(f"Hotkeys callback error: {e}")
        return event

    def _run(self) -> None:
        """Main event tap loop (runs in background thread)."""
        try:
            mask = CGEventMaskBit(kCGEventKeyDown) | CGEventMaskBit(kCGEventKeyUp)
            self._port = CGEventTapCreate(
                kCGHIDEventTap,
                kCGHeadInsertEventTap,
                0,
                mask,
                self._tap_callback,
                None,
            )
            if not self._port:
                self.log("Hotkeys: failed to create event tap")
                return
            source = CFMachPortCreateRunLoopSource(None, self._port, 0)
            self._runloop = CFRunLoopGetCurrent()
            CFRunLoopAddSource(self._runloop, source, 0)
            self.log("Hotkeys: event tap active (Space+Esc to stop)")
            CFRunLoopRun()
        except Exception as e:
            self.log(f"Hotkeys error: {e}")
