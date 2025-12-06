"""
Data models for the Bedrock mcfunction validator.

This module contains the core dataclasses used throughout the validator:
- Severity: Error levels (ERROR, WARNING)
- Issue: A single validation issue found in a file
- ValidationResult: Result of validating a single file
- Token: A lexical token from the tokenizer
- ValidationContext: Context passed to checks for contextual validation
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Set


class Severity(str, Enum):
    """Severity level of a validation issue."""
    ERROR = "error"
    WARNING = "warning"


class TokenType(Enum):
    """Types of tokens produced by the tokenizer."""
    COMMAND = "command"              # /give, /summon, etc.
    SELECTOR = "selector"            # @s, @a[...], etc.
    COORDINATE = "coordinate"        # ~5, ^0, 100
    NBT_OPEN = "nbt_open"            # {
    NBT_CLOSE = "nbt_close"          # }
    BRACKET_OPEN = "bracket_open"    # [
    BRACKET_CLOSE = "bracket_close"  # ]
    STRING = "string"                # Quoted content
    IDENTIFIER = "identifier"        # Block names, item names
    NUMBER = "number"                # Numeric literals
    COLON = "colon"                  # :
    COMMA = "comma"                  # ,
    EQUALS = "equals"                # =
    MACRO = "macro"                  # $(...) patterns
    WHITESPACE = "whitespace"        # Spaces
    COMMENT = "comment"              # # lines
    RAW = "raw"                      # Unparsed content (fallback)


@dataclass
class Token:
    """A lexical token from command parsing."""
    type: TokenType
    value: str
    start: int          # Character position in line
    end: int
    is_in_quote: bool = False   # True if inside quoted string
    brace_depth: int = 0        # Nesting level of braces
    bracket_depth: int = 0      # Nesting level of brackets


@dataclass
class Issue:
    """A validation issue found in a mcfunction file."""
    line_num: int
    line: str
    severity: Severity
    code: str
    message: str
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        sev = "ERROR" if self.severity == Severity.ERROR else "WARN"
        result = f"[{sev}] Line {self.line_num}: {self.message} [{self.code}]"
        if self.suggestion:
            result += f"\n  Suggestion: {self.suggestion}"
        return result


@dataclass
class ValidationResult:
    """Result of validating a single mcfunction file."""
    file: Path
    issues: List[Issue] = field(default_factory=list)
    encoding_used: Optional[str] = None

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


@dataclass
class ValidationContext:
    """Context passed to all checks for contextual validation."""
    line: str
    line_num: int
    tokens: List[Token]
    ignore_codes: Set[str] = field(default_factory=set)
    command_name: str = ""           # Top-level command (e.g., "tellraw", "give")
    is_safe_context: bool = False    # Inside tellraw, say, title (text context)
    execute_depth: int = 0           # Nesting level of execute chains

    def has_token_type(self, token_type: TokenType) -> bool:
        """Check if any token has the given type."""
        return any(t.type == token_type for t in self.tokens)

    def get_tokens_of_type(self, token_type: TokenType) -> List[Token]:
        """Get all tokens of a given type."""
        return [t for t in self.tokens if t.type == token_type]
