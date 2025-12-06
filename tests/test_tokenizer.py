"""
Unit tests for the tokenizer module.

Tests cover:
- Basic tokenization
- Quote handling (single, double, nested)
- Escape sequences
- Brace/bracket depth tracking
- Selectors (@s, @a[...])
- Coordinates (~, ^, absolute)
- Macros $(...)
- Edge cases and regression tests
"""

import pytest
from maricraft.validator.tokenizer import (
    Tokenizer, tokenize, get_command_name,
    has_nbt_structure, get_tokens_outside_quotes,
    find_selectors, find_identifiers
)
from maricraft.validator.models import TokenType


class TestBasicTokenization:
    """Test basic tokenization functionality."""

    def test_simple_command(self):
        """Simple command should produce COMMAND token."""
        tokens = tokenize("give")
        assert len(tokens) >= 1
        assert tokens[0].type == TokenType.COMMAND
        assert tokens[0].value == "give"

    def test_command_with_slash(self):
        """Command with leading / should include it."""
        tokens = tokenize("/give")
        assert tokens[0].type == TokenType.COMMAND
        assert tokens[0].value == "/give"

    def test_command_with_selector(self):
        """Command with selector should tokenize both."""
        tokens = tokenize("give @s")
        non_ws = [t for t in tokens if t.type != TokenType.WHITESPACE]
        assert non_ws[0].type == TokenType.COMMAND
        assert non_ws[1].type == TokenType.SELECTOR
        assert non_ws[1].value == "@s"

    def test_selector_with_arguments(self):
        """Selector with arguments should be one token."""
        tokens = tokenize("kill @e[type=zombie]")
        non_ws = [t for t in tokens if t.type != TokenType.WHITESPACE]
        selector_tokens = [t for t in non_ws if t.type == TokenType.SELECTOR]
        assert len(selector_tokens) == 1
        assert selector_tokens[0].value == "@e[type=zombie]"


class TestQuoteHandling:
    """Test quote handling - critical for preventing false positives."""

    def test_double_quoted_string(self):
        """Double-quoted strings should be marked as in_quote."""
        tokens = tokenize('say "Hello World"')
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) == 1
        assert string_tokens[0].is_in_quote
        assert '"Hello World"' in string_tokens[0].value

    def test_single_quoted_string(self):
        """Single-quoted strings should also work."""
        tokens = tokenize("say 'Hello World'")
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) == 1
        assert string_tokens[0].is_in_quote

    def test_command_inside_quotes_not_detected(self):
        """Commands inside quotes should NOT be detected as commands."""
        # This is the critical false positive test!
        tokens = tokenize('tellraw @a {"text":"Use /data get"}')

        # Find command tokens
        command_tokens = [t for t in tokens if t.type == TokenType.COMMAND]

        # Only 'tellraw' should be a command, not '/data'
        command_values = [t.value.lower().lstrip('/') for t in command_tokens]
        assert 'tellraw' in command_values
        assert 'data' not in command_values

    def test_nested_quotes(self):
        """Nested quotes like CustomName should be handled."""
        tokens = tokenize("summon sheep ~ ~ ~ {CustomName:'\"jeb_\"'}")
        # Should not crash and should have string token
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) >= 1

    def test_escaped_quotes(self):
        """Escaped quotes inside strings."""
        tokens = tokenize('say "He said \\"hello\\""')
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) == 1
        # The escaped quotes should be inside the string
        assert '\\"' in string_tokens[0].value


class TestBraceTracking:
    """Test brace depth tracking for NBT."""

    def test_simple_nbt(self):
        """Simple NBT should track brace depth."""
        tokens = tokenize("summon zombie ~ ~ ~ {Health:20}")
        open_braces = [t for t in tokens if t.type == TokenType.NBT_OPEN]
        close_braces = [t for t in tokens if t.type == TokenType.NBT_CLOSE]
        assert len(open_braces) == 1
        assert len(close_braces) == 1

    def test_nested_nbt(self):
        """Nested NBT should count all braces."""
        tokens = tokenize("give @s sword{display:{Name:'Test'}}")
        open_braces = [t for t in tokens if t.type == TokenType.NBT_OPEN]
        close_braces = [t for t in tokens if t.type == TokenType.NBT_CLOSE]
        assert len(open_braces) == 2
        assert len(close_braces) == 2

    def test_deeply_nested_nbt(self):
        """Deeply nested NBT from firework command."""
        line = "summon firework_rocket ~ ~1 ~ {LifeTime:20,FireworksItem:{id:\"x\",components:{\"minecraft:fireworks\":{explosions:[{}]}}}}"
        tokens = tokenize(line)
        open_braces = [t for t in tokens if t.type == TokenType.NBT_OPEN]
        close_braces = [t for t in tokens if t.type == TokenType.NBT_CLOSE]
        # Should have balanced braces
        assert len(open_braces) == len(close_braces)

    def test_has_nbt_structure(self):
        """has_nbt_structure should detect NBT."""
        tokens_with_nbt = tokenize("summon zombie ~ ~ ~ {Health:20}")
        tokens_without_nbt = tokenize("give @s diamond 1")

        assert has_nbt_structure(tokens_with_nbt)
        assert not has_nbt_structure(tokens_without_nbt)


