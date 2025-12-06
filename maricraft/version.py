"""Version checking for Maricraft."""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from typing import Optional, Tuple

__version__ = "2.0.3"

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/markov-kernel/Maricraft-private/master/version.json"


@dataclass
class UpdateInfo:
    """Information about an available update."""

    version: str
    download_url: str
    exe_download_url: str
    sha256: str
    release_notes: str


def check_for_update() -> Optional[UpdateInfo]:
    """Check GitHub for newer version.

    Returns:
        UpdateInfo if update available, else None
    """
    try:
        with urllib.request.urlopen(GITHUB_VERSION_URL, timeout=5) as response:
            data = json.loads(response.read().decode())
            latest = data.get("version", "")

            if _version_newer(latest, __version__):
                return UpdateInfo(
                    version=latest,
                    download_url=data.get("download_url", ""),
                    exe_download_url=data.get("exe_download_url", ""),
                    sha256=data.get("sha256", ""),
                    release_notes=data.get("release_notes", ""),
                )
    except Exception:
        pass  # Silently fail - don't block app startup

    return None


def check_for_update_legacy() -> Optional[Tuple[str, str]]:
    """Legacy version check returning (version, url) tuple.

    Kept for backward compatibility.
    """
    info = check_for_update()
    if info:
        return (info.version, info.download_url)
    return None


def _version_newer(v1: str, v2: str) -> bool:
    """Check if v1 is newer than v2 using semver comparison."""
    try:
        parts1 = [int(x) for x in v1.split(".")]
        parts2 = [int(x) for x in v2.split(".")]
        return parts1 > parts2
    except ValueError:
        return False
