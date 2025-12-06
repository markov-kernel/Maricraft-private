"""
Bedrock-specific syntax validation checks.

This module detects:
- LINE_TOO_LONG: Commands exceeding 256 character limit
- EXECUTE_DEPTH: Deeply nested execute chains (warning)
- JAVA_EXECUTE: Java-only execute subcommands (store, if data, if predicate)
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
