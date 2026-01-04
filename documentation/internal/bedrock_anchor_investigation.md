# Bedrock Anchor Pattern Investigation

**Date:** 2025-12-06
**Status:** UNRESOLVED - Multiple bugs fixed, core issue remains
**Platform:** Minecraft Bedrock Edition (Windows via Parallels on macOS)

---

## Latest Session Summary (2025-12-06 Evening)

### Bugs Fixed

| Bug | Problem | Fix | File |
|-----|---------|-----|------|
| Wrong Execute Syntax | Used Java syntax `execute as @e[...] at @s run` | Changed to Bedrock OLD syntax `execute @e[...] ~ ~ ~ <cmd>` | `add_anchor.py:43` |
| Wrong StatusCode Check | Handshake checked `header.statusCode` | Changed to `body.statusCode` | `server.py:220` |
| Kill Filter Too Strict | Only matched exact `kill @e[name="X"]` | Now matches any `kill @e[` with anchor name | `server.py:273` |

### Current State

The handshake now detects the anchor successfully:
```
[Anchor] Ready after 1 polls (0.10s)
```

But execute commands still fail:
```
Error: No targets matched selector
```

### The New Paradox

1. Python summons anchor: `summon armor_stand "mc_anchor" ~1 ~ ~1`
2. Python's testfor succeeds: `testfor @e[name="mc_anchor"]` → statusCode=0
3. Execute commands fail: `execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock` → "No targets matched"
4. Python cleanup succeeds

**Question:** If testfor finds the entity, why can't execute find it?

### Possible Remaining Issues

1. **Filter not catching all commands** - Output shows "Filtered 1 anchor commands" but test file has 3 (1 summon + 2 kills)
2. **Timing between handshake and execute** - Maybe anchor disappears after testfor but before execute
3. **Different selector matching** - testfor uses `@e[name="X"]` but execute uses `@e[type=armor_stand,name="X",c=1]`

---

## Problem Statement

We need to implement an "anchor" pattern for building mcfunction files so that multi-command structures build correctly regardless of player movement during execution.

### The Challenge

When commands are sent via WebSocket (using py-mcws library), each command executes with `~` coordinates relative to the **player's current position at that moment**. If the player moves between commands, the building becomes misaligned.

### Desired Behavior

1. Summon an armor stand at a fixed position
2. Tag it for easy selection
3. All subsequent building commands execute relative to the anchor's position
4. Player movement during execution doesn't affect the build

---

## Technical Environment

### Software Stack
- **Minecraft:** Bedrock Edition (running in Parallels VM on macOS)
- **Python:** 3.x with uv package manager
- **Library:** py-mcws (Minecraft Bedrock WebSocket)
- **Connection:** `/connect 192.168.0.227:19132` (LAN IP)

### WebSocket Command Execution
Commands are sent via WebSocket with configurable delays between each command. The game acknowledges receipt, but entity registration may take additional game ticks.

---

## Approaches Attempted

### Approach 1: Name-Based Selection (FAILED)
```mcfunction
summon armor_stand ~ ~ ~ maricraft_anchor
execute at @e[name=maricraft_anchor] run fill ~3 ~ ~3 ~10 ~5 ~10 stone
kill @e[name=maricraft_anchor]
```

**Result:** Bedrock Edition does NOT support naming entities via summon command. The `name` selector doesn't work as expected.

---

### Approach 2: Tag-Based Selection with Radius (PARTIAL)
```mcfunction
summon armor_stand ~1 ~ ~1
tag @e[type=armor_stand,c=1,r=2] add mc_anchor
execute at @e[tag=mc_anchor] run fill ~3 ~ ~3 ~10 ~5 ~10 stone
kill @e[tag=mc_anchor]
```

**Result:** Inconsistent. Sometimes works, sometimes doesn't. The `r=2` radius was too restrictive when player drifts between commands.

---

