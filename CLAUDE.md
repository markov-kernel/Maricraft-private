# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## IMPORTANT: Read Documentation First

**Before making any changes or generating Minecraft commands, you MUST read:**

```
documentation/INDEX.md
```

The INDEX.md provides a complete map of all documentation including:
- Minecraft 1.21.1 command syntax and critical limits
- AI prompt rules and validation checklists
- Example gear templates
- Architecture overview

**Do not proceed without consulting the INDEX.md first.**

---

## Project Overview

Maricraft is a macOS-only Minecraft chat macro runner. It provides a Tkinter GUI to paste a list of chat commands and send them to a running Minecraft Java client via AppleScript/Quartz automation. It also includes an AI assistant feature that uses OpenRouter + LiteLLM to generate or debug Minecraft commands.

## Quick Commands

```bash
# Run the application
uv run python -m maricraft

# Debug tools
uv run python -m maricraft.debug_tools paste-test --text "/tp @s ~ ~ ~"
uv run python -m maricraft.debug_tools type-tilde-test --text "/fill ~-1 ~ ~-1 ~1 ~1 ~1 air"
```

## Architecture

### Module Structure

| Module | Purpose |
|--------|---------|
| `maricraft/ui.py` | Main entry point: `App` (Tkinter GUI), `MacAutomator`, `Settings`, `Logger` |
| `maricraft/ai_chat.py` | AI assistant using OpenAI Agents SDK + LiteLLM via OpenRouter |
| `maricraft/hotkeys.py` | Global hotkey watcher (Space+Escape) using Quartz event taps |
| `maricraft/debug_tools.py` | CLI tools for testing paste/type mechanisms |
| `maricraft/automator.py` | Automation utilities |
| `maricraft/constants.py` | Shared constants |
| `maricraft/logger.py` | Logging utilities |
| `maricraft/settings.py` | Settings management |

### Key Components

| Component | Location | Description |
|-----------|----------|-------------|
| `MacAutomator` | ui.py:45-554 | AppleScript/Quartz automation for Minecraft window control |
| `App` | ui.py:557-954 | Tkinter GUI with Commands and AI tabs |
| `AIChatController` | ai_chat.py:123-304 | AI interactions via OpenRouter |
| `Settings` | ui.py:30-43 | Run configuration dataclass |
| `Logger` | ui.py:964-984 | Timestamped file logger |

### Settings Fields

| Field | Description |
|-------|-------------|
| `chat_key` | Chat open key: `t` or `/` |
| `delay_ms` | Delay between commands |
| `press_escape_first` | Press Escape before starting |
| `type_instead_of_paste` | Type characters instead of clipboard paste |
| `use_quartz_injection` | Use Quartz for faster input |
| `turbo_mode` | ~40ms delays (default: False) |
| `ultra_mode` | ~5ms aggressive delays (default: True) |

## Critical Rules (Quick Reference)

> **Full details in `documentation/INDEX.md`**

### Minecraft 1.21.1 Limits

| Limit | Value |
|-------|-------|
| Chat command length | 256 characters max |
| Fill/clone volume | 32,768 blocks max per command |
| Attribute ID format | `minecraft:generic.*` (e.g., `minecraft:generic.attack_damage`) |

### Automatic Command Preprocessing

`MacAutomator._normalize_carets()` automatically fixes commands:

| Input | Output | Reason |
|-------|--------|--------|
| `^` | `^0` | Bare caret invalid |
| `~` | `~0` | Prevents edge case errors |
| `~+5` | `~5` | Minecraft rejects `+` after `~` or `^` |
| `^+2` | `^2` | Same as above |

### Coordinate Rules

- **Never mix** `~` and `^` in the same XYZ triplet
- Look-direction placement: `execute positioned ^0 ^0 ^D run ...`
- Always use explicit zeros: `^0 ^0 ^10` not `^ ^ ^10`

## Environment Variables

Create `.env` in project root:

```bash
OPENROUTER_API_KEY=...        # Required
OR_SITE_URL=...               # Optional: attribution header
OR_APP_NAME=...               # Optional: attribution header
```

## macOS Requirements

1. **Accessibility permissions** - System Settings > Privacy & Security > Accessibility
2. Grant access to Terminal/IDE and `osascript`
3. Minecraft must be running as `java` or `javaw` process

## Known Issues

- `HotkeyWatcher` is used in `ui.py` but not imported. The global hotkey (Space+Escape) will silently fail. Fix: add `from .hotkeys import HotkeyWatcher` to `ui.py` imports.

## Documentation Map

```
Maricraft/
├── CLAUDE.md                              # This file (dev guidance)
├── README.md                              # User quick start
└── documentation/
    ├── INDEX.md                           # START HERE - full documentation index
    ├── 1.21.1-command-playbook.md         # Complete command reference
    ├── maricraft-ai-prompt.txt            # AI system prompt
    ├── ai-prompt-example.md               # Extended prompt example
    ├── minecraft-chat-cheatsheet.txt      # Quick syntax reference
    ├── example-netherite-gear.md          # Vanilla gear example
    └── example-cataclysm-gear.md          # Modded gear example
```
