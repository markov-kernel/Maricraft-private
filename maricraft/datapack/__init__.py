"""Datapack management for Maricraft.

This package provides datapack/behavior pack management for both
Java Edition and Bedrock Edition Minecraft.

All public functions are re-exported here for backward compatibility.
"""

from __future__ import annotations

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..commands import CommandButton

# Re-export from debug module
from .debug import (
    debug_log,
    set_debug_log_path,
    reset_debug_log,
)

# Re-export from version module
from .version import (
    PACK_FORMAT_MAP,
    DEFAULT_PACK_FORMAT,
    get_pack_format_for_version,
    is_version_1_21_or_later,
    get_functions_folder_name,
    detect_minecraft_version,
    detect_version_for_saves_path,
    compare_versions,
    _compare_versions,  # Backward compatibility alias
)

# Re-export from paths module
from .paths import (
    DATAPACK_NAME,
    BEHAVIOR_PACK_NAME,
    get_bundled_datapack_path,
    get_bundled_behavior_pack_path,
    get_minecraft_saves_path,
    get_all_bedrock_worlds_paths,
    get_bedrock_worlds_path,
    list_bedrock_worlds,
    get_all_minecraft_instances,
    list_worlds,
)

# Re-export from conversion module
from .conversion import (
    convert_nbt_to_components,
    convert_mcfunction_for_version,
)

# Re-export from java_datapack module
from .java_datapack import (
    PACK_DESCRIPTION,
    is_datapack_installed,
    get_datapack_version,
    check_any_world_has_datapack,
    get_bundled_datapack_version,
    needs_datapack_update,
    install_datapack,
    install_datapack_to_worlds,
    generate_datapack,
)

# Re-export from bedrock_pack module
from .bedrock_pack import (
    BEHAVIOR_PACK_DESCRIPTION,
    BEHAVIOR_PACK_UUID,
    BEHAVIOR_PACK_MODULE_UUID,
    get_bundled_behavior_pack_version,
    is_behavior_pack_installed,
    get_behavior_pack_version,
    needs_behavior_pack_update,
    generate_behavior_pack,
    install_behavior_pack,
)


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
    from ..commands import ALL_CATEGORIES

    buttons = []
    for category in ALL_CATEGORIES:
        buttons.extend(category.buttons)
    return buttons


# Public API (for `from maricraft.datapack import *`)
__all__ = [
    # Debug
    "debug_log",
    "set_debug_log_path",
    "reset_debug_log",
    # Version
    "PACK_FORMAT_MAP",
    "DEFAULT_PACK_FORMAT",
    "get_pack_format_for_version",
    "is_version_1_21_or_later",
    "get_functions_folder_name",
    "detect_minecraft_version",
    "detect_version_for_saves_path",
    "compare_versions",
    "_compare_versions",
    # Paths
    "DATAPACK_NAME",
    "BEHAVIOR_PACK_NAME",
    "get_bundled_datapack_path",
    "get_bundled_behavior_pack_path",
    "get_minecraft_saves_path",
    "get_all_bedrock_worlds_paths",
    "get_bedrock_worlds_path",
    "list_bedrock_worlds",
    "get_all_minecraft_instances",
    "list_worlds",
    # Conversion
    "convert_nbt_to_components",
    "convert_mcfunction_for_version",
    # Java Datapack
    "PACK_DESCRIPTION",
    "is_datapack_installed",
    "get_datapack_version",
    "check_any_world_has_datapack",
    "get_bundled_datapack_version",
    "needs_datapack_update",
    "install_datapack",
    "install_datapack_to_worlds",
    "generate_datapack",
    # Bedrock Pack
    "BEHAVIOR_PACK_DESCRIPTION",
    "BEHAVIOR_PACK_UUID",
    "BEHAVIOR_PACK_MODULE_UUID",
    "get_bundled_behavior_pack_version",
    "is_behavior_pack_installed",
    "get_behavior_pack_version",
    "needs_behavior_pack_update",
    "generate_behavior_pack",
    "install_behavior_pack",
    # Orchestration
    "auto_install_all_datapacks",
    "get_all_buttons",
]
