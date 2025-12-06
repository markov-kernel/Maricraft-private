"""
Main entry point for the Bedrock Command Tester.

Usage:
    python -m maricraft.bedrock_tester [OPTIONS]

Options:
    --host HOST     WebSocket server host (default: 0.0.0.0)
    --port PORT     WebSocket server port (default: 19132)
    --output FILE   Output JSON report to file
    --delay SECS    Delay between commands in seconds (default: 0.1)
    --path PATH     Path to mcfunction files (default: auto-detect)

Prerequisites:
    1. pip install py-mcws
    2. Minecraft Bedrock Edition on Windows
    3. Settings -> General -> Disable "Require Encrypted Websockets"
    4. Open world with cheats enabled
    5. In Minecraft: /connect localhost:19132
"""

import argparse
import asyncio
import sys
from pathlib import Path
from datetime import datetime

try:
    import py_mcws
except ImportError:
    print("ERROR: py-mcws is required for Bedrock testing.")
    print("Install it with: pip install py-mcws")
    sys.exit(1)

from .server import BedrockCommandTester
from .command_runner import CommandRunner
from .report import generate_report, print_summary, print_file_results


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Test Minecraft Bedrock commands via WebSocket",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="WebSocket server host (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=19132,
        help="WebSocket server port (default: 19132)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output JSON report to file"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Delay between commands in seconds (default: 0.1)"
    )
    parser.add_argument(
        "--path",
        type=Path,
        help="Path to mcfunction files (default: auto-detect)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=300,
        help="Connection timeout in seconds (default: 300)"
    )
    return parser.parse_args()


def run_tests(args):
    """Main test runner (non-async - py_mcws handles its own event loop)."""
    # Create tester
    tester = BedrockCommandTester(host=args.host, port=args.port)

    # Determine path to test
    if args.path:
        functions_path = args.path
    else:
        functions_path = CommandRunner.get_default_functions_path()

    if not functions_path.exists():
        print(f"ERROR: Path does not exist: {functions_path}")
        sys.exit(1)

    print(f"[Tester] Will test files in: {functions_path}")

    # Count files
    mcfunction_files = list(functions_path.rglob('*.mcfunction'))
    print(f"[Tester] Found {len(mcfunction_files)} mcfunction files")

    # Create runner
    runner = CommandRunner(tester, delay=args.delay)

    # Set up test execution on connect
    file_results = []

    @tester.on_connect
    async def on_connect():
        nonlocal file_results

        print("\n[Tester] Starting tests...")

        def progress(file_num, total, filename):
            print(f"[{file_num}/{total}] Testing {Path(filename).name}...")

        file_results = await runner.test_directory(
            functions_path,
            recursive=True,
            progress_callback=progress
        )

        # Generate report
        report = generate_report(file_results)

        # Print summary
        print_summary(report)
        print_file_results(file_results)

        # Save to file if requested
        if args.output:
            report.save(args.output)
        else:
            # Default output filename
            default_output = Path(f"bedrock_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            report.save(default_output)

        print("\n[Tester] Done! You can disconnect from Minecraft now.")
        print("[Tester] Press Ctrl+C to exit.")

    # Start server (this blocks until Ctrl+C)
    print("\n" + "=" * 60)
    print("BEDROCK COMMAND TESTER")
    print("=" * 60)
    print("\nPrerequisites:")
    print("1. Minecraft Bedrock Edition running")
    print("2. Settings -> General -> Disable 'Require Encrypted Websockets'")
    print("3. World with cheats enabled")
    print("\nInstructions:")
    print(f"1. In Minecraft, open chat and type: /connect {args.host}:{args.port}")
    print("2. Tests will run automatically after connection")
    print("\nWaiting for Minecraft to connect...")
    print("=" * 60 + "\n")

    tester.start()


def main():
    """Main entry point."""
    args = parse_args()

    try:
        run_tests(args)
    except KeyboardInterrupt:
        print("\n[Tester] Interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
