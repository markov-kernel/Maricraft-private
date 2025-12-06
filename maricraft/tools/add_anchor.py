#!/usr/bin/env python3
"""
Add armor stand anchor pattern to mcfunction files.

This script transforms mcfunction files so that all commands using relative
coordinates (~) execute at a fixed armor stand position, preventing player
movement from breaking builds.

Usage:
    python -m maricraft.tools.add_anchor [--dry-run] [path]
"""

import argparse
import sys
from pathlib import Path


# Commands that use relative coordinates and need anchoring
ANCHOR_COMMANDS = {
    'fill', 'setblock', 'clone', 'summon', 'particle', 'playsound',
    'tp', 'teleport', 'spreadplayers', 'spawnpoint', 'setworldspawn'
}

# Commands that should NOT be wrapped (they don't use relative coords meaningfully)
SKIP_COMMANDS = {'say', 'tellraw', 'title', 'effect', 'gamemode', 'give', 'clear', 'kill'}

# Anchor entity name - used with atomic naming in Bedrock
# Bedrock summon syntax: summon armor_stand "name" ~ ~ ~ (name BEFORE coordinates)
ANCHOR_NAME = "mc_anchor"
OLD_ANCHOR_TAG = "mc_anchor"  # For detecting old tag-based format
OLD_ANCHOR_NAME = "maricraft_anchor"  # For detecting very old format

# New name-based format (Bedrock atomic naming)
# Summon at ~1 ~ ~1 to be outside typical build areas (which start at ~3)
# Name comes BEFORE coordinates in Bedrock Edition summon command
SUMMON_LINE = f'summon armor_stand "{ANCHOR_NAME}" ~1 ~ ~1'
# No separate tag command needed - the name is set atomically during summon
# The Python handshake pattern polls with testfor until entity is queryable
KILL_LINE = f'kill @e[type=armor_stand,name="{ANCHOR_NAME}"]'
# Bedrock OLD execute syntax: execute <target> <position> <command>
# This sets both WHO and WHERE - the command runs as the target at target's position
# Note: Bedrock does NOT support Java's "execute as ... at @s run" syntax!
EXECUTE_PREFIX = f'execute @e[type=armor_stand,name="{ANCHOR_NAME}",c=1] ~ ~ ~ '


def needs_anchoring(line: str) -> bool:
    """Check if a command line needs to be wrapped with execute at anchor."""
    stripped = line.strip()

    # Skip empty lines and comments
    if not stripped or stripped.startswith('#'):
        return False

    # Get the command name
    parts = stripped.split()
    if not parts:
        return False

    cmd = parts[0].lower()

    # Skip commands that don't need anchoring
    if cmd in SKIP_COMMANDS:
        return False

    # Already has execute - check if it uses relative coords
    if cmd == 'execute':
        # If the line contains anchor name or old formats, skip it
        if ANCHOR_NAME in stripped or OLD_ANCHOR_TAG in stripped or OLD_ANCHOR_NAME in stripped:
            return False
        # Only anchor if it uses relative coords
        return '~' in stripped

    # For other commands, anchor if they use relative coords
    if cmd in ANCHOR_COMMANDS or '~' in stripped:
        return '~' in stripped

    return False


