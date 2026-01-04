"""Bedrock Edition behavior pack management."""

from __future__ import annotations

import json
import shutil
import traceback
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

from .debug import debug_log
from .paths import BEHAVIOR_PACK_NAME, get_bundled_behavior_pack_path
from .version import compare_versions

if TYPE_CHECKING:
    from ..commands import CommandButton


# Behavior pack metadata
BEHAVIOR_PACK_DESCRIPTION = "Maricraft Helper - Kid-friendly Minecraft commands"

# Fixed UUIDs for the behavior pack (Bedrock requires UUIDs)
BEHAVIOR_PACK_UUID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
BEHAVIOR_PACK_MODULE_UUID = "b2c3d4e5-f6a7-8901-bcde-f12345678901"


def get_bundled_behavior_pack_version() -> str:
    """Get version from bundled behavior pack.

    Returns:
        Version string like "2.0.0", or "0.0.0" if not found.
    """
    pack_path = get_bundled_behavior_pack_path()
    if pack_path is None:
        return "0.0.0"

    version_file = pack_path / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"


def is_behavior_pack_installed(world_path: Path) -> bool:
    """Check if Maricraft behavior pack is installed in a Bedrock world.

    Args:
        world_path: Path to the Bedrock world folder.

    Returns:
        True if the behavior pack is installed.
    """
    pack_path = world_path / "behavior_packs" / BEHAVIOR_PACK_NAME / "manifest.json"
    return pack_path.exists()


def get_behavior_pack_version(world_path: Path) -> Optional[str]:
    """Get the installed behavior pack version from a Bedrock world.

    Args:
        world_path: Path to the Bedrock world folder.

    Returns:
        Version string or None if not found.
    """
    version_file = world_path / "behavior_packs" / BEHAVIOR_PACK_NAME / "version.txt"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def needs_behavior_pack_update(world_path: Path) -> bool:
    """Check if a Bedrock world needs behavior pack install/update.

    Args:
        world_path: Path to the Bedrock world folder.

    Returns:
        True if behavior pack should be installed or updated.
    """
    installed = get_behavior_pack_version(world_path)
    bundled = get_bundled_behavior_pack_version()

    if not installed:
        return True

    return compare_versions(installed, bundled) < 0


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


def _log_pack_contents(pack_path: Path, label: str) -> None:
    """Log all files in a pack directory for debugging.

    Args:
        pack_path: Path to the pack directory
        label: Label for the log section (e.g., "Source" or "Installed")
    """
    debug_log(f"--- {label} pack contents ---")
    for f in sorted(pack_path.rglob("*")):
        if f.is_file():
            rel = f.relative_to(pack_path)
            size = f.stat().st_size
            debug_log(f"  {rel} ({size} bytes)")

    # Log manifest.json
    manifest = pack_path / "manifest.json"
    if manifest.exists():
        debug_log(f"--- {label} manifest.json ---")
        debug_log(manifest.read_text(encoding="utf-8"))

    # Log version.txt if present
    version_file = pack_path / "version.txt"
    if version_file.exists():
        debug_log(f"{label} version.txt: {version_file.read_text(encoding='utf-8').strip()}")


def _copy_pack_files(source: Path, dest: Path) -> None:
    """Copy pack files from source to destination.

    Args:
        source: Source pack directory
        dest: Destination pack directory

    Raises:
        PermissionError: If access is denied
        OSError: If file operation fails
    """
    # Create parent directory
    dest.parent.mkdir(parents=True, exist_ok=True)
    debug_log(f"Created parent dir: {dest.parent}")

    # Remove existing pack if present
    if dest.exists():
        debug_log(f"Removing existing pack at {dest}")
        shutil.rmtree(dest)

    # Copy pack
    debug_log("Copying behavior pack...")
    shutil.copytree(source, dest)
    debug_log("Copy complete!")


def _verify_pack_installation(dest: Path) -> int:
    """Verify pack installation and return mcfunction file count.

    Args:
        dest: Installed pack directory

    Returns:
        Number of .mcfunction files installed
    """
    _log_pack_contents(dest, "Installed")

    mcfunction_count = sum(
        1 for f in dest.rglob("*.mcfunction") if f.is_file()
    )
    debug_log(f"Total .mcfunction files installed: {mcfunction_count}")

    # Log sample functions to verify content
    for sample_path in [
        dest / "functions" / "test.mcfunction",
        dest / "functions" / "buffs" / "super_regen.mcfunction",
    ]:
        if sample_path.exists():
            debug_log(f"--- Sample: {sample_path.name} ---")
            debug_log(sample_path.read_text(encoding="utf-8"))

    return mcfunction_count


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

    # Get source pack
    if source_path is None:
        source_path = get_bundled_behavior_pack_path()

    if source_path is None or not source_path.exists():
        debug_log(f"ERROR: No bundled behavior pack found. source_path={source_path}")
        return False

    debug_log(f"Source pack: {source_path}")
    _log_pack_contents(source_path, "Source")

    dest = world_path / "behavior_packs" / BEHAVIOR_PACK_NAME
    debug_log(f"Destination: {dest}")

    try:
        _copy_pack_files(source_path, dest)
        _verify_pack_installation(dest)
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
        debug_log(traceback.format_exc())
        return False


def _enable_behavior_pack_in_world(world_path: Path) -> None:
    """Add Maricraft behavior pack to world_behavior_packs.json.

    This file tells Bedrock which behavior packs are enabled for the world.

    Args:
        world_path: Path to the Bedrock world folder.
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
    except (json.JSONDecodeError, KeyError, OSError) as e:
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
                debug_log("WARNING: Content was not a list, resetting")
                packs = []
        except (json.JSONDecodeError, OSError) as e:
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
    debug_log("Writing world_behavior_packs.json:")
    debug_log(final_content)
    packs_file.write_text(final_content, encoding="utf-8")
    debug_log("world_behavior_packs.json written successfully")
