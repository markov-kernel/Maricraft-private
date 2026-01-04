"""
WebSocket server for Bedrock command testing.

Uses py-mcws to create a WebSocket server that Minecraft can connect to.

Implements the "Handshake Pattern" to solve the Anchor Paradox:
- Entities summoned via WebSocket aren't queryable until the game tick ends
- We use atomic naming (name in summon command) and testfor polling to ensure
  the anchor is ready before sending build commands

Configuration via environment variables:
- MARICRAFT_WS_HOST: WebSocket server host (default: 0.0.0.0)
- MARICRAFT_WS_PORT: WebSocket server port (default: 19132)
"""

import asyncio
import os
import time
from dataclasses import dataclass, field
from typing import Optional, Callable, Awaitable
from pathlib import Path

try:
    import py_mcws
except ImportError:
    py_mcws = None


# WebSocket server configuration with environment variable overrides
DEFAULT_WS_HOST = "0.0.0.0"
DEFAULT_WS_PORT = 19132

def get_ws_config() -> tuple[str, int]:
    """Get WebSocket server configuration from environment or defaults."""
    host = os.environ.get("MARICRAFT_WS_HOST", DEFAULT_WS_HOST)
    try:
        port = int(os.environ.get("MARICRAFT_WS_PORT", str(DEFAULT_WS_PORT)))
    except ValueError:
        port = DEFAULT_WS_PORT
    return host, port


# Anchor configuration
ANCHOR_NAME = "mc_anchor"
ANCHOR_SELECTOR = f'@e[name="{ANCHOR_NAME}"]'


@dataclass
class CommandResult:
    """Result of testing a single command."""
    command: str
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    file: Optional[str] = None
    line_num: Optional[int] = None


