"""Datapack management for Maricraft."""

from __future__ import annotations

import datetime
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .commands import CommandButton

# Debug logging for Bedrock behavior pack troubleshooting
_DEBUG_LOG_PATH: Optional[Path] = None


def set_debug_log_path(path: Path) -> None:
    """Set the path for debug logging."""
    global _DEBUG_LOG_PATH
    _DEBUG_LOG_PATH = path
    # Clear existing log
    if path.exists():
        path.unlink()
    debug_log("=== Bedrock Debug Log Started ===")


def debug_log(message: str) -> None:
    """Write a debug message to log file and console."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(f"DEBUG: {message}")
    if _DEBUG_LOG_PATH:
        try:
            with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except Exception as e:
            print(f"DEBUG LOG ERROR: {e}")

# Datapack metadata
DATAPACK_NAME = "maricraft_datapack"
PACK_DESCRIPTION = "Maricraft Helper - Kid-friendly Minecraft commands"

# Version-specific pack_format mapping
# https://minecraft.wiki/w/Pack_format
PACK_FORMAT_MAP = {
    "1.20": 15,    # 1.20-1.20.1
    "1.20.1": 15,
    "1.20.2": 18,
    "1.20.3": 26,
    "1.20.4": 26,
    "1.20.5": 41,
    "1.20.6": 41,
    "1.21": 48,
    "1.21.1": 48,
    "1.21.2": 57,
    "1.21.3": 57,
    "1.21.4": 61,
}

# Default for unknown versions
DEFAULT_PACK_FORMAT = 15  # Conservative default for 1.20.x


def get_pack_format_for_version(mc_version: str) -> int:
    """Get the correct pack_format for a Minecraft version.

    Args:
        mc_version: Minecraft version string (e.g. "1.20.1", "1.21")

    Returns:
        The pack_format number for that version.
    """
    # Try exact match first
    if mc_version in PACK_FORMAT_MAP:
        return PACK_FORMAT_MAP[mc_version]

    # Try major.minor match (e.g., "1.20.1" -> try "1.20")
    parts = mc_version.split(".")
    if len(parts) >= 2:
        major_minor = f"{parts[0]}.{parts[1]}"
        if major_minor in PACK_FORMAT_MAP:
            return PACK_FORMAT_MAP[major_minor]

    return DEFAULT_PACK_FORMAT


def is_version_1_21_or_later(mc_version: str) -> bool:
    """Check if a Minecraft version is 1.21 or later.

    1.21+ uses different syntax:
    - folder: 'function' (singular) vs 'functions' (plural)
    - components: [enchantments={...}] vs {Enchantments:[...]}
    """
    try:
        parts = mc_version.split(".")
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        return major > 1 or (major == 1 and minor >= 21)
    except (ValueError, IndexError):
        return False  # Default to 1.20.x behavior


def get_functions_folder_name(mc_version: str) -> str:
    """Get the correct functions folder name for a Minecraft version.

    Args:
        mc_version: Minecraft version string

    Returns:
        'function' for 1.21+, 'functions' for 1.20.x
    """
    return "function" if is_version_1_21_or_later(mc_version) else "functions"


def detect_minecraft_version(instance_path: Path) -> Optional[str]:
    """Detect Minecraft version from a CurseForge or vanilla instance.

    Checks for:
    1. CurseForge minecraftinstance.json
    2. CurseForge instance.json
    3. Vanilla launcher_profiles.json (future)

    Args:
        instance_path: Path to the instance folder (parent of 'saves')

    Returns:
        Version string like "1.20.1" or None if not detected.
    """
    # For CurseForge: instance_path should be the instance folder
    # (e.g., C:\Users\X\CurseForge\Minecraft\Instances\ATM9)

    # Check for minecraftinstance.json (CurseForge standard)
    instance_json = instance_path / "minecraftinstance.json"
    if instance_json.exists():
        try:
            data = json.loads(instance_json.read_text(encoding="utf-8"))
            # CurseForge format: {"baseModLoader": {"minecraftVersion": "1.20.1"}}
            if "baseModLoader" in data and "minecraftVersion" in data["baseModLoader"]:
                return data["baseModLoader"]["minecraftVersion"]
            # Alternative format
            if "gameVersion" in data:
                return data["gameVersion"]
        except (json.JSONDecodeError, KeyError):
            pass

    # Check for instance.json (alternative CurseForge format)
    alt_json = instance_path / "instance.json"
    if alt_json.exists():
        try:
            data = json.loads(alt_json.read_text(encoding="utf-8"))
            if "gameVersion" in data:
                return data["gameVersion"]
        except (json.JSONDecodeError, KeyError):
            pass

    return None


def detect_version_for_saves_path(saves_path: Path) -> Optional[str]:
    """Detect Minecraft version from a saves path.

    Args:
        saves_path: Path to the 'saves' folder

    Returns:
        Version string or None if not detected.
    """
    # Instance folder is parent of saves
    instance_path = saves_path.parent
    return detect_minecraft_version(instance_path)


def get_bundled_datapack_path() -> Optional[Path]:
    """Get path to the bundled datapack in the resources folder.

    Works both in development and PyInstaller builds.
    """
    # When running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)  # type: ignore
    else:
        # Development mode - relative to this file
        base_path = Path(__file__).parent

    datapack_path = base_path / "resources" / DATAPACK_NAME
    if datapack_path.exists():
        return datapack_path
    return None


def get_minecraft_saves_path() -> Optional[Path]:
    """Get the Minecraft saves directory path on Windows."""
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return None
    mc_path = Path(appdata) / ".minecraft" / "saves"
    return mc_path if mc_path.exists() else None


def get_all_bedrock_worlds_paths() -> List[Path]:
    """Get all Bedrock Edition worlds directories on Windows.

    Bedrock Edition can be installed in multiple locations:
    1. Xbox App / Launcher GDK: %APPDATA%/Minecraft Bedrock/Users/{UUID}/games/com.mojang/minecraftWorlds
    2. Microsoft Store/UWP: %LOCALAPPDATA%/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/com.mojang/minecraftWorlds

    Returns:
        List of existing worlds directory paths.
    """
    paths = []

    # -------------------------------------------------------------------------
    # 1. Xbox App / Launcher GDK Path (New Architecture)
    # Structure: %APPDATA%\Minecraft Bedrock\Users\{UUID}\games\com.mojang\minecraftWorlds
    # -------------------------------------------------------------------------
    appdata = os.environ.get("APPDATA")
    if appdata:
        base_bedrock = Path(appdata) / "Minecraft Bedrock"

        # Check inside 'Users' for specific account folders (GDK structure)
        users_dir = base_bedrock / "Users"
        if users_dir.exists():
            for user_folder in users_dir.iterdir():
                if user_folder.is_dir():
                    # Check for the worlds folder deep inside
                    user_worlds = user_folder / "games" / "com.mojang" / "minecraftWorlds"
                    if user_worlds.exists():
                        paths.append(user_worlds)

        # Fallback for older GDK installs (direct in base)
        direct_path = base_bedrock / "games" / "com.mojang" / "minecraftWorlds"
        if direct_path.exists() and direct_path not in paths:
            paths.append(direct_path)

    # -------------------------------------------------------------------------
    # 2. Microsoft Store / UWP Path (Legacy Architecture)
    # Structure: %LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP...\LocalState\...
    # -------------------------------------------------------------------------
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        uwp_path = (
            Path(localappdata) / "Packages" /
            "Microsoft.MinecraftUWP_8wekyb3d8bbwe" /
            "LocalState" / "games" / "com.mojang" / "minecraftWorlds"
        )
        if uwp_path.exists() and uwp_path not in paths:
            paths.append(uwp_path)

    return paths


def get_bedrock_worlds_path() -> Optional[Path]:
    """Get Bedrock Edition worlds directory on Windows.

    Returns the first found path for backwards compatibility.
    Use get_all_bedrock_worlds_paths() for all installations.
    """
    paths = get_all_bedrock_worlds_paths()
    return paths[0] if paths else None


def list_bedrock_worlds() -> List[Tuple[str, Path]]:
    """List Bedrock Edition worlds with their display names.

    Bedrock worlds have random folder names, but the actual world name
    is stored in a levelname.txt file inside each folder.

    Checks ALL known Bedrock installation paths.

    Returns:
        List of (world_name, world_path) tuples, sorted alphabetically.
    """
    all_paths = get_all_bedrock_worlds_paths()
    if not all_paths:
        return []

    worlds = []
    seen_paths = set()  # Avoid duplicates if somehow paths overlap

    for worlds_path in all_paths:
        for folder in worlds_path.iterdir():
            if folder.is_dir() and folder not in seen_paths:
                seen_paths.add(folder)
                levelname_file = folder / "levelname.txt"
                if levelname_file.exists():
                    try:
                        world_name = levelname_file.read_text(encoding="utf-8").strip()
                        worlds.append((world_name, folder))
                    except Exception:
                        # Fallback to folder name if levelname.txt is unreadable
                        worlds.append((folder.name, folder))

    return sorted(worlds, key=lambda x: x[0].lower())


def get_all_minecraft_instances() -> List[Tuple[str, Path, Optional[str]]]:
    """Find all Minecraft installations (vanilla + CurseForge).

    Scans common locations for Minecraft instances and their saves folders.
    Also detects the Minecraft version for each instance.

    Returns:
        List of (instance_name, saves_path, version) tuples, sorted by name.
        version may be None if not detected.
    """
    instances = []
    appdata = os.environ.get("APPDATA")

    # 1. Vanilla Minecraft
    if appdata:
        vanilla = Path(appdata) / ".minecraft" / "saves"
        if vanilla.exists():
            # Vanilla doesn't have a single version - could have multiple
            instances.append(("Vanilla Minecraft", vanilla, None))

    # 2. CurseForge instances (new location)
    # Common path: C:\Users\<user>\CurseForge\Minecraft\Instances\
    curseforge_base = Path.home() / "CurseForge" / "Minecraft" / "Instances"
    if curseforge_base.exists():
        for instance_dir in curseforge_base.iterdir():
            if instance_dir.is_dir():
                saves = instance_dir / "saves"
                if saves.exists():
                    version = detect_minecraft_version(instance_dir)
                    instances.append((f"CurseForge: {instance_dir.name}", saves, version))

    # 3. Alternative CurseForge location (older installations)
    if appdata:
        alt_curseforge = Path(appdata) / ".curseforge" / "minecraft" / "Instances"
        if alt_curseforge.exists():
            for instance_dir in alt_curseforge.iterdir():
                if instance_dir.is_dir():
                    saves = instance_dir / "saves"
                    if saves.exists():
                        version = detect_minecraft_version(instance_dir)
                        instances.append((f"CurseForge: {instance_dir.name}", saves, version))

    # 4. Bedrock Edition (check all installation paths)
    bedrock_paths = get_all_bedrock_worlds_paths()
    for i, bedrock_worlds in enumerate(bedrock_paths):
        # Use "bedrock" as special version identifier
        if len(bedrock_paths) == 1:
            name = "Bedrock Edition"
        else:
            # Multiple installations - add path hint
            if "Microsoft.MinecraftUWP" in str(bedrock_worlds):
                name = "Bedrock Edition (Microsoft Store)"
            elif "Minecraft Bedrock" in str(bedrock_worlds):
                name = "Bedrock Edition (Xbox/Launcher)"
            else:
                name = f"Bedrock Edition ({i + 1})"
        instances.append((name, bedrock_worlds, "bedrock"))

    # Sort by instance name (case-insensitive)
    return sorted(instances, key=lambda x: x[0].lower())


def list_worlds(saves_path: Optional[Path] = None) -> List[Tuple[str, Path]]:
    """List all Minecraft worlds in the saves directory.

    Args:
        saves_path: Path to saves folder. If None, uses default location.

    Returns:
        List of (world_name, world_path) tuples, sorted alphabetically.
    """
    if saves_path is None:
        saves_path = get_minecraft_saves_path()

    if saves_path is None or not saves_path.exists():
        return []

    worlds = []
    for item in saves_path.iterdir():
        if item.is_dir() and (item / "level.dat").exists():
            worlds.append((item.name, item))
    return sorted(worlds, key=lambda x: x[0].lower())


def is_datapack_installed(world_path: Path) -> bool:
    """Check if Maricraft datapack is installed in a world."""
    datapack_path = world_path / "datapacks" / DATAPACK_NAME / "pack.mcmeta"
    return datapack_path.exists()


def get_datapack_version(world_path: Path) -> Optional[str]:
    """Get the installed datapack version from a world."""
    version_file = world_path / "datapacks" / DATAPACK_NAME / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def check_any_world_has_datapack() -> bool:
    """Check if any Minecraft world has the datapack installed.

    Checks across all instances (vanilla + CurseForge).
    """
    for _instance_name, saves_path, _version in get_all_minecraft_instances():
        for _world_name, world_path in list_worlds(saves_path):
            if is_datapack_installed(world_path):
                return True
    return False


def convert_nbt_to_components(command: str) -> str:
    """Convert 1.20.x NBT syntax to 1.21+ component syntax.

    Examples:
    - {Enchantments:[{id:"sharpness",lvl:5}]} -> [enchantments={levels:{sharpness:5}}]
    - {Unbreakable:1b} -> [unbreakable={}]

    Args:
        command: A Minecraft command using 1.20.x NBT syntax.

    Returns:
        The same command with 1.21+ component syntax.
    """
    # Pattern for give commands with NBT: give @s item{NBT} count
    # Match: give @s item_name{...} count
    give_pattern = r'(give\s+@\w+\s+)(\w+)\{([^}]+)\}(\s+\d+)?'

    def convert_give_match(match):
        prefix = match.group(1)  # "give @s "
        item = match.group(2)    # "netherite_sword"
        nbt = match.group(3)     # "Enchantments:[...],Unbreakable:1b"
        count = match.group(4) or ""  # " 1"

        components = []

        # Convert Unbreakable:1b -> unbreakable={}
        if "Unbreakable:1b" in nbt:
            components.append("unbreakable={}")
            nbt = nbt.replace("Unbreakable:1b", "").strip(",")

        # Convert Enchantments:[{id:"minecraft:xxx",lvl:N},...] -> enchantments={levels:{xxx:N,...}}
        ench_match = re.search(r'Enchantments:\[(.*?)\]', nbt)
        if ench_match:
            ench_data = ench_match.group(1)
            # Parse each enchantment
            levels = {}
            # Match {id:"minecraft:sharpness",lvl:5} or {id:"sharpness",lvl:5}
            for ench in re.finditer(r'\{id:"(?:minecraft:)?(\w+)",lvl:(\d+)\}', ench_data):
                ench_name = ench.group(1)
                ench_level = ench.group(2)
                levels[ench_name] = int(ench_level)

            if levels:
                levels_str = ",".join(f"{k}:{v}" for k, v in levels.items())
                components.append(f"enchantments={{levels:{{{levels_str}}}}}")

        if components:
            components_str = "[" + ",".join(components) + "]"
            return f"{prefix}{item}{components_str}{count}"
        else:
            return match.group(0)  # Return unchanged if no conversion needed

    # Apply conversion
    result = re.sub(give_pattern, convert_give_match, command)
    return result


def convert_mcfunction_for_version(content: str, mc_version: str) -> str:
    """Convert mcfunction file content for a specific Minecraft version.

    If mc_version is 1.21+, converts NBT syntax to component syntax.

    Args:
        content: The mcfunction file content (1.20.x syntax).
        mc_version: Target Minecraft version.

    Returns:
        Converted content appropriate for the target version.
    """
    if not is_version_1_21_or_later(mc_version):
        # 1.20.x - no conversion needed
        return content

    # 1.21+ - convert each line
    lines = content.split("\n")
    converted_lines = []
    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            converted_lines.append(line)
        else:
            converted_lines.append(convert_nbt_to_components(line))
    return "\n".join(converted_lines)


def install_datapack(world_path: Path, source_path: Optional[Path] = None,
                     mc_version: Optional[str] = None) -> bool:
    """Install/update the datapack in a world.

    Args:
        world_path: Path to the Minecraft world folder.
        source_path: Path to datapack folder. If None, uses bundled datapack.
        mc_version: Target Minecraft version. If None, uses 1.20.x defaults.

    Returns:
        True if installation succeeded.
    """
    if source_path is None:
        source_path = get_bundled_datapack_path()

    if source_path is None or not source_path.exists():
        return False

    # Default to 1.20.x if no version specified
    if mc_version is None:
        mc_version = "1.20.1"

    dest = world_path / "datapacks" / DATAPACK_NAME
    try:
        # Create datapacks folder if it doesn't exist
        dest.parent.mkdir(parents=True, exist_ok=True)

        # Remove existing datapack if present
        if dest.exists():
            shutil.rmtree(dest)

        # Copy to temp location first for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_datapack = Path(temp_dir) / DATAPACK_NAME
            shutil.copytree(source_path, temp_datapack)

            # Update pack.mcmeta with correct pack_format
            pack_format = get_pack_format_for_version(mc_version)
            pack_mcmeta = {
                "pack": {
                    "pack_format": pack_format,
                    "description": PACK_DESCRIPTION
                }
            }
            (temp_datapack / "pack.mcmeta").write_text(
                json.dumps(pack_mcmeta, indent=2)
            )

            # Bundled datapack uses 1.20.x syntax with 'functions' folder
            functions_src = temp_datapack / "data" / "maricraft" / "functions"

            if is_version_1_21_or_later(mc_version):
                # 1.21+: rename functions -> function, convert syntax
                function_dst = temp_datapack / "data" / "maricraft" / "function"

                if functions_src.exists():
                    # Convert each mcfunction file and copy to new location
                    function_dst.mkdir(parents=True, exist_ok=True)
                    for mcfunc in functions_src.rglob("*.mcfunction"):
                        rel_path = mcfunc.relative_to(functions_src)
                        dst_file = function_dst / rel_path
                        dst_file.parent.mkdir(parents=True, exist_ok=True)

                        content = mcfunc.read_text(encoding="utf-8")
                        converted = convert_mcfunction_for_version(content, mc_version)
                        dst_file.write_text(converted, encoding="utf-8")

                    # Remove old functions folder
                    shutil.rmtree(functions_src)

            # Copy processed datapack to destination
            shutil.copytree(temp_datapack, dest)

        return True
    except Exception:
        return False


def install_datapack_to_worlds(world_paths: List[Path], source_path: Optional[Path] = None,
                               mc_version: Optional[str] = None) -> Tuple[int, int]:
    """Install datapack to multiple worlds.

    Args:
        world_paths: List of world folder paths.
        source_path: Path to datapack folder. If None, uses bundled datapack.
        mc_version: Target Minecraft version. If None, uses 1.20.x defaults.

    Returns:
        Tuple of (success_count, failure_count)
    """
    success = 0
    failure = 0
    for world_path in world_paths:
        if install_datapack(world_path, source_path, mc_version):
            success += 1
        else:
            failure += 1
    return success, failure


def generate_datapack(output_path: Path, buttons: List["CommandButton"], version: str,
                      mc_version: Optional[str] = None) -> Path:
    """Generate the datapack folder structure with all mcfunction files.

    Args:
        output_path: Directory to create datapack in.
        buttons: List of CommandButton objects with function_id set.
        version: Version string for version.txt.
        mc_version: Target Minecraft version. If None, uses 1.20.x defaults.

    Returns:
        Path to the created datapack folder.
    """
    if mc_version is None:
        mc_version = "1.20.1"

    # Create base structure
    datapack_dir = output_path / DATAPACK_NAME
    folder_name = get_functions_folder_name(mc_version)
    data_dir = datapack_dir / "data" / "maricraft" / folder_name

    # Create category directories
    for category in ["buffs", "gear", "teleport", "world"]:
        (data_dir / category).mkdir(parents=True, exist_ok=True)

    # Write pack.mcmeta with correct pack_format
    pack_format = get_pack_format_for_version(mc_version)
    pack_mcmeta = {
        "pack": {
            "pack_format": pack_format,
            "description": PACK_DESCRIPTION
        }
    }
    (datapack_dir / "pack.mcmeta").write_text(json.dumps(pack_mcmeta, indent=2))

    # Write version file
    (datapack_dir / "version.txt").write_text(version)

    # Generate mcfunction files from buttons
    for button in buttons:
        if not button.function_id:
            continue

        # Parse function_id: "maricraft:buffs/god_mode" -> "buffs/god_mode.mcfunction"
        # Handle any namespace (strip everything before and including ':')
        func_id = button.function_id
        if ":" in func_id:
            func_id = func_id.split(":", 1)[1]  # Take part after ':'
        func_path = func_id + ".mcfunction"
        file_path = data_dir / func_path

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write commands (strip leading / if present)
        content = f"# Maricraft: {button.name}\n"
        for cmd in button.commands:
            clean_cmd = cmd.lstrip("/")
            content += f"{clean_cmd}\n"

        file_path.write_text(content)

    return datapack_dir


def get_bundled_datapack_version() -> str:
    """Get version from bundled datapack.

    Returns:
        Version string like "2.0.0", or "0.0.0" if not found.
    """
    datapack_path = get_bundled_datapack_path()
    if datapack_path is None:
        return "0.0.0"

    version_file = datapack_path / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"


def _compare_versions(v1: str, v2: str) -> int:
    """Compare two semantic version strings.

    Args:
        v1: First version string (e.g., "1.0.0")
        v2: Second version string (e.g., "2.0.0")

    Returns:
        -1 if v1 < v2, 0 if equal, 1 if v1 > v2
    """
    try:
        parts1 = [int(x) for x in v1.split('.')]
        parts2 = [int(x) for x in v2.split('.')]
    except ValueError:
        # If parsing fails, treat as needing update
        return -1

    # Pad shorter version with zeros
    while len(parts1) < len(parts2):
        parts1.append(0)
    while len(parts2) < len(parts1):
        parts2.append(0)

    for p1, p2 in zip(parts1, parts2):
        if p1 < p2:
            return -1
        if p1 > p2:
            return 1
    return 0


def needs_datapack_update(world_path: Path) -> bool:
    """Check if a world needs datapack install/update.

    Args:
        world_path: Path to the Minecraft world folder.

    Returns:
        True if datapack should be installed or updated.
    """
    installed = get_datapack_version(world_path)
    bundled = get_bundled_datapack_version()

    if not installed:
        return True  # Not installed

    return _compare_versions(installed, bundled) < 0


def auto_install_all_datapacks() -> dict:
    """Automatically install/update datapack to all worlds that need it.

    Scans all Minecraft instances (vanilla + CurseForge + Bedrock) and installs
    or updates the datapack/behavior pack in any world that doesn't have it or has
    an older version.

    Returns:
        Dict with keys:
            - installed: list of world names where pack was newly installed
            - updated: list of world names where pack was updated
            - failed: list of (world_name, error) tuples
            - skipped: list of world names already up to date
    """
    results = {"installed": [], "updated": [], "failed": [], "skipped": []}

    for instance_name, saves_path, mc_version in get_all_minecraft_instances():
        is_bedrock = mc_version == "bedrock"

        # Get worlds list - Bedrock uses different detection
        if is_bedrock:
            worlds = list_bedrock_worlds()
        else:
            worlds = list_worlds(saves_path)

        for world_name, world_path in worlds:
            try:
                if is_bedrock:
                    # Bedrock: use behavior pack
                    if not needs_behavior_pack_update(world_path):
                        results["skipped"].append(world_name)
                        continue

                    was_installed = is_behavior_pack_installed(world_path)

                    if install_behavior_pack(world_path):
                        if was_installed:
                            results["updated"].append(world_name)
                        else:
                            results["installed"].append(world_name)
                    else:
                        results["failed"].append((world_name, "Behavior pack installation failed"))
                else:
                    # Java: use datapack
                    if not needs_datapack_update(world_path):
                        results["skipped"].append(world_name)
                        continue

                    was_installed = is_datapack_installed(world_path)

                    if install_datapack(world_path, mc_version=mc_version):
                        if was_installed:
                            results["updated"].append(world_name)
                        else:
                            results["installed"].append(world_name)
                    else:
                        results["failed"].append((world_name, "Datapack installation failed"))
            except Exception as e:
                results["failed"].append((world_name, str(e)))

    return results


def get_all_buttons() -> List["CommandButton"]:
    """Get all buttons from all categories.

    Returns:
        Flat list of all CommandButton objects.
    """
    from .commands import ALL_CATEGORIES

    buttons = []
    for category in ALL_CATEGORIES:
        buttons.extend(category.buttons)
    return buttons


# === BEDROCK EDITION SUPPORT ===

BEHAVIOR_PACK_NAME = "maricraft_behavior"
BEHAVIOR_PACK_DESCRIPTION = "Maricraft Helper - Kid-friendly Minecraft commands"

# Fixed UUIDs for the behavior pack (Bedrock requires UUIDs)
BEHAVIOR_PACK_UUID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
BEHAVIOR_PACK_MODULE_UUID = "b2c3d4e5-f6a7-8901-bcde-f12345678901"


def get_bundled_behavior_pack_path() -> Optional[Path]:
    """Get path to the bundled behavior pack in the resources folder.

    Works both in development and PyInstaller builds.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)  # type: ignore
    else:
        base_path = Path(__file__).parent

    pack_path = base_path / "resources" / BEHAVIOR_PACK_NAME
    if pack_path.exists():
        return pack_path
    return None


