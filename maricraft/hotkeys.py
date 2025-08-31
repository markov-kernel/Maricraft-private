from __future__ import annotations

import threading
import time
from typing import Optional

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
    )
    from Quartz import CFMachPortCreateRunLoopSource
    from Quartz import CFRunLoopAddSource, CFRunLoopRun, CFRunLoopStop, CFRunLoopGetCurrent
    HAVE_HOTKEYS = True
except Exception:
    HAVE_HOTKEYS = False


class HotkeyWatcher:
    """Global hotkey watcher for Space+Escape combo (stop signal).

    Uses a Quartz event tap when available. If unavailable, acts as a no-op.
    """

    def __init__(self, stop_event: threading.Event, logger=None, window_ms: int = 500):
        self.stop_event = stop_event
        self.logger = logger
        self.window_ms = window_ms
        self._thread: Optional[threading.Thread] = None
        self._runloop = None
        self._port = None
        self._last_space = 0.0
        self._last_esc = 0.0

    def log(self, msg: str):
        try:
            if self.logger:
                self.logger.log(msg)
        except Exception:
            pass

    def start(self):
        if not HAVE_HOTKEYS:
            self.log("Hotkeys: Quartz not available; global stop disabled")
            return
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        if not HAVE_HOTKEYS:
            return
        try:
            if self._runloop is not None:
                CFRunLoopStop(self._runloop)
        except Exception:
            pass

    # === internals ===
    def _tap_callback(self, proxy, etype, event, refcon):
        try:
            if etype == kCGEventKeyDown:
                code = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
                now = time.monotonic()
                if code == 49:  # Space
                    self._last_space = now
                    if (now - self._last_esc) * 1000.0 <= self.window_ms:
                        self.log("Hotkeys: Space+Esc detected -> stop")
                        self.stop_event.set()
                elif code == 53:  # Escape
                    self._last_esc = now
                    if (now - self._last_space) * 1000.0 <= self.window_ms:
                        self.log("Hotkeys: Space+Esc detected -> stop")
                        self.stop_event.set()
        except Exception:
            pass
        return event

    def _run(self):
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

