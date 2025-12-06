"""Windows automation for Minecraft chat commands using pyautogui."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import re
import time
import threading
from typing import Callable, Optional, List

import pyautogui

try:
    import pygetwindow as gw
    HAVE_GETWINDOW = True
except ImportError:
    HAVE_GETWINDOW = False

from .constants import (
    MINECRAFT_WINDOW_TITLES,
)
from .logger import LoggerProtocol
from .settings import Settings


# Configure pyautogui for reliability
pyautogui.PAUSE = 0.05  # 50ms between actions (increased from 30ms)
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort


class WindowsAutomator:
    """Windows automation for sending commands to Minecraft via pyautogui."""

    def __init__(
        self,
        status_cb: Optional[Callable[[str], None]] = None,
        stop_event: Optional[threading.Event] = None,
        logger: Optional[LoggerProtocol] = None,
    ) -> None:
        self.status_cb = status_cb or (lambda _msg: None)
        self.stop_event = stop_event or threading.Event()
        self.logger = logger

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

    def focus_minecraft(self, attempts: int = 3, settle_ms: int = 200) -> bool:
        """Bring the running Minecraft window to front.

        Returns:
            True if Minecraft was successfully focused.
        """
        if not HAVE_GETWINDOW:
            self._log("pygetwindow not available, cannot focus window automatically")
            self._status("Please click on Minecraft window manually...")
            self._sleep(2000)
            return True  # Assume user clicked

        for i in range(max(1, attempts)):
            for title_pattern in MINECRAFT_WINDOW_TITLES:
                try:
                    windows = gw.getWindowsWithTitle(title_pattern)
                    if windows:
                        win = windows[0]
                        if win.isMinimized:
                            win.restore()
                        win.activate()
                        self._sleep(settle_ms)
                        self._log(f"Focused window: {win.title}")
                        return True
                except Exception as e:
                    self._log(f"Focus attempt {i+1} failed: {e}")
            self._sleep(100)

        self._status("Could not find Minecraft window. Is it running?")
        return False

    def key_escape(self) -> None:
        """Press the Escape key."""
        pyautogui.press('escape')

    def key_enter(self) -> None:
        """Press the Enter key."""
        pyautogui.press('enter')

    def _copy_to_clipboard_win32(self, text: str) -> bool:
        """Copy text to Windows clipboard using Win32 API with proper Unicode.

        This bypasses pyperclip and uses the native Windows API directly
        with explicit UTF-16-LE encoding for maximum compatibility.
        """
        try:
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            # Windows clipboard constants
            CF_UNICODETEXT = 13
            GMEM_MOVEABLE = 0x0002

            # Open clipboard (0 = current task)
            if not user32.OpenClipboard(0):
                self._log("Failed to open clipboard")
                return False

            try:
                # Empty the clipboard
                user32.EmptyClipboard()

                # Encode text as UTF-16-LE with null terminator (Windows Unicode format)
                data = text.encode('utf-16-le') + b'\x00\x00'

                # Allocate global memory
                h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
                if not h_mem:
                    self._log("Failed to allocate clipboard memory")
                    return False

                # Lock memory and copy data
                p_mem = kernel32.GlobalLock(h_mem)
                if not p_mem:
                    kernel32.GlobalFree(h_mem)
                    self._log("Failed to lock clipboard memory")
                    return False

                ctypes.memmove(p_mem, data, len(data))
                kernel32.GlobalUnlock(h_mem)

                # Set clipboard data
                if not user32.SetClipboardData(CF_UNICODETEXT, h_mem):
                    kernel32.GlobalFree(h_mem)
                    self._log("Failed to set clipboard data")
                    return False

                self._log(f"Copied to clipboard (Win32): {text[:50]}...")
                return True

            finally:
                user32.CloseClipboard()

        except Exception as e:
            self._log(f"Win32 clipboard failed: {e}")
            return False

    def _send_ctrl_v_sendinput(self) -> bool:
        """Send Ctrl+V using Windows SendInput API."""
        try:
            # Virtual key codes
            VK_CONTROL = 0x11
            VK_V = 0x56
            KEYEVENTF_KEYUP = 0x0002
            INPUT_KEYBOARD = 1

            # Define the KEYBDINPUT structure
            class KEYBDINPUT(ctypes.Structure):
                _fields_ = [
                    ("wVk", wintypes.WORD),
                    ("wScan", wintypes.WORD),
                    ("dwFlags", wintypes.DWORD),
                    ("time", wintypes.DWORD),
                    ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
                ]

            # Define the INPUT structure
            class INPUT(ctypes.Structure):
                _fields_ = [
                    ("type", wintypes.DWORD),
                    ("ki", KEYBDINPUT),
                    ("padding", ctypes.c_ubyte * 8)
                ]

            user32 = ctypes.windll.user32

            def send_key(vk: int, up: bool = False) -> None:
                inp = INPUT()
                inp.type = INPUT_KEYBOARD
                inp.ki.wVk = vk
                inp.ki.wScan = 0
                inp.ki.dwFlags = KEYEVENTF_KEYUP if up else 0
                inp.ki.time = 0
                inp.ki.dwExtraInfo = None
                user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

            # Send Ctrl+V with proper timing
            # Ctrl down
            send_key(VK_CONTROL)
            self._sleep(50)  # Increased delay

            # V down
            send_key(VK_V)
            self._sleep(50)  # Increased delay

            # V up
            send_key(VK_V, up=True)
            self._sleep(50)  # Increased delay

            # Ctrl up
            send_key(VK_CONTROL, up=True)

            return True

        except Exception as e:
            self._log(f"SendInput Ctrl+V failed: {e}")
            return False

    def paste_text(self, text: str) -> None:
        """Paste text to Minecraft using Win32 clipboard API.

        Uses native Windows clipboard API for proper Unicode handling
        on all keyboard layouts (including Belgian AZERTY).
        """
        self._log(f"Pasting text: {text}")

        # Step 1: Copy to clipboard using Win32 API
        if not self._copy_to_clipboard_win32(text):
            # Fallback to pyperclip if Win32 fails
            self._log("Falling back to pyperclip")
            try:
                import pyperclip
                pyperclip.copy(text)
            except Exception as e:
                self._log(f"pyperclip also failed: {e}")
                return

        # Step 2: Wait for clipboard to be ready
        self._sleep(200)  # Increased from 150ms

        # Step 3: Send Ctrl+V
        if self._send_ctrl_v_sendinput():
            self._log("Paste via SendInput successful")
        else:
            # Fallback to pyautogui
            self._log("Falling back to pyautogui for paste")
            pyautogui.hotkey('ctrl', 'v')

        # Step 4: Wait for paste to complete
        self._sleep(200)  # Increased from 100ms

    def open_chat(self, chat_key: str) -> None:
        """Open Minecraft chat with the specified key."""
        if chat_key == "/":
            pyautogui.press('/')
        else:
            pyautogui.press('t')

    def _normalize_carets(self, s: str) -> str:
        """Normalize coordinate syntax to avoid common parse errors.

        - Remove explicit plus signs after '~' or '^' (e.g., '~+5' -> '~5').
        - Replace any bare caret '^' with '^0'.
        - Replace any bare tilde '~' with '~0'.
        """
        # Remove explicit '+' after ~ or ^ FIRST (Minecraft doesn't accept '+')
        s = re.sub(r"([~\^])\+(?=\d)", r"\1", s)
        # Caret must be followed by a number: '^' -> '^0'
        s = re.sub(r"\^(?!-?\d)", "^0", s)
        # Tilde may be bare, but normalize to '~0'
        s = re.sub(r"~(?!-?\d)", "~0", s)
        return s

    def send_command(self, command: str, settings: Settings) -> bool:
        """Send a single command to Minecraft.

        Args:
            command: The command to send (with or without leading /)
            settings: Configuration settings

        Returns:
            True if command was sent successfully
        """
        # Strip leading / if using / as chat key (will be auto-added)
        if settings.chat_key == "/" and command.startswith("/"):
            command = command[1:]

        # Normalize coordinates
        command = self._normalize_carets(command)

        # Open chat and wait for it to be ready
        self.open_chat(settings.chat_key)
        self._sleep(300)  # INCREASED: Wait 300ms for chat to fully open

        # Paste the command
        self.paste_text(command)
        self._sleep(200)  # INCREASED: Wait 200ms after paste

        # Send the command
        self.key_enter()
        self._sleep(settings.delay_ms)

        return True

    def run_commands(self, commands: List[str], settings: Settings) -> None:
        """Run a list of commands in Minecraft.

        Args:
            commands: List of commands to send
            settings: Configuration for automation
        """
        self._status("Focusing Minecraft...")
        if not self.focus_minecraft():
            return

        self._sleep(300)  # INCREASED: Wait 300ms after focus

        # Press escape first to ensure game is resumed
        if settings.press_escape_first:
            self._status("Resuming game (Esc)...")
            self.key_escape()
            self._sleep(300)  # INCREASED: Wait 300ms after escape

        # Filter out comments and blank lines
        cleaned = [ln for ln in commands if (s := ln.strip()) and not s.startswith("#")]
        total = len(cleaned)

        for idx, command in enumerate(cleaned, start=1):
            if self.stop_event.is_set():
                self._status("Stopped by user.")
                return

            self._status(f"Sending command {idx}/{total}...")
            self._log(f"Command: {command}")
            self.send_command(command, settings)

        self._status("Done!")
