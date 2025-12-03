"""macOS automation for Minecraft chat commands."""

from __future__ import annotations

import re
import subprocess
import threading
import time
from typing import Callable, Optional, Tuple

from .constants import (
    KEY_ENTER,
    KEY_ESCAPE,
    KEY_DELETE,
    KEY_SPACE,
    KEY_N,
    KEY_V,
    DELAY_ULTRA_MS,
    DELAY_TURBO_MS,
    DELAY_STANDARD_MS,
    QUARTZ_INJECT_CHUNK_SIZE,
    MINECRAFT_PROCESS_NAMES,
    KEYBOARD_LAYOUT_CANDIDATES,
    SENTINEL_PREFIX,
    VERIFY_TIMEOUT_MS,
)
from .logger import LoggerProtocol
from .settings import Settings

# Optional Quartz injection (fast, layout-agnostic typing)
_QUARTZ_IMPORT_ERROR: Optional[str] = None
try:
    from Quartz import (
        CGEventCreateKeyboardEvent,
        CGEventKeyboardSetUnicodeString,
        CGEventPost,
        kCGHIDEventTap,
    )
    _HAVE_QUARTZ = True
except ImportError as e:
    _HAVE_QUARTZ = False
    _QUARTZ_IMPORT_ERROR = f"ImportError: {e}"
except Exception as e:
    _HAVE_QUARTZ = False
    _QUARTZ_IMPORT_ERROR = f"{type(e).__name__}: {e}"


def quartz_available() -> bool:
    """Check if Quartz text injection is available."""
    return _HAVE_QUARTZ


# Backwards compatibility alias (deprecated - use quartz_available())
HAVE_QUARTZ = _HAVE_QUARTZ


