"""
State-machine tokenizer for Minecraft commands.

This tokenizer correctly handles:
- Quoted strings (preserves content, marks with is_in_quote)
- Nested braces and brackets (tracks depth)
- Escape sequences
- Selectors (@s, @a[...])
- Coordinates (~, ^, absolute)
- Macros ($(var))

The key feature is that tokens inside quoted strings are marked with
is_in_quote=True, allowing downstream checks to skip false positives.
"""

import re
from typing import List, Optional, Tuple
from .models import Token, TokenType


class Tokenizer:
    """
    State-machine tokenizer for Minecraft command syntax.

    Respects quotes to prevent false positives (e.g., /data inside tellraw text).
    """

    # Regex patterns for different token types
    COMMAND_PATTERN = re.compile(r'^/?([a-zA-Z_][a-zA-Z0-9_]*)')
    SELECTOR_PATTERN = re.compile(r'^@[aepsr](\[.*?\])?')
    COORDINATE_PATTERN = re.compile(r'^([~^]?-?\d*\.?\d+|[~^])')
    NUMBER_PATTERN = re.compile(r'^-?\d+\.?\d*[bBsSlLfFdD]?')
    IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_:\.]*')
    MACRO_PATTERN = re.compile(r'^\$\([^)]+\)')

    def __init__(self, line: str, line_num: int = 1):
        """Initialize tokenizer with a command line."""
        self.line = line
        self.line_num = line_num
        self.pos = 0
        self.tokens: List[Token] = []

        # State tracking
        self.in_quote = False
        self.quote_char: Optional[str] = None
        self.brace_depth = 0
        self.bracket_depth = 0

    def tokenize(self) -> List[Token]:
        """
        Tokenize the command line into a list of tokens.

        Returns:
            List of Token objects with position and context information.
        """
        self.tokens = []
        self.pos = 0
        self.in_quote = False
        self.quote_char = None
        self.brace_depth = 0
        self.bracket_depth = 0

        while self.pos < len(self.line):
            # Skip whitespace (but track it)
            if self._skip_whitespace():
                continue

            # Check for comments
            if self.line[self.pos] == '#' and not self.in_quote:
                self._read_comment()
                break

            # Handle quotes
            if self.line[self.pos] in '"\'':
                self._read_string()
                continue

            # Handle braces (NBT)
            if self.line[self.pos] == '{' and not self.in_quote:
                self._add_token(TokenType.NBT_OPEN, '{')
                self.brace_depth += 1
                self.pos += 1
                continue

            if self.line[self.pos] == '}' and not self.in_quote:
                self._add_token(TokenType.NBT_CLOSE, '}')
                self.brace_depth = max(0, self.brace_depth - 1)
                self.pos += 1
                continue

            # Handle brackets (selectors, components)
            if self.line[self.pos] == '[' and not self.in_quote:
                self._add_token(TokenType.BRACKET_OPEN, '[')
                self.bracket_depth += 1
                self.pos += 1
                continue

            if self.line[self.pos] == ']' and not self.in_quote:
                self._add_token(TokenType.BRACKET_CLOSE, ']')
                self.bracket_depth = max(0, self.bracket_depth - 1)
                self.pos += 1
                continue

            # Handle special characters
            if self.line[self.pos] == ':':
                self._add_token(TokenType.COLON, ':')
                self.pos += 1
                continue

            if self.line[self.pos] == ',':
                self._add_token(TokenType.COMMA, ',')
                self.pos += 1
                continue

            if self.line[self.pos] == '=':
                self._add_token(TokenType.EQUALS, '=')
                self.pos += 1
                continue

            # Check for macros $(...)
            if self.line[self.pos] == '$':
                if self._read_macro():
                    continue

            # Check for selectors (@s, @a[...])
            if self.line[self.pos] == '@':
                if self._read_selector():
                    continue

            # Check for coordinates (~, ^, numbers)
            if self.line[self.pos] in '~^' or (self.line[self.pos].isdigit() or
                                                 (self.line[self.pos] == '-' and
                                                  self.pos + 1 < len(self.line) and
                                                  self.line[self.pos + 1].isdigit())):
                if self._read_coordinate():
                    continue

            # Check for command at start of line
            if self.pos == 0 or (len(self.tokens) == 0):
                if self._read_command():
                    continue

            # Read identifier (block names, item names, etc.)
            if self._read_identifier():
                continue

            # Fallback: read single character as raw
            self._add_token(TokenType.RAW, self.line[self.pos])
            self.pos += 1

        return self.tokens

    def _skip_whitespace(self) -> bool:
        """Skip whitespace characters. Returns True if any was skipped."""
        if self.pos < len(self.line) and self.line[self.pos].isspace():
            start = self.pos
            while self.pos < len(self.line) and self.line[self.pos].isspace():
                self.pos += 1
            self._add_token(TokenType.WHITESPACE, self.line[start:self.pos])
            return True
        return False

    def _read_comment(self) -> None:
        """Read a comment to end of line."""
        start = self.pos
        self._add_token(TokenType.COMMENT, self.line[start:])
        self.pos = len(self.line)

    def _read_string(self) -> None:
        """
        Read a quoted string, handling escape sequences.

        Sets is_in_quote=True for the string token to mark quoted content.
        """
        start = self.pos
        quote = self.line[self.pos]
        self.pos += 1
        content = [quote]

        while self.pos < len(self.line):
            char = self.line[self.pos]

            # Handle escape sequences
            if char == '\\' and self.pos + 1 < len(self.line):
                content.append(char)
                content.append(self.line[self.pos + 1])
                self.pos += 2
                continue

            # End of string
            if char == quote:
                content.append(char)
                self.pos += 1
                break

            content.append(char)
            self.pos += 1

        self._add_token(TokenType.STRING, ''.join(content), is_in_quote=True)

    def _read_macro(self) -> bool:
        """Read a macro pattern $(...)."""
        match = self.MACRO_PATTERN.match(self.line[self.pos:])
        if match:
            self._add_token(TokenType.MACRO, match.group(0))
            self.pos += len(match.group(0))
            return True
        return False

    def _read_selector(self) -> bool:
        """Read a selector (@s, @a[...], etc.)."""
        if self.pos + 1 >= len(self.line):
            return False

        if self.line[self.pos + 1] not in 'aepsr':
            return False

        start = self.pos
        self.pos += 2  # Skip @ and type character

        # Check for selector arguments [...]
        if self.pos < len(self.line) and self.line[self.pos] == '[':
            depth = 1
            self.pos += 1
            while self.pos < len(self.line) and depth > 0:
                if self.line[self.pos] == '[':
                    depth += 1
                elif self.line[self.pos] == ']':
                    depth -= 1
                elif self.line[self.pos] in '"\'':
                    # Skip quoted content inside selector
                    quote = self.line[self.pos]
                    self.pos += 1
                    while self.pos < len(self.line) and self.line[self.pos] != quote:
                        if self.line[self.pos] == '\\':
                            self.pos += 1
                        self.pos += 1
                self.pos += 1

        self._add_token(TokenType.SELECTOR, self.line[start:self.pos])
        return True

    def _read_coordinate(self) -> bool:
        """Read a coordinate value (~, ^, ~5, ^-3, 100, etc.)."""
        match = self.COORDINATE_PATTERN.match(self.line[self.pos:])
        if match:
            value = match.group(0)
            # Only accept if it looks like a coordinate (starts with ~, ^, or is a number)
            if value.startswith('~') or value.startswith('^') or value.replace('-', '').replace('.', '').isdigit():
                self._add_token(TokenType.COORDINATE, value)
                self.pos += len(value)
                return True
        return False

    def _read_command(self) -> bool:
        """Read a command name (possibly with leading /)."""
        match = self.COMMAND_PATTERN.match(self.line[self.pos:])
        if match:
            full_match = match.group(0)
            self._add_token(TokenType.COMMAND, full_match)
            self.pos += len(full_match)
            return True
        return False

    def _read_identifier(self) -> bool:
        """Read an identifier (block name, item name, etc.)."""
        match = self.IDENTIFIER_PATTERN.match(self.line[self.pos:])
        if match:
            self._add_token(TokenType.IDENTIFIER, match.group(0))
            self.pos += len(match.group(0))
            return True
        return False

    def _add_token(self, token_type: TokenType, value: str, is_in_quote: bool = False) -> None:
        """Add a token to the list with current context."""
        token = Token(
            type=token_type,
            value=value,
            start=self.pos - len(value),
            end=self.pos,
            is_in_quote=is_in_quote or self.in_quote,
            brace_depth=self.brace_depth,
            bracket_depth=self.bracket_depth
        )
        self.tokens.append(token)


