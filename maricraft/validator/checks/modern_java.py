"""
Checks for modern Java Edition syntax (1.20.2+).

This module detects:
- MACRO_SYNTAX: Function macros $(...) that are Java-only
- COMPONENT_SYNTAX: Java 1.20.5+ item component syntax item[key=val]
"""

import re
from typing import List

from ..models import Issue, Token, TokenType, Severity, ValidationContext
from ..tokenizer import get_tokens_outside_quotes
from . import Check, register_check


@register_check
class MacroSyntaxCheck(Check):
    """Check for Java function macros."""

    code = "MACRO_SYNTAX"
    severity = Severity.ERROR
    description = "Detects function macros $(...) which are Java-only"

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        # Look for MACRO tokens
        macro_tokens = [t for t in tokens if t.type == TokenType.MACRO]

        for macro_token in macro_tokens:
            # Only report if outside quotes
            if not macro_token.is_in_quote:
                issues.append(self.create_issue(
                    context,
                    f"Function macros {macro_token.value} are Java-only (1.20.2+)",
                    suggestion="Remove macro syntax or use alternative approach"
                ))

        return issues


@register_check
class ComponentSyntaxCheck(Check):
    """Check for Java 1.20.5+ item component syntax."""

    code = "COMPONENT_SYNTAX"
    severity = Severity.ERROR
    description = "Detects Java 1.20.5+ item component syntax [key=val]"

    # Pattern for item[component=value] syntax
    # Must not be a selector (@a[...])
    COMPONENT_PATTERN = re.compile(r'(?<!@)(?<!@[aepsr])\b\w+\[[^\]]*\w+=[^\]]+\]')

    # Commands that use items
    ITEM_COMMANDS = {'give', 'replaceitem', 'clear', 'loot'}

    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        issues = []

        cmd = context.command_name.lower()

        # Only check item-related commands
        if cmd not in self.ITEM_COMMANDS:
            return issues

        # Get tokens outside quotes
        outside_tokens = get_tokens_outside_quotes(tokens)

        # Look for identifier tokens followed by bracket tokens
        # This indicates item[...] syntax
        for i, token in enumerate(outside_tokens):
            if token.type == TokenType.IDENTIFIER:
                # Check if next token is a bracket
                if i + 1 < len(outside_tokens):
                    next_token = outside_tokens[i + 1]
                    if next_token.type == TokenType.BRACKET_OPEN:
                        # This looks like item[...] component syntax
                        # But we need to be careful not to flag block states

                        # Check if it contains = which indicates component syntax
                        # Block states use : instead
                        bracket_content = self._get_bracket_content(outside_tokens, i + 1)
                        if bracket_content and '=' in bracket_content:
                            issues.append(self.create_issue(
                                context,
                                f"Item component syntax '{token.value}[...]' is Java 1.20.5+ only",
                                suggestion="Use NBT syntax or Bedrock-equivalent commands"
                            ))
                            break  # One issue per line is enough

        return issues

    def _get_bracket_content(self, tokens: List[Token], start_idx: int) -> str:
        """Extract content between brackets starting at start_idx."""
        if start_idx >= len(tokens) or tokens[start_idx].type != TokenType.BRACKET_OPEN:
            return ""

        content = []
        depth = 0

        for i in range(start_idx, len(tokens)):
            token = tokens[i]
            if token.type == TokenType.BRACKET_OPEN:
                depth += 1
            elif token.type == TokenType.BRACKET_CLOSE:
                depth -= 1
                if depth == 0:
                    break
            content.append(token.value)

        return ''.join(content)
