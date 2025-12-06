"""
Configuration and knowledge base for the Bedrock mcfunction validator.

This module contains:
- BedrockKnowledge: Static knowledge about Bedrock vs Java differences
- Default encoding fallback chain
- Block mappings and validation lists
"""

from pathlib import Path
from typing import Dict, Set, List, Optional


# Default encoding fallback chain for reading files
ENCODING_FALLBACK: List[str] = ["utf-8", "latin-1", "cp1252"]


class BedrockKnowledge:
    """Static knowledge base for Bedrock validation."""

    # Commands that exist ONLY in Java Edition
    JAVA_ONLY_COMMANDS: Set[str] = {
        'advancement', 'attribute', 'ban', 'ban-ip', 'bossbar', 'data',
        'datapack', 'debug', 'defaultgamemode', 'forceload', 'item',
        'jfr', 'loot', 'pardon', 'pardon-ip', 'perf', 'place',
        'publish', 'recipe', 'return', 'save-all', 'save-off', 'save-on',
        'seed', 'spectate', 'team', 'teammsg', 'tm', 'trigger',
        'worldborder'
    }

    # Commands where text content should be treated as safe (no command detection)
    SAFE_CONTEXT_COMMANDS: Set[str] = {
        'tellraw', 'titleraw', 'title', 'dialogue', 'scriptevent',
        'me', 'say', 'msg', 'w', 'tell'
    }

    # Java selector arguments that don't exist in Bedrock
    JAVA_SELECTOR_ARGS: Dict[str, str] = {
        'nbt': 'Bedrock does not support NBT in selectors.',
        'predicate': 'Predicates are Java-only.',
        'team': 'Teams do not exist in Bedrock (use tags).',
        'advancements': 'Advancements are Java-only.',
        'limit': 'Use "c" (count) instead.',
        'sort': 'Bedrock does not support explicit sort types.',
        'level': 'Use "l" (max) and "lm" (min).',
        'gamemode': 'Use "m".',
        'x_rotation': 'Use "rx/rxm".',
        'y_rotation': 'Use "ry/rym".',
        'distance': 'Use "r/rm".',
    }

    # Java block names that need different names in Bedrock
    # NOTE: Many blocks have been unified in recent Bedrock versions (1.20+)
    # Only include blocks that are STILL different
    BLOCK_MAPPINGS: Dict[str, str] = {
        # Enchanting - still different in Bedrock
        'enchanting_table': 'enchant_table',

        # Flowers (Bedrock still uses red_flower/yellow_flower for many)
        'poppy': 'red_flower',
        'dandelion': 'yellow_flower',
        'blue_orchid': 'red_flower',
        'allium': 'red_flower',
        'azure_bluet': 'red_flower',
        'red_tulip': 'red_flower',
        'orange_tulip': 'red_flower',
        'white_tulip': 'red_flower',
        'pink_tulip': 'red_flower',
        'oxeye_daisy': 'red_flower',
        'cornflower': 'red_flower',
        'lily_of_the_valley': 'red_flower',

        # Legacy names
        'wooden_door': 'oak_door',
    }

    # Blocks that REQUIRE a color prefix in Bedrock
    # Note: Some blocks have valid uncolored forms (candle, shulker_box)
    # This list is for blocks where the base name alone is invalid
    COLOR_REQUIRED_BLOCKS: Set[str] = {
        'bed', 'banner', 'wool', 'carpet', 'concrete', 'concrete_powder',
        'stained_glass', 'stained_glass_pane', 'glazed_terracotta'
    }

    # Valid color prefixes in Bedrock
    VALID_COLORS: Set[str] = {
        'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime',
        'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue',
        'brown', 'green', 'red', 'black'
    }

    @classmethod
    def is_java_only_command(cls, command: str) -> bool:
        """Check if a command is Java-only."""
        return command.lower().lstrip('/') in cls.JAVA_ONLY_COMMANDS

    @classmethod
    def is_safe_context_command(cls, command: str) -> bool:
        """Check if a command creates a safe text context."""
        return command.lower().lstrip('/') in cls.SAFE_CONTEXT_COMMANDS

    @classmethod
    def get_block_replacement(cls, block_name: str) -> Optional[str]:
        """Get the Bedrock replacement for a Java block name, or None if valid."""
        clean_name = block_name.lower().replace('minecraft:', '')
        return cls.BLOCK_MAPPINGS.get(clean_name)

    @classmethod
    def needs_color_prefix(cls, block_name: str) -> bool:
        """Check if a block name requires a color prefix in Bedrock."""
        clean_name = block_name.lower().replace('minecraft:', '')
        # Check if it's a base block name without color
        if clean_name in cls.COLOR_REQUIRED_BLOCKS:
            return True
        return False

    @classmethod
    def has_valid_color_prefix(cls, block_name: str) -> bool:
        """Check if a block name has a valid color prefix."""
        clean_name = block_name.lower().replace('minecraft:', '')
        for color in cls.VALID_COLORS:
            if clean_name.startswith(f"{color}_"):
                return True
        return False


def load_block_list(blocks_file: Optional[Path] = None) -> Set[str]:
    """Load valid Bedrock block IDs from file."""
    # Try custom file first
    if blocks_file and blocks_file.exists():
        with open(blocks_file, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip() and not line.startswith('#')}

    # Try default location (validator/resources/bedrock_blocks.txt)
    default_path = Path(__file__).parent / 'resources' / 'bedrock_blocks.txt'
    if default_path.exists():
        with open(default_path, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip() and not line.startswith('#')}

    # Try legacy location (maricraft/resources/bedrock_blocks.txt)
    legacy_path = Path(__file__).parent.parent / 'resources' / 'bedrock_blocks.txt'
    if legacy_path.exists():
        with open(legacy_path, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip() and not line.startswith('#')}

    # Return empty set if no file found
    return set()