### Approach 3: Execute Positioned for Tagging (FAILED)
```mcfunction
summon armor_stand ~1 ~ ~1
execute positioned ~1 ~ ~1 run tag @e[type=armor_stand,c=1,r=1] add mc_anchor
execute at @e[tag=mc_anchor] run fill ~3 ~ ~3 ~10 ~5 ~10 stone
kill @e[tag=mc_anchor]
```

**Result:** The `execute positioned` adds complexity without solving the core timing issue.

---

### Approach 4: Larger Radius (INCONSISTENT)
```mcfunction
summon armor_stand ~1 ~ ~1
tag @e[type=armor_stand,c=1,r=5] add mc_anchor
execute at @e[tag=mc_anchor] run setblock ~ ~2 ~ gold_block
kill @e[tag=mc_anchor]
```

**Result:** Sometimes works perfectly, sometimes no blocks appear despite armor stand spawning and being killed (proving tag was applied eventually).

---

### Approach 5: Multiple Tag Attempts (FAILED)
```mcfunction
summon armor_stand ~1 ~ ~1
tag @e[type=armor_stand,c=1,r=10] add mc_anchor
tag @e[type=armor_stand,c=1,r=10] add mc_anchor
tag @e[type=armor_stand,c=1,r=10] add mc_anchor
tag @e[type=armor_stand,c=1,r=10] add mc_anchor
tag @e[type=armor_stand,c=1,r=10] add mc_anchor
execute at @e[tag=mc_anchor] run setblock ~ ~2 ~ glowstone
kill @e[tag=mc_anchor]
```

**Result:** Still no blocks appear, even with 5 tag attempts (1.5+ seconds total delay).

---

## Observed Behavior

### What Works
| Command | Via WebSocket | Notes |
|---------|---------------|-------|
| `say <message>` | ✓ | Always works |
| `summon armor_stand ~1 ~ ~1` | ✓ | Entity appears visually |
| `kill @e[tag=mc_anchor]` | ✓ | Entity disappears (proves tag exists) |
| `setblock ~5 ~2 ~5 emerald_block` | ? | Direct placement, untested with anchor |

### What Doesn't Work (Inconsistently)
| Command | Via WebSocket | Notes |
|---------|---------------|-------|
| `tag @e[type=armor_stand,c=1,r=N] add mc_anchor` | ? | May not tag immediately |
| `execute at @e[tag=mc_anchor] run setblock` | ✗ | No blocks appear |
| `execute at @e[tag=mc_anchor] run fill` | ✗ | No blocks appear |
| `execute if entity @e[tag=mc_anchor] run say` | ✗ | No output |

### The Paradox

1. Armor stand spawns (visible in game)
2. At end of test, `kill @e[tag=mc_anchor]` successfully removes the armor stand
3. This proves the tag WAS applied at some point
4. But `execute at @e[tag=mc_anchor] run setblock` during the test places no blocks
5. **Conclusion:** Tag is applied eventually, but not visible to subsequent WebSocket commands

---

## Code Components

### Bedrock Tester Module
Location: `maricraft/bedrock_tester/`

```python
# maricraft/bedrock_tester/__init__.py
import asyncio
import json
from pathlib import Path
from datetime import datetime
import py_mcws

class BedrockTester:
    def __init__(self, port: int = 19132):
        self.port = port
        self.server = None
        self.results = []

    async def test_command(self, cmd: str) -> dict:
        """Send a command and capture result."""
        try:
            result = await self.server.command(cmd)
            return {"command": cmd, "success": True, "result": result}
        except Exception as e:
            return {"command": cmd, "success": False, "error": str(e)}

    async def test_mcfunction(self, path: Path, delay: float = 0.1):
        """Test all commands in an mcfunction file."""
        content = path.read_text(encoding='utf-8')
        lines = content.splitlines()

        results = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                result = await self.test_command(line)
                results.append(result)
                await asyncio.sleep(delay)

        return results
```

