# Datapack & Behavior Pack System

> Maricraft provides pre-built function packs for both Java and Bedrock editions.

## Overview

Instead of sending raw commands, Maricraft uses datapacks (Java) and behavior packs (Bedrock) containing pre-defined mcfunction files. Each button sends a single `/function maricraft:xxx` command.

## Benefits

| Approach | Commands Per Button | Execution Time | Character Limit |
|----------|---------------------|----------------|-----------------|
| Raw Commands | 1-7 commands | ~3.5s for GOD MODE | 256 char limit |
| Function Packs | 1 command | ~100ms | No limit |

## Pack Locations

### Java Datapack

```
maricraft/resources/maricraft_datapack/
├── pack.mcmeta                    # pack_format: 48 (MC 1.21.x)
├── version.txt                    # Pack version
└── data/maricraft/function/
    ├── buffs/                     # 16 functions
    │   ├── full_heal.mcfunction
    │   ├── god_mode.mcfunction
    │   └── ...
    ├── gear/                      # 16 functions
    ├── teleport/                  # 16 functions
    └── world/                     # 16 functions
```

### Bedrock Behavior Pack

```
maricraft/resources/maricraft_behavior/
├── manifest.json                  # Pack metadata
├── pack_icon.png                  # Pack icon
└── functions/
    ├── buffs/
    ├── gear/
    ├── teleport/
    └── world/
```

## Installation Logic

The `datapack.py` module handles pack installation:

### 1. Edition Detection

```python
def is_bedrock_running():
    """Check if Bedrock Edition is running."""
    # Uses tasklist to find Minecraft.Windows.exe
    output = subprocess.check_output(['tasklist'], ...)
    return 'Minecraft.Windows.exe' in output
```

### 2. World Discovery

**Java Edition:**
```
%APPDATA%/.minecraft/saves/
├── World1/
│   └── datapacks/     <- Install here
├── World2/
└── ...
```

**Bedrock Edition (Microsoft Store):**
```
%LOCALAPPDATA%/Packages/Microsoft.MinecraftUWP_*/
└── LocalState/games/com.mojang/
    ├── minecraftWorlds/
    │   ├── world_abc123/
    │   │   └── behavior_packs/  <- Install here
    │   └── ...
    └── development_behavior_packs/  <- Alternative location
```

**Bedrock Edition (Xbox App / GDK):**
```
%LOCALAPPDATA%/Packages/Microsoft.MinecraftWindowsBeta_*/
└── LocalState/games/com.mojang/
    └── ...
```

### 3. Pack Copying

```python
def install_datapack(world_path: Path) -> bool:
    """Install datapack to a Java world."""
    datapacks_dir = world_path / "datapacks"
    datapacks_dir.mkdir(exist_ok=True)

    # Copy entire datapack folder
    src = RESOURCES / "maricraft_datapack"
    dst = datapacks_dir / "maricraft_datapack"
    shutil.copytree(src, dst, dirs_exist_ok=True)

    return True
```

### 4. Validation

Before installation, packs are validated:
- `pack.mcmeta` exists and is valid JSON (Java)
- `manifest.json` exists and has correct format (Bedrock)
- Required function files present

## Path Detection Logic

```python
def find_minecraft_worlds() -> list[WorldInfo]:
    """Find all Minecraft worlds on this system."""
    worlds = []

    # Java paths
    java_saves = Path.home() / "AppData/Roaming/.minecraft/saves"
    if java_saves.exists():
        for world in java_saves.iterdir():
            if (world / "level.dat").exists():
                worlds.append(WorldInfo(
                    path=world,
                    name=world.name,
                    edition="java"
                ))

    # Bedrock paths (UWP)
    uwp_pattern = Path.home() / "AppData/Local/Packages/Microsoft.MinecraftUWP_*"
    for pkg in uwp_pattern.parent.glob(uwp_pattern.name):
        worlds_dir = pkg / "LocalState/games/com.mojang/minecraftWorlds"
        if worlds_dir.exists():
            for world in worlds_dir.iterdir():
                if (world / "level.dat").exists():
                    # Read world name from levelname.txt
                    name = read_levelname(world)
                    worlds.append(WorldInfo(
                        path=world,
                        name=name,
                        edition="bedrock"
                    ))

    return worlds
```

## mcfunction File Format

### Java Edition

```mcfunction
# Maricraft: Full Heal
# Restores player to full health instantly

effect give @s instant_health 1 255
effect clear @s poison
effect clear @s wither
```

### Bedrock Edition

```mcfunction
# Maricraft: Full Heal (Bedrock)
# Note: Bedrock uses different syntax

effect @s instant_health 1 255
effect @s clear
```

**Key Differences:**
| Feature | Java | Bedrock |
|---------|------|---------|
| Effect give | `effect give @s ...` | `effect @s ...` |
| Clear effects | `effect clear @s poison` | `effect @s clear` |
| Execute syntax | `execute as @e at @s run` | `execute @e ~ ~ ~ ` |
| NBT data | Supported | Not supported |

## Troubleshooting

### "World not found"
- Ensure Minecraft is installed
- Create at least one world first
- Check if using custom launcher (paths may differ)

### "Permission denied"
- Close Minecraft before installing
- Run as administrator on Windows
- Check antivirus isn't blocking

### "Datapack not loading"
- In-game: Run `/reload`
- Check pack_format matches Minecraft version
- Verify no syntax errors in mcfunction files

### Bedrock pack not showing
- May need to activate in world settings
- Check manifest.json format
- Ensure correct UUID format

## Related Documentation

- [1.21.1 Command Playbook](../1.21.1-command-playbook.md) - Command syntax
- [Java/Bedrock Parity](../1.20-and-up-syntax_doc.md) - Edition differences
- [TECHNICAL.md](../../TECHNICAL.md) - Deep technical docs
