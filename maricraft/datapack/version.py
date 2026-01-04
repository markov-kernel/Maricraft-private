"""Version detection and pack format mapping for Minecraft datapacks."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional


# Embedded defaults (fallback if config file is missing)
_EMBEDDED_PACK_FORMAT_MAP = {
    "1.20": 15,
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
_EMBEDDED_DEFAULT_PACK_FORMAT = 15


def _load_pack_format_config() -> tuple[dict[str, int], int]:
    """Load pack_format mapping from JSON config with fallback to embedded defaults.

    Returns:
        Tuple of (version_map, default_format)
    """
    # Resolve path relative to the package's parent (maricraft/)
    config_path = Path(__file__).parent.parent / "resources" / "pack_format_map.json"

    # For PyInstaller builds
    if getattr(sys, 'frozen', False):
        config_path = Path(sys._MEIPASS) / "resources" / "pack_format_map.json"  # type: ignore

    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            versions = {k: int(v) for k, v in data.get("versions", {}).items()}
            default = int(data.get("default", _EMBEDDED_DEFAULT_PACK_FORMAT))
            return versions, default
        except (json.JSONDecodeError, ValueError, KeyError):
            pass  # Fall through to embedded defaults

    return _EMBEDDED_PACK_FORMAT_MAP, _EMBEDDED_DEFAULT_PACK_FORMAT


# Load config at module import time
PACK_FORMAT_MAP, DEFAULT_PACK_FORMAT = _load_pack_format_config()


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

    Args:
        mc_version: Minecraft version string

    Returns:
        True if version is 1.21 or later.
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


def compare_versions(v1: str, v2: str) -> int:
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


# Backward compatibility alias
_compare_versions = compare_versions
