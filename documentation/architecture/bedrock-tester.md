# Bedrock Command Tester

> WebSocket-based testing system for validating Minecraft Bedrock commands in real-time.

## Overview

The Bedrock Command Tester allows developers to send mcfunction commands directly to Minecraft Bedrock Edition via WebSocket connection and receive immediate feedback on command success/failure.

## Architecture

```
maricraft/bedrock_tester/
├── __init__.py         # Package exports
├── __main__.py         # CLI entry point
├── server.py           # WebSocket server (py-mcws)
├── command_runner.py   # Test execution engine (if exists)
└── report.py           # JSON/text report generation (if exists)
```

## Dependencies

- **py-mcws**: WebSocket library for Minecraft Bedrock communication
- Install with: `pip install py-mcws`

## Usage

### Starting the Tester

```bash
# Basic usage - test all .mcfunction files in a directory
python -m maricraft.bedrock_tester --path ./functions --delay 0.3

# With custom port
python -m maricraft.bedrock_tester --path ./functions --port 19132
```

### Connecting from Minecraft

In Minecraft Bedrock Edition, open chat and run:
```
/connect <your-ip>:19132
```

**Note:** Use your LAN IP address (e.g., `192.168.0.227`), not `localhost`.

## Handshake Pattern

The tester implements an "anchor handshake" to solve entity registration delays:

### The Problem
When entities are summoned via WebSocket, they aren't immediately queryable. The game needs time to register them in the entity map.

### The Solution

1. **Summon anchor entity** with atomic naming:
   ```
   summon armor_stand "mc_anchor" ~1 ~ ~1
   ```

2. **Poll with testfor** until entity is queryable:
   ```
   testfor @e[name="mc_anchor"]
   ```

3. **Execute build commands** relative to anchor:
   ```
   execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~3 ~ gold_block
   ```

4. **Cleanup anchor** when done:
   ```
   kill @e[name="mc_anchor"]
   ```

## Key Classes

### BedrockCommandTester

Main server class that manages WebSocket connections.

```python
from maricraft.bedrock_tester import BedrockCommandTester

tester = BedrockCommandTester(host="0.0.0.0", port=19132)
tester.start()
```

**Key Methods:**
- `start()` - Start the WebSocket server (blocking)
- `test_command(cmd)` - Send a single command and get result
- `test_commands(commands, delay)` - Send multiple commands with delay
- `establish_anchor()` - Set up anchor entity with handshake
- `cleanup_anchor()` - Remove anchor entity

### CommandResult

Dataclass containing command execution results.

```python
@dataclass
class CommandResult:
    command: str           # The command that was sent
    success: bool          # Whether it succeeded
    response: str | None   # Success message from game
    error: str | None      # Error message if failed
    file: str | None       # Source file (if from mcfunction)
    line_num: int | None   # Line number in source file
```

## Bedrock Execute Syntax

**Important:** Bedrock Edition uses different execute syntax than Java Edition.

| Edition | Syntax |
|---------|--------|
| **Java** | `execute as @e[...] at @s run <command>` |
| **Bedrock (OLD)** | `execute @e[...] ~ ~ ~ <command>` |
| **Bedrock (NEW 1.19.50+)** | `execute at @e[...] run <command>` |

The OLD Bedrock syntax sets both WHO runs the command and WHERE it runs.

## Test Output

The tester produces JSON reports with:
- List of all commands tested
- Success/failure status for each
- Error messages for failures
- Summary statistics

## Troubleshooting

### "Connection refused"
- Ensure Minecraft is running before connecting
- Check firewall settings allow port 19132

### "No targets matched selector"
- Entity may not be registered yet (use handshake pattern)
- Check selector syntax matches Bedrock format

### WebSocket disconnects
- Minecraft may timeout idle connections
- Keep sending commands or implement keepalive

## Related Documentation

- [Anchor Investigation](../internal/bedrock_anchor_investigation.md) - Ongoing research
- [Java/Bedrock Parity](../1.20-and-up-syntax_doc.md) - Syntax differences
