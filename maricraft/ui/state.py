"""Application state management with JSON persistence."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, List, Tuple


def get_config_dir() -> Path:
    """Get the configuration directory path.

    Uses %APPDATA%/Maricraft for both development and PyInstaller builds.
    """
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "Maricraft"

    # Fallback to home directory
    return Path.home() / ".maricraft"


def get_config_path() -> Path:
    """Get the full path to the config file."""
    return get_config_dir() / "config.json"


@dataclass
class WindowState:
    """Window geometry state."""
    width: int = 950
    height: int = 750
    x: Optional[int] = None
    y: Optional[int] = None
    maximized: bool = False


@dataclass
class SettingsState:
    """User settings."""
    chat_key: str = "t"
    delay_ms: int = 100
    use_datapack_mode: bool = True
    auto_install_datapack: bool = True


@dataclass
class QuickToolbarState:
    """Quick access toolbar state."""
    visible: bool = False
    x: int = 100
    y: int = 100
    always_on_top: bool = True


@dataclass
class AppearanceState:
    """UI appearance settings."""
    mode: str = "dark"  # "dark", "light", or "system"


@dataclass
class AppState:
    """Complete application state."""
    version: int = 1
    window: WindowState = field(default_factory=WindowState)
    settings: SettingsState = field(default_factory=SettingsState)
    favorites: List[str] = field(default_factory=list)  # function_ids
    quick_toolbar: QuickToolbarState = field(default_factory=QuickToolbarState)
    appearance: AppearanceState = field(default_factory=AppearanceState)

    # Runtime state (not persisted)
    search_query: str = field(default="", repr=False)
    datapack_warning_shown: bool = field(default=False, repr=False)

    def add_favorite(self, function_id: str) -> bool:
        """Add a function to favorites. Returns True if added."""
        if function_id not in self.favorites and len(self.favorites) < 10:
            self.favorites.append(function_id)
            return True
        return False

    def remove_favorite(self, function_id: str) -> bool:
        """Remove a function from favorites. Returns True if removed."""
        if function_id in self.favorites:
            self.favorites.remove(function_id)
            return True
        return False

    def toggle_favorite(self, function_id: str) -> bool:
        """Toggle favorite status. Returns new state (True = favorited)."""
        if function_id in self.favorites:
            self.favorites.remove(function_id)
            return False
        elif len(self.favorites) < 10:
            self.favorites.append(function_id)
            return True
        return False

    def is_favorite(self, function_id: str) -> bool:
        """Check if a function is favorited."""
        return function_id in self.favorites

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "window": asdict(self.window),
            "settings": asdict(self.settings),
            "favorites": self.favorites,
            "quick_toolbar": asdict(self.quick_toolbar),
            "appearance": asdict(self.appearance),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AppState":
        """Create AppState from dictionary."""
        state = cls()

        if "version" in data:
            state.version = data["version"]

        if "window" in data:
            w = data["window"]
            state.window = WindowState(
                width=w.get("width", 950),
                height=w.get("height", 750),
                x=w.get("x"),
                y=w.get("y"),
                maximized=w.get("maximized", False),
            )

        if "settings" in data:
            s = data["settings"]
            state.settings = SettingsState(
                chat_key=s.get("chat_key", "t"),
                delay_ms=s.get("delay_ms", 100),
                use_datapack_mode=s.get("use_datapack_mode", True),
                auto_install_datapack=s.get("auto_install_datapack", True),
            )

        if "favorites" in data:
            state.favorites = data["favorites"][:10]  # Max 10

        if "quick_toolbar" in data:
            qt = data["quick_toolbar"]
            state.quick_toolbar = QuickToolbarState(
                visible=qt.get("visible", False),
                x=qt.get("x", 100),
                y=qt.get("y", 100),
                always_on_top=qt.get("always_on_top", True),
            )

        if "appearance" in data:
            a = data["appearance"]
            state.appearance = AppearanceState(
                mode=a.get("mode", "dark"),
            )

        return state


class StateManager:
    """Manages loading and saving application state."""

    def __init__(self):
        self.state = AppState()
        self._save_scheduled = False

    def load(self) -> AppState:
        """Load state from config file, or create default."""
        config_path = get_config_path()

        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.state = AppState.from_dict(data)
            except (json.JSONDecodeError, KeyError, TypeError):
                # Corrupted config, use defaults
                self.state = AppState()
        else:
            self.state = AppState()

        return self.state

    def save(self) -> bool:
        """Save state to config file."""
        config_path = get_config_path()

        try:
            # Ensure directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.state.to_dict(), f, indent=2)
            return True
        except (OSError, IOError):
            return False

    def schedule_save(self, root, delay_ms: int = 500) -> None:
        """Schedule a debounced save operation."""
        if self._save_scheduled:
            return

        self._save_scheduled = True

        def do_save():
            self.save()
            self._save_scheduled = False

        root.after(delay_ms, do_save)


# Global state manager instance
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get or create the global state manager."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager


def get_state() -> AppState:
    """Get the current application state."""
    return get_state_manager().state
