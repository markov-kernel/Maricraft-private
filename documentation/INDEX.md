# Maricraft Documentation Index

> Kid-friendly Minecraft command helper for Java & Bedrock Edition

## Quick Links

| Audience | Start Here |
|----------|-----------|
| **New Users** | [Getting Started](guides/getting-started.md) |
| **Developers** | [CLAUDE.md](../CLAUDE.md) → [TECHNICAL.md](../TECHNICAL.md) |
| **Contributors** | [CLAUDE.md](../CLAUDE.md) |

---

## About Maricraft

Maricraft is a **Windows-only**, kid-friendly Minecraft command helper. Click colorful buttons to send commands to Minecraft - no typing required!

### Features
- 64 pre-programmed buttons across 4 categories
- **Datapack-powered** - Commands execute instantly via Minecraft functions
- **Auto-update check** - Get notified when new versions are available
- Works with **Minecraft Java Edition 1.21.x** and **Bedrock Edition**
- Simple installation (just run INSTALL.bat)

### Button Categories

| Category | Examples |
|----------|----------|
| **Buffs & Effects** | Full Heal, Regen, Night Vision, GOD MODE |
| **Gear & Items** | Netherite Armor, Super Sword, Elytra |
| **Teleport & Locate** | Find Village, Find Stronghold, TP Forward |
| **World Control** | Set Day, Weather, Difficulty, Keep Inventory |

---

## Documentation Map

### Guides

| Document | Description |
|----------|-------------|
| [Getting Started](guides/getting-started.md) | 5-minute setup for new users |
| [README.md](../README.md) | User guide - installation and usage |

### Reference

| Document | Description |
|----------|-------------|
| [1.21.1-command-playbook.md](1.21.1-command-playbook.md) | Complete Minecraft Java 1.21.1 command reference |
| [1.20-and-up-syntax_doc.md](1.20-and-up-syntax_doc.md) | Java/Bedrock Edition parity guide |
| [minecraft-chat-cheatsheet.txt](minecraft-chat-cheatsheet.txt) | Quick syntax reference card |
| [maricraft-ai-prompt.txt](maricraft-ai-prompt.txt) | Canonical AI system prompt |

### Examples

| Document | Description |
|----------|-------------|
| [example-netherite-gear.md](example-netherite-gear.md) | Vanilla Netherite gear command templates |
| [example-cataclysm-gear.md](example-cataclysm-gear.md) | Cataclysm mod gear command templates |
| [ai-prompt-example.md](ai-prompt-example.md) | AI command generation format example |

### Architecture (Developers)

| Document | Description |
|----------|-------------|
| [UI Components](architecture/ui-components.md) | CustomTkinter GUI structure |
| [Bedrock Tester](architecture/bedrock-tester.md) | WebSocket testing system |
| [Datapack System](architecture/datapack-system.md) | Pack installation logic |
| [CLAUDE.md](../CLAUDE.md) | Developer quick reference |
| [TECHNICAL.md](../TECHNICAL.md) | Deep technical documentation |

### Internal (Maintainers)

| Document | Description |
|----------|-------------|
| [Anchor Investigation](internal/bedrock_anchor_investigation.md) | Active research on Bedrock entity timing |
| [Bedrock Bug Report](internal/BEDROCK_BUG_REPORT.md) | Historical bug tracking |

---

## Key Syntax (1.21.x)

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

## Module Structure

```
maricraft/
├── __main__.py      # Entry point with error handling
├── ui/              # CustomTkinter GUI package
│   ├── app.py       # Main App class, Bedrock detection
│   ├── state.py     # JSON state persistence
│   ├── theme.py     # Color/font definitions
│   └── components/  # UI widgets
├── commands.py      # Pre-defined command buttons
├── automator.py     # WindowsAutomator (pyautogui + Win32 clipboard)
├── constants.py     # Timing and UI constants
├── settings.py      # Simple settings dataclass
├── logger.py        # File logging
├── version.py       # Version constant + GitHub update check
├── datapack.py      # Datapack/behavior pack installation
├── validator/       # Command syntax validator
├── bedrock_tester/  # WebSocket Bedrock testing
└── resources/
    ├── maricraft_datapack/   # Java datapack (64 mcfunction files)
    └── maricraft_behavior/   # Bedrock behavior pack
```

---

## Installation

### Quick Start
1. Unzip the Maricraft folder
2. Double-click `INSTALL.bat` (installs Python packages)
3. Double-click `RUN_MARICRAFT.bat`
4. **First time:** Click "Install Datapack" button and select your worlds
5. In Minecraft, run `/reload` to activate

See [Getting Started](guides/getting-started.md) for detailed instructions.

### Bedrock Edition

Maricraft automatically detects when Minecraft Bedrock Edition is running and uses **behavior packs** instead of datapacks.

| Aspect | Java Edition | Bedrock Edition |
|--------|--------------|-----------------|
| Pack type | Datapack | Behavior pack |
| Reload method | `/reload` command | **Full Minecraft restart** |
| Install location | `<world>/datapacks/` | `<world>/behavior_packs/` |

---

## Troubleshooting

**"Unknown function" or commands not working?**
- Make sure the datapack/behavior pack is installed
- **Java Edition:** Run `/reload` in Minecraft
- **Bedrock Edition:** Completely restart Minecraft
- Make sure cheats are enabled in your world

**Commands not working?**
- Run Minecraft in windowed mode (not fullscreen)
- Increase delay in Settings if commands are missed

**App won't start?**
- Run `DEBUG_MARICRAFT.bat` to see error details
- Run `INSTALL.bat` again to reinstall packages

---

## Version History

### v2.0.23 (Current)
- **Bedrock Edition support**: Auto-detects Java vs Bedrock
- **Behavior pack installation**: Bedrock worlds use behavior packs
- **Documentation restructure**: New guides, architecture, and internal docs

### v2.0.0
- **Datapack system**: All 64 buttons use `/function` calls
- **Auto-update check**: Notifies when new versions available
- **Install Datapack button**: Easy one-click setup
