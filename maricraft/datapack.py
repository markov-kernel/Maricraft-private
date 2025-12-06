"""Datapack management for Maricraft."""

from __future__ import annotations

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
        func_path = button.function_id.replace("maricraft:", "") + ".mcfunction"
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

    Scans all Minecraft instances (vanilla + CurseForge) and installs
    or updates the datapack in any world that doesn't have it or has
    an older version.

    Returns:
        Dict with keys:
            - installed: list of world names where datapack was newly installed
            - updated: list of world names where datapack was updated
            - failed: list of (world_name, error) tuples
            - skipped: list of world names already up to date
    """
    results = {"installed": [], "updated": [], "failed": [], "skipped": []}

    for instance_name, saves_path, mc_version in get_all_minecraft_instances():
        for world_name, world_path in list_worlds(saves_path):
            try:
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
                    results["failed"].append((world_name, "Installation failed"))
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
