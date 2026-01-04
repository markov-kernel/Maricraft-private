"""Minecraft path discovery for Java and Bedrock installations."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from .version import detect_minecraft_version


# Datapack metadata
DATAPACK_NAME = "maricraft_datapack"
BEHAVIOR_PACK_NAME = "maricraft_behavior"


def get_bundled_datapack_path() -> Optional[Path]:
    """Get path to the bundled datapack in the resources folder.

    Works both in development and PyInstaller builds.

    Returns:
        Path to the bundled datapack, or None if not found.
    """
    # When running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)  # type: ignore
    else:
        # Development mode - relative to package parent
        base_path = Path(__file__).parent.parent

    datapack_path = base_path / "resources" / DATAPACK_NAME
    if datapack_path.exists():
        return datapack_path
    return None


def get_bundled_behavior_pack_path() -> Optional[Path]:
    """Get path to the bundled behavior pack in the resources folder.

    Works both in development and PyInstaller builds.

    Returns:
        Path to the bundled behavior pack, or None if not found.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)  # type: ignore
    else:
        base_path = Path(__file__).parent.parent

    pack_path = base_path / "resources" / BEHAVIOR_PACK_NAME
    if pack_path.exists():
        return pack_path
    return None


def get_minecraft_saves_path() -> Optional[Path]:
    """Get the Minecraft saves directory path on Windows.

    Returns:
        Path to the vanilla Minecraft saves folder, or None if not found.
    """
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

    Returns:
        First found worlds path, or None if not found.
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
                    except (OSError, UnicodeDecodeError):
                        # Fallback to folder name if levelname.txt is unreadable
                        worlds.append((folder.name, folder))

    return sorted(worlds, key=lambda x: x[0].lower())


def get_all_minecraft_instances() -> List[Tuple[str, Path, Optional[str]]]:
    """Find all Minecraft installations (vanilla + CurseForge + Bedrock).

    Scans common locations for Minecraft instances and their saves folders.
    Also detects the Minecraft version for each instance.

    Returns:
        List of (instance_name, saves_path, version) tuples, sorted by name.
        version may be None if not detected, or "bedrock" for Bedrock Edition.
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
