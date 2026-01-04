"""
CLI entry point for the Bedrock mcfunction validator.

Usage:
    python -m maricraft.validator [path] [--json] [--strict] [--ignore CODE,CODE]

Backward compatible with the original validator CLI.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List

from . import BedrockValidator, ValidationResult, Severity


def format_results_text(results: List[ValidationResult], show_valid: bool = False) -> str:
    """Format validation results as human-readable text."""
    output = []
    total_errors = 0
    total_warnings = 0

    for result in results:
        if not result.issues and not show_valid:
            continue

        # Get relative path for display
        rel_path = result.file.name
        try:
            parts = result.file.parts
            if 'functions' in parts:
                idx = parts.index('functions')
                rel_path = '/'.join(parts[idx+1:])
        except Exception:
            pass  # Path parsing failed, use filename only

        if result.issues:
            output.append(f"\n{rel_path}")
            for issue in result.issues:
                severity_str = "ERROR" if issue.severity == Severity.ERROR else "WARN"
                line_preview = issue.line[:60] + '...' if len(issue.line) > 60 else issue.line
                output.append(f"  LINE {issue.line_num}: {line_preview}")
                output.append(f"  {severity_str} [{issue.code}]: {issue.message}")
                if issue.suggestion:
                    output.append(f"  → Suggestion: {issue.suggestion}")
        elif show_valid:
            output.append(f"\n{rel_path}")
            output.append("  [OK] No issues")

        total_errors += result.error_count
        total_warnings += result.warning_count

    valid_count = sum(1 for r in results if r.is_valid)
    output.append(f"\n{'='*50}")
    output.append(f"Summary: {len(results)} files, {valid_count} valid, {total_errors} errors, {total_warnings} warnings")

    return '\n'.join(output)


def format_results_json(results: List[ValidationResult]) -> str:
    """Format validation results as JSON."""
    output = {
        "summary": {
            "total_files": len(results),
            "valid_files": sum(1 for r in results if r.is_valid),
            "total_errors": sum(r.error_count for r in results),
            "total_warnings": sum(r.warning_count for r in results)
        },
        "files": []
    }

    for result in results:
        file_data = {
            "path": str(result.file),
            "is_valid": result.is_valid,
            "encoding": result.encoding_used,
            "issues": [
                {
                    "line": issue.line_num,
                    "severity": issue.severity.value,
                    "code": issue.code,
                    "message": issue.message,
                    "suggestion": issue.suggestion
                }
                for issue in result.issues
            ]
        }
        output["files"].append(file_data)

    return json.dumps(output, indent=2)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Bedrock .mcfunction files for compatibility issues"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="File or directory to validate (default: maricraft behavior pack functions)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--strict", "-s",
        action="store_true",
        help="Exit with error code if any warnings"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Show all files including valid ones"
    )
    parser.add_argument(
        "--ignore", "-i",
        help="Comma-separated list of error codes to ignore (e.g., JAVA_BLOCK,NBT_SYNTAX)"
    )
    parser.add_argument(
        "--encoding",
        help="Comma-separated list of encodings to try (default: utf-8,latin-1,cp1252)"
    )

    args = parser.parse_args()

    # Determine path
    if args.path:
        path = Path(args.path)
    else:
        # Default to Bedrock behavior pack functions
        path = Path(__file__).parent.parent / 'resources' / 'maricraft_behavior' / 'functions'

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(2)

    # Parse ignore codes
    ignore_codes = set()
    if args.ignore:
        ignore_codes = {code.strip().upper() for code in args.ignore.split(',')}

    # Parse encodings
    encodings = None
    if args.encoding:
        encodings = [e.strip() for e in args.encoding.split(',')]

    # Create validator
    validator = BedrockValidator(
        ignore_codes=ignore_codes,
        encoding_fallback=encodings
    )

    # Run validation
    if path.is_file():
        results = [validator.validate_file(path)]
    else:
        results = validator.validate_directory(path)

    # Output results
    if args.json:
        print(format_results_json(results))
    else:
        print("Validating Bedrock mcfunction files...")
        print(format_results_text(results, show_valid=args.all))

    # Exit code
    has_errors = any(not r.is_valid for r in results)
    has_warnings = any(r.warning_count > 0 for r in results)

    if has_errors:
        sys.exit(1)
    elif args.strict and has_warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