### Add Anchor Script
Location: `maricraft/tools/add_anchor.py`

```python
# Key constants (UPDATED - using name-based selection, Bedrock OLD execute syntax)
ANCHOR_NAME = "mc_anchor"

# Bedrock summon syntax: name BEFORE coordinates
SUMMON_LINE = f'summon armor_stand "{ANCHOR_NAME}" ~1 ~ ~1'

# No tag needed - using atomic naming
KILL_LINE = f'kill @e[type=armor_stand,name="{ANCHOR_NAME}"]'

# Bedrock OLD execute syntax: execute <target> <position> <command>
# NOT Java's: execute as @e[...] at @s run <command>
EXECUTE_PREFIX = f'execute @e[type=armor_stand,name="{ANCHOR_NAME}",c=1] ~ ~ ~ '
```

### Bedrock Tester Server
Location: `maricraft/bedrock_tester/server.py`

Key methods:
- `establish_anchor()` - Summons anchor, polls with testfor until queryable
- `cleanup_anchor()` - Kills anchor and removes ticking area
- `test_mcfunction_with_anchor()` - Filters anchor commands, uses Python handshake

### Current Wizard Tower Header
```mcfunction
# Maricraft: Wizard Tower (Bedrock Edition)
# Builds an elaborate mystical wizard tower

# Anchor point for building
summon armor_stand ~1 ~ ~1
tag @e[type=armor_stand,c=1,r=5] add mc_anchor

execute at @e[tag=mc_anchor] run fill ~3 ~-2 ~3 ~17 ~30 ~17 air
execute at @e[tag=mc_anchor] run fill ~3 ~-2 ~3 ~17 ~-2 ~17 cobblestone
# ... 500+ more commands ...

# Clean up anchor
kill @e[tag=mc_anchor]
```

---

## Debug Test Files

### debug_bedrock_syntax.mcfunction (Current Test)
```mcfunction
# Test Bedrock OLD execute syntax
# Format: execute <target> <position> <command>
say === TESTING BEDROCK OLD EXECUTE SYNTAX ===

# Cleanup any previous anchors
kill @e[type=armor_stand,name="mc_anchor"]

# Summon with name BEFORE coordinates (Bedrock syntax)
summon armor_stand "mc_anchor" ~1 ~ ~1

# Build using Bedrock OLD execute syntax
# Blocks appear ABOVE anchor (+3, +4, +5 Y offset)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~3 ~ gold_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~4 ~ diamond_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~5 ~ emerald_block

# Glass platform ABOVE anchor (+2 Y offset, not at ground level)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~2 ~2 ~2 ~4 ~2 ~4 glass

say === LOOK FOR: gold/diamond/emerald tower + glass platform ABOVE anchor ===

# Cleanup
kill @e[type=armor_stand,name="mc_anchor"]
```

### Latest Test Results (2025-12-06 22:20)
```
[Runner] debug_bedrock_syntax.mcfunction uses anchor pattern - using handshake
[Runner] Filtered 1 anchor commands (handled by Python)   <-- Should be 3!
[Anchor] Establishing anchor...
[Anchor] Summoned armor stand with name 'mc_anchor'
[Anchor] Ready after 1 polls (0.10s)                      <-- Handshake works!
[Anchor] Cleaning up...
[Anchor] Cleanup complete

FAILURES:
1. execute @e[...] ~ ~ ~ setblock ~ ~3 ~ gold_block     → No targets matched selector
2. execute @e[...] ~ ~ ~ setblock ~ ~4 ~ diamond_block  → No targets matched selector
3. execute @e[...] ~ ~ ~ setblock ~ ~5 ~ emerald_block  → No targets matched selector
4. execute @e[...] ~ ~ ~ fill ~2 ~2 ~2 ~4 ~2 ~4 glass   → No targets matched selector
5. kill @e[type=armor_stand,name="mc_anchor"]           → No targets matched selector
```

