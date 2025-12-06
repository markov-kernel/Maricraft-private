#!/usr/bin/env python3
"""
Maricraft Release Script

Automates the release process:
1. Updates version in version.py and version.json
2. Builds the .exe with PyInstaller
3. Calculates SHA256 hash
4. Creates git commit and tag
5. Creates GitHub release with .exe attachment

Usage:
    python scripts/release.py 2.1.0 "Added new feature"
    python scripts/release.py --help

Requirements:
    - Windows (for PyInstaller .exe build)
    - gh CLI installed and authenticated
    - Git configured with push access
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


# Paths relative to repo root
REPO_ROOT = Path(__file__).parent.parent
VERSION_PY = REPO_ROOT / "maricraft" / "version.py"
VERSION_JSON = REPO_ROOT / "version.json"
SPEC_FILE = REPO_ROOT / "maricraft.spec"
DIST_DIR = REPO_ROOT / "dist"
EXE_NAME = "MariCraft.exe"
GITHUB_REPO = "markov-kernel/Maricraft-private"


def run_command(cmd: list[str], check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        check=check,
        capture_output=capture,
        text=True,
    )
    return result


def get_current_version() -> str:
    """Read current version from version.py."""
    content = VERSION_PY.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find __version__ in version.py")


def update_version_py(new_version: str) -> None:
    """Update __version__ in version.py."""
    content = VERSION_PY.read_text()
    new_content = re.sub(
        r'(__version__\s*=\s*["\'])([^"\']+)(["\'])',
        f'\\g<1>{new_version}\\g<3>',
        content,
    )
    VERSION_PY.write_text(new_content)
    print(f"  Updated version.py: {new_version}")


def update_version_json(new_version: str, release_notes: str, sha256: str = "", exe_url: str = "") -> None:
    """Update version.json with new version info."""
    data = json.loads(VERSION_JSON.read_text())
    data["version"] = new_version
    data["release_notes"] = release_notes
    data["sha256"] = sha256
    data["exe_download_url"] = exe_url
    VERSION_JSON.write_text(json.dumps(data, indent=4) + "\n")
    print(f"  Updated version.json: {new_version}")


def build_exe() -> Path:
    """Build the .exe with PyInstaller."""
    print("\nBuilding .exe with PyInstaller...")

    # Check if on Windows
    if sys.platform != "win32":
        print("  WARNING: Not on Windows. PyInstaller .exe build requires Windows.")
        print("  Skipping build. Use GitHub Actions or build on Windows manually.")
        exe_path = DIST_DIR / EXE_NAME
        if exe_path.exists():
            print(f"  Using existing: {exe_path}")
            return exe_path
        raise RuntimeError("Cannot build .exe on non-Windows platform")

    # Install dependencies
    run_command([sys.executable, "-m", "pip", "install", "-q", "pyinstaller", "pyautogui", "pygetwindow", "pyperclip"])

    # Run PyInstaller
    run_command(["pyinstaller", str(SPEC_FILE), "--clean", "--noconfirm"])

    exe_path = DIST_DIR / EXE_NAME
    if not exe_path.exists():
        raise RuntimeError(f"Build failed: {exe_path} not found")

    print(f"  Built: {exe_path} ({exe_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return exe_path


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def git_commit_and_tag(version: str, release_notes: str) -> None:
    """Create git commit and tag."""
    print("\nCreating git commit and tag...")

    # Check for uncommitted changes
    result = run_command(["git", "status", "--porcelain"], capture=True)
    if result.stdout.strip():
        run_command(["git", "add", "-A"])
        run_command(["git", "commit", "-m", f"chore: release v{version}\n\n{release_notes}"])

    # Create tag
    run_command(["git", "tag", f"v{version}"])
    print(f"  Created tag: v{version}")


def git_push(version: str) -> None:
    """Push commits and tags to remote."""
    print("\nPushing to remote...")
    run_command(["git", "push", "origin", "master"])
    run_command(["git", "push", "origin", f"v{version}"])


def create_github_release(version: str, release_notes: str, exe_path: Path) -> str:
    """Create GitHub release with .exe attachment."""
    print("\nCreating GitHub release...")

    # Check if gh is installed
    try:
        run_command(["gh", "--version"], capture=True)
    except FileNotFoundError:
        raise RuntimeError("gh CLI not found. Install from https://cli.github.com/")

    # Create release
    result = run_command([
        "gh", "release", "create", f"v{version}",
        str(exe_path),
        "--repo", GITHUB_REPO,
        "--title", f"Maricraft v{version}",
        "--notes", release_notes,
    ], capture=True)

    # Get the release URL
    result = run_command([
        "gh", "release", "view", f"v{version}",
        "--repo", GITHUB_REPO,
        "--json", "url",
        "-q", ".url",
    ], capture=True)

    release_url = result.stdout.strip()
    print(f"  Created release: {release_url}")
    return release_url


def get_exe_download_url(version: str) -> str:
    """Get the direct download URL for the .exe."""
    return f"https://github.com/{GITHUB_REPO}/releases/download/v{version}/{EXE_NAME}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a new Maricraft release",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/release.py 2.1.0 "Added one-click auto-update"
    python scripts/release.py 2.2.0 "Bug fixes and improvements"
    python scripts/release.py --current  # Show current version
        """,
    )
    parser.add_argument("version", nargs="?", help="New version number (e.g., 2.1.0)")
    parser.add_argument("notes", nargs="?", default="", help="Release notes")
    parser.add_argument("--current", action="store_true", help="Show current version and exit")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--skip-build", action="store_true", help="Skip PyInstaller build (use existing .exe)")

    args = parser.parse_args()

    # Show current version
    if args.current:
        print(f"Current version: {get_current_version()}")
        return

    # Validate arguments
    if not args.version:
        parser.error("version is required")

    version = args.version
    notes = args.notes or f"Maricraft v{version}"

    # Validate version format
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        parser.error(f"Invalid version format: {version} (expected: X.Y.Z)")

    current = get_current_version()
    print(f"Maricraft Release Script")
    print(f"========================")
    print(f"Current version: {current}")
    print(f"New version:     {version}")
    print(f"Release notes:   {notes}")
    print()

    if args.dry_run:
        print("[DRY RUN] Would perform the following steps:")
        print(f"  1. Update version.py and version.json to {version}")
        print(f"  2. Build MariCraft.exe with PyInstaller")
        print(f"  3. Calculate SHA256 hash")
        print(f"  4. Commit changes and create tag v{version}")
        print(f"  5. Push to origin")
        print(f"  6. Create GitHub release with .exe")
        return

    # Confirm
    confirm = input("Proceed with release? [y/N] ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    print("\n" + "=" * 50)
    print("Step 1: Update version files")
    print("=" * 50)
    update_version_py(version)
    update_version_json(version, notes)  # sha256 and exe_url will be updated later

    print("\n" + "=" * 50)
    print("Step 2: Build .exe")
    print("=" * 50)
    if args.skip_build:
        exe_path = DIST_DIR / EXE_NAME
        if not exe_path.exists():
            raise RuntimeError(f"--skip-build specified but {exe_path} not found")
        print(f"  Using existing: {exe_path}")
    else:
        exe_path = build_exe()

    print("\n" + "=" * 50)
    print("Step 3: Calculate SHA256")
    print("=" * 50)
    sha256 = calculate_sha256(exe_path)
    print(f"  SHA256: {sha256}")

    print("\n" + "=" * 50)
    print("Step 4: Update version.json with SHA256 and URL")
    print("=" * 50)
    exe_url = get_exe_download_url(version)
    update_version_json(version, notes, sha256, exe_url)

    print("\n" + "=" * 50)
    print("Step 5: Git commit and tag")
    print("=" * 50)
    git_commit_and_tag(version, notes)

    print("\n" + "=" * 50)
    print("Step 6: Push to remote")
    print("=" * 50)
    git_push(version)

    print("\n" + "=" * 50)
    print("Step 7: Create GitHub release")
    print("=" * 50)
    release_url = create_github_release(version, notes, exe_path)

    print("\n" + "=" * 50)
    print("Release Complete!")
    print("=" * 50)
    print(f"  Version:  {version}")
    print(f"  SHA256:   {sha256}")
    print(f"  Release:  {release_url}")
    print(f"  Download: {exe_url}")


if __name__ == "__main__":
    main()