class BedrockCommandTester:
    """
    WebSocket server for testing Bedrock commands.

    Usage:
        tester = BedrockCommandTester()
        await tester.start()
        # In Minecraft: /connect localhost:19132
        # Once connected:
        results = await tester.test_commands(["give @s diamond", "tp @s ~ ~10 ~"])
    """

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None):
        if py_mcws is None:
            raise ImportError(
                "py-mcws is required for Bedrock testing. "
                "Install it with: pip install py-mcws"
            )

        # Use provided values or load from environment/defaults
        default_host, default_port = get_ws_config()
        self.host = host if host is not None else default_host
        self.port = port if port is not None else default_port
        self.server = py_mcws.WebsocketServer()
        self.connected = asyncio.Event()
        self.results: list[CommandResult] = []
        self._on_connect_callback: Optional[Callable[[], Awaitable[None]]] = None

        # Register event handlers
        @self.server.event
        async def on_ready(host, port):
            print(f"[Tester] Server started at ws://{host}:{port}")
            print(f"[Tester] In Minecraft, run: /connect {host}:{port}")

        @self.server.event
        async def on_connect():
            print("[Tester] Minecraft connected!")
            self.connected.set()
            if self._on_connect_callback:
                await self._on_connect_callback()

    def on_connect(self, callback: Callable[[], Awaitable[None]]):
        """Register a callback to run when Minecraft connects."""
        self._on_connect_callback = callback
        return callback

    async def wait_for_connection(self, timeout: float = 300):
        """Wait for Minecraft to connect."""
        print(f"[Tester] Waiting for Minecraft connection (timeout: {timeout}s)...")
        await asyncio.wait_for(self.connected.wait(), timeout=timeout)

    async def test_command(self, cmd: str, file: str = None, line_num: int = None) -> CommandResult:
        """
        Test a single command and return the result.

        Args:
            cmd: The command to test (without leading /)
            file: Optional source file name
            line_num: Optional line number in source file

        Returns:
            CommandResult with success/failure info
        """
        if not self.connected.is_set():
            return CommandResult(
                command=cmd,
                success=False,
                error="Minecraft not connected",
                file=file,
                line_num=line_num
            )

        # Strip leading slash if present
        cmd = cmd.lstrip('/')

        try:
            result = await self.server.command(cmd)

            # Extract status from WebSocket response
            # Response format: {"header": {...}, "body": {"statusCode": 0, "statusMessage": "..."}}
            body = {}
            if isinstance(result, dict):
                body = result.get("body", {})

            status_code = body.get("statusCode") if isinstance(body, dict) else None
            status_message = body.get("statusMessage", "") if isinstance(body, dict) else ""

            # statusCode 0 = success, non-zero = error
            success = (status_code == 0) if status_code is not None else True

            return CommandResult(
                command=cmd,
                success=success,
                response=status_message or str(result) if result else None,
                error=status_message if not success and status_message else None,
                file=file,
                line_num=line_num
            )
        except Exception as e:
            return CommandResult(
                command=cmd,
                success=False,
                error=str(e),
                file=file,
                line_num=line_num
            )

    async def test_commands(
        self,
        commands: list[str],
        delay: float = 0.1,
        progress_callback: Optional[Callable[[int, int, CommandResult], None]] = None
    ) -> list[CommandResult]:
        """
        Test multiple commands sequentially.

        Args:
            commands: List of commands to test
            delay: Delay between commands in seconds
            progress_callback: Optional callback(current, total, result)

        Returns:
            List of CommandResult objects
        """
        results = []
        total = len(commands)

        for i, cmd in enumerate(commands, 1):
            result = await self.test_command(cmd)
            results.append(result)

            if progress_callback:
                progress_callback(i, total, result)

            if delay > 0:
                await asyncio.sleep(delay)

        return results

    async def establish_anchor(self, timeout: float = 5.0) -> bool:
        """
        Summon an anchor entity and poll until it's queryable.

        This implements the "Handshake Pattern" to solve the Anchor Paradox:
        entities summoned via WebSocket aren't immediately queryable because
        they're not added to the entity map until the game tick ends.

        Args:
            timeout: Maximum time to wait for anchor to be ready

        Returns:
            True if anchor is ready, False if timeout
        """
        if not self.connected.is_set():
            print("[Anchor] Not connected to Minecraft")
            return False

        print("[Anchor] Establishing anchor...")

        # Step 1: Kill any existing anchors (from previous tests)
        await self.server.command(f'kill {ANCHOR_SELECTOR}')
        await asyncio.sleep(0.1)

        # Step 2: Create ticking area to keep chunk loaded
        # This ensures the anchor entity stays loaded during building
        await self.server.command(f'tickingarea add circle ~1 ~ ~1 2 {ANCHOR_NAME}_zone')
        await asyncio.sleep(0.05)

        # Step 3: Atomic summon with name (Bedrock syntax: name BEFORE coordinates)
        await self.server.command(f'summon armor_stand "{ANCHOR_NAME}" ~1 ~ ~1')
        print(f"[Anchor] Summoned armor stand with name '{ANCHOR_NAME}'")

        # Step 4: Polling handshake - wait until entity is queryable
        start_time = time.time()
        poll_count = 0
        while (time.time() - start_time) < timeout:
            poll_count += 1
            try:
                result = await self.server.command(f'testfor {ANCHOR_SELECTOR}')
                # testfor returns success if entity found
                if result:
                    result_dict = result if isinstance(result, dict) else {}
                    # Response format: {"header": {...}, "body": {"statusCode": 0, ...}}
                    body = result_dict.get('body', {}) if isinstance(result_dict, dict) else {}
                    status_code = body.get('statusCode') if isinstance(body, dict) else -1
                    if status_code == 0:
                        elapsed = time.time() - start_time
                        print(f"[Anchor] Ready after {poll_count} polls ({elapsed:.2f}s)")
                        return True
            except Exception as e:
                pass  # testfor may fail if entity not found yet

            await asyncio.sleep(0.1)  # Poll every 100ms

        print(f"[Anchor] TIMEOUT after {timeout}s ({poll_count} polls)")
        return False

    async def cleanup_anchor(self):
        """Remove the anchor entity and ticking area."""
        if not self.connected.is_set():
            return

        print("[Anchor] Cleaning up...")
        await self.server.command(f'kill {ANCHOR_SELECTOR}')
        await self.server.command(f'tickingarea remove {ANCHOR_NAME}_zone')
        print("[Anchor] Cleanup complete")

    async def test_mcfunction_with_anchor(
        self,
        commands: list[str],
        delay: float = 0.1,
        progress_callback: Optional[Callable[[int, int, CommandResult], None]] = None
    ) -> tuple[bool, list[CommandResult]]:
        """
        Test mcfunction commands using the anchor pattern.

        Filters out anchor setup/cleanup commands from the file and handles
        them via the handshake pattern instead.

        Args:
            commands: List of commands from the mcfunction file
            delay: Delay between commands
            progress_callback: Optional progress callback

        Returns:
            Tuple of (anchor_success, results)
        """
        # Filter out anchor-related commands - we handle them ourselves
        filtered_commands = []
        for cmd in commands:
            cmd_lower = cmd.lower().strip()
            # Skip anchor setup/cleanup commands
            if any([
                'summon armor_stand' in cmd_lower and ANCHOR_NAME.lower() in cmd_lower,
                f'tag @e[type=armor_stand' in cmd_lower and 'mc_anchor' in cmd_lower,
                'kill @e[' in cmd_lower and ANCHOR_NAME.lower() in cmd_lower,  # Match any kill with anchor name
                cmd_lower.startswith('tickingarea'),
            ]):
                print(f"[Anchor] Skipping (handled by handshake): {cmd[:60]}...")
                continue
            filtered_commands.append(cmd)

        # Establish anchor first
        anchor_ready = await self.establish_anchor()
        if not anchor_ready:
            print("[Anchor] Failed to establish anchor - running commands anyway")

        # Run the filtered commands
        results = await self.test_commands(filtered_commands, delay, progress_callback)

        # Cleanup anchor
        await self.cleanup_anchor()

        return anchor_ready, results

    def start(self):
        """Start the WebSocket server (blocking)."""
        self.server.start(host=self.host, port=self.port)

    async def start_async(self):
        """Start the WebSocket server asynchronously."""
        # Run server in background
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.start)