---

## Hypotheses

### Hypothesis 1: Entity Registration Delay
Newly summoned entities may not be immediately selectable. The armor stand exists visually but isn't registered in the entity system yet.

**Evidence Against:** Even with 1.5+ seconds of tag command delays, no improvement.

### Hypothesis 2: WebSocket Command Isolation
Each WebSocket command may run in an isolated context where entity data changes aren't visible to subsequent commands until a game tick boundary.

**Evidence For:** The `kill` command at the END works (many seconds later), but `execute at` commands in the middle don't.

### Hypothesis 3: Execute At Bug via WebSocket
The `execute at @e[...]` command may have different behavior when sent via WebSocket vs typed in chat or run from command block.

**Evidence:** Needs more testing with old Bedrock syntax.

### Hypothesis 4: Selector Evaluation Timing
The `@e[tag=mc_anchor]` selector may be evaluated before the tag is applied, even though the tag command ran earlier.

**Evidence For:** Consistent with the paradox where kill works but execute at doesn't.

---

## Research Findings

### WebSocket Limitations (from Microsoft/Community Docs)

1. **Not Officially Supported:** "Minecraft doesn't currently have plans to support websockets as a formal, external facing API"
2. **No Documentation:** "There aren't plans on publishing any formal documentation for websockets"
3. **Client Context:** "The server runs commands as the client, which means that @s refers to the player connected"

### Bedrock Execute Command Syntax

**CRITICAL DISCOVERY:** Bedrock Edition does NOT support Java's `execute as ... at @s run` syntax!

**Java Edition Syntax (DOES NOT WORK IN BEDROCK):**
```
execute as @e[...] at @s run <command>
```
Error: `Syntax error: Unexpected "@e": at "xecute as >>@e<<[type=armo"`

**Bedrock OLD Syntax (WORKS):**
```
execute @e[...] ~ ~ ~ <command>
```
This sets both WHO runs the command and WHERE it runs (at the target's position).

**Bedrock NEW Syntax (1.19.50+):**
```
execute at @e[...] run <command>
```
Only changes WHERE, not WHO. May not work correctly for anchor pattern.

---

## Next Steps to Try

### Immediate Debugging
1. **Fix filter count bug** - Only 1 command filtered when 3 expected. Check if file's summon/kill commands are passing through
2. **Add verbose logging** - Print each command before/after filtering to see what's happening
3. **Check command order** - Is file's kill command running before Python's execute commands?

### Alternative Approaches
4. **Skip file entirely** - Don't run file commands, just use Python to send the build commands directly
5. **Use ticking area** - Ensure anchor stays loaded during entire test
6. **Abandon name-based** - Go back to tag-based with longer delays

### Already Tested
- ~~Test Old Execute Syntax~~ - Using Bedrock OLD syntax now
- ~~Increase Delay~~ - Handshake works in 1 poll (0.1s)
- ~~Test Direct Setblock~~ - Works fine with `setblock ~X ~Y ~Z block`

---

## Files Modified

| File | Changes |
|------|---------|
| `maricraft/tools/add_anchor.py` | Changed to name-based selection, Bedrock OLD execute syntax |
| `maricraft/bedrock_tester/server.py` | Added handshake pattern, fixed statusCode check, fixed kill filter |
| `maricraft/resources/maricraft_behavior/functions/**/*.mcfunction` | Updated 103 files with Bedrock OLD execute syntax |
| `/tmp/test_funcs/debug_bedrock_syntax.mcfunction` | Current test file |

---

## Connection Details

```bash
# Start tester
uv run python -m maricraft.bedrock_tester --path /tmp/test_funcs --delay 0.5

# Connect from Minecraft Bedrock (in Parallels)
/connect 192.168.0.227:19132
```

**Note:** Only the LAN IP (192.168.0.227) works from Parallels VM. The Parallels vnet IP (10.211.55.2) does not connect.