def get_bundled_behavior_pack_version() -> str:
    """Get version from bundled behavior pack."""
    pack_path = get_bundled_behavior_pack_path()
    if pack_path is None:
        return "0.0.0"

    version_file = pack_path / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"


def is_behavior_pack_installed(world_path: Path) -> bool:
    """Check if Maricraft behavior pack is installed in a Bedrock world."""
    pack_path = world_path / "behavior_packs" / BEHAVIOR_PACK_NAME / "manifest.json"
    return pack_path.exists()


def get_behavior_pack_version(world_path: Path) -> Optional[str]:
    """Get the installed behavior pack version from a Bedrock world."""
    version_file = world_path / "behavior_packs" / BEHAVIOR_PACK_NAME / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def needs_behavior_pack_update(world_path: Path) -> bool:
    """Check if a Bedrock world needs behavior pack install/update."""
    installed = get_behavior_pack_version(world_path)
    bundled = get_bundled_behavior_pack_version()

    if not installed:
        return True

    return _compare_versions(installed, bundled) < 0


def generate_behavior_pack(output_path: Path, buttons: List["CommandButton"], version: str) -> Path:
    """Generate Bedrock behavior pack with mcfunction files.

    Args:
        output_path: Directory to create behavior pack in.
        buttons: List of CommandButton objects with function_id set.
        version: Version string for version.txt.

    Returns:
        Path to the created behavior pack folder.
    """
    pack_dir = output_path / BEHAVIOR_PACK_NAME
    functions_dir = pack_dir / "functions"

    # Parse version for manifest
    try:
        version_parts = [int(x) for x in version.split(".")[:3]]
        while len(version_parts) < 3:
            version_parts.append(0)
    except ValueError:
        version_parts = [1, 0, 0]

    # Create manifest.json (Bedrock format)
    manifest = {
        "format_version": 2,
        "header": {
            "name": "Maricraft Helper",
            "description": BEHAVIOR_PACK_DESCRIPTION,
            "uuid": BEHAVIOR_PACK_UUID,
            "version": version_parts,
            "min_engine_version": [1, 20, 0]
        },
        "modules": [{
            "type": "data",
            "uuid": BEHAVIOR_PACK_MODULE_UUID,
            "version": version_parts
        }]
    }

    pack_dir.mkdir(parents=True, exist_ok=True)
    (pack_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (pack_dir / "version.txt").write_text(version)

    # Create mcfunction files using bedrock_commands
    for button in buttons:
        if not button.function_id:
            continue

        # Parse function_id: "maricraft:buffs/god_mode" -> "buffs/god_mode"
        func_id = button.function_id
        if ":" in func_id:
            func_id = func_id.split(":", 1)[1]

        func_path = functions_dir / (func_id + ".mcfunction")
        func_path.parent.mkdir(parents=True, exist_ok=True)

        # Use bedrock_commands if available, otherwise fall back to commands
        cmds = button.bedrock_commands if button.bedrock_commands else button.commands
        content = f"# Maricraft: {button.name}\n"
        for cmd in cmds:
            content += cmd.lstrip("/") + "\n"

        func_path.write_text(content)

    return pack_dir


def install_behavior_pack(world_path: Path, source_path: Optional[Path] = None) -> bool:
    """Install/update the behavior pack in a Bedrock world.

    Also updates world_behavior_packs.json to enable the pack.

    Args:
        world_path: Path to the Bedrock world folder.
        source_path: Path to behavior pack folder. If None, uses bundled pack.

    Returns:
        True if installation succeeded.
    """
    debug_log(f"=== Installing behavior pack to: {world_path} ===")

    if source_path is None:
        source_path = get_bundled_behavior_pack_path()

    if source_path is None or not source_path.exists():
        debug_log(f"ERROR: No bundled behavior pack found. source_path={source_path}")
        return False

    debug_log(f"Source pack: {source_path}")

    # Log all files in source pack
    debug_log("--- Source pack contents ---")
    source_files = list(source_path.rglob("*"))
    for f in sorted(source_files):
        if f.is_file():
            rel = f.relative_to(source_path)
            size = f.stat().st_size
            debug_log(f"  {rel} ({size} bytes)")

    # Log source manifest.json
    source_manifest = source_path / "manifest.json"
    if source_manifest.exists():
        debug_log(f"--- Source manifest.json ---")
        debug_log(source_manifest.read_text(encoding="utf-8"))

    # Log source version.txt
    source_version = source_path / "version.txt"
    if source_version.exists():
        debug_log(f"Source version.txt: {source_version.read_text(encoding='utf-8').strip()}")

    dest = world_path / "behavior_packs" / BEHAVIOR_PACK_NAME
    debug_log(f"Destination: {dest}")

    try:
        # Create behavior_packs folder if it doesn't exist
        dest.parent.mkdir(parents=True, exist_ok=True)
        debug_log(f"Created parent dir: {dest.parent}")

        # Remove existing pack if present
        if dest.exists():
            debug_log(f"Removing existing pack at {dest}")
            shutil.rmtree(dest)

        # Copy behavior pack
        debug_log("Copying behavior pack...")
        shutil.copytree(source_path, dest)
        debug_log("Copy complete!")

        # Verify copied files
        debug_log("--- Installed pack contents ---")
        installed_files = list(dest.rglob("*"))
        mcfunction_count = 0
        for f in sorted(installed_files):
            if f.is_file():
                rel = f.relative_to(dest)
                size = f.stat().st_size
                debug_log(f"  {rel} ({size} bytes)")
                if str(rel).endswith(".mcfunction"):
                    mcfunction_count += 1
        debug_log(f"Total .mcfunction files installed: {mcfunction_count}")

        # Log installed manifest.json
        installed_manifest = dest / "manifest.json"
        if installed_manifest.exists():
            debug_log(f"--- Installed manifest.json ---")
            debug_log(installed_manifest.read_text(encoding="utf-8"))

        # Log a sample function to verify content
        test_func = dest / "functions" / "test.mcfunction"
        if test_func.exists():
            debug_log(f"--- Sample: test.mcfunction ---")
            debug_log(test_func.read_text(encoding="utf-8"))

        buffs_func = dest / "functions" / "buffs" / "super_regen.mcfunction"
        if buffs_func.exists():
            debug_log(f"--- Sample: buffs/super_regen.mcfunction ---")
            debug_log(buffs_func.read_text(encoding="utf-8"))

        # Enable the pack in world_behavior_packs.json
        _enable_behavior_pack_in_world(world_path)

        debug_log("=== Installation successful ===")
        return True
    except PermissionError as e:
        debug_log(f"ERROR: Permission denied for {world_path}: {e}")
        return False
    except OSError as e:
        debug_log(f"ERROR: OS error for {world_path}: {e}")
        return False
    except Exception as e:
        debug_log(f"ERROR: Unexpected error for {world_path}: {type(e).__name__}: {e}")
        import traceback
        debug_log(traceback.format_exc())
        return False


def _enable_behavior_pack_in_world(world_path: Path) -> None:
    """Add Maricraft behavior pack to world_behavior_packs.json.

    This file tells Bedrock which behavior packs are enabled for the world.
    """
    debug_log("--- Enabling behavior pack in world ---")
    packs_file = world_path / "world_behavior_packs.json"
    debug_log(f"world_behavior_packs.json path: {packs_file}")

    # Read manifest to get version
    manifest_path = world_path / "behavior_packs" / BEHAVIOR_PACK_NAME / "manifest.json"
    debug_log(f"Reading manifest from: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        version = manifest["header"]["version"]
        debug_log(f"Manifest version: {version}")
    except Exception as e:
        version = [2, 0, 0]
        debug_log(f"WARNING: Could not read manifest, using default version: {e}")

    pack_entry = {
        "pack_id": BEHAVIOR_PACK_UUID,
        "version": version
    }
    debug_log(f"Pack entry to add: {pack_entry}")

    # Read existing packs or start fresh
    packs = []
    if packs_file.exists():
        debug_log("world_behavior_packs.json exists, reading...")
        try:
            content = packs_file.read_text(encoding="utf-8")
            debug_log(f"Existing content: {content}")
            packs = json.loads(content)
            if not isinstance(packs, list):
                debug_log(f"WARNING: Content was not a list, resetting")
                packs = []
        except Exception as e:
            debug_log(f"WARNING: Could not read existing packs file: {e}")
            packs = []
    else:
        debug_log("world_behavior_packs.json does not exist, will create new")

    # Remove existing Maricraft entry if present
    old_len = len(packs)
    packs = [p for p in packs if p.get("pack_id") != BEHAVIOR_PACK_UUID]
    if len(packs) < old_len:
        debug_log(f"Removed existing Maricraft entry (was at position {old_len - len(packs)})")

    # Add our pack at the beginning
    packs.insert(0, pack_entry)

    # Write back
    final_content = json.dumps(packs, indent=2)
    debug_log(f"Writing world_behavior_packs.json:")
    debug_log(final_content)
    packs_file.write_text(final_content, encoding="utf-8")
    debug_log("world_behavior_packs.json written successfully")
