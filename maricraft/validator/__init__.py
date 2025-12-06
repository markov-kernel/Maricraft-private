"""
Bedrock mcfunction Validator

A robust, modular validation tool for Minecraft Bedrock Edition .mcfunction files.

This package validates mcfunction files for Bedrock Edition compatibility,
catching Java-only syntax before it causes silent failures in-game.

Usage:
    # CLI
    python -m maricraft.validator [path] [--json] [--strict] [--ignore CODE]

    # Programmatic
    from maricraft.validator import BedrockValidator, validate_file
    result = validate_file("path/to/file.mcfunction")

Key Features:
    - Tokenizer-based parsing (no false positives from quoted strings)
    - Recursive execute chain parsing
    - Encoding fallback (UTF-8 → Latin-1 → CP1252)
    - Modern Java syntax detection (macros, 1.20.5+ components)
    - Context-aware validation (skips safe commands like tellraw)
"""

from .models import (
    Severity,
    TokenType,
    Token,
    Issue,
    ValidationResult,
    ValidationContext,
)

from .tokenizer import (
    Tokenizer,
    tokenize,
    get_command_name,
    has_nbt_structure,
    get_tokens_outside_quotes,
    find_selectors,
    find_identifiers,
)

from .config import (
    BedrockKnowledge,
    ENCODING_FALLBACK,
    load_block_list,
)

from .parser import (
    ParsedCommand,
    parse_command,
    create_validation_context,
    parse_inline_ignores,
    extract_selector_args,
    get_all_commands_in_line,
)

from .checks import (
    Check,
    CheckRegistry,
    registry,
    register_check,
)

# Import check modules to register all checks
from .checks import java_only, blocks, modern_java, bedrock_syntax


class BedrockValidator:
    """
    Main validator class for Bedrock mcfunction files.

    Usage:
        validator = BedrockValidator()
        result = validator.validate_file(Path("my_function.mcfunction"))

        # Or validate a directory
        results = validator.validate_directory(Path("functions/"))
    """

    def __init__(
        self,
        blocks_file: Path = None,
        ignore_codes: set = None,
        encoding_fallback: list = None,
    ):
        """
        Initialize the validator.

        Args:
            blocks_file: Optional path to custom block list file
            ignore_codes: Set of error codes to ignore globally
            encoding_fallback: List of encodings to try when reading files
        """
        self.blocks = load_block_list(blocks_file)
        self.ignore_codes = ignore_codes or set()
        self.encoding_fallback = encoding_fallback or ENCODING_FALLBACK

    def validate_file(self, path: Path) -> ValidationResult:
        """
        Validate a single .mcfunction file.

        Args:
            path: Path to the file to validate

        Returns:
            ValidationResult with all issues found
        """
        result = ValidationResult(file=path)

        # Read file with encoding fallback
        try:
            lines, encoding = self._read_file(path)
            result.encoding_used = encoding
        except Exception as e:
            result.issues.append(Issue(
                line_num=0,
                line="",
                severity=Severity.ERROR,
                code="FILE_ERROR",
                message=f"Could not read file: {e}"
            ))
            return result

        # Validate each line
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue

            # Parse inline ignores
            clean_line, line_ignores = parse_inline_ignores(stripped)
            all_ignores = self.ignore_codes | line_ignores

            # Skip if line is now empty after removing ignore comment
            if not clean_line:
                continue

            # Tokenize and validate
            tokens = tokenize(clean_line, line_num)
            context = create_validation_context(
                clean_line, line_num, tokens, all_ignores
            )

            # Run all checks
            issues = registry.run_all(tokens, context)
            result.issues.extend(issues)

        return result

    def validate_directory(self, path: Path) -> list:
        """
        Validate all .mcfunction files in a directory recursively.

        Args:
            path: Directory path to scan

        Returns:
            List of ValidationResult objects
        """
        results = []
        for mcfunction_file in path.rglob('*.mcfunction'):
            results.append(self.validate_file(mcfunction_file))
        return results

    def validate_command(self, command: str, line_num: int = 1) -> list:
        """
        Validate a single command string.

        Args:
            command: The command to validate
            line_num: Line number for error reporting

        Returns:
            List of Issue objects
        """
        tokens = tokenize(command, line_num)
        context = create_validation_context(
            command, line_num, tokens, self.ignore_codes
        )
        return registry.run_all(tokens, context)

    def _read_file(self, path: Path) -> tuple:
        """
        Read a file with encoding fallback.

        Returns:
            Tuple of (lines, encoding_used)
        """
        for encoding in self.encoding_fallback:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    return f.readlines(), encoding
            except UnicodeDecodeError:
                continue

        # If all encodings fail, raise error
        raise ValueError(
            f"Could not decode {path} with any of: {self.encoding_fallback}"
        )


def validate_file(path: Path, **kwargs) -> ValidationResult:
    """
    Convenience function to validate a single file.

    Args:
        path: Path to the file to validate
        **kwargs: Arguments passed to BedrockValidator

    Returns:
        ValidationResult
    """
    return BedrockValidator(**kwargs).validate_file(path)


def validate_command(command: str, **kwargs) -> list:
    """
    Convenience function to validate a single command.

    Args:
        command: The command to validate
        **kwargs: Arguments passed to BedrockValidator

    Returns:
        List of Issue objects
    """
    return BedrockValidator(**kwargs).validate_command(command)


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
]
