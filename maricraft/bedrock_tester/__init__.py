"""
Bedrock Command Tester

A WebSocket-based tool for testing Minecraft Bedrock commands against a live game.
Uses py-mcws to connect to Minecraft and test commands line-by-line.

Usage:
    python -m maricraft.bedrock_tester [--port PORT] [--output FILE]

Prerequisites:
    1. pip install py-mcws
    2. Minecraft Bedrock Edition on Windows
    3. Settings -> General -> Disable "Require Encrypted Websockets"
    4. Open world with cheats enabled
    5. In Minecraft: /connect localhost:19132
"""

from .server import BedrockCommandTester
from .command_runner import CommandRunner
from .report import TestReport, generate_report

__all__ = [
    'BedrockCommandTester',
    'CommandRunner',
    'TestReport',
    'generate_report',
]
