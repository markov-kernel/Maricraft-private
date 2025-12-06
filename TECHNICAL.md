# Maricraft Technical Documentation

This document provides detailed technical information for developers working on Maricraft.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Structure](#module-structure)
3. [Windows Automation](#windows-automation)
4. [Clipboard Handling](#clipboard-handling)
5. [Keyboard Input](#keyboard-input)
6. [Minecraft Command Processing](#minecraft-command-processing)
7. [GUI Implementation](#gui-implementation)
8. [Configuration & Settings](#configuration--settings)
9. [Logging System](#logging-system)
10. [Build & Packaging](#build--packaging)
11. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

Maricraft is a Windows-only Python application that automates sending commands to Minecraft (Java and Bedrock editions). It uses a button-based CustomTkinter GUI where users click pre-programmed buttons to execute Minecraft commands.

### Data Flow

```
User clicks button
       │
       ▼
┌─────────────────┐
│  ui/app.py      │  Button click handler
│   App class     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  automator.py   │  Windows automation
│ WindowsAutomator│
└────────┬────────┘
         │
         ├──► Focus Minecraft window (pygetwindow)
         │
         ├──► Open chat (SendInput: T or / key)
         │
         ├──► Copy command to clipboard (Win32 API)
         │
         ├──► Paste command (SendInput: Ctrl+V)
         │
         └──► Send command (SendInput: Enter key)
```

### Technology Stack

| Component | Technology |
|-----------|------------|
| GUI | CustomTkinter (modern Tkinter wrapper) |
| Window Management | pygetwindow |
| Keyboard Automation | Win32 SendInput API (via ctypes) |
| Clipboard | Win32 Clipboard API (via ctypes) |
| Fallback Keyboard | pyautogui |
| Fallback Clipboard | pyperclip |
| Process Detection | Windows `tasklist` command (via subprocess) |

---

## Module Structure

```
maricraft/
├── __init__.py        # Package marker (empty)
├── __main__.py        # Entry point with error handling
├── ui/                # CustomTkinter GUI package
│   ├── __init__.py
│   ├── app.py         # Main App class, Bedrock detection
│   ├── state.py       # JSON state persistence
│   ├── theme.py       # Color/font definitions
│   └── components/    # UI widgets
├── commands.py        # Pre-defined command buttons and categories
├── automator.py       # Windows automation (WindowsAutomator)
├── constants.py       # Timing constants, window titles
├── settings.py        # Settings dataclass
├── datapack.py        # Datapack/behavior pack installation
├── version.py         # Version constant + GitHub update check
└── logger.py          # File logging
```

### Module Dependencies

```
__main__.py
    └── ui/app.py
            ├── commands.py
            ├── automator.py
            │       ├── constants.py
            │       ├── settings.py
            │       └── logger.py
            ├── datapack.py
            ├── version.py
            └── settings.py
```

---

## Windows Automation

### Window Focus (pygetwindow)

The `focus_minecraft()` method uses `pygetwindow` to find and activate the Minecraft window:

```python
import pygetwindow as gw

windows = gw.getWindowsWithTitle("Minecraft")
if windows:
    win = windows[0]
    if win.isMinimized:
        win.restore()
    win.activate()
```

**Window Title Patterns** (defined in `constants.py`):
```python
MINECRAFT_WINDOW_TITLES = ["Minecraft"]
```

The search is case-insensitive substring matching. "Minecraft 1.21.1" will match.

### Fallback Behavior

If `pygetwindow` is not available or fails:
1. Log the failure
2. Display "Please click on Minecraft window manually..."
3. Wait 2 seconds for user to click
4. Proceed assuming Minecraft is focused

---

## Clipboard Handling

### Primary Method: Win32 API (ctypes)

We use the native Windows clipboard API for maximum compatibility with all keyboard layouts:

```python
import ctypes
from ctypes import wintypes

def _copy_to_clipboard_win32(self, text: str) -> bool:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    CF_UNICODETEXT = 13      # Unicode text format
    GMEM_MOVEABLE = 0x0002   # Moveable memory allocation

    # Open clipboard
    if not user32.OpenClipboard(0):
        return False

    try:
        user32.EmptyClipboard()

        # Encode as UTF-16-LE with null terminator
        data = text.encode('utf-16-le') + b'\x00\x00'

        # Allocate and copy to global memory
        h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
        p_mem = kernel32.GlobalLock(h_mem)
        ctypes.memmove(p_mem, data, len(data))
        kernel32.GlobalUnlock(h_mem)

        # Set clipboard data
        user32.SetClipboardData(CF_UNICODETEXT, h_mem)
        return True
    finally:
        user32.CloseClipboard()
```

**Why UTF-16-LE?**
- Windows internally uses UTF-16-LE for Unicode text
- `CF_UNICODETEXT` expects this encoding
- Ensures proper handling of all characters including `@`, `/`, `~`, `^`

### Fallback Method: pyperclip

If Win32 API fails, we fall back to pyperclip:
```python
import pyperclip
pyperclip.copy(text)
```

---

## Keyboard Input

### Primary Method: Win32 SendInput API

We use `SendInput` for the most reliable keyboard input across all keyboard layouts:

```python
import ctypes
from ctypes import wintypes

# Virtual Key Codes (layout-independent)
VK_CONTROL = 0x11  # Ctrl key
VK_V = 0x56        # V key
VK_RETURN = 0x0D   # Enter key
VK_ESCAPE = 0x1B   # Escape key
VK_T = 0x54        # T key

KEYEVENTF_KEYUP = 0x0002
INPUT_KEYBOARD = 1

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),        # Virtual key code
        ("wScan", wintypes.WORD),      # Hardware scan code
        ("dwFlags", wintypes.DWORD),   # Key event flags
        ("time", wintypes.DWORD),      # Timestamp
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),      # INPUT_KEYBOARD = 1
        ("ki", KEYBDINPUT),
        ("padding", ctypes.c_ubyte * 8)
    ]

def send_key(vk: int, up: bool = False) -> None:
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.ki.wVk = vk
    inp.ki.dwFlags = KEYEVENTF_KEYUP if up else 0
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
```

### Ctrl+V Sequence

To paste, we send the following key sequence with delays:

```
1. Ctrl DOWN     (wait 50ms)
2. V DOWN        (wait 50ms)
3. V UP          (wait 50ms)
4. Ctrl UP
```

### Fallback Method: pyautogui

If SendInput fails:
```python
import pyautogui
pyautogui.hotkey('ctrl', 'v')
```

### AZERTY Keyboard Support

The solution works on AZERTY (Belgian French) keyboards because:

1. **Virtual Key Codes are layout-independent** - `VK_V` (0x56) refers to the physical key, not the character
2. **Clipboard uses Unicode** - The actual text is stored in the clipboard, not key codes
3. **Ctrl+V is universal** - The paste shortcut is the same on all Windows keyboard layouts

---

## Minecraft Command Processing

### Command Normalization

The `_normalize_carets()` method fixes common coordinate syntax issues:

```python
def _normalize_carets(self, s: str) -> str:
    # Remove '+' after ~ or ^ (Minecraft rejects ~+5)
    s = re.sub(r"([~\^])\+(?=\d)", r"\1", s)

    # Replace bare ^ with ^0
    s = re.sub(r"\^(?!-?\d)", "^0", s)

    # Replace bare ~ with ~0
    s = re.sub(r"~(?!-?\d)", "~0", s)

    return s
```

**Examples:**
| Input | Output | Reason |
|-------|--------|--------|
| `~+5` | `~5` | Minecraft rejects `+` after tilde |
| `^` | `^0` | Bare caret is invalid |
| `~` | `~0` | Prevents edge case errors |
| `^ ^ ^10` | `^0 ^0 ^10` | All carets need values |

### Chat Key Handling

The `chat_key` setting determines how chat is opened:

| Setting | Action | Result |
|---------|--------|--------|
| `"t"` | Press T | Opens chat, command needs `/` prefix |
| `"/"` | Press / | Opens chat with `/` pre-typed |

When `chat_key == "/"` and command starts with `/`, we strip the leading `/` to avoid `//command`.

### Enchantment Syntax (1.21.x)

Minecraft 1.21+ requires the `levels` sub-key for enchantments:

```
# CORRECT
/give @s netherite_sword[enchantments={levels:{sharpness:5,fire_aspect:2}}] 1

# WRONG - causes "Expected whitespace" error
/give @s netherite_sword[enchantments={sharpness:5,fire_aspect:2}] 1
```

---

## GUI Implementation

### Technology Update (v2.0.0+)

Maricraft uses **CustomTkinter** instead of native Tkinter:

| Component | Technology |
|-----------|------------|
| GUI Framework | CustomTkinter (modern Tkinter wrapper) |
| Main Window | `CTk` (not `tk.Tk`) |
| Buttons | `CTkButton` with hover effects |
| Frames | `CTkFrame`, `CTkScrollableFrame` |
| Theme | Kid-friendly colors via `ui/theme.py` |

### Main Window (App class)

```python
from customtkinter import CTk

class App(CTk):
    def __init__(self):
        super().__init__()
        # Window setup
        self.title("Maricraft")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Components
        self.header_frame    # Title + Settings button
        self.scroll_frame    # Scrollable container with buttons
        self.status_bar      # Status label at bottom
```

### ScrollableFrame

Custom scrollable container using Canvas + Scrollbar:

```python
class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent)
        self.scrollbar = tk.Scrollbar(parent, orient="vertical",
                                       command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Bind mousewheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
```

### Button Grid

Buttons are arranged in a grid (4 columns by default):

```python
BUTTONS_PER_ROW = 4

for idx, button in enumerate(category.buttons):
    row = idx // BUTTONS_PER_ROW
    col = idx % BUTTONS_PER_ROW

    btn = tk.Button(
        frame,
        text=button.name,
        bg=button.color,
        command=lambda b=button: self._on_button_click(b)
    )
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
```

### ToolTip

Hover tooltips show button descriptions:

```python
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event):
        # Create toplevel window near cursor
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        label = tk.Label(self.tip, text=self.text, bg="#FFFFD0")
        label.pack()

    def hide(self, event):
        if self.tip:
            self.tip.destroy()
```

### Threading

Button commands run in background threads to keep the GUI responsive:

```python
def _on_button_click(self, button: CommandButton):
    thread = threading.Thread(
        target=self._execute_button,
        args=(button,),
        daemon=True
    )
    thread.start()
```

---

## Configuration & Settings

### Settings Dataclass

```python
@dataclass
class Settings:
    chat_key: str = "t"          # "t" or "/"
    delay_ms: int = 100          # Delay between commands
    press_escape_first: bool = True  # Press Esc before commands
```

### Timing Constants

Defined in `constants.py`:

```python
# Delays (milliseconds)
DELAY_FAST_MS = 50       # Minimum delay
DELAY_STANDARD_MS = 100  # Default delay

# Window detection
MINECRAFT_WINDOW_TITLES = ["Minecraft"]
```

### Actual Timing in Automation

| Action | Delay |
|--------|-------|
| After window focus | 300ms |
| After Escape key | 300ms |
| After opening chat | 300ms |
| After clipboard copy | 200ms |
| Between SendInput keys | 50ms |
| After paste | 200ms |
| After Enter (configurable) | `settings.delay_ms` |

---

## Logging System

### Logger Class

```python
class Logger:
    def __init__(self, filename: str = "maricraft_log.txt"):
        self.filename = filename

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
```

### Log Output Example

```
[2025-12-06 10:36:28] === Maricraft run started ===
[2025-12-06 10:36:28] Focusing Minecraft...
[2025-12-06 10:36:28] Focused window: Minecraft
[2025-12-06 10:36:28] Resuming game (Esc)...
[2025-12-06 10:36:28] Sending command 1/1...
[2025-12-06 10:36:28] Command: /effect give @s regeneration 300 2 true
[2025-12-06 10:36:28] Pasting text: effect give @s regeneration 300 2 true
[2025-12-06 10:36:28] Copied to clipboard (Win32): effect give @s regeneration...
[2025-12-06 10:36:28] Paste via SendInput successful
[2025-12-06 10:36:29] Done!
[2025-12-06 10:36:29] === Maricraft run finished ===
```

---

## Build & Packaging

### PyInstaller Configuration

`maricraft.spec`:

```python
a = Analysis(
    ['maricraft/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pygetwindow', 'pyperclip', 'pyautogui'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='MariCraft',
    debug=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    icon=None,
)
```

### Build Commands

```bash
# Install PyInstaller
pip install pyinstaller

# Build .exe
pyinstaller maricraft.spec --clean

# Output: dist/MariCraft.exe
```

### Dependencies

```toml
# pyproject.toml
dependencies = [
    "pyautogui>=0.9.54",    # Fallback keyboard/mouse
    "pygetwindow>=0.0.9",   # Window management
    "pyperclip>=1.8.2",     # Fallback clipboard
]
```

**Note:** The primary automation uses `ctypes` (Python standard library) for Win32 API calls, so no external dependencies are required for core functionality.

---

## Troubleshooting

### Common Issues

#### "Commands not working"
1. Ensure Minecraft is in **windowed mode** (not fullscreen)
2. Enable **cheats** in the Minecraft world
3. Increase delay in Settings

#### "Clipboard paste fails on AZERTY keyboard"
- Verify Win32 clipboard API is being used (check log for "Copied to clipboard (Win32)")
- Check `maricraft_log.txt` for errors

#### "Window not found"
- Ensure Minecraft is running
- Window title must contain "Minecraft"

#### "App opens and closes immediately"
- Run `DEBUG_MARICRAFT.bat` to see error details
- Check Python is installed correctly

### Debug Mode

Run `DEBUG_MARICRAFT.bat` to:
1. Check Python version
2. Verify all packages are installed
3. Test module imports
4. Run with full error output

### Log File Location

Log file is created in the same directory as the application:
- `maricraft_log.txt`

---

## API Reference

### WindowsAutomator

```python
class WindowsAutomator:
    def __init__(
        self,
        status_cb: Optional[Callable[[str], None]] = None,
        stop_event: Optional[threading.Event] = None,
        logger: Optional[LoggerProtocol] = None,
    ) -> None

    def focus_minecraft(self, attempts: int = 3, settle_ms: int = 200) -> bool
    def key_escape(self) -> None
    def key_enter(self) -> None
    def open_chat(self, chat_key: str) -> None
    def paste_text(self, text: str) -> None
    def send_command(self, command: str, settings: Settings) -> bool
    def run_commands(self, commands: List[str], settings: Settings) -> None
```

### CommandButton

```python
@dataclass
class CommandButton:
    name: str           # Button label
    description: str    # Tooltip text
    commands: List[str] # Commands to execute
    color: str          # Hex color code (#RRGGBB)
```

### CommandCategory

```python
@dataclass
class CommandCategory:
    name: str                       # Category header
    buttons: List[CommandButton]    # Buttons in category
```

---

## Version History

| Version | Changes |
|---------|---------|
| 1.0.0 | Initial Windows release with button-based UI |
| 1.0.1 | Added keyboard library for AZERTY support |
| 1.0.2 | Switched to native Win32 clipboard API |
| 1.0.3 | Increased timing delays for reliability |

---

## References

- [Win32 Clipboard API](https://docs.microsoft.com/en-us/windows/win32/dataxchg/clipboard)
- [Win32 SendInput](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput)
- [Virtual-Key Codes](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes)
- [Minecraft Commands Wiki](https://minecraft.wiki/w/Commands)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)
