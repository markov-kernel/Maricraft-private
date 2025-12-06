"""
Report generation for Bedrock command test results.
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from .server import CommandResult
from .command_runner import FileTestResult


@dataclass
class TestReport:
    """Summary report of all test results."""
    timestamp: str
    total_files: int
    total_commands: int
    passed: int
    failed: int
    success_rate: float
    failures: list[dict]
    file_results: list[dict]

    def to_dict(self) -> dict:
        """Convert report to dictionary."""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: Path):
        """Save report to a JSON file."""
        path.write_text(self.to_json())
        print(f"[Report] Saved to {path}")


def generate_report(file_results: list[FileTestResult]) -> TestReport:
    """
    Generate a summary report from test results.

    Args:
        file_results: List of FileTestResult from testing

    Returns:
        TestReport with summary and failure details
    """
    total_commands = sum(r.total_commands for r in file_results)
    total_passed = sum(r.passed for r in file_results)
    total_failed = sum(r.failed for r in file_results)

    # Collect all failures
    failures = []
    for file_result in file_results:
        for cmd_result in file_result.results:
            if not cmd_result.success:
                failures.append({
                    "file": str(file_result.file),
                    "line": cmd_result.line_num,
                    "command": cmd_result.command,
                    "error": cmd_result.error
                })

    # Summary per file
    file_summaries = []
    for file_result in file_results:
        file_summaries.append({
            "file": str(file_result.file),
            "total": file_result.total_commands,
            "passed": file_result.passed,
            "failed": file_result.failed,
            "success_rate": round(file_result.success_rate, 1)
        })

    success_rate = (total_passed / total_commands * 100) if total_commands > 0 else 100.0

    return TestReport(
        timestamp=datetime.now().isoformat(),
        total_files=len(file_results),
        total_commands=total_commands,
        passed=total_passed,
        failed=total_failed,
        success_rate=round(success_rate, 2),
        failures=failures,
        file_results=file_summaries
    )


def print_summary(report: TestReport):
    """Print a human-readable summary to console."""
    print("\n" + "=" * 60)
    print("BEDROCK COMMAND TEST REPORT")
    print("=" * 60)
    print(f"Timestamp: {report.timestamp}")
    print(f"Files tested: {report.total_files}")
    print(f"Total commands: {report.total_commands}")
    print(f"Passed: {report.passed}")
    print(f"Failed: {report.failed}")
    print(f"Success rate: {report.success_rate}%")

    if report.failures:
        print("\n" + "-" * 60)
        print("FAILURES:")
        print("-" * 60)
        for i, failure in enumerate(report.failures[:20], 1):  # Show first 20
            print(f"\n{i}. {failure['file']}:{failure['line']}")
            print(f"   Command: {failure['command'][:60]}...")
            print(f"   Error: {failure['error']}")

        if len(report.failures) > 20:
            print(f"\n... and {len(report.failures) - 20} more failures")

    print("\n" + "=" * 60)


def print_file_results(file_results: list[FileTestResult]):
    """Print per-file results."""
    print("\nPer-file results:")
    print("-" * 60)

    # Sort by failure count descending
    sorted_results = sorted(file_results, key=lambda r: r.failed, reverse=True)

    for result in sorted_results:
        status = "PASS" if result.failed == 0 else "FAIL"
        icon = "OK" if result.failed == 0 else "!!"
        print(f"[{icon}] {result.file.name}: {result.passed}/{result.total_commands} ({result.success_rate:.0f}%)")
