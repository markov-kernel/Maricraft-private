"""
Bedrock mcfunction Validator

Validates .mcfunction files for Bedrock Edition compatibility.
Catches Java-only syntax before it causes silent failures in-game.

Usage:
    python -m maricraft.validator [path] [--json] [--strict]
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set, Dict
from enum import Enum
import re
import json
import sys


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass
class Issue:
    """A validation issue found in a mcfunction file."""
    line_num: int
    line: str
    severity: Severity
    code: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of validating a single mcfunction file."""
    file: Path
    issues: List[Issue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """True if no errors (warnings allowed)."""
        return not any(i.severity == Severity.ERROR for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)


class BedrockValidator:
    """Validates .mcfunction files for Bedrock Edition compatibility."""

    # Java-only commands that don't exist in Bedrock
    JAVA_ONLY_COMMANDS = {'loot', 'data', 'attribute', 'item'}

    # Known Java -> Bedrock block/item mappings
    BLOCK_MAPPINGS: Dict[str, str] = {
        # Enchanting
        'enchanting_table': 'enchant_table',

        # Beds (must specify color)
        'bed': 'red_bed',

        # Flowers (Bedrock uses different naming)
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

    # Blocks that require color specification in Bedrock
    COLOR_REQUIRED_BLOCKS = {'bed', 'banner', 'wool', 'carpet', 'concrete', 'concrete_powder',
                             'terracotta', 'stained_glass', 'stained_glass_pane', 'shulker_box'}

    def __init__(self, blocks_file: Optional[Path] = None):
        """Initialize validator with optional custom blocks file."""
        self.bedrock_blocks = self._load_block_list(blocks_file)
        self.issues: List[Issue] = []

    def _load_block_list(self, blocks_file: Optional[Path] = None) -> Set[str]:
        """Load valid Bedrock block IDs from file or use built-in list."""
        # Try to load from file
        if blocks_file and blocks_file.exists():
            with open(blocks_file, 'r') as f:
                return {line.strip() for line in f if line.strip() and not line.startswith('#')}

        # Try default location
        default_path = Path(__file__).parent / 'resources' / 'bedrock_blocks.txt'
        if default_path.exists():
            with open(default_path, 'r') as f:
                return {line.strip() for line in f if line.strip() and not line.startswith('#')}

        # Fallback to built-in curated list of blocks used in Maricraft
        return {
            # Basic blocks
            'air', 'stone', 'cobblestone', 'glass', 'water', 'lava', 'ice', 'packed_ice', 'blue_ice',
            'dirt', 'grass', 'grass_block', 'sand', 'gravel', 'clay', 'snow', 'snow_layer',

            # Stone variants
            'stone_bricks', 'stonebrick', 'mossy_stone_bricks', 'cracked_stone_bricks',
            'chiseled_stone_bricks', 'smooth_stone', 'stone_brick_stairs',

            # Deepslate
            'deepslate', 'deepslate_bricks', 'polished_deepslate', 'deepslate_tiles',
            'cobbled_deepslate', 'chiseled_deepslate',

            # Blackstone
            'blackstone', 'polished_blackstone', 'polished_blackstone_bricks',
            'gilded_blackstone', 'chiseled_polished_blackstone',

            # Wood planks
            'planks', 'oak_planks', 'spruce_planks', 'birch_planks', 'jungle_planks',
            'acacia_planks', 'dark_oak_planks', 'mangrove_planks', 'cherry_planks',
            'bamboo_planks', 'crimson_planks', 'warped_planks',

            # Wood logs
            'log', 'oak_log', 'spruce_log', 'birch_log', 'jungle_log',
            'acacia_log', 'dark_oak_log', 'mangrove_log', 'cherry_log',
            'crimson_stem', 'warped_stem',

            # Doors
            'oak_door', 'spruce_door', 'birch_door', 'jungle_door',
            'acacia_door', 'dark_oak_door', 'iron_door', 'crimson_door', 'warped_door',

            # Stairs
            'oak_stairs', 'spruce_stairs', 'birch_stairs', 'jungle_stairs',
            'stone_stairs', 'cobblestone_stairs', 'sandstone_stairs',
            'nether_brick_stairs', 'quartz_stairs', 'prismarine_stairs',

            # Fences
            'oak_fence', 'spruce_fence', 'birch_fence', 'jungle_fence',
            'nether_brick_fence', 'crimson_fence', 'warped_fence',

            # Wool (colors)
            'white_wool', 'orange_wool', 'magenta_wool', 'light_blue_wool',
            'yellow_wool', 'lime_wool', 'pink_wool', 'gray_wool',
            'light_gray_wool', 'cyan_wool', 'purple_wool', 'blue_wool',
            'brown_wool', 'green_wool', 'red_wool', 'black_wool',

            # Beds (colors)
            'white_bed', 'orange_bed', 'magenta_bed', 'light_blue_bed',
            'yellow_bed', 'lime_bed', 'pink_bed', 'gray_bed',
            'light_gray_bed', 'cyan_bed', 'purple_bed', 'blue_bed',
            'brown_bed', 'green_bed', 'red_bed', 'black_bed',

            # Carpet (colors)
            'white_carpet', 'orange_carpet', 'magenta_carpet', 'light_blue_carpet',
            'yellow_carpet', 'lime_carpet', 'pink_carpet', 'gray_carpet',
            'light_gray_carpet', 'cyan_carpet', 'purple_carpet', 'blue_carpet',
            'brown_carpet', 'green_carpet', 'red_carpet', 'black_carpet',

            # Stained glass
            'white_stained_glass', 'orange_stained_glass', 'magenta_stained_glass',
            'light_blue_stained_glass', 'yellow_stained_glass', 'lime_stained_glass',
            'pink_stained_glass', 'gray_stained_glass', 'light_gray_stained_glass',
            'cyan_stained_glass', 'purple_stained_glass', 'blue_stained_glass',
            'brown_stained_glass', 'green_stained_glass', 'red_stained_glass',
            'black_stained_glass',

            # Terracotta
            'terracotta', 'white_terracotta', 'orange_terracotta', 'magenta_terracotta',
            'light_blue_terracotta', 'yellow_terracotta', 'lime_terracotta',
            'pink_terracotta', 'gray_terracotta', 'light_gray_terracotta',
            'cyan_terracotta', 'purple_terracotta', 'blue_terracotta',
            'brown_terracotta', 'green_terracotta', 'red_terracotta', 'black_terracotta',

            # Banners
            'white_banner', 'orange_banner', 'magenta_banner', 'light_blue_banner',
            'yellow_banner', 'lime_banner', 'pink_banner', 'gray_banner',
            'light_gray_banner', 'cyan_banner', 'purple_banner', 'blue_banner',
            'brown_banner', 'green_banner', 'red_banner', 'black_banner',

            # Ores and minerals
            'gold_block', 'diamond_block', 'emerald_block', 'iron_block',
            'coal_block', 'lapis_block', 'redstone_block', 'netherite_block',
            'copper_block', 'raw_iron_block', 'raw_gold_block', 'raw_copper_block',
            'amethyst_block',

            # Obsidian
            'obsidian', 'crying_obsidian',

            # End blocks
            'end_stone', 'end_stone_bricks', 'end_rod', 'dragon_egg', 'end_portal_frame',

            # Nether blocks
            'netherrack', 'nether_bricks', 'nether_brick_fence', 'soul_sand', 'soul_soil',
            'magma_block', 'glowstone', 'shroomlight', 'basalt', 'polished_basalt',

            # Prismarine
            'prismarine', 'prismarine_bricks', 'dark_prismarine', 'sea_lantern',

            # Sandstone
            'sandstone', 'chiseled_sandstone', 'smooth_sandstone', 'cut_sandstone',
            'red_sandstone', 'chiseled_red_sandstone', 'smooth_red_sandstone',

            # Functional blocks
            'enchant_table', 'bookshelf', 'brewing_stand', 'cauldron',
            'chest', 'trapped_chest', 'ender_chest', 'barrel',
            'crafting_table', 'furnace', 'blast_furnace', 'smoker',
            'anvil', 'grindstone', 'stonecutter', 'loom', 'cartography_table',
            'fletching_table', 'smithing_table', 'lectern', 'composter',
            'beehive', 'bee_nest', 'conduit', 'beacon', 'bell', 'lodestone',
            'respawn_anchor',

            # Redstone
            'redstone_torch', 'redstone_lamp', 'redstone_wire', 'redstone_block',
            'piston', 'sticky_piston', 'observer', 'dropper', 'dispenser',
            'hopper', 'comparator', 'repeater', 'lever', 'tripwire_hook',
            'daylight_detector', 'note_block', 'jukebox', 'target',

            # Lighting
            'torch', 'wall_torch', 'lantern', 'soul_lantern', 'soul_torch',
            'candle', 'campfire', 'soul_campfire', 'jack_o_lantern',

            # Coral
            'brain_coral_block', 'tube_coral_block', 'fire_coral_block',
            'bubble_coral_block', 'horn_coral_block',
            'dead_brain_coral_block', 'dead_tube_coral_block', 'dead_fire_coral_block',
            'dead_bubble_coral_block', 'dead_horn_coral_block',

            # Plants
            'red_flower', 'yellow_flower', 'kelp', 'seagrass', 'tall_grass',
            'fern', 'large_fern', 'vine', 'lily_pad', 'sugar_cane',
            'cactus', 'bamboo', 'dead_bush', 'sweet_berry_bush',

            # Leaves
            'oak_leaves', 'spruce_leaves', 'birch_leaves', 'jungle_leaves',
            'acacia_leaves', 'dark_oak_leaves', 'azalea_leaves',
            'flowering_azalea_leaves', 'mangrove_leaves', 'cherry_leaves',

            # Misc
            'ladder', 'chain', 'iron_bars', 'glass_pane',
            'lightning_rod', 'pointed_dripstone', 'dripstone_block',
            'tinted_glass', 'copper_grate', 'trial_spawner',
            'spawner', 'mob_spawner', 'tnt', 'slime_block', 'honey_block',
            'scaffolding', 'hay_block', 'melon_block', 'pumpkin',
            'carved_pumpkin', 'lit_pumpkin', 'sponge', 'wet_sponge',
            'cobweb', 'skeleton_skull', 'wither_skeleton_skull', 'zombie_head',
            'creeper_head', 'dragon_head', 'player_head',

            # Fire
            'fire', 'soul_fire',

            # Command blocks
            'command_block', 'chain_command_block', 'repeating_command_block',
            'structure_block', 'jigsaw', 'barrier', 'light_block',
        }

    def validate_file(self, path: Path) -> ValidationResult:
        """Validate a single .mcfunction file."""
        result = ValidationResult(file=path)

        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            result.issues.append(Issue(
                line_num=0,
                line="",
                severity=Severity.ERROR,
                code="FILE_ERROR",
                message=f"Could not read file: {e}"
            ))
            return result

        for line_num, line in enumerate(lines, start=1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Run all checks
            result.issues.extend(self._check_line(line, line_num))

        return result

    def validate_directory(self, path: Path) -> List[ValidationResult]:
        """Validate all .mcfunction files in a directory recursively."""
        results = []
        for mcfunction_file in path.rglob('*.mcfunction'):
            results.append(self.validate_file(mcfunction_file))
        return results

    def _check_line(self, line: str, line_num: int) -> List[Issue]:
        """Check a single command line for issues."""
        issues = []

        # Check for Java-only commands
        issues.extend(self._check_java_commands(line, line_num))

        # Check for Java-only syntax
        issues.extend(self._check_java_syntax(line, line_num))

        # Check block names in setblock/fill commands
        issues.extend(self._check_block_commands(line, line_num))

        # Check effect command syntax
        issues.extend(self._check_effect_syntax(line, line_num))

        return issues

    def _check_java_commands(self, line: str, line_num: int) -> List[Issue]:
        """Check for Java-only commands."""
        issues = []

        # Get the command (first word, possibly after /)
        match = re.match(r'^/?(\w+)', line)
        if match:
            command = match.group(1).lower()
            if command in self.JAVA_ONLY_COMMANDS:
                issues.append(Issue(
                    line_num=line_num,
                    line=line,
                    severity=Severity.ERROR,
                    code="JAVA_COMMAND",
                    message=f"'{command}' command does not exist in Bedrock Edition"
                ))

        return issues

    def _check_java_syntax(self, line: str, line_num: int) -> List[Issue]:
        """Check for Java-only syntax patterns."""
        issues = []

        # Check for NBT syntax {...} after commands like summon, give, etc.
        # Look for patterns like: summon zombie ~ ~ ~ {Health:20}
        # or: give @s diamond_sword{Enchantments:[...]}
        nbt_pattern = re.search(r'(summon|give|setblock|fill)\s+.*\{[^}]+\}', line, re.IGNORECASE)
        if nbt_pattern:
            issues.append(Issue(
                line_num=line_num,
                line=line,
                severity=Severity.ERROR,
                code="NBT_SYNTAX",
                message="NBT syntax {...} is not supported in Bedrock Edition"
            ))

        # Check for component syntax [...] after items (Java 1.21+)
        # Pattern: item_name[...]
        if re.search(r'\w+\[[^\]]*\w+=[^\]]+\]', line):
            # This might match selectors, so be careful
            if not re.search(r'@[aepsr]\[', line):
                # Check if it looks like item components
                if re.search(r'(give|replaceitem).*\w+\[', line):
                    issues.append(Issue(
                        line_num=line_num,
                        line=line,
                        severity=Severity.ERROR,
                        code="COMPONENT_SYNTAX",
                        message="Item component syntax [...] is not supported in Bedrock Edition"
                    ))

        # Check for predicate selector
        if re.search(r'@[aepsr]\[.*predicate=', line):
            issues.append(Issue(
                line_num=line_num,
                line=line,
                severity=Severity.ERROR,
                code="PREDICATE",
                message="Predicates are not supported in Bedrock Edition selectors"
            ))

        return issues

    def _check_block_commands(self, line: str, line_num: int) -> List[Issue]:
        """Check block names in setblock/fill/testforblock commands."""
        issues = []

        # Pattern for setblock: setblock <coords> <block>
        setblock_match = re.search(
            r'\bsetblock\s+[~^0-9\-\.\s]+\s+(\w+)',
            line, re.IGNORECASE
        )

        # Pattern for fill: fill <coords> <coords> <block>
        fill_match = re.search(
            r'\bfill\s+[~^0-9\-\.\s]+\s+[~^0-9\-\.\s]+\s+(\w+)',
            line, re.IGNORECASE
        )

        # Pattern for testforblock: testforblock <coords> <block>
        testforblock_match = re.search(
            r'\btestforblock\s+[~^0-9\-\.\s]+\s+(\w+)',
            line, re.IGNORECASE
        )

        # Check each match
        for match in [setblock_match, fill_match, testforblock_match]:
            if match:
                block_name = match.group(1).lower()
                issue = self._validate_block_name(block_name, line_num, line)
                if issue:
                    issues.append(issue)

        return issues

    def _validate_block_name(self, block_name: str, line_num: int, line: str) -> Optional[Issue]:
        """Validate a single block name."""
        # Strip minecraft: namespace if present
        if block_name.startswith('minecraft:'):
            block_name = block_name[10:]

        # Check if it's a known Java-only block
        if block_name in self.BLOCK_MAPPINGS:
            suggestion = self.BLOCK_MAPPINGS[block_name]
            return Issue(
                line_num=line_num,
                line=line,
                severity=Severity.ERROR,
                code="JAVA_BLOCK",
                message=f"'{block_name}' is not valid in Bedrock Edition",
                suggestion=f"Use '{suggestion}' instead"
            )

        # Check if block requires color (e.g., 'bed' without color)
        for base_block in self.COLOR_REQUIRED_BLOCKS:
            if block_name == base_block:
                return Issue(
                    line_num=line_num,
                    line=line,
                    severity=Severity.ERROR,
                    code="COLOR_REQUIRED",
                    message=f"'{block_name}' requires a color prefix in Bedrock Edition",
                    suggestion=f"Use 'white_{block_name}', 'red_{block_name}', etc."
                )

        # Check against known valid blocks (if whitelist is comprehensive)
        # For now, we only flag known problematic blocks
        # Uncomment below to enforce whitelist:
        # if block_name not in self.bedrock_blocks:
        #     return Issue(
        #         line_num=line_num,
        #         line=line,
        #         severity=Severity.WARNING,
        #         code="UNKNOWN_BLOCK",
        #         message=f"'{block_name}' not in known Bedrock block list (may still be valid)"
        #     )

        return None

    def _check_effect_syntax(self, line: str, line_num: int) -> List[Issue]:
        """Check for Java-style effect command syntax."""
        issues = []

        # Java uses: effect give @s <effect>
        # Bedrock uses: effect @s <effect>
        if re.search(r'\beffect\s+give\b', line, re.IGNORECASE):
            issues.append(Issue(
                line_num=line_num,
                line=line,
                severity=Severity.ERROR,
                code="EFFECT_SYNTAX",
                message="'effect give' is Java syntax",
                suggestion="Use 'effect @s <effect>' (remove 'give')"
            ))

        return issues


def format_results_text(results: List[ValidationResult], show_valid: bool = False) -> str:
    """Format validation results as colored text."""
    output = []
    total_errors = 0
    total_warnings = 0

    for result in results:
        if not result.issues and not show_valid:
            continue

        rel_path = result.file.name
        try:
            # Try to get relative path from functions directory
            parts = result.file.parts
            if 'functions' in parts:
                idx = parts.index('functions')
                rel_path = '/'.join(parts[idx+1:])
        except:
            pass

        if result.issues:
            output.append(f"\n{rel_path}")
            for issue in result.issues:
                severity_str = "ERROR" if issue.severity == Severity.ERROR else "WARN"
                output.append(f"  LINE {issue.line_num}: {issue.line[:60]}{'...' if len(issue.line) > 60 else ''}")
                output.append(f"  {severity_str} [{issue.code}]: {issue.message}")
                if issue.suggestion:
                    output.append(f"  → Suggestion: {issue.suggestion}")
        elif show_valid:
            output.append(f"\n{rel_path}")
            output.append("  [OK] No issues")

        total_errors += result.error_count
        total_warnings += result.warning_count

    valid_count = sum(1 for r in results if r.is_valid)
    output.append(f"\n{'='*50}")
    output.append(f"Summary: {len(results)} files, {valid_count} valid, {total_errors} errors, {total_warnings} warnings")

    return '\n'.join(output)


def format_results_json(results: List[ValidationResult]) -> str:
    """Format validation results as JSON."""
    output = {
        "summary": {
            "total_files": len(results),
            "valid_files": sum(1 for r in results if r.is_valid),
            "total_errors": sum(r.error_count for r in results),
            "total_warnings": sum(r.warning_count for r in results)
        },
        "files": []
    }

    for result in results:
        file_data = {
            "path": str(result.file),
            "is_valid": result.is_valid,
            "issues": [
                {
                    "line": issue.line_num,
                    "severity": issue.severity.value,
                    "code": issue.code,
                    "message": issue.message,
                    "suggestion": issue.suggestion
                }
                for issue in result.issues
            ]
        }
        output["files"].append(file_data)

    return json.dumps(output, indent=2)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate Bedrock .mcfunction files for compatibility issues"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="File or directory to validate (default: maricraft/resources/maricraft_behavior/functions)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--strict", "-s",
        action="store_true",
        help="Exit with error code if any warnings"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Show all files including valid ones"
    )

    args = parser.parse_args()

    # Determine path
    if args.path:
        path = Path(args.path)
    else:
        # Default to Bedrock behavior pack functions
        path = Path(__file__).parent / 'resources' / 'maricraft_behavior' / 'functions'

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(2)

    # Run validation
    validator = BedrockValidator()

    if path.is_file():
        results = [validator.validate_file(path)]
    else:
        results = validator.validate_directory(path)

    # Output results
    if args.json:
        print(format_results_json(results))
    else:
        print("Validating Bedrock mcfunction files...")
        print(format_results_text(results, show_valid=args.all))

    # Exit code
    has_errors = any(not r.is_valid for r in results)
    has_warnings = any(r.warning_count > 0 for r in results)

    if has_errors:
        sys.exit(1)
    elif args.strict and has_warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