def tokenize(line: str, line_num: int = 1) -> List[Token]:
    """
    Convenience function to tokenize a command line.

    Args:
        line: The command line to tokenize.
        line_num: Line number for error reporting.

    Returns:
        List of Token objects.
    """
    return Tokenizer(line, line_num).tokenize()


def get_command_name(tokens: List[Token]) -> Optional[str]:
    """
    Extract the command name from tokenized command.

    Returns the first COMMAND token's value, stripped of leading /.
    """
    for token in tokens:
        if token.type == TokenType.COMMAND:
            return token.value.lstrip('/')
    return None


def has_nbt_structure(tokens: List[Token]) -> bool:
    """Check if the tokens contain NBT structure (braces outside quotes)."""
    for token in tokens:
        if token.type == TokenType.NBT_OPEN and not token.is_in_quote:
            return True
    return False


def get_tokens_outside_quotes(tokens: List[Token]) -> List[Token]:
    """Get only tokens that are outside of quoted strings."""
    return [t for t in tokens if not t.is_in_quote]


def find_selectors(tokens: List[Token]) -> List[Token]:
    """Find all selector tokens."""
    return [t for t in tokens if t.type == TokenType.SELECTOR]


def find_identifiers(tokens: List[Token]) -> List[Token]:
    """Find all identifier tokens (potential block/item names)."""
    return [t for t in tokens if t.type == TokenType.IDENTIFIER]
