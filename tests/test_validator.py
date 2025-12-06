"""
Integration tests for the BedrockValidator.

Tests cover:
- File validation
- Directory validation
- Encoding fallback
- Ignore codes functionality
- CLI interface
"""

import pytest
from pathlib import Path
import tempfile
import os

from maricraft.validator import (
    BedrockValidator,
    ValidationResult,
    validate_file,
    validate_command,
)


class TestBedrockValidator:
    """Integration tests for BedrockValidator class."""

    def test_validate_valid_file(self, tmp_path):
        """Valid mcfunction file should have no issues."""
        # Create a valid mcfunction file
        mcfunction = tmp_path / "test.mcfunction"
        mcfunction.write_text("give @s diamond 64\ntp @s ~ ~10 ~\n")

        validator = BedrockValidator()
        result = validator.validate_file(mcfunction)

        assert result.is_valid
        assert result.error_count == 0
        assert result.file == mcfunction

    def test_validate_file_with_java_command(self, tmp_path):
        """File with Java-only commands should have errors."""
        mcfunction = tmp_path / "test.mcfunction"
        mcfunction.write_text("data get entity @s\n")

        validator = BedrockValidator()
        result = validator.validate_file(mcfunction)

        assert not result.is_valid
        assert result.error_count >= 1
        assert any(i.code == "JAVA_COMMAND" for i in result.issues)

    def test_validate_file_with_ignore_codes(self, tmp_path):
        """Ignored error codes should not produce issues."""
        mcfunction = tmp_path / "test.mcfunction"
        mcfunction.write_text("data get entity @s\n")

        validator = BedrockValidator(ignore_codes={"JAVA_COMMAND"})
        result = validator.validate_file(mcfunction)

        assert result.is_valid
        assert not any(i.code == "JAVA_COMMAND" for i in result.issues)

    def test_validate_directory(self, tmp_path):
        """Directory validation should process all mcfunction files."""
        # Create multiple files
        (tmp_path / "valid.mcfunction").write_text("give @s diamond")
        (tmp_path / "invalid.mcfunction").write_text("data get entity @s")

        validator = BedrockValidator()
        results = validator.validate_directory(tmp_path)

        assert len(results) == 2
        valid_count = sum(1 for r in results if r.is_valid)
        assert valid_count == 1

    def test_validate_command(self):
        """validate_command should work on single commands."""
        issues = validate_command("data get entity @s")
        assert any(i.code == "JAVA_COMMAND" for i in issues)

        issues = validate_command("give @s diamond 64")
        assert not any(i.code == "JAVA_COMMAND" for i in issues)

    def test_encoding_fallback(self, tmp_path):
        """Files with different encodings should be readable."""
        mcfunction = tmp_path / "test.mcfunction"

        # Write with latin-1 encoding
        mcfunction.write_bytes("give @s diamond 64\n".encode('latin-1'))

        validator = BedrockValidator()
        result = validator.validate_file(mcfunction)

        assert result.is_valid
        assert result.encoding_used in ['utf-8', 'latin-1']

    def test_inline_ignore(self, tmp_path):
        """Inline ignore comments should work."""
        mcfunction = tmp_path / "test.mcfunction"
        mcfunction.write_text("data get entity @s  # ignore: JAVA_COMMAND\n")

        validator = BedrockValidator()
        result = validator.validate_file(mcfunction)

        assert result.is_valid
        assert not any(i.code == "JAVA_COMMAND" for i in result.issues)

    def test_comments_are_skipped(self, tmp_path):
        """Comment lines should not be validated."""
        mcfunction = tmp_path / "test.mcfunction"
        mcfunction.write_text("# data get entity @s\ngive @s diamond\n")

        validator = BedrockValidator()
        result = validator.validate_file(mcfunction)

        assert result.is_valid

    def test_empty_file(self, tmp_path):
        """Empty files should be valid."""
        mcfunction = tmp_path / "test.mcfunction"
        mcfunction.write_text("")

        validator = BedrockValidator()
        result = validator.validate_file(mcfunction)

        assert result.is_valid

    def test_nonexistent_file(self):
        """Nonexistent files should produce FILE_ERROR."""
        validator = BedrockValidator()
        result = validator.validate_file(Path("/nonexistent/file.mcfunction"))

        assert not result.is_valid
        assert any(i.code == "FILE_ERROR" for i in result.issues)


class TestValidateMaricraft:
    """Integration tests against actual Maricraft mcfunction files."""

    @pytest.fixture
    def maricraft_functions_path(self):
        """Path to the Maricraft behavior pack functions."""
        path = Path(__file__).parent.parent / "maricraft" / "resources" / "maricraft_behavior" / "functions"
        if not path.exists():
            pytest.skip("Maricraft functions not found")
        return path

    def test_all_maricraft_files_valid(self, maricraft_functions_path):
        """All Maricraft mcfunction files should pass validation."""
        validator = BedrockValidator()
        results = validator.validate_directory(maricraft_functions_path)

        # Count errors
        total_errors = sum(r.error_count for r in results)
        invalid_files = [r.file.name for r in results if not r.is_valid]

        assert total_errors == 0, f"Found errors in: {invalid_files}"

    def test_no_false_positives_in_tellraw(self, maricraft_functions_path):
        """tellraw commands should not produce false positives."""
        validator = BedrockValidator()
        results = validator.validate_directory(maricraft_functions_path)

        # Check that no JAVA_COMMAND errors come from tellraw-related files
        for result in results:
            for issue in result.issues:
                if issue.code == "JAVA_COMMAND":
                    # Make sure this isn't a false positive from a string
                    assert "tellraw" not in issue.line.lower() or issue.line.startswith("tellraw")


class TestConvenienceFunctions:
    """Test convenience function wrappers."""

    def test_validate_file_function(self, tmp_path):
        """validate_file convenience function should work."""
        mcfunction = tmp_path / "test.mcfunction"
        mcfunction.write_text("give @s diamond")

        result = validate_file(mcfunction)
        assert isinstance(result, ValidationResult)
        assert result.is_valid

    def test_validate_command_function(self):
        """validate_command convenience function should work."""
        issues = validate_command("give @s diamond")
        assert isinstance(issues, list)