def add_anchor_to_file(filepath: Path, dry_run: bool = False, fix: bool = False) -> tuple[int, int]:
    """
    Add armor stand anchor pattern to an mcfunction file.

    Uses atomic naming (name in summon command) for Bedrock compatibility.
    The Python handshake pattern handles polling until entity is queryable.

    Args:
        filepath: Path to mcfunction file
        dry_run: If True, don't actually modify the file
        fix: If True, fix files with old anchor format

    Returns:
        Tuple of (lines_modified, total_lines)
    """
    content = filepath.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Check for various anchor formats
    has_name_anchor = f'name="{ANCHOR_NAME}"' in content or f"name='{ANCHOR_NAME}'" in content
    has_tag_anchor = f'tag={OLD_ANCHOR_TAG}' in content
    has_old_anchor = OLD_ANCHOR_NAME in content

    # If file already has new name-based anchor format, skip it
    if has_name_anchor:
        return (0, len(lines))

    # If file has old tag-based format, we need to fix it
    if has_tag_anchor:
        if not fix:
            return (0, len(lines))
        # Replace tag-based format with name-based format
        content = content.replace(f'@e[tag={OLD_ANCHOR_TAG}]', f'@e[name="{ANCHOR_NAME}"]')
        # Replace old summon + tag with new atomic summon
        content = content.replace('summon armor_stand ~1 ~ ~1', SUMMON_LINE)
        # Remove tag lines (no longer needed with atomic naming)
        new_content_lines = []
        for line in content.splitlines():
            if 'tag @e[type=armor_stand' in line.lower() and 'mc_anchor' in line.lower():
                continue  # Skip tag commands
            new_content_lines.append(line)
        content = '\n'.join(new_content_lines)
        if not dry_run:
            filepath.write_text(content, encoding='utf-8')
        return (1, len(lines))  # Report as 1 modification

    # If file has very old format with maricraft_anchor, fix it
    if has_old_anchor:
        if not fix:
            return (0, len(lines))
        # Replace old format with new format
        content = content.replace(f'@e[type=armor_stand,name={OLD_ANCHOR_NAME}]', f'@e[name="{ANCHOR_NAME}"]')
        content = content.replace(f'@e[name={OLD_ANCHOR_NAME}]', f'@e[name="{ANCHOR_NAME}"]')
        content = content.replace(f'summon armor_stand ~ ~ ~ {OLD_ANCHOR_NAME}', SUMMON_LINE)
        if not dry_run:
            filepath.write_text(content, encoding='utf-8')
        return (1, len(lines))  # Report as 1 modification

    new_lines = []
    header_done = False
    lines_modified = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Preserve header comments and empty lines at start
        if not header_done:
            if stripped.startswith('#') or not stripped:
                new_lines.append(line)
                continue
            else:
                # Insert summon before first command (no separate tag needed with atomic naming)
                new_lines.append(f"# Anchor point for building (atomic naming)")
                new_lines.append(SUMMON_LINE)
                new_lines.append("")
                header_done = True

        # Check if this line needs anchoring
        if needs_anchoring(line):
            # Preserve original indentation
            indent = len(line) - len(line.lstrip())
            indent_str = line[:indent]
            new_lines.append(f"{indent_str}{EXECUTE_PREFIX}{stripped}")
            lines_modified += 1
        else:
            new_lines.append(line)

    # Add cleanup at end
    new_lines.append("")
    new_lines.append("# Clean up anchor")
    new_lines.append(KILL_LINE)

    if not dry_run:
        filepath.write_text('\n'.join(new_lines), encoding='utf-8')

    return (lines_modified, len(lines))


def process_directory(path: Path, dry_run: bool = False, fix: bool = False) -> dict:
    """Process all mcfunction files in a directory."""
    results = {
        'files_processed': 0,
        'files_skipped': 0,
        'files_fixed': 0,
        'total_lines_modified': 0,
        'files': []
    }

    mcfunction_files = sorted(path.rglob('*.mcfunction'))

    for filepath in mcfunction_files:
        relative_path = filepath.relative_to(path)

        # Check if file has old format (tag-based or very old name-based)
        content = filepath.read_text(encoding='utf-8')
        has_old_tag = f'tag={OLD_ANCHOR_TAG}' in content
        has_old_name = OLD_ANCHOR_NAME in content
        needs_fix = has_old_tag or has_old_name

        modified, total = add_anchor_to_file(filepath, dry_run, fix)

        if modified > 0:
            if needs_fix and fix:
                results['files_fixed'] += 1
                status = "FIXED" if not dry_run else "WOULD FIX"
            else:
                results['files_processed'] += 1
                status = "MODIFIED" if not dry_run else "WOULD MODIFY"
            results['total_lines_modified'] += modified
            results['files'].append({
                'path': str(relative_path),
                'lines_modified': modified,
                'total_lines': total
            })
            print(f"[{status}] {relative_path}: {modified}/{total} lines")
        else:
            results['files_skipped'] += 1
            if needs_fix and not fix:
                print(f"[NEEDS FIX] {relative_path}: has old anchor format (use --fix)")
            else:
                print(f"[SKIPPED] {relative_path}: already has anchor or no relative coords")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Add armor stand anchor pattern to mcfunction files"
    )
    parser.add_argument(
        'path',
        nargs='?',
        type=Path,
        default=Path(__file__).parent.parent / 'resources' / 'maricraft_behavior' / 'functions',
        help="Path to mcfunction file or directory (default: maricraft functions)"
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help="Show what would be changed without modifying files"
    )
    parser.add_argument(
        '--fix', '-f',
        action='store_true',
        help="Fix files with old anchor format (name-based) to new format (tag-based)"
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}")
        sys.exit(1)

    prefix = 'DRY RUN - ' if args.dry_run else ''
    prefix += 'FIX MODE - ' if args.fix else ''
    print(f"{prefix}Processing: {args.path}")
    print("=" * 60)

    if args.path.is_file():
        modified, total = add_anchor_to_file(args.path, args.dry_run, args.fix)
        print(f"Modified {modified}/{total} lines")
    else:
        results = process_directory(args.path, args.dry_run, args.fix)
        print("=" * 60)
        print(f"Files processed: {results['files_processed']}")
        print(f"Files fixed: {results['files_fixed']}")
        print(f"Files skipped: {results['files_skipped']}")
        print(f"Total lines modified: {results['total_lines_modified']}")

    if args.dry_run:
        print("\nThis was a dry run. No files were modified.")
        print("Run without --dry-run to apply changes.")


if __name__ == '__main__':
    main()
