"""NBT to component conversion for Minecraft 1.21+ compatibility."""

from __future__ import annotations

import re

from .version import is_version_1_21_or_later


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
