"""Java Edition datapack management."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple, TYPE_CHECKING

from .conversion import convert_mcfunction_for_version
from .paths import DATAPACK_NAME, get_bundled_datapack_path, get_all_minecraft_instances, list_worlds
from .version import (
    get_pack_format_for_version,
    get_functions_folder_name,
    is_version_1_21_or_later,
    compare_versions,
)

if TYPE_CHECKING:
    from ..commands import CommandButton


# Datapack metadata
PACK_DESCRIPTION = "Maricraft Helper - Kid-friendly Minecraft commands"


def is_datapack_installed(world_path: Path) -> bool:
    """Check if Maricraft datapack is installed in a world.

    Args:
        world_path: Path to the Minecraft world folder.

    Returns:
        True if the datapack is installed.
    """
    datapack_path = world_path / "datapacks" / DATAPACK_NAME / "pack.mcmeta"
    return datapack_path.exists()


def get_datapack_version(world_path: Path) -> Optional[str]:
    """Get the installed datapack version from a world.

    Args:
        world_path: Path to the Minecraft world folder.

    Returns:
        Version string or None if not found.
    """
    version_file = world_path / "datapacks" / DATAPACK_NAME / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def check_any_world_has_datapack() -> bool:
    """Check if any Minecraft world has the datapack installed.

    Checks across all instances (vanilla + CurseForge).

    Returns:
        True if at least one world has the datapack.
    """
    for _instance_name, saves_path, _version in get_all_minecraft_instances():
        for _world_name, world_path in list_worlds(saves_path):
            if is_datapack_installed(world_path):
                return True
    return False


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

    return compare_versions(installed, bundled) < 0


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
    except (OSError, shutil.Error):
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
