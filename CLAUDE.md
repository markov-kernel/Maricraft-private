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

Maricraft is a **Windows-only**, kid-friendly Minecraft command helper. It provides a button-based CustomTkinter GUI where users click pre-programmed buttons to send commands to Minecraft.

**Key Features (v2.0.23):**
- **Java & Bedrock Support**: Auto-detects edition and uses appropriate commands
- **Datapack Mode**: Buttons send `/function maricraft:xxx` calls for instant execution
- **Auto-Update Check**: Checks GitHub for new versions on startup
- **64 Pre-built Buttons**: Organized in 4 categories

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
| `maricraft/__main__.py` | Entry point with error handling |
| `maricraft/ui/` | CustomTkinter GUI package |
| `maricraft/ui/app.py` | Main App class, button handling, Bedrock detection |
| `maricraft/ui/state.py` | JSON state persistence |
| `maricraft/ui/theme.py` | Color/font definitions |
| `maricraft/ui/components/` | UI widgets (buttons, dialogs, toolbar) |
| `maricraft/commands.py` | CommandButton definitions with function_id and bedrock_commands |
| `maricraft/automator.py` | `WindowsAutomator`: pyautogui + Win32 clipboard |
| `maricraft/datapack.py` | Datapack/behavior pack installation |
| `maricraft/version.py` | Version constant and GitHub update check |
| `maricraft/constants.py` | Timing, window dimensions, UI constants |
| `maricraft/settings.py` | Settings dataclass (chat_key, delay_ms) |
| `maricraft/logger.py` | Timestamped file logging |

### Datapack System

Buttons use a Minecraft datapack with 64 mcfunction files. Each button click sends a single `/function maricraft:xxx` command instead of multiple raw commands.

**Datapack location:**
```
maricraft/resources/maricraft_datapack/
├── pack.mcmeta                    # pack_format: 48 (MC 1.21.x)
├── version.txt
└── data/maricraft/function/
    ├── buffs/                     # 16 functions
    ├── gear/                      # 16 functions
    ├── teleport/                  # 16 functions
    └── world/                     # 16 functions
```

**Benefits:**
- Single command per button (vs 1-7 raw commands)
- Faster execution (~100ms vs ~3.5s for GOD MODE)
- No 256-char limit concerns
- Atomic server-side execution

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
    name="Button Label",
    description="Tooltip",
    commands=["/command1", "/command2"],  # Raw commands (fallback)
    color="#FF6B6B",
    function_id="maricraft:category/function_name"  # Datapack function
)
```

After adding a button:
1. Create matching `.mcfunction` file in `maricraft/resources/maricraft_datapack/data/maricraft/function/`
2. Rebuild the app if using PyInstaller

### Bedrock Edition Support

Maricraft supports both Java and Bedrock Edition:

- **Detection**: Uses `tasklist` to check for `Minecraft.Windows.exe` process
- **Commands**: Each `CommandButton` has optional `bedrock_commands` list
- **Behavior Packs**: Bedrock uses behavior packs instead of datapacks
- **Path Detection**: Supports GDK (Xbox App), UWP (Microsoft Store) installations

Example button with Bedrock support:
```python
CommandButton(
    name="Full Heal",
    commands=["/effect give @s instant_health 1 255"],  # Java
    bedrock_commands=["/effect @s instant_health 1 255"],  # Bedrock (no "give")
    function_id="maricraft:buffs/full_heal"
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
| `^` | `^0` | Bare caret invalid in Minecraft |
| `~` | `~0` | Normalized for consistency |
| `~+5` | `~5` | Minecraft rejects `+` after `~` or `^` |

### Coordinate Rules

- **Never mix** `~` and `^` in the same XYZ triplet
- Look-direction placement: `execute at @s run tp @s ^0 ^0 ^D`
- Always use explicit zeros: `^0 ^0 ^10` not `^ ^ ^10`

## Version and Updates

- Version defined in `maricraft/version.py` as `__version__`
- `version.json` in repo root contains version info for update checking
- App checks GitHub on startup and shows banner if update available

To release a new version:
1. Update `__version__` in `maricraft/version.py`
2. Update `version.json` in repo root
3. Build with `pyinstaller maricraft.spec --clean`
4. Create GitHub release with the new `.exe`

## Windows Requirements

1. **Minecraft Java Edition** must be running
2. The app will automatically focus the Minecraft window
3. For best results, run Minecraft in **windowed mode** (not fullscreen)
4. **Datapack must be installed** in the world (use "Install Datapack" button)

## Dependencies

```toml
pyautogui>=0.9.54    # Keyboard automation
pygetwindow>=0.0.9   # Window focus
pyperclip>=1.8.2     # Clipboard
```

## File Structure

```
Maricraft/
├── CLAUDE.md                              # This file
├── README.md                              # User guide
├── TECHNICAL.md                           # Deep technical documentation
├── version.json                           # Version info for update check
├── INSTALL.bat                            # Installer script
├── RUN_MARICRAFT.bat                      # Launch script
├── DEBUG_MARICRAFT.bat                    # Debug script
├── build.bat                              # PyInstaller build script
├── maricraft.spec                         # PyInstaller config
├── maricraft/
│   ├── __init__.py                        # Package init, exports __version__
│   ├── __main__.py                        # Entry point
│   ├── ui/                                # CustomTkinter GUI package
│   │   ├── __init__.py
│   │   ├── app.py                         # Main App class
│   │   ├── state.py                       # State persistence
│   │   ├── theme.py                       # Color/font definitions
│   │   └── components/                    # UI widgets
│   ├── commands.py                        # 64 button definitions
│   ├── automator.py                       # Windows automation
│   ├── datapack.py                        # Datapack/behavior pack management
│   ├── version.py                         # Version and update check
│   ├── constants.py                       # UI constants
│   ├── settings.py                        # Settings dataclass
│   ├── logger.py                          # File logging
│   └── resources/
│       ├── maricraft_datapack/            # Java datapack (64 mcfunction files)
│       └── maricraft_behavior/            # Bedrock behavior pack
└── documentation/
    ├── INDEX.md                           # Documentation index
    ├── 1.21.1-command-playbook.md         # Minecraft command reference
    ├── minecraft-chat-cheatsheet.txt      # Quick syntax reference
    ├── example-netherite-gear.md          # Example vanilla gear
    └── example-cataclysm-gear.md          # Example modded gear
```

## Installation (for users)

1. Unzip the Maricraft folder
2. Double-click `INSTALL.bat` (installs Python packages)
3. Double-click `RUN_MARICRAFT.bat`
4. Click "Install Datapack" and select your Minecraft world(s)
5. In Minecraft, run `/reload` or restart the world
