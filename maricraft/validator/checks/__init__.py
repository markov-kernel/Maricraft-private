"""
Validation checks for Bedrock mcfunction files.

This module contains the base Check class and check registry.
Individual checks are implemented in separate modules:
- java_only.py: Java-only commands, NBT syntax, effect syntax
- blocks.py: Block name validation
- modern_java.py: Macros, 1.20.5+ components
- bedrock_syntax.py: Selector args, execute syntax, line length
"""

from abc import ABC, abstractmethod
from typing import List, Type, Dict

from ..models import Issue, Severity, Token, ValidationContext


class Check(ABC):
    """
    Base class for all validation checks.

    Subclasses must implement:
    - code: str - Error code (e.g., "JAVA_COMMAND")
    - severity: Severity - ERROR or WARNING
    - check() - The actual validation logic
    """

    code: str
    severity: Severity
    description: str = ""

    @abstractmethod
    def check(self, tokens: List[Token], context: ValidationContext) -> List[Issue]:
        """
        Run the check against tokenized command.

        Args:
            tokens: Tokenized command line
            context: Validation context with line info and settings

        Returns:
            List of issues found (empty if none)
        """
        pass

    def should_skip(self, context: ValidationContext) -> bool:
        """
        Check if this check should be skipped for the given context.

        Override to skip checks in safe contexts (e.g., inside tellraw).

        Returns:
            True if check should be skipped
        """
        # Skip if this check's code is in the ignore list
        if self.code in context.ignore_codes:
            return True
        return False

    def create_issue(
        self,
        context: ValidationContext,
        message: str,
        suggestion: str = None
    ) -> Issue:
        """Helper to create an Issue with this check's code and severity."""
        return Issue(
            line_num=context.line_num,
            line=context.line,
            severity=self.severity,
            code=self.code,
            message=message,
            suggestion=suggestion
        )


class CheckRegistry:
    """Registry of all validation checks."""

    def __init__(self):
        self._checks: Dict[str, Check] = {}

    def register(self, check: Check) -> None:
        """Register a check instance."""
        self._checks[check.code] = check

    def get(self, code: str) -> Check:
        """Get a check by code."""
        return self._checks.get(code)

    def all_checks(self) -> List[Check]:
        """Get all registered checks."""
        return list(self._checks.values())

    def run_all(
        self,
        tokens: List[Token],
        context: ValidationContext
    ) -> List[Issue]:
        """Run all registered checks and collect issues."""
        issues = []
        for check in self._checks.values():
            if not check.should_skip(context):
                issues.extend(check.check(tokens, context))
        return issues


# Global registry instance
registry = CheckRegistry()


def register_check(check_class: Type[Check]) -> Type[Check]:
    """Decorator to register a check class."""
    registry.register(check_class())
    return check_class