class MacAutomator:
    """macOS automation for sending commands to Minecraft via AppleScript/Quartz."""

    def __init__(
        self,
        status_cb: Optional[Callable[[str], None]] = None,
        stop_event: Optional[threading.Event] = None,
        logger: Optional[LoggerProtocol] = None,
    ) -> None:
        self.status_cb = status_cb or (lambda _msg: None)
        self.stop_event = stop_event or threading.Event()
        self.logger = logger

    def _osascript(self, script: str) -> subprocess.CompletedProcess:
        """Execute an AppleScript and return the result."""
        proc = subprocess.run(
            ["osascript", "-"],
            input=script.encode("utf-8"),
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            self._log(
                f"osascript error rc={proc.returncode} "
                f"stdout={proc.stdout.decode('utf-8', 'ignore').strip()} "
                f"stderr={proc.stderr.decode('utf-8', 'ignore').strip()}"
            )
        return proc

    def _status(self, msg: str) -> None:
        """Update status and log."""
        self._log(msg)
        self.status_cb(msg)

    def _log(self, msg: str) -> None:
        """Log a message if logger is available."""
        if self.logger is not None:
            self.logger.log(msg)

    def _sleep(self, ms: int) -> None:
        """Sleep for specified milliseconds."""
        time.sleep(max(ms, 0) / 1000.0)

    # ===== Input source helpers (for reliable typing on non-US layouts) =====
    def _get_input_source_name(self) -> str:
        """Get the current keyboard input source name."""
        script = r'''
        try
            tell application "System Events"
                set n to name of current input source
            end tell
            return n
        on error
            return ""
        end try
        '''
        proc = self._osascript(script)
        return proc.stdout.decode("utf-8", "ignore").strip()

    def _set_input_source_by_name(self, name: str) -> bool:
        """Switch to a keyboard layout by name. Returns True if successful."""
        script = rf'''
        try
            tell application "System Events"
                set target to first input source whose name is "{name}"
                set current input source to target
                return name of current input source
            end tell
        on error
            return ""
        end try
        '''
        proc = self._osascript(script)
        return proc.stdout.decode("utf-8", "ignore").strip() == name

    def _maybe_force_ascii_input(self) -> Tuple[bool, str]:
        prev = self._get_input_source_name()
        for candidate in KEYBOARD_LAYOUT_CANDIDATES:
            if self._set_input_source_by_name(candidate):
                self._log(f"Switched input source to '{candidate}' from '{prev}'")
                return True, prev
        return False, prev

    def _generate_sentinel(self) -> str:
        """Generate a unique sentinel string for clipboard verification."""
        return f"{SENTINEL_PREFIX}{int(time.time() * 1000)}__"

    def _restore_input_source(self, prev: str) -> None:
        """Restore a previous input source."""
        if not prev:
            return
        ok = self._set_input_source_by_name(prev)
        self._log(f"Restored input source to '{prev}' => {'ok' if ok else 'failed'}")

    def _frontmost_process_name(self) -> str:
        """Get the name of the frontmost process."""
        script = r'''
        tell application "System Events"
            set pname to name of first process whose frontmost is true
        end tell
        return pname
        '''
        proc = self._osascript(script)
        return proc.stdout.decode("utf-8", "ignore").strip()

    def _frontmost_process_pid(self) -> int:
        """Get the PID of the frontmost process."""
        script = r'''
        try
            tell application "System Events"
                set pidnum to unix id of first process whose frontmost is true
            end tell
            return pidnum as text
        on error
            return "0"
        end try
        '''
        proc = self._osascript(script)
        try:
            return int(proc.stdout.decode("utf-8", "ignore").strip() or "0")
        except ValueError:
            return 0

    def focus_minecraft(self, attempts: int = 3, settle_ms: int = 100) -> bool:
        """Bring the running Minecraft Java client to front.
        
        Returns:
            True if Minecraft was successfully focused.
        """
        script = r'''
        tell application "System Events"
            try
                set frontmost of process "java" to true
                try
                    tell process "java" to tell window 1 to perform action "AXRaise"
                end try
            end try
            try
                set frontmost of process "javaw" to true
                try
                    tell process "javaw" to tell window 1 to perform action "AXRaise"
                end try
            end try
        end tell
        '''

        for i in range(max(1, attempts)):
            self._osascript(script)
            self._log(f"Focus attempt {i+1}/{attempts}: raised 'java/javaw'")
            time.sleep(max(settle_ms, 0) / 1000.0)
            front = (self._frontmost_process_name() or "").lower()
            self._log(f"Frontmost after attempt {i+1}: '{front}'")
            if any(proc_name in front for proc_name in MINECRAFT_PROCESS_NAMES):
                return True
        return False

    def key_escape(self) -> None:
        """Press the Escape key."""
        script = f'tell application "System Events" to key code {KEY_ESCAPE}'
        self._osascript(script)

    def keystroke(self, text: str) -> None:
        """Send literal characters via AppleScript keystroke."""
        if '"' in text:
            parts = text.split('"')
            lines = ['tell application "System Events"']
            for i, seg in enumerate(parts):
                if seg:
                    seg_esc = seg.replace("\\", "\\\\").replace("\n", " ")
                    lines.append(f'    keystroke "{seg_esc}"')
                if i < len(parts) - 1:
                    lines.append('    keystroke quote')
            lines.append('end tell')
            script = "\n".join(lines)
            self._osascript(script)
        else:
            seg_esc = text.replace("\\", "\\\\").replace("\n", " ")
            script = f'tell application "System Events" to keystroke "{seg_esc}"'
            self._osascript(script)

    def _type_tilde(self) -> None:
        """Type a tilde character using Option+n then Space (for non-US layouts)."""
        script = rf'''
        tell application "System Events"
            key down option
            key code {KEY_N}
            key up option
            key code {KEY_SPACE}
            key code {KEY_SPACE}
            key code {KEY_DELETE}
        end tell
        '''
        self._osascript(script)
        self._sleep(20)

    def type_line_safely(self, text: str, per_segment_delay_ms: int = 10) -> None:
        """Type text, handling '~' explicitly with Option+n then Space."""
        parts = text.split("~")
        for i, seg in enumerate(parts):
            if seg:
                self.keystroke(seg)
            if i < len(parts) - 1:
                self._type_tilde()
            if per_segment_delay_ms:
                self._sleep(per_segment_delay_ms)

    def keycode(self, code: int) -> None:
        """Press a key by its key code."""
        script = f'tell application "System Events" to key code {code}'
        self._osascript(script)

    def paste_from_clipboard(self) -> None:
        """Paste from clipboard using multiple variants for compatibility."""
        variants = [
            f'tell application "System Events" to key code {KEY_V} using {{command down}}',
            'tell application "System Events" to keystroke "v" using {command down}',
            rf'''
            tell application "System Events"
                key down command
                delay 0.02
                key code {KEY_V}
                delay 0.02
                key up command
            end tell
            ''',
        ]
        for script in variants:
            self._osascript(script)
            self._sleep(35)

    def poke_input(self) -> None:
        """Type a space then delete; helps some clients accept subsequent paste."""
        script = rf'''
        tell application "System Events"
            keystroke " "
            key code {KEY_DELETE}
        end tell
        '''
        self._osascript(script)

    def select_all(self) -> None:
        """Select all text (Cmd+A)."""
        script = 'tell application "System Events" to keystroke "a" using {command down}'
        self._osascript(script)

    def copy_selection(self) -> None:
        """Copy selection to clipboard (Cmd+C)."""
        script = 'tell application "System Events" to keystroke "c" using {command down}'
        self._osascript(script)

    def set_clipboard(self, text: str) -> None:
        try:
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=False)
        except OSError:
            pass

    def get_clipboard(self) -> str:
        try:
            out = subprocess.run(["pbpaste"], capture_output=True, check=False)
            return out.stdout.decode("utf-8", errors="ignore")
        except OSError:
            return ""

    def open_chat(self, chat_key: str) -> None:
        """Open Minecraft chat with the specified key."""
        if chat_key == "/":
            self.keystroke("/")
        else:
            self.keystroke("t")

    def press_enter(self) -> None:
        """Press the Enter/Return key."""
        self.keycode(KEY_ENTER)

    def send_quick_command(self, line: str, settings: Settings) -> None:
        """Send a single command quickly (assumes game is already focused)."""
        if settings.chat_key == "/" and line.startswith("/"):
            line = line[1:]
        line = self._normalize_carets(line)

        self._status("Post-run: teleporting back 75…")
        self.open_chat(settings.chat_key)
        self._sleep(DELAY_ULTRA_MS if settings.ultra_mode else max(60, settings.delay_ms // 2))

        if settings.force_ascii_layout:
            self.keystroke(line)
        else:
            self.type_line_safely(line, per_segment_delay_ms=max(0, int(settings.typing_segment_delay_ms)))

        self._sleep(DELAY_ULTRA_MS if settings.ultra_mode else max(60, settings.delay_ms // 2))
        self.press_enter()
        self._status("Post-run teleport sent.")

    def _setup_automation(self, settings: Settings) -> Tuple[bool, str]:
        """Set up automation environment (focus, layout, escape).
        
        Returns:
            Tuple of (switched_layout: bool, prev_layout: str)
        """
        self._status("Bringing Minecraft to front…")
        focused = self.focus_minecraft()
        if not focused:
            self._status(
                "Could not focus Minecraft. Ensure Accessibility is enabled "
                "and the game window is visible, then try again."
            )
            return False, ""

        if settings.turbo_mode:
            self._sleep(60)
        else:
            self._sleep(max(DELAY_STANDARD_MS, settings.delay_ms))

        if settings.type_instead_of_paste and not settings.use_quartz_injection and settings.force_ascii_layout:
            switched_layout, prev_layout = self._maybe_force_ascii_input()
        else:
            switched_layout, prev_layout = False, ""
        if switched_layout:
            self._sleep(DELAY_STANDARD_MS)

        if settings.press_escape_first:
            self._status("Resuming game (Esc)…")
            self.key_escape()
            if settings.ultra_mode:
                self._sleep(DELAY_ULTRA_MS)
            else:
                self._sleep(DELAY_STANDARD_MS)

        return switched_layout, prev_layout

    def _verify_input_field(
        self,
        expected: str,
        line_to_send: str,
        settings: Settings,
        max_timeout_ms: int = VERIFY_TIMEOUT_MS,
    ) -> bool:
        """Verify that the input field contains the expected text.

        Args:
            expected: Expected text in the input field
            line_to_send: Text to re-paste on failure
            settings: Current settings
            max_timeout_ms: Maximum time to spend verifying (default 5000ms)

        Returns:
            True if verification succeeded, False if timed out or failed
        """
        sentinel = self._generate_sentinel()
        start_time = time.monotonic()
        max_attempts = 3

        for attempt in range(max_attempts):
            # Check timeout
            elapsed_ms = (time.monotonic() - start_time) * 1000
            if elapsed_ms >= max_timeout_ms:
                self._log(f"Verify timeout after {elapsed_ms:.0f}ms")
                return False

            self.set_clipboard(sentinel)
            self._sleep(80)
            self.select_all()
            self._sleep(70)
            self.copy_selection()
            self._sleep(110)
            got = self.get_clipboard()

            if not got or got == sentinel:
                self._log(f"Verify attempt {attempt+1}: copy failed (clipboard unchanged)")
            else:
                got_s = got.strip().replace("\r", "")
                exp_s = expected.strip().replace("\r", "")
                self._log(f"Verify attempt {attempt+1}: got_len={len(got_s)} match={got_s==exp_s}")
                if got_s == exp_s:
                    return True

            # Check timeout before re-paste
            elapsed_ms = (time.monotonic() - start_time) * 1000
            if elapsed_ms >= max_timeout_ms:
                self._log(f"Verify timeout after {elapsed_ms:.0f}ms (before re-paste)")
                return False

            # Re-paste and try again with longer waits
            self.set_clipboard(line_to_send)
            self._sleep(120)
            self.paste_from_clipboard()
            self._sleep(200 + attempt * 100)

        return False

    def _send_single_command(self, idx: int, total: int, line: str, settings: Settings) -> None:
        """Send a single command to Minecraft."""
        if settings.chat_key == "/" and line.startswith("/"):
            line = line[1:]

        normalized = self._normalize_carets(line)
        if normalized != line:
            self._log(f"Normalized carets: '{line}' -> '{normalized}'")
        line = normalized

        use_typing = settings.type_instead_of_paste

        self._status(f"{idx}/{total}: Open chat…")
        self.open_chat(settings.chat_key)
        
        # Allow chat field to appear
        if use_typing:
            if settings.ultra_mode:
                self._sleep(DELAY_ULTRA_MS)
            else:
                self._sleep(30 if settings.turbo_mode else max(80, settings.delay_ms // 2))
        else:
            self._sleep(max(220, settings.delay_ms))
            self.poke_input()
            self._sleep(max(90, settings.delay_ms // 3))

        mode_desc = "typed" if use_typing else "pasted"
        self._status(f"{idx}/{total}: Input line ({mode_desc})…")
        self._log(f"Command line: {line}")
        line_start = time.monotonic()

        if use_typing:
            self._handle_typing_input(idx, total, line, settings)
        else:
            self._handle_paste_input(idx, total, line, settings)

        dur_ms = int((time.monotonic() - line_start) * 1000)
        turbo_txt = " turbo" if settings.turbo_mode and use_typing else ""
        self._status(f"{idx}/{total}: Send… (typed_ms={dur_ms}{turbo_txt})")
        self.press_enter()

        if settings.ultra_mode and use_typing:
            self._sleep(DELAY_ULTRA_MS)
        elif settings.turbo_mode and use_typing:
            self._sleep(DELAY_TURBO_MS)
        else:
            self._sleep(max(60, settings.delay_ms))

    def _handle_typing_input(self, idx: int, total: int, line_to_send: str, settings: Settings) -> None:
        """Handle input via typing (keystroke or Quartz injection)."""
        injected = False
        if settings.use_quartz_injection and _HAVE_QUARTZ:
            pid = self._frontmost_process_pid()
            injected = self.inject_text_quartz(line_to_send, target_pid=pid if pid > 0 else None)
            if injected:
                self._status(f"{idx}/{total}: Input line (injected)…")
                # Verify injection landed
                expected_field = ("/" + line_to_send) if settings.chat_key == "/" else line_to_send
                sentinel = self._generate_sentinel()
                self.set_clipboard(sentinel)
                self._sleep(60)
                self.select_all()
                self._sleep(40)
                self.copy_selection()
                self._sleep(80)
                got = (self.get_clipboard() or "").strip().replace("\r", "")
                exp = expected_field.strip().replace("\r", "")
                if not got or got == sentinel or got != exp:
                    self._log("Injection verify failed; falling back to keystroke typing")
                    injected = False
                else:
                    self._log("Injection verified OK")
            if not injected:
                self._log("Quartz injection failed; falling back to keystroke typing")

        if not injected:
            if settings.force_ascii_layout:
                self.keystroke(line_to_send)
            else:
                self.type_line_safely(
                    line_to_send, per_segment_delay_ms=max(0, int(settings.typing_segment_delay_ms))
                )

        if settings.ultra_mode:
            self._sleep(DELAY_ULTRA_MS)
        elif settings.turbo_mode:
            self._sleep(30)
        else:
            self._sleep(max(60, settings.delay_ms // 2))

    def _handle_paste_input(self, idx: int, total: int, line_to_send: str, settings: Settings) -> None:
        """Handle input via clipboard paste."""
        self.set_clipboard(line_to_send)
        self._sleep(max(160, settings.delay_ms // 2))
        
        # Paste once or more depending on reliability preference
        reps = max(1, int(settings.paste_repeats))
        for i in range(reps):
            self.paste_from_clipboard()
            if i < reps - 1:
                self._sleep(max(120, settings.delay_ms // 3))
        self._sleep(max(120, settings.delay_ms // 2))

        # Verify pasted content
        expected_field = ("/" + line_to_send) if settings.chat_key == "/" else line_to_send
        verified = self._verify_input_field(expected_field, line_to_send, settings)
        
        if not verified:
            self._log("Paste verify failed; falling back to safe typing for this line")
            self.poke_input()
            self._sleep(60)
            self.type_line_safely(line_to_send, per_segment_delay_ms=12)
            self._sleep(max(140, settings.delay_ms // 2))

    def run_commands(self, commands: list[str], settings: Settings) -> None:
        """Run a list of commands in Minecraft.
        
        Args:
            commands: List of commands to send (one per line)
            settings: Configuration for automation
        """
        original_clipboard = self.get_clipboard()

        try:
            switched_layout, prev_layout = self._setup_automation(settings)
            if not switched_layout and not prev_layout:
                return

            cleaned = [ln for ln in commands if (s := ln.strip()) and not s.startswith("#")]
            for idx, line in enumerate(cleaned, start=1):
                if self.stop_event.is_set():
                    self._status("Stopped by user.")
                    return
                self._send_single_command(idx, len(cleaned), line, settings)

            self._status("Done.")
        finally:
            self.set_clipboard(original_clipboard)
            if switched_layout:
                self._sleep(DELAY_STANDARD_MS)
                self._restore_input_source(prev_layout)

    def _normalize_carets(self, s: str) -> str:
        """Normalize coordinate syntax to avoid common parse errors.

        - Replace any bare caret '^' with '^0'.
        - Replace any bare tilde '~' with '~0'.
        - Remove explicit plus signs after '~' or '^' (e.g., '~+5' -> '~5').
        """
        # Caret must be followed by a number: '^' -> '^0'
        s = re.sub(r"\^(?!-?\d)", "^0", s)
        # Tilde may be bare, but normalize to '~0'
        s = re.sub(r"~(?!-?\d)", "~0", s)
        # Remove explicit '+' after ~ or ^ (Minecraft doesn't accept '+')
        s = re.sub(r"([~\^])\+(?=\d)", r"\1", s)
        return s

    def inject_text_quartz(self, text: str, target_pid: Optional[int] = None) -> bool:
        if not _HAVE_QUARTZ:
            return False

        try:
            from Quartz import CGEventPostToPid as _post_pid
        except ImportError:
            _post_pid = None

        try:
            for i in range(0, len(text), QUARTZ_INJECT_CHUNK_SIZE):
                seg = text[i : i + QUARTZ_INJECT_CHUNK_SIZE]
                ev_down = CGEventCreateKeyboardEvent(None, 0, True)
                CGEventKeyboardSetUnicodeString(ev_down, len(seg), seg)
                if target_pid and _post_pid:
                    _post_pid(target_pid, ev_down)
                else:
                    CGEventPost(kCGHIDEventTap, ev_down)
                ev_up = CGEventCreateKeyboardEvent(None, 0, False)
                CGEventKeyboardSetUnicodeString(ev_up, len(seg), seg)
                if target_pid and _post_pid:
                    _post_pid(target_pid, ev_up)
                else:
                    CGEventPost(kCGHIDEventTap, ev_up)
                self._sleep(1)
            return True
        except Exception as e:
            self._log(f"Quartz inject error: {e}")
            return False