class TestCoordinates:
    """Test coordinate tokenization."""

    def test_relative_coordinates(self):
        """~ coordinates should be tokenized."""
        tokens = tokenize("tp @s ~10 ~0 ~-5")
        coord_tokens = [t for t in tokens if t.type == TokenType.COORDINATE]
        assert len(coord_tokens) == 3

    def test_caret_coordinates(self):
        """^ coordinates should be tokenized."""
        tokens = tokenize("tp @s ^0 ^0 ^10")
        coord_tokens = [t for t in tokens if t.type == TokenType.COORDINATE]
        assert len(coord_tokens) == 3

    def test_absolute_coordinates(self):
        """Absolute coordinates should be tokenized."""
        tokens = tokenize("tp @s 100 64 -200")
        coord_tokens = [t for t in tokens if t.type == TokenType.COORDINATE]
        assert len(coord_tokens) == 3


class TestMacros:
    """Test macro detection."""

    def test_simple_macro(self):
        """$(var) should be detected as MACRO."""
        tokens = tokenize("say $(message)")
        macro_tokens = [t for t in tokens if t.type == TokenType.MACRO]
        assert len(macro_tokens) == 1
        assert macro_tokens[0].value == "$(message)"

    def test_macro_in_command(self):
        """Macro in command should be detected."""
        tokens = tokenize("give @s $(item) $(count)")
        macro_tokens = [t for t in tokens if t.type == TokenType.MACRO]
        assert len(macro_tokens) == 2


class TestHelperFunctions:
    """Test helper functions."""

    def test_get_command_name(self):
        """get_command_name should return command without /."""
        tokens = tokenize("/give @s diamond")
        assert get_command_name(tokens) == "give"

    def test_get_command_name_no_slash(self):
        """get_command_name should work without /."""
        tokens = tokenize("give @s diamond")
        assert get_command_name(tokens) == "give"

    def test_get_tokens_outside_quotes(self):
        """Should filter out quoted tokens."""
        tokens = tokenize('tellraw @a {"text":"Hello"}')
        outside = get_tokens_outside_quotes(tokens)
        # String token should be filtered out
        assert not any(t.type == TokenType.STRING for t in outside)

    def test_find_selectors(self):
        """Should find all selector tokens."""
        tokens = tokenize("execute as @a at @s run tp @s ~ ~1 ~")
        selectors = find_selectors(tokens)
        assert len(selectors) == 3

    def test_find_identifiers(self):
        """Should find identifier tokens."""
        tokens = tokenize("setblock ~ ~ ~ stone_bricks")
        identifiers = find_identifiers(tokens)
        assert any("stone_bricks" in t.value for t in identifiers)


class TestEdgeCases:
    """Test edge cases and potential crash scenarios."""

    def test_empty_line(self):
        """Empty line should return empty list."""
        tokens = tokenize("")
        assert tokens == []

    def test_comment_only(self):
        """Comment line should have COMMENT token."""
        tokens = tokenize("# This is a comment")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.COMMENT

    def test_unclosed_quote(self):
        """Unclosed quote should not crash."""
        tokens = tokenize('say "Hello')
        # Should still produce tokens without crashing
        assert len(tokens) >= 1

    def test_unclosed_brace(self):
        """Unclosed brace should not crash."""
        tokens = tokenize("summon zombie ~ ~ ~ {Health:20")
        assert len(tokens) >= 1

    def test_only_whitespace(self):
        """Whitespace-only line should work."""
        tokens = tokenize("   ")
        assert len(tokens) >= 1
        assert all(t.type == TokenType.WHITESPACE for t in tokens)

    def test_very_long_line(self):
        """Very long line should not crash."""
        long_line = "fill " + " ".join(["~0"] * 100) + " stone"
        tokens = tokenize(long_line)
        assert len(tokens) > 0

    def test_special_characters_in_string(self):
        """Special characters in strings should work."""
        tokens = tokenize('tellraw @a {"text":"[!@#$%^&*()]"}')
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) >= 1


class TestRegressionCases:
    """Regression tests for specific bugs or edge cases found in real files."""

    def test_tellraw_with_command_mention(self):
        """tellraw mentioning commands should not flag them."""
        # This was the original false positive case
        line = 'tellraw @a {"text":"Use /data get to see NBT data"}'
        tokens = tokenize(line)

        # Get non-quoted command tokens
        command_tokens = [t for t in tokens
                         if t.type == TokenType.COMMAND and not t.is_in_quote]

        # Only tellraw should be detected as a command
        assert len(command_tokens) == 1
        assert command_tokens[0].value == "tellraw"

    def test_particle_with_dust_nbt(self):
        """Particle command with dust NBT."""
        line = "particle dust{color:[1.0,0.0,0.0],scale:2} ~ ~2 ~ 3 3 3 0 50"
        tokens = tokenize(line)
        # Should parse without error
        assert len(tokens) > 0

    def test_execute_chain(self):
        """Execute chain should tokenize correctly."""
        line = "execute at @s run tp @s ^0 ^0 ^100"
        tokens = tokenize(line)

        # Tokenizer only detects first command - execute chain parsing is done by parser
        command_tokens = [t for t in tokens if t.type == TokenType.COMMAND]
        cmd_names = [t.value for t in command_tokens]
        assert "execute" in cmd_names

        # 'tp' will be detected as identifier by tokenizer (parser handles execute chains)
        identifiers = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        id_names = [t.value for t in identifiers]
        assert "tp" in id_names

    def test_complex_selector(self):
        """Complex selector with multiple arguments."""
        line = "kill @e[type=#minecraft:raiders,distance=..100]"
        tokens = tokenize(line)

        selector_tokens = find_selectors(tokens)
        assert len(selector_tokens) == 1
        # Entire selector should be one token
        assert "type=#minecraft:raiders" in selector_tokens[0].value
