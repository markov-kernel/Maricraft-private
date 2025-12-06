"""
Unit tests for validation checks.

Tests cover:
- Java-only command detection
- NBT syntax detection
- Effect syntax detection
- Selector argument validation
- Block name validation
- Macro and component syntax detection
- Line length and execute depth warnings
"""

import pytest
from maricraft.validator.tokenizer import tokenize
from maricraft.validator.parser import create_validation_context
from maricraft.validator.models import Severity

# Import checks to register them
from maricraft.validator.checks import java_only, blocks, modern_java, bedrock_syntax
from maricraft.validator.checks import registry


def run_checks(line: str, line_num: int = 1, ignore_codes: set = None) -> list:
    """Helper to run all checks on a line and return issues."""
    tokens = tokenize(line, line_num)
    context = create_validation_context(line, line_num, tokens, ignore_codes or set())
    return registry.run_all(tokens, context)


class TestJavaCommandCheck:
    """Test Java-only command detection."""

    def test_java_only_command_data(self):
        """'data' command should be flagged."""
        issues = run_checks("data get entity @s")
        assert any(i.code == "JAVA_COMMAND" for i in issues)

    def test_java_only_command_loot(self):
        """'loot' command should be flagged."""
        issues = run_checks("loot give @s loot minecraft:chests/desert_pyramid")
        assert any(i.code == "JAVA_COMMAND" for i in issues)

    def test_java_only_command_attribute(self):
        """'attribute' command should be flagged."""
        issues = run_checks("attribute @s minecraft:generic.max_health base set 40")
        assert any(i.code == "JAVA_COMMAND" for i in issues)

    def test_valid_bedrock_command(self):
        """Valid Bedrock commands should not be flagged."""
        issues = run_checks("give @s diamond 64")
        assert not any(i.code == "JAVA_COMMAND" for i in issues)

    def test_command_in_tellraw_not_flagged(self):
        """Commands mentioned in tellraw text should NOT be flagged."""
        # This is the critical false positive test
        issues = run_checks('tellraw @a {"text":"Use /data get to see NBT"}')
        assert not any(i.code == "JAVA_COMMAND" for i in issues)

    def test_command_in_say_not_flagged(self):
        """Commands mentioned in say should NOT be flagged."""
        issues = run_checks('say Use /loot to get items')
        assert not any(i.code == "JAVA_COMMAND" for i in issues)


class TestNBTSyntaxCheck:
    """Test NBT syntax detection."""

    def test_nbt_on_summon(self):
        """NBT on summon should be flagged."""
        issues = run_checks("summon zombie ~ ~ ~ {Health:20}")
        assert any(i.code == "NBT_SYNTAX" for i in issues)

    def test_nbt_on_give(self):
        """NBT on give should be flagged."""
        issues = run_checks("give @s diamond_sword{Enchantments:[{id:sharpness,lvl:5}]}")
        assert any(i.code == "NBT_SYNTAX" for i in issues)

    def test_no_nbt_valid(self):
        """Commands without NBT should be valid."""
        issues = run_checks("summon zombie ~ ~ ~")
        assert not any(i.code == "NBT_SYNTAX" for i in issues)

    def test_nbt_inside_tellraw_not_flagged(self):
        """NBT-like JSON in tellraw should NOT be flagged."""
        # tellraw legitimately uses JSON
        issues = run_checks('tellraw @a {"text":"Hello","color":"red"}')
        assert not any(i.code == "NBT_SYNTAX" for i in issues)


class TestEffectSyntaxCheck:
    """Test effect command syntax detection."""

    def test_effect_give_flagged(self):
        """'effect give' should be flagged."""
        issues = run_checks("effect give @s speed 30 1")
        assert any(i.code == "EFFECT_SYNTAX" for i in issues)

    def test_effect_bedrock_valid(self):
        """Bedrock-style effect should be valid."""
        issues = run_checks("effect @s speed 30 1")
        assert not any(i.code == "EFFECT_SYNTAX" for i in issues)


class TestJavaSelectorCheck:
    """Test Java-only selector argument detection."""

    def test_nbt_selector_flagged(self):
        """NBT in selector should be flagged."""
        issues = run_checks("kill @e[nbt={CustomName:'Test'}]")
        assert any(i.code == "JAVA_SELECTOR" for i in issues)

    def test_predicate_selector_flagged(self):
        """Predicate in selector should be flagged."""
        issues = run_checks("execute as @a[predicate=my:predicate] run say hi")
        assert any(i.code == "JAVA_SELECTOR" for i in issues)

    def test_team_selector_flagged(self):
        """Team in selector should be flagged."""
        issues = run_checks("kill @a[team=red]")
        assert any(i.code == "JAVA_SELECTOR" for i in issues)

    def test_valid_bedrock_selector(self):
        """Valid Bedrock selector should not be flagged."""
        issues = run_checks("kill @e[type=zombie,r=10]")
        assert not any(i.code == "JAVA_SELECTOR" for i in issues)


