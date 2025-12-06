"""
Checks for Java-only commands and syntax.

This module detects:
- JAVA_COMMAND: Commands that don't exist in Bedrock (data, loot, attribute, item)
- NBT_SYNTAX: NBT {...} syntax on entities/items
- EFFECT_SYNTAX: Java's "effect give" vs Bedrock's "effect"
- JAVA_SELECTOR: Java-only selector arguments (nbt, predicate, team)
"""

from typing import List

from ..models import Issue, Token, TokenType, Severity, ValidationContext
from ..config import BedrockKnowledge
from ..tokenizer import get_command_name, has_nbt_structure, get_tokens_outside_quotes
from ..parser import get_all_commands_in_line, extract_selector_args
from . import Check, register_check


@register_check
class JavaCommandCheck(Check):
    """Check for Java-only commands."""

    code = "JAVA_COMMAND"
    severity = Severity.ERROR
    description = "Detects commands that only exist in Java Edition"

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        # Get all commands in the line (including execute subcommands)
        all_commands = get_all_commands_in_line(tokens)

        for cmd in all_commands:
            if BedrockKnowledge.is_java_only_command(cmd):
                issues.append(self.create_issue(
                    context,
                    f"Command '{cmd}' does not exist in Bedrock Edition",
                    suggestion=f"Remove or replace the '{cmd}' command"
                ))

        return issues

    def should_skip(self, context: ValidationContext) -> bool:
        # Skip if inside safe context (like tellraw text)
        if context.is_safe_context:
            return True
        return super().should_skip(context)


@register_check
class NBTSyntaxCheck(Check):
    """Check for NBT syntax that doesn't work in Bedrock."""

    code = "NBT_SYNTAX"
    severity = Severity.ERROR
    description = "Detects NBT {...} syntax not supported in Bedrock"

    # Commands that legitimately use NBT-like syntax in Bedrock
    SAFE_NBT_COMMANDS = {'particle', 'playsound', 'scriptevent'}

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        # Get command name
        cmd = context.command_name.lower()

        # Skip safe NBT commands
        if cmd in self.SAFE_NBT_COMMANDS:
            return issues

        # Look for NBT braces outside quotes
        outside_quote_tokens = get_tokens_outside_quotes(tokens)

        if has_nbt_structure(outside_quote_tokens):
            # Check what comes before the brace
            # NBT after give/summon is Java-only
            nbt_commands = {'give', 'summon', 'setblock', 'fill', 'execute'}

            if cmd in nbt_commands:
                issues.append(self.create_issue(
                    context,
                    f"NBT syntax {{...}} is not supported in Bedrock Edition",
                    suggestion="Use Bedrock-specific syntax or remove NBT data"
                ))

        return issues

    def should_skip(self, context: ValidationContext) -> bool:
        if context.is_safe_context:
            return True
        return super().should_skip(context)


@register_check
class EffectSyntaxCheck(Check):
    """Check for Java-style effect command syntax."""

    code = "EFFECT_SYNTAX"
    severity = Severity.ERROR
    description = "Detects 'effect give' which is Java-only"

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        cmd = context.command_name.lower()
        if cmd != 'effect':
            return issues

        # Look for 'give' or 'clear' after 'effect'
        # In Bedrock, it's just: effect @s speed 10 1
        # In Java, it's: effect give @s speed 10 1

        non_ws = [t for t in tokens if t.type != TokenType.WHITESPACE]

        # Check second token (after 'effect')
        if len(non_ws) >= 2:
            second = non_ws[1]
            if second.type == TokenType.IDENTIFIER and second.value.lower() == 'give':
                issues.append(self.create_issue(
                    context,
                    "'effect give' is Java syntax",
                    suggestion="Use 'effect @s <effect>' (remove 'give')"
                ))

        return issues


@register_check
class JavaSelectorCheck(Check):
    """Check for Java-only selector arguments."""

    code = "JAVA_SELECTOR"
    severity = Severity.ERROR
    description = "Detects selector arguments not supported in Bedrock"

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        # Find all selector tokens
        selector_tokens = [t for t in tokens if t.type == TokenType.SELECTOR]

        for selector_token in selector_tokens:
            selector = selector_token.value

            # Extract arguments
            args = extract_selector_args(selector)

            for key, value in args:
                if key in BedrockKnowledge.JAVA_SELECTOR_ARGS:
                    reason = BedrockKnowledge.JAVA_SELECTOR_ARGS[key]
                    issues.append(self.create_issue(
                        context,
                        f"Selector argument '{key}' is Java-only. {reason}",
                        suggestion=f"Remove or replace '{key}' argument"
                    ))

        return issues

    def should_skip(self, context: ValidationContext) -> bool:
        if context.is_safe_context:
            return True
        return super().should_skip(context)
