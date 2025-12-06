"""
Checks for Java-only commands and syntax.

This module detects:
- JAVA_COMMAND: Commands that don't exist in Bedrock (data, attribute, item, etc.)
- NBT_SYNTAX: Java SNBT {...} syntax (unquoted keys) not supported in Bedrock
- EFFECT_SYNTAX: Java's "effect give" vs Bedrock's "effect"
- JAVA_SELECTOR: Java-only selector arguments (nbt, predicate, team)

NOTE: Bedrock /give supports JSON components with quoted keys:
  give @s diamond_sword 1 0 {"can_destroy":{"blocks":["stone"]}}
This is different from Java SNBT which uses unquoted keys:
  give @s diamond_sword{Enchantments:[{id:sharpness,lvl:5}]}
"""

import re
from typing import List

from ..models import Issue, Token, TokenType, Severity, ValidationContext
from ..config import BedrockKnowledge
from ..tokenizer import get_command_name, has_nbt_structure, get_tokens_outside_quotes
from ..parser import get_all_commands_in_line, extract_selector_args
from . import Check, register_check


def is_snbt_syntax(line: str) -> bool:
    """
    Detect if a line contains Java SNBT syntax (unquoted keys).

    SNBT (Java): {Health:20, CustomName:"Test"} - keys are bare identifiers
    JSON (Bedrock): {"can_destroy":{"blocks":["stone"]}} - keys are quoted strings

    Returns True if SNBT pattern is detected (should be flagged).
    """
    # Look for patterns like: {word: or ,word: or [word:
    # These indicate SNBT with unquoted keys
    # Exclude patterns where key is quoted: {"key": or {'key':

    # Pattern: brace or comma followed by whitespace, then identifier, then colon
    # but NOT preceded by a quote
    snbt_pattern = re.compile(r'[{,\[]\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:')

    # Also check for item attached NBT: item{...} pattern (Java-only)
    attached_nbt_pattern = re.compile(r'[a-zA-Z_][a-zA-Z0-9_:]*\{')

    if attached_nbt_pattern.search(line):
        # This is definitely Java SNBT - items can't have attached NBT in Bedrock
        return True

    # Check for unquoted keys in braces
    for match in snbt_pattern.finditer(line):
        # Get the context - check if we're in a JSON structure (quoted keys)
        # or SNBT structure (unquoted keys)
        start = match.start()

        # Look backwards to see if this is inside a JSON object (has quoted keys)
        # Simple heuristic: if there's a { followed by " before this key, it's JSON
        prefix = line[:start+1]  # Include the { or , character

        # Count unquoted vs quoted keys before this point
        # If we find ANY unquoted key pattern, it's SNBT
        return True

    return False


def has_attached_nbt(tokens: List[Token]) -> bool:
    """
    Check if tokens contain item{NBT} pattern (Java-only attached NBT).

    In Java: give @s diamond_sword{Enchantments:[...]}
    In Bedrock: give @s diamond_sword 1 0 {"components":{...}}
    """
    for i, token in enumerate(tokens):
        if token.type == TokenType.NBT_OPEN and not token.is_in_quote:
            # Check if previous token is an identifier (item name)
            if i > 0:
                prev = tokens[i-1]
                if prev.type == TokenType.IDENTIFIER and not prev.is_in_quote:
                    # This is item{NBT} pattern - Java SNBT
                    return True
    return False


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
    """Check for Java SNBT syntax that doesn't work in Bedrock.

    IMPORTANT: Bedrock /give DOES support JSON components:
        give @s diamond_sword 1 0 {"can_destroy":{"blocks":["stone"]}}

    This check only flags Java SNBT syntax (unquoted keys):
        give @s diamond_sword{Enchantments:[{id:sharpness}]}  # INVALID in Bedrock
    """

    code = "NBT_SYNTAX"
    severity = Severity.ERROR
    description = "Detects Java SNBT {...} syntax not supported in Bedrock"

    # Commands that legitimately use NBT-like syntax in Bedrock
    SAFE_NBT_COMMANDS = {'particle', 'playsound', 'scriptevent', 'tellraw', 'titleraw'}

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        # Get command name
        cmd = context.command_name.lower()

        # Skip safe NBT commands (text commands handled by tokenizer already)
        if cmd in self.SAFE_NBT_COMMANDS:
            return issues

        # Check for attached NBT pattern: item{NBT} (always Java-only)
        if has_attached_nbt(tokens):
            issues.append(self.create_issue(
                context,
                "Attached NBT syntax (item{...}) is Java-only",
                suggestion="In Bedrock, use: give @s item count data {\"components\":{...}}"
            ))
            return issues

        # Check for SNBT syntax (unquoted keys like {Health:20})
        # This is different from valid Bedrock JSON ({"key":"value"})
        if is_snbt_syntax(context.line):
            # Only flag for commands where SNBT would be problematic
            nbt_commands = {'summon', 'setblock', 'fill', 'execute', 'replaceitem'}

            if cmd in nbt_commands:
                issues.append(self.create_issue(
                    context,
                    "SNBT syntax (unquoted keys) is not supported in Bedrock",
                    suggestion="Bedrock does not support NBT data on entities/blocks"
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
