# Maricraft Documentation Index

## Quick Start

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | User guide - installation and usage |
| [CLAUDE.md](../CLAUDE.md) | Developer guide for Claude Code |

---

## About Maricraft

Maricraft is a **Windows-only**, kid-friendly Minecraft command helper. Click colorful buttons to send commands to Minecraft - no typing required!

### Features
- 64 pre-programmed buttons across 4 categories
- Works with Minecraft Java Edition 1.21.x
- Simple installation (just run INSTALL.bat)

### Button Categories

| Category | Examples |
|----------|----------|
| **Buffs & Effects** | Full Heal, Regen, Night Vision, GOD MODE |
| **Gear & Items** | Netherite Armor, Super Sword, Elytra |
| **Teleport & Locate** | Find Village, Find Stronghold, TP Forward |
| **World Control** | Set Day, Weather, Difficulty, Keep Inventory |

---

## Minecraft Command References

| Document | Description |
|----------|-------------|
| [1.21.1-command-playbook.md](1.21.1-command-playbook.md) | Complete Minecraft Java 1.21.1 command reference |
| [minecraft-chat-cheatsheet.txt](minecraft-chat-cheatsheet.txt) | Quick syntax reference card |

### Key Syntax (1.21.x)

**Enchantments** (note the `levels` key):
```
/give @s netherite_sword[enchantments={levels:{sharpness:5,fire_aspect:2}}] 1
```

**Attributes**:
```
/give @s netherite_sword[attribute_modifiers=[{type:"minecraft:generic.attack_damage",amount:100,operation:"add_value",slot:"mainhand",id:"custom:dmg"}]] 1
```

**Unbreakable**:
```
/give @s elytra[unbreakable={}] 1
```

---

## Critical Limits

| Limit | Value |
|-------|-------|
| Chat command length | 256 characters max |
| Fill/clone volume | 32,768 blocks max |

---

## Architecture (for Developers)

### Module Structure

```
maricraft/
├── __main__.py      # Entry point with error handling
├── ui.py            # Tkinter GUI with button grid
├── commands.py      # Pre-defined command buttons
├── automator.py     # WindowsAutomator (pyautogui)
├── constants.py     # Timing and UI constants
├── settings.py      # Simple settings dataclass
└── logger.py        # File logging
```

### Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `WindowsAutomator` | automator.py | Windows automation via pyautogui |
| `App` | ui.py | Tkinter GUI with button categories |
| `CommandButton` | commands.py | Button definition (name, commands, color) |
| `CommandCategory` | commands.py | Group of related buttons |
| `Settings` | settings.py | Configuration (chat_key, delay_ms) |

### Adding New Buttons

Edit `maricraft/commands.py`:
```python
CommandButton(
    name="Button Name",
    description="Tooltip text",
    commands=["/command1", "/command2"],
    color="#FF6B6B"
)
```

---

## Installation

### On Windows
1. Unzip the Maricraft folder
2. Double-click `INSTALL.bat` (installs Python packages)
3. Double-click `RUN_MARICRAFT.bat`

### Dependencies
- Python 3.10+
- pyautogui
- pygetwindow
- pyperclip

---

## Troubleshooting

**Commands not working?**
- Make sure cheats are enabled in your Minecraft world
- Run Minecraft in windowed mode (not fullscreen)
- Increase delay in Settings if commands are missed

**App won't start?**
- Run `DEBUG_MARICRAFT.bat` to see error details
- Run `INSTALL.bat` again to reinstall packages
