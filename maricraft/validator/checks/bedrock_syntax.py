"""
Bedrock-specific syntax validation checks.

This module detects:
- LINE_TOO_LONG: Commands exceeding 256 character limit
- EXECUTE_DEPTH: Deeply nested execute chains (warning)
- JAVA_EXECUTE: Java-only execute subcommands (store, if data, if predicate)
- DOOR_BLOCK_STATES: Door placed without required block states
"""

import re
from typing import List

from ..models import Issue, Token, TokenType, Severity, ValidationContext
from ..parser import parse_command
from . import Check, register_check


@register_check
class LineTooLongCheck(Check):
    """Check for commands that exceed the chat limit."""

    code = "LINE_TOO_LONG"
    severity = Severity.WARNING
    description = "Commands exceeding 256 characters may cause issues"

    MAX_LENGTH = 256

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        if len(context.line) > self.MAX_LENGTH:
            issues.append(self.create_issue(
                context,
                f"Command is {len(context.line)} characters (max {self.MAX_LENGTH})",
                suggestion="Split into multiple commands or simplify"
            ))

        return issues


@register_check
class ExecuteDepthCheck(Check):
    """Check for deeply nested execute chains."""

    code = "EXECUTE_DEPTH"
    severity = Severity.WARNING
    description = "Warns about deeply nested execute chains"

    MAX_DEPTH = 5

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        if context.execute_depth > self.MAX_DEPTH:
            issues.append(self.create_issue(
                context,
                f"Execute chain is {context.execute_depth} levels deep (recommended max {self.MAX_DEPTH})",
                suggestion="Consider simplifying the execute chain"
            ))

        return issues


@register_check
class JavaExecuteSubcommandCheck(Check):
    """Check for Java-only execute subcommands.

    Bedrock execute does NOT support:
    - execute store (result/success)
    - execute if/unless data (NBT checks)
    - execute if/unless predicate
    - execute summon
    - execute on

    Bedrock execute DOES support:
    - execute as/at/positioned/rotated/facing/align/anchored/in
    - execute if/unless entity/block/score/blocks
    - execute run
    """

    code = "JAVA_EXECUTE"
    severity = Severity.ERROR
    description = "Detects Java-only execute subcommands"

    # Java-only execute subcommand patterns
    JAVA_ONLY_PATTERNS = [
        (r'\bexecute\s+store\b', "execute store", "Bedrock does not support execute store"),
        (r'\bexecute\s+(?:if|unless)\s+data\b', "execute if/unless data", "NBT data checks are Java-only"),
        (r'\bexecute\s+(?:if|unless)\s+predicate\b', "execute if/unless predicate", "Predicates are Java-only"),
        (r'\bexecute\s+(?:if|unless)\s+biome\b', "execute if/unless biome", "Biome checks are Java-only"),
        (r'\bexecute\s+(?:if|unless)\s+dimension\b', "execute if/unless dimension", "Dimension checks are Java-only"),
        (r'\bexecute\s+(?:if|unless)\s+loaded\b', "execute if/unless loaded", "Chunk loaded checks are Java-only"),
        (r'\bexecute\s+(?:if|unless)\s+function\b', "execute if/unless function", "Function return checks are Java-only"),
        (r'\bexecute\s+summon\b', "execute summon", "execute summon is Java-only"),
        (r'\bexecute\s+on\b', "execute on", "execute on is Java-only"),
    ]

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        # Only check execute commands
        cmd = context.command_name.lower()
        if cmd != 'execute':
            return issues

        line = context.line.lower()

        for pattern, name, reason in self.JAVA_ONLY_PATTERNS:
            if re.search(pattern, line):
                issues.append(self.create_issue(
                    context,
                    f"'{name}' is not supported in Bedrock Edition",
                    suggestion=reason
                ))

        return issues


@register_check
class DoorBlockStatesCheck(Check):
    """Check for door placement without required block states.

    In Bedrock Edition, doors need block states for proper placement:
    - direction: 0-3 for facing direction
    - upper_block_bit: false for bottom, true for top
    - open_bit: whether door is open
    - door_hinge_bit: hinge side (for top half)

    Both halves of the door must be placed separately.

    Example correct syntax:
        setblock ~ ~ ~ oak_door ["direction"=1,"upper_block_bit"=false,"open_bit"=false]
        setblock ~ ~1 ~ oak_door ["direction"=1,"upper_block_bit"=true,"door_hinge_bit"=false]
    """

    code = "DOOR_BLOCK_STATES"
    severity = Severity.WARNING
    description = "Door placed without block states may not work correctly"

    # Door block types
    DOOR_BLOCKS = {
        'oak_door', 'spruce_door', 'birch_door', 'jungle_door',
        'acacia_door', 'dark_oak_door', 'mangrove_door', 'cherry_door',
        'bamboo_door', 'crimson_door', 'warped_door', 'iron_door',
        'copper_door', 'exposed_copper_door', 'weathered_copper_door',
        'oxidized_copper_door', 'waxed_copper_door', 'waxed_exposed_copper_door',
        'waxed_weathered_copper_door', 'waxed_oxidized_copper_door',
    }

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        cmd = context.command_name.lower()
        if cmd != 'setblock':
            return issues

        line = context.line.lower()

        # Check if any door block is used
        for door in self.DOOR_BLOCKS:
            if door in line:
                # Check if block states are provided (look for [...])
                if not re.search(r'\[.*\]', line):
                    issues.append(self.create_issue(
                        context,
                        f"Door '{door}' placed without block states",
                        suggestion='Add block states like ["direction"=1,"upper_block_bit"=false,"open_bit"=false] and place both top and bottom halves'
                    ))
                break

        return issues
