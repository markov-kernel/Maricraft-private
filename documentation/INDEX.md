# Maricraft Documentation Index

## Quick Start

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | User guide - installation, usage tips, permissions |
| [CLAUDE.md](../CLAUDE.md) | Developer guide for Claude Code integration |

---

## Core References

### Minecraft Commands

| Document | Description |
|----------|-------------|
| [1.21.1-command-playbook.md](1.21.1-command-playbook.md) | Complete Minecraft Java 1.21.1 command reference |
| [minecraft-chat-cheatsheet.txt](minecraft-chat-cheatsheet.txt) | Quick syntax reference card |

**Key Topics:**
- Data Components (1.21.x item syntax): `item[component=value]`
- Attribute modifiers: `minecraft:generic.attack_damage`, `minecraft:generic.attack_speed`
- Coordinates: absolute (`100 64 -30`), relative (`~5 ~ ~-3`), local (`^0 ^0 ^10`)
- Target selectors: `@p`, `@a`, `@s`, `@e[type=...,distance=...]`
- NBT/SNBT and Raw JSON text embedding

### AI Assistant

| Document | Description |
|----------|-------------|
| [maricraft-ai-prompt.txt](maricraft-ai-prompt.txt) | System prompt for the AI command generator |
| [ai-prompt-example.md](ai-prompt-example.md) | Extended prompt example with full rules |

**AI Prompt Rules:**
- Output exactly one fenced code block (`mcfunction`)
- Look-direction placement: `execute positioned ^0 ^0 ^D run ...`
- Site preparation (flatten ground before building)
- Block budgeting (split fills >32,768 blocks)
- Caret normalization (`^` → `^0`)
- No `~+N` or `^+N` (use `~N` / `^N`)

---

## Examples

| Document | Description |
|----------|-------------|
| [example-netherite-gear.md](example-netherite-gear.md) | Vanilla Netherite gear with custom attributes |
| [example-cataclysm-gear.md](example-cataclysm-gear.md) | Modded Cataclysm gear (requires mod) |

**Example Features:**
- Full armor sets with enchantments and attribute modifiers
- Weapons with one-shot damage (`amount:2048`)
- Custom names with JSON text styling
- Permanent effect buffs
- Compact versions for chat (<256 chars)

---

## Critical Limits

| Limit | Value | Workaround |
|-------|-------|------------|
| Chat command length | 256 characters | Use command blocks or shorten |
| Fill/clone volume | 32,768 blocks | Split into multiple commands |
| Attribute ID format (1.21.1) | `minecraft:generic.*` | Updated to `minecraft:*` in 1.21.2+ |

---

## Architecture (for Developers)

### Module Structure

```
maricraft/
├── __main__.py      # Entry point
├── ui.py            # Tkinter GUI + MacAutomator + Logger
├── ai_chat.py       # AI assistant (OpenAI Agents SDK + LiteLLM)
├── hotkeys.py       # Global hotkey watcher (Space+Escape)
├── debug_tools.py   # CLI testing tools
├── automator.py     # (new) Automation utilities
├── constants.py     # (new) Shared constants
├── logger.py        # (new) Logging utilities
└── settings.py      # (new) Settings management
```

### Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `MacAutomator` | ui.py:45-554 | AppleScript/Quartz automation for Minecraft |
| `App` | ui.py:557-954 | Tkinter GUI with Commands and AI tabs |
| `AIChatController` | ai_chat.py:123-304 | AI interaction via OpenRouter |
| `Settings` | ui.py:30-43 | Run configuration dataclass |
| `Logger` | ui.py:964-984 | Timestamped file logger |

### Command Preprocessing

`MacAutomator._normalize_carets()` automatically fixes:
- Bare `^` → `^0`
- Bare `~` → `~0`
- `~+5` → `~5`, `^+2` → `^2`

---

## Environment Setup

### Required
```bash
# .env file in project root
OPENROUTER_API_KEY=your_key_here
```

### Optional
```bash
OR_SITE_URL=https://example.com    # Attribution header
OR_APP_NAME=Maricraft              # Attribution header
```

### macOS Permissions
1. System Settings → Privacy & Security → Accessibility
2. Enable: Terminal (or your IDE), `osascript`
3. Minecraft must be running as `java` or `javaw` process

---

## Running the Application

```bash
# Start the GUI
uv run python -m maricraft

# Debug tools
uv run python -m maricraft.debug_tools paste-test --text "/tp @s ~ ~ ~"
uv run python -m maricraft.debug_tools type-tilde-test --text "/fill ~-1 ~ ~-1 ~1 ~1 ~1 air"
```

---

## Emergency Stop

Press **Space+Escape** (either order, within 500ms) to immediately stop a running macro. Works globally even when Minecraft is focused.
