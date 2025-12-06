"""
Bedrock mcfunction Validator - Backward Compatibility Shim

This module re-exports from the new maricraft.validator package
for backward compatibility with existing imports.

The actual implementation is now in maricraft/validator/ package.

Usage:
    python -m maricraft.validator [path] [--json] [--strict] [--ignore CODE]
"""

# Re-export everything from the new validator package
from maricraft.validator import (
    # Models
    Severity,
    TokenType,
    Token,
    Issue,
    ValidationResult,
    ValidationContext,
    # Tokenizer
    Tokenizer,
    tokenize,
    get_command_name,
    has_nbt_structure,
    get_tokens_outside_quotes,
    find_selectors,
    find_identifiers,
    # Config
    BedrockKnowledge,
    ENCODING_FALLBACK,
    load_block_list,
    # Parser
    ParsedCommand,
    parse_command,
    create_validation_context,
    parse_inline_ignores,
    extract_selector_args,
    get_all_commands_in_line,
    # Checks
    Check,
    CheckRegistry,
    registry,
    register_check,
    # Main validator
    BedrockValidator,
    validate_file,
    validate_command,
)

# Re-export formatting functions from __main__
from maricraft.validator.__main__ import (
    format_results_text,
    format_results_json,
    main,
)

__all__ = [
    # Models
    'Severity',
    'TokenType',
    'Token',
    'Issue',
    'ValidationResult',
    'ValidationContext',
    # Tokenizer
    'Tokenizer',
    'tokenize',
    'get_command_name',
    'has_nbt_structure',
    'get_tokens_outside_quotes',
    'find_selectors',
    'find_identifiers',
    # Config
    'BedrockKnowledge',
    'ENCODING_FALLBACK',
    'load_block_list',
    # Parser
    'ParsedCommand',
    'parse_command',
    'create_validation_context',
    'parse_inline_ignores',
    'extract_selector_args',
    'get_all_commands_in_line',
    # Checks
    'Check',
    'CheckRegistry',
    'registry',
    'register_check',
    # Main validator
    'BedrockValidator',
    'validate_file',
    'validate_command',
    # Formatting
    'format_results_text',
    'format_results_json',
    'main',
]


if __name__ == "__main__":
    main()
