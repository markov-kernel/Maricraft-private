"""
Block name validation checks.

This module detects:
- JAVA_BLOCK: Java-only block names that need mapping in Bedrock
- COLOR_REQUIRED: Blocks that require a color prefix in Bedrock
"""

from typing import List

from ..models import Issue, Token, TokenType, Severity, ValidationContext
from ..config import BedrockKnowledge
from ..parser import ParsedCommand, parse_command
from . import Check, register_check


@register_check
class JavaBlockCheck(Check):
    """Check for Java-only block names."""

    code = "JAVA_BLOCK"
    severity = Severity.ERROR
    description = "Detects Java Edition block names not valid in Bedrock"

    # Commands that use block names
    BLOCK_COMMANDS = {'setblock', 'fill', 'testforblock', 'clone', 'execute'}

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        cmd = context.command_name.lower()

        # Only check commands that use blocks
        if cmd not in self.BLOCK_COMMANDS:
            return issues

        # Parse command to extract block names
        parsed = parse_command(context.line, context.line_num)

        for block_name in parsed.block_names:
            replacement = BedrockKnowledge.get_block_replacement(block_name)
            if replacement:
                issues.append(self.create_issue(
                    context,
                    f"Block '{block_name}' is not valid in Bedrock Edition",
                    suggestion=f"Use '{replacement}' instead"
                ))

        return issues


@register_check
class ColorRequiredCheck(Check):
    """Check for blocks that require a color prefix."""

    code = "COLOR_REQUIRED"
    severity = Severity.ERROR
    description = "Detects blocks that need a color prefix in Bedrock"

    BLOCK_COMMANDS = {'setblock', 'fill', 'testforblock', 'clone', 'execute'}

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        cmd = context.command_name.lower()

        if cmd not in self.BLOCK_COMMANDS:
            return issues

        # Parse command to extract block names
        parsed = parse_command(context.line, context.line_num)

        for block_name in parsed.block_names:
            # Check if this is a base block that needs color
            if BedrockKnowledge.needs_color_prefix(block_name):
                # Make sure it doesn't already have a color
                if not BedrockKnowledge.has_valid_color_prefix(block_name):
                    issues.append(self.create_issue(
                        context,
                        f"Block '{block_name}' requires a color prefix in Bedrock Edition",
                        suggestion=f"Use 'white_{block_name}', 'red_{block_name}', etc."
                    ))

        return issues