class TestJavaBlockCheck:
    """Test Java-only block name detection."""

    def test_enchanting_table_flagged(self):
        """'enchanting_table' should be flagged (use enchant_table)."""
        issues = run_checks("setblock ~ ~ ~ enchanting_table")
        assert any(i.code == "JAVA_BLOCK" for i in issues)

    def test_enchant_table_valid(self):
        """'enchant_table' (Bedrock name) should be valid."""
        issues = run_checks("setblock ~ ~ ~ enchant_table")
        assert not any(i.code == "JAVA_BLOCK" for i in issues)

    def test_poppy_flagged(self):
        """'poppy' should be flagged (use red_flower)."""
        issues = run_checks("setblock ~ ~ ~ poppy")
        assert any(i.code == "JAVA_BLOCK" for i in issues)


class TestColorRequiredCheck:
    """Test color-required block detection."""

    def test_bed_without_color_flagged(self):
        """'bed' without color should be flagged."""
        issues = run_checks("setblock ~ ~ ~ bed")
        assert any(i.code == "COLOR_REQUIRED" for i in issues)

    def test_red_bed_valid(self):
        """'red_bed' should be valid."""
        issues = run_checks("setblock ~ ~ ~ red_bed")
        assert not any(i.code == "COLOR_REQUIRED" for i in issues)

    def test_wool_without_color_flagged(self):
        """'wool' without color should be flagged."""
        issues = run_checks("fill ~ ~ ~ ~10 ~10 ~10 wool")
        assert any(i.code == "COLOR_REQUIRED" for i in issues)

    def test_white_wool_valid(self):
        """'white_wool' should be valid."""
        issues = run_checks("fill ~ ~ ~ ~10 ~10 ~10 white_wool")
        assert not any(i.code == "COLOR_REQUIRED" for i in issues)


class TestMacroSyntaxCheck:
    """Test macro syntax detection."""

    def test_macro_flagged(self):
        """$(var) macro should be flagged."""
        issues = run_checks("say $(message)")
        assert any(i.code == "MACRO_SYNTAX" for i in issues)

    def test_no_macro_valid(self):
        """Commands without macros should be valid."""
        issues = run_checks("say Hello World")
        assert not any(i.code == "MACRO_SYNTAX" for i in issues)


class TestComponentSyntaxCheck:
    """Test Java 1.20.5+ component syntax detection."""

    def test_component_syntax_flagged(self):
        """item[component=val] should be flagged."""
        issues = run_checks("give @s diamond_sword[enchantments={levels:{sharpness:5}}]")
        assert any(i.code == "COMPONENT_SYNTAX" for i in issues)

    def test_selector_not_flagged(self):
        """Selectors @a[...] should NOT be flagged as components."""
        issues = run_checks("give @a[type=player] diamond")
        assert not any(i.code == "COMPONENT_SYNTAX" for i in issues)


class TestLineTooLongCheck:
    """Test line length warning."""

    def test_long_line_warning(self):
        """Lines over 256 chars should warn."""
        long_cmd = "fill " + " ".join(["~0"] * 100) + " stone"
        issues = run_checks(long_cmd)
        assert any(i.code == "LINE_TOO_LONG" for i in issues)

    def test_normal_line_no_warning(self):
        """Normal length lines should not warn."""
        issues = run_checks("give @s diamond 64")
        assert not any(i.code == "LINE_TOO_LONG" for i in issues)


class TestIgnoreCodes:
    """Test ignore code functionality."""

    def test_ignore_specific_code(self):
        """Ignored codes should not produce issues."""
        issues = run_checks("data get entity @s", ignore_codes={"JAVA_COMMAND"})
        assert not any(i.code == "JAVA_COMMAND" for i in issues)

    def test_other_codes_still_checked(self):
        """Non-ignored codes should still be checked."""
        issues = run_checks("effect give @s speed", ignore_codes={"JAVA_COMMAND"})
        assert any(i.code == "EFFECT_SYNTAX" for i in issues)


class TestRegressionCases:
    """Regression tests for specific bugs."""

    def test_no_false_positive_tellraw_json(self):
        """tellraw JSON should not trigger NBT errors."""
        line = 'tellraw @a {"text":"Click here","clickEvent":{"action":"run_command","value":"/data get"}}'
        issues = run_checks(line)
        # Should not flag the /data inside the JSON
        assert not any(i.code == "JAVA_COMMAND" for i in issues)
        # Should not flag the JSON as NBT
        assert not any(i.code == "NBT_SYNTAX" for i in issues)

    def test_particle_dust_not_flagged(self):
        """Particle dust command should be valid."""
        line = "particle dust{color:[1.0,0.0,0.0],scale:2} ~ ~2 ~ 3 3 3 0 50"
        issues = run_checks(line)
        # particle is a safe NBT command
        assert not any(i.code == "NBT_SYNTAX" for i in issues)
