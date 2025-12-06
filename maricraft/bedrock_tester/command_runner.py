"""
Command runner for batch testing mcfunction files.

Supports the "Handshake Pattern" for anchor-based building:
- Establishes anchor entity with polling before build commands
- Filters out anchor setup/cleanup from mcfunction files (handled by Python)
"""

import asyncio
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Callable

from .server import BedrockCommandTester, CommandResult, ANCHOR_NAME


@dataclass
class FileTestResult:
    """Result of testing a single mcfunction file."""
    file: Path
    total_commands: int
    passed: int
    failed: int
    results: list[CommandResult]
    anchor_established: bool = True  # Whether anchor handshake succeeded
    used_anchor: bool = False  # Whether this file used anchor pattern

    @property
    def success_rate(self) -> float:
        """Return success rate as percentage."""
        if self.total_commands == 0:
            return 100.0
        return (self.passed / self.total_commands) * 100


class CommandRunner:
    """
    Batch command runner for testing mcfunction files.

    Supports the "Handshake Pattern" for anchor-based building:
    - Detects if mcfunction uses anchor pattern (summon armor_stand with mc_anchor)
    - Filters out anchor setup/cleanup commands (handled by Python polling)
    - Uses establish_anchor() before build commands for reliable entity selection

    Usage:
        runner = CommandRunner(tester, use_anchor=True)
        results = await runner.test_file(Path("building/wizard_tower.mcfunction"))
        # or test all files
        results = await runner.test_directory(Path("functions/"))
    """

    # Commands that indicate anchor pattern usage
    ANCHOR_INDICATORS = [
        'mc_anchor',
        'maricraft_anchor',
    ]

    # Patterns for commands to filter when using handshake pattern
    ANCHOR_COMMAND_PATTERNS = [
        'summon armor_stand',
        'tag @e[type=armor_stand',
        'kill @e[tag=mc_anchor]',
        'kill @e[name="mc_anchor"]',
        'tickingarea add',
        'tickingarea remove',
    ]

    def __init__(
        self,
        tester: BedrockCommandTester,
        delay: float = 0.1,
        skip_comments: bool = True,
        skip_empty: bool = True,
        use_anchor: bool = True  # Enable handshake pattern by default
    ):
        self.tester = tester
        self.delay = delay
        self.skip_comments = skip_comments
        self.skip_empty = skip_empty
        self.use_anchor = use_anchor

    def _uses_anchor(self, content: str) -> bool:
        """Check if file content uses the anchor pattern."""
        content_lower = content.lower()
        return any(ind.lower() in content_lower for ind in self.ANCHOR_INDICATORS)

    def _is_anchor_command(self, cmd: str) -> bool:
        """Check if a command is an anchor setup/cleanup command."""
        cmd_lower = cmd.lower()
        # Check if it's an anchor-related command that we should filter
        for pattern in self.ANCHOR_COMMAND_PATTERNS:
            if pattern.lower() in cmd_lower and 'mc_anchor' in cmd_lower:
                return True
        # Also filter bare summon armor_stand without mc_anchor (likely anchor setup)
        if 'summon armor_stand' in cmd_lower and '~1 ~ ~1' in cmd_lower:
            return True
        return False

    def _parse_commands(self, content: str) -> list[tuple[int, str]]:
        """
        Parse mcfunction content into (line_num, command) tuples.

        Args:
            content: File content

        Returns:
            List of (line_number, command) tuples
        """
        commands = []
        for line_num, line in enumerate(content.splitlines(), 1):
            line = line.strip()

            # Skip empty lines
            if self.skip_empty and not line:
                continue

            # Skip comments
            if self.skip_comments and line.startswith('#'):
                continue

            # Handle inline comments (strip everything after # outside quotes)
            # Simple approach: strip trailing # comments
            if '  #' in line:
                line = line.split('  #')[0].strip()

            if line:
                commands.append((line_num, line))

        return commands

    async def test_file(
        self,
        file_path: Path,
        progress_callback: Optional[Callable[[int, int, str, CommandResult], None]] = None
    ) -> FileTestResult:
        """
        Test all commands in a single mcfunction file.

        If use_anchor is True and the file uses the anchor pattern, this method:
        1. Filters out anchor setup/cleanup commands from the file
        2. Establishes the anchor via Python polling (handshake pattern)
        3. Runs the remaining commands
        4. Cleans up the anchor

        Args:
            file_path: Path to the .mcfunction file
            progress_callback: Optional callback(current, total, filename, result)

        Returns:
            FileTestResult with all command results
        """
        content = file_path.read_text(encoding='utf-8')
        commands = self._parse_commands(content)

        # Check if file uses anchor pattern
        uses_anchor = self.use_anchor and self._uses_anchor(content)
        anchor_established = True

        if uses_anchor:
            print(f"[Runner] {file_path.name} uses anchor pattern - using handshake")

            # Filter out anchor-related commands
            original_count = len(commands)
            commands = [(ln, cmd) for ln, cmd in commands if not self._is_anchor_command(cmd)]
            filtered_count = original_count - len(commands)
            if filtered_count > 0:
                print(f"[Runner] Filtered {filtered_count} anchor commands (handled by Python)")

            # Establish anchor via handshake pattern
            anchor_established = await self.tester.establish_anchor()
            if not anchor_established:
                print(f"[Runner] WARNING: Anchor handshake failed for {file_path.name}")

        results = []
        passed = 0
        failed = 0

        for i, (line_num, cmd) in enumerate(commands, 1):
            result = await self.tester.test_command(
                cmd,
                file=str(file_path),
                line_num=line_num
            )
            results.append(result)

            if result.success:
                passed += 1
            else:
                failed += 1

            if progress_callback:
                progress_callback(i, len(commands), str(file_path), result)

            if self.delay > 0:
                await asyncio.sleep(self.delay)

        # Cleanup anchor if we used it
        if uses_anchor:
            await self.tester.cleanup_anchor()

        return FileTestResult(
            file=file_path,
            total_commands=len(commands),
            passed=passed,
            failed=failed,
            results=results,
            anchor_established=anchor_established,
            used_anchor=uses_anchor
        )

    async def test_directory(
        self,
        directory: Path,
        recursive: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> list[FileTestResult]:
        """
        Test all mcfunction files in a directory.

        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories
            progress_callback: Optional callback(file_num, total_files, filename)

        Returns:
            List of FileTestResult objects
        """
        if recursive:
            files = list(directory.rglob('*.mcfunction'))
        else:
            files = list(directory.glob('*.mcfunction'))

        results = []
        total = len(files)

        for i, file_path in enumerate(files, 1):
            if progress_callback:
                progress_callback(i, total, str(file_path))

            result = await self.test_file(file_path)
            results.append(result)

        return results

    @staticmethod
    def get_default_functions_path() -> Path:
        """Get the default path to Maricraft mcfunction files."""
        # Find the maricraft package directory
        import maricraft
        package_dir = Path(maricraft.__file__).parent
        return package_dir / "resources" / "maricraft_behavior" / "functions"
