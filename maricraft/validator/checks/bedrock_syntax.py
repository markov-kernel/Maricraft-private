"""
Bedrock-specific syntax validation checks.

This module detects:
- LINE_TOO_LONG: Commands exceeding 256 character limit
- EXECUTE_DEPTH: Deeply nested execute chains (warning)
"""

from typing import List

from ..models import Issue, Token, Severity, ValidationContext
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
