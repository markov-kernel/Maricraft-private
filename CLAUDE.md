# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## IMPORTANT: Read Documentation First

**Before making any changes or generating Minecraft commands, read:**

```
documentation/INDEX.md
```

This provides a complete map of all documentation including command syntax and critical limits.

---

## Project Overview

Maricraft is a **Windows-only**, kid-friendly Minecraft command helper. It provides a button-based Tkinter GUI where users click pre-programmed buttons to send commands to Minecraft Java Edition. The app uses pyautogui for Windows automation.

## Quick Commands

```bash
# Run the application (requires Python)
pip install pyautogui pygetwindow pyperclip
python -m maricraft

# Build standalone .exe (no Python required to run)
pip install pyinstaller
pyinstaller maricraft.spec --clean
# Output: dist/MariCraft.exe
```

Or on Windows, just double-click `build.bat`.

## Architecture

### Module Structure

| Module | Purpose |
|--------|---------|
| `maricraft/ui.py` | Main entry point: button-based Tkinter GUI |
| `maricraft/commands.py` | Pre-defined command buttons organized by category |
| `maricraft/automator.py` | `WindowsAutomator`: pyautogui automation for Minecraft |
| `maricraft/constants.py` | Timing, window dimensions, UI constants |
| `maricraft/settings.py` | Simple settings dataclass (chat_key, delay_ms) |
| `maricraft/logger.py` | Timestamped file logging |

### Button Categories

Defined in `commands.py`:

| Category | Examples |
|----------|----------|
| **Buffs & Effects** | Full Heal, Regen, Night Vision, GOD MODE |
| **Gear & Items** | Diamond/Netherite Armor, Super Sword, Elytra |
| **Teleport & Locate** | Find Village, Find Stronghold, TP Forward 100 |
| **World Control** | Set Day, Clear Weather, Peaceful Mode, Keep Inventory |

### Adding New Buttons

Edit `maricraft/commands.py`:

```python
CommandButton(
    name="Button Label",      # Shown on button
    description="Tooltip",    # Shown on hover
    commands=["/command1", "/command2"],  # Commands to execute
    color="#FF6B6B"           # Button background color (hex)
)
```

## Minecraft Command Rules

### Critical Limits

| Limit | Value |
|-------|-------|
| Chat command length | 256 characters max |
| Fill/clone volume | 32,768 blocks max per command |

### Enchantment Syntax (1.21.x)

**IMPORTANT**: In Minecraft 1.21.x, enchantments require the `levels` sub-key:

```
# CORRECT (1.21.x)
/give @s netherite_sword[enchantments={levels:{sharpness:5,fire_aspect:2}}] 1

# WRONG - causes "Expected whitespace" error
/give @s netherite_sword[enchantments={sharpness:5,fire_aspect:2}] 1
```

### Coordinate Normalization

`WindowsAutomator._normalize_carets()` automatically fixes:

| Input | Output | Reason |
|-------|--------|--------|
| `^` | `^0` | Bare caret invalid |
| `~` | `~0` | Prevents edge case errors |
| `~+5` | `~5` | Minecraft rejects `+` after `~` or `^` |

### Coordinate Rules

- **Never mix** `~` and `^` in the same XYZ triplet
- Look-direction placement: `execute at @s run tp @s ^0 ^0 ^D`
- Always use explicit zeros: `^0 ^0 ^10` not `^ ^ ^10`

## Windows Requirements

1. **Minecraft Java Edition** must be running
2. The app will automatically focus the Minecraft window
3. For best results, run Minecraft in **windowed mode** (not fullscreen)

## Dependencies

```toml
pyautogui>=0.9.54    # Keyboard automation
pygetwindow>=0.0.9   # Window focus
pyperclip>=1.8.2     # Clipboard
```

## Documentation

```
Maricraft/
├── CLAUDE.md                              # This file
├── README.md                              # User guide
├── INSTALL.bat                            # Installer script
├── RUN_MARICRAFT.bat                      # Launch script
├── DEBUG_MARICRAFT.bat                    # Debug script
├── build.bat                              # PyInstaller build script
├── maricraft.spec                         # PyInstaller config
└── documentation/
    ├── INDEX.md                           # START HERE - documentation index
    ├── 1.21.1-command-playbook.md         # Minecraft command reference
    ├── minecraft-chat-cheatsheet.txt      # Quick syntax reference
    └── example-netherite-gear.md          # Example gear templates
```

## Installation (for users)

1. Unzip the Maricraft folder
2. Double-click `INSTALL.bat` (installs Python packages)
3. Double-click `RUN_MARICRAFT.bat`
