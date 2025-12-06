"""
Command parser for Minecraft commands.

This module provides higher-level parsing of tokenized commands:
- Execute chain parsing (recursive execute ... run ... parsing)
- Command context extraction (what command, is it a safe context?)
- Block name extraction from setblock/fill commands
- Selector argument extraction

The parser builds on the tokenizer to provide semantic understanding.
"""

import re
from typing import List, Optional, Tuple, Set
from dataclasses import dataclass

from .models import Token, TokenType, ValidationContext
from .tokenizer import tokenize, get_command_name, find_selectors, find_identifiers
from .config import BedrockKnowledge


@dataclass
class ParsedCommand:
    """Result of parsing a command."""
    command: str                      # Top-level command name
    tokens: List[Token]               # All tokens
    is_execute_chain: bool = False    # Whether this is an execute chain
    execute_depth: int = 0            # Nesting level of execute
    inner_commands: List[str] = None  # Commands inside execute chain
    block_names: List[str] = None     # Block names found (for setblock/fill)
    selectors: List[str] = None       # Selectors found


def parse_command(line: str, line_num: int = 1) -> ParsedCommand:
    """
    Parse a command line into a structured ParsedCommand.

    Args:
        line: The command line to parse
        line_num: Line number for error reporting

    Returns:
        ParsedCommand with extracted information
    """
    tokens = tokenize(line, line_num)
    command = get_command_name(tokens) or ""

    result = ParsedCommand(
        command=command,
        tokens=tokens,
        inner_commands=[],
        block_names=[],
        selectors=[]
    )

    # Extract selectors
    selector_tokens = find_selectors(tokens)
    result.selectors = [t.value for t in selector_tokens]

    # Check if this is an execute chain
    if command.lower() == "execute":
        result.is_execute_chain = True
        result.execute_depth, result.inner_commands = _parse_execute_chain(tokens)

    # Extract block names for relevant commands
    if command.lower() in ('setblock', 'fill', 'testforblock', 'clone'):
        result.block_names = _extract_block_names(tokens, command.lower())

    return result


def _parse_execute_chain(tokens: List[Token]) -> Tuple[int, List[str]]:
    """
    Parse an execute chain to find nested commands.

    Returns:
        Tuple of (execute_depth, list of inner command names)
    """
    depth = 1
    inner_commands = []

    # Find all 'run' keywords and what follows
    # In tokenized form, 'run' will be an identifier
    non_ws_tokens = [t for t in tokens if t.type != TokenType.WHITESPACE]

    i = 0
    while i < len(non_ws_tokens):
        token = non_ws_tokens[i]

        # Look for 'run' identifier
        if token.type == TokenType.IDENTIFIER and token.value.lower() == 'run':
            # Next token after 'run' is the subcommand
            if i + 1 < len(non_ws_tokens):
                next_token = non_ws_tokens[i + 1]
                if next_token.type in (TokenType.COMMAND, TokenType.IDENTIFIER):
                    cmd_name = next_token.value.lstrip('/')
                    inner_commands.append(cmd_name)

                    # Check for nested execute
                    if cmd_name.lower() == 'execute':
                        depth += 1

        i += 1

    return depth, inner_commands


def _extract_block_names(tokens: List[Token], command: str) -> List[str]:
    """
    Extract block names from setblock/fill/testforblock commands.

    Block names appear after coordinates in these commands.
    """
    block_names = []
    non_ws_tokens = [t for t in tokens if t.type != TokenType.WHITESPACE]

    # Skip command token and count coordinates
    # setblock: x y z block
    # fill: x1 y1 z1 x2 y2 z2 block
    # testforblock: x y z block

    coords_needed = 6 if command == 'fill' else 3

    coord_count = 0
    for i, token in enumerate(non_ws_tokens[1:], start=1):  # Skip command
        if token.type == TokenType.COORDINATE:
            coord_count += 1
        elif coord_count >= coords_needed:
            # This should be the block name
            if token.type == TokenType.IDENTIFIER:
                # Clean up the block name
                block_name = token.value.lower().replace('minecraft:', '')
                # Remove state suffix [...]
                if '[' in block_name:
                    block_name = block_name.split('[')[0]
                block_names.append(block_name)
            break

    return block_names


def create_validation_context(
    line: str,
    line_num: int,
    tokens: List[Token],
    ignore_codes: Set[str] = None
) -> ValidationContext:
    """
    Create a ValidationContext from parsed information.

    Args:
        line: Original command line
        line_num: Line number
        tokens: Tokenized line
        ignore_codes: Set of error codes to ignore

    Returns:
        ValidationContext with all context information
    """
    command = get_command_name(tokens) or ""

    # Determine if this is a safe context (inside text commands)
    is_safe = BedrockKnowledge.is_safe_context_command(command)

    # Check for execute chains
    execute_depth = 0
    if command.lower() == "execute":
        execute_depth, _ = _parse_execute_chain(tokens)

    return ValidationContext(
        line=line,
        line_num=line_num,
        tokens=tokens,
        ignore_codes=ignore_codes or set(),
        command_name=command,
        is_safe_context=is_safe,
        execute_depth=execute_depth
    )


def parse_inline_ignores(line: str) -> Tuple[str, Set[str]]:
    """
    Parse inline ignore comments from a line.

    Format: command  # ignore: CODE1, CODE2

    Returns:
        Tuple of (line without ignore comment, set of codes to ignore)
    """
    ignore_codes = set()

    # Look for ignore comment pattern
    match = re.search(r'#\s*ignore:\s*([A-Z_,\s]+)$', line, re.IGNORECASE)
    if match:
        # Extract codes
        codes_str = match.group(1)
        codes = [c.strip().upper() for c in codes_str.split(',')]
        ignore_codes = {c for c in codes if c}

        # Remove the ignore comment from the line
        line = line[:match.start()].rstrip()

    return line, ignore_codes


def extract_selector_args(selector: str) -> List[Tuple[str, str]]:
    """
    Extract argument key-value pairs from a selector.

    Args:
        selector: Full selector string like "@a[type=zombie,distance=..10]"

    Returns:
        List of (key, value) tuples
    """
    args = []

    # Extract content inside brackets
    match = re.match(r'@[aepsr]\[(.*)\]', selector)
    if not match:
        return args

    content = match.group(1)

    # Simple parsing - split by comma, then by equals
    # This is naive but handles most cases
    parts = content.split(',')
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            args.append((key.strip(), value.strip()))

    return args


def get_all_commands_in_line(tokens: List[Token]) -> List[str]:
    """
    Get all command names that appear in a line.

    This includes:
    - The main command
    - Commands after 'run' in execute chains
    - Commands in function calls (if identifiable)

    Returns:
        List of command names (lowercase, without /)
    """
    commands = []

    # Get main command
    main_cmd = get_command_name(tokens)
    if main_cmd:
        commands.append(main_cmd.lower())

    # If execute, parse inner commands
    if main_cmd and main_cmd.lower() == "execute":
        _, inner = _parse_execute_chain(tokens)
        commands.extend([c.lower() for c in inner])

    return commands
