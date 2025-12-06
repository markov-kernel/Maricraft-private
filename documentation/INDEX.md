# Maricraft Documentation Index

## Quick Start

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | User guide - installation and usage |
| [CLAUDE.md](../CLAUDE.md) | Developer guide for Claude Code |
| [TECHNICAL.md](../TECHNICAL.md) | Deep technical implementation details |

---

## About Maricraft

Maricraft is a **Windows-only**, kid-friendly Minecraft command helper. Click colorful buttons to send commands to Minecraft - no typing required!

### Features
- 64 pre-programmed buttons across 4 categories
- **Datapack-powered** - Commands execute instantly via Minecraft functions
- **Auto-update check** - Get notified when new versions are available
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

---

## Examples

| Document | Description |
|----------|-------------|
| [example-netherite-gear.md](example-netherite-gear.md) | Vanilla Netherite gear command templates |
| [example-cataclysm-gear.md](example-cataclysm-gear.md) | Cataclysm mod gear command templates |
| [ai-prompt-example.md](ai-prompt-example.md) | AI command generation format example |
| [maricraft-ai-prompt.txt](maricraft-ai-prompt.txt) | Canonical AI system prompt |

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
├── ui/              # CustomTkinter GUI package
│   ├── app.py       # Main App class, Bedrock detection
│   ├── state.py     # JSON state persistence
│   ├── theme.py     # Color/font definitions
│   └── components/  # UI widgets
├── commands.py      # Pre-defined command buttons (with function_id, bedrock_commands)
├── automator.py     # WindowsAutomator (pyautogui + Win32 clipboard)
├── constants.py     # Timing and UI constants
├── settings.py      # Simple settings dataclass
├── logger.py        # File logging
├── version.py       # Version constant + GitHub update check
├── datapack.py      # Datapack/behavior pack installation
└── resources/
    ├── maricraft_datapack/   # Java datapack (64 mcfunction files)
    └── maricraft_behavior/   # Bedrock behavior pack
```

### Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `WindowsAutomator` | automator.py | Windows automation via pyautogui |
| `App` | ui/app.py | CustomTkinter GUI with button categories |
| `CommandButton` | commands.py | Button definition (name, commands, bedrock_commands, function_id) |
| `CommandCategory` | commands.py | Group of related buttons |
| `Settings` | settings.py | Configuration (chat_key, delay_ms) |

### How Commands Work (v2.0.0+)

Each button has a `function_id` (e.g., `maricraft:buffs/god_mode`). When clicked:

1. App sends `/function maricraft:buffs/god_mode` to Minecraft
2. The installed datapack executes the mcfunction file
3. Multiple commands run server-side in a single tick

**Benefits:**
- GOD MODE: ~100ms instead of ~3.5 seconds (7 effects)
- Single command per button (no 256-char limit concerns)
- Atomic execution (all-or-nothing)

### Adding New Buttons

Edit `maricraft/commands.py`:
```python
CommandButton(
    name="Button Name",
    description="Tooltip text",
    commands=["/command1", "/command2"],  # Fallback if no datapack
    color="#FF6B6B",
    function_id="maricraft:category/button_name"  # Datapack function
)
```

Also create the corresponding mcfunction file in:
`maricraft/resources/maricraft_datapack/data/maricraft/function/category/button_name.mcfunction`

---

## Installation

### On Windows
1. Unzip the Maricraft folder
2. Double-click `INSTALL.bat` (installs Python packages)
3. Double-click `RUN_MARICRAFT.bat`
4. **First time:** Click "Install Datapack" button and select your worlds
5. In Minecraft, run `/reload` to activate

### Dependencies
- Python 3.10+
- pyautogui
- pygetwindow
- pyperclip

### Datapack Installation

The datapack is required for commands to work. It's installed automatically per-world:

1. Click **"Install Datapack"** button in the app header
2. Select one or more Minecraft worlds
3. Click **"Install to Selected"**
4. In Minecraft, run `/reload` or restart the world

The datapack is copied to: `<world>/datapacks/maricraft_datapack/`

---

## Troubleshooting

**"Unknown function" or commands not working?**
- Make sure the datapack is installed (click "Install Datapack" button)
- Run `/reload` in Minecraft after installing the datapack
- Make sure cheats are enabled in your Minecraft world

**Commands not working?**
- Run Minecraft in windowed mode (not fullscreen)
- Increase delay in Settings if commands are missed

**App won't start?**
- Run `DEBUG_MARICRAFT.bat` to see error details
- Run `INSTALL.bat` again to reinstall packages

**Update available banner?**
- Click "Download" to get the latest version from GitHub
- Or click X to dismiss the banner

---

## Version History

### v2.0.23 (Current)
- **Bedrock Edition support**: Auto-detects Java vs Bedrock via process detection
- **Behavior pack installation**: Bedrock worlds use behavior packs instead of datapacks
- **`tasklist`-based detection**: No psutil dependency required

### v2.0.0
- **Datapack system**: All 64 buttons use `/function` calls for instant execution
- **Auto-update check**: Notifies when new versions are available on GitHub
- **Install Datapack button**: Easy one-click setup for Minecraft worlds
- **Faster execution**: GOD MODE now ~100ms instead of ~3.5 seconds
