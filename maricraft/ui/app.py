"""Main application window for Maricraft."""

from __future__ import annotations

import threading
import webbrowser
from typing import Optional, Tuple, Callable

import customtkinter as ctk

from ..automator import WindowsAutomator
from ..commands import ALL_CATEGORIES, CommandButton
from ..constants import DEFAULT_LOG_PATH
from ..datapack import check_any_world_has_datapack
from ..logger import Logger
from ..settings import Settings
from ..version import __version__, check_for_update

from .state import get_state_manager, get_state, AppState
from .theme import COLORS, FONTS, WINDOW, SPACING, RADIUS
from .components.command_button import CommandButtonWidget
from .components.category_frame import CategoryFrame
from .components.search_bar import SearchBar
from .components.favorites_bar import FavoritesBar
from .components.status_bar import StatusBar
from .components.tooltip import ToolTip


class App(ctk.CTk):
    """Main Maricraft application window."""

    def __init__(self):
        super().__init__()

        # Load state
        self.state_manager = get_state_manager()
        self.state = self.state_manager.load()

        # Configure appearance
        ctk.set_appearance_mode(self.state.appearance.mode)
        ctk.set_default_color_theme("blue")

        # Window setup
        self.title(f"Maricraft Helper v{__version__}")
        self._setup_window_geometry()

        # Configure colors
        self.configure(fg_color=COLORS["background"])

        # State
        self.stop_event = threading.Event()
        self.automator = WindowsAutomator(status_cb=self._set_status, stop_event=self.stop_event)
        self.is_running = False
        self.update_available: Optional[Tuple[str, str]] = None
        self.category_frames: list[CategoryFrame] = []
        self.all_buttons: list[CommandButtonWidget] = []

        # Build UI
        self._build_ui()

        # Bind events
        self.bind("<Configure>", self._on_configure)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Check for updates
        self.after(1000, self._check_for_updates_async)

    def _setup_window_geometry(self) -> None:
        """Set up window size and position from saved state."""
        w = self.state.window
        self.geometry(f"{w.width}x{w.height}")
        self.minsize(WINDOW["min_width"], WINDOW["min_height"])

        if w.x is not None and w.y is not None:
            self.geometry(f"+{w.x}+{w.y}")

    def _build_ui(self) -> None:
        """Build the main UI layout."""
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])

        # Update banner container (will be populated if update available)
        self.update_banner = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=0)
        self.update_banner.pack(fill="x")

        # Header with title and buttons
        self._build_header()

        # Search bar
        self.search_bar = SearchBar(
            self.main_frame,
            on_search=self._on_search,
            placeholder="Search commands..."
        )
        self.search_bar.pack(fill="x", pady=(SPACING["md"], SPACING["sm"]))

        # Favorites bar
        self.favorites_bar = FavoritesBar(
            self.main_frame,
            favorites=self.state.favorites,
            on_click=self._on_favorite_click,
            get_button_info=self._get_button_info
        )
        self.favorites_bar.pack(fill="x", pady=(0, SPACING["md"]))

        # Scrollable content area
        self.content_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            scrollbar_button_color=COLORS["surface_light"],
            scrollbar_button_hover_color=COLORS["hover"],
        )
        self.content_frame.pack(fill="both", expand=True)

        # Build button categories
        self._build_categories()

        # Status bar
        self.status_bar = StatusBar(self.main_frame)
        self.status_bar.pack(fill="x", pady=(SPACING["md"], 0))
        self._set_status("Ready - Click a button to send commands!")

    def _build_header(self) -> None:
        """Build the header with title and action buttons."""
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x")

        # Title
        title = ctk.CTkLabel(
            header,
            text="Maricraft Helper",
            font=FONTS["title"],
            text_color=COLORS["text"],
        )
        title.pack(side="left")

        # Settings button
        self.settings_btn = ctk.CTkButton(
            header,
            text="Settings",
            font=FONTS["body"],
            width=100,
            height=35,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["hover"],
            command=self._show_settings,
        )
        self.settings_btn.pack(side="right")

        # Install Datapack button
        self.datapack_btn = ctk.CTkButton(
            header,
            text="Install Datapack",
            font=FONTS["body"],
            width=130,
            height=35,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["hover"],
            command=self._show_install_datapack,
        )
        self.datapack_btn.pack(side="right", padx=(0, SPACING["sm"]))

        # Stop button (hidden initially)
        self.stop_btn = ctk.CTkButton(
            header,
            text="STOP",
            font=FONTS["button"],
            width=80,
            height=35,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["danger"],
            hover_color=COLORS["warning"],
            command=self._on_stop,
        )
        # Hidden by default

    def _build_categories(self) -> None:
        """Build command button categories."""
        for category in ALL_CATEGORIES:
            frame = CategoryFrame(
                self.content_frame,
                category=category,
                on_button_click=self._on_button_click,
                on_favorite_toggle=self._on_favorite_toggle,
                is_favorite_fn=self.state.is_favorite,
            )
            frame.pack(fill="x", pady=(0, SPACING["md"]))
            self.category_frames.append(frame)
            self.all_buttons.extend(frame.buttons)

    def _get_button_info(self, function_id: str) -> Optional[CommandButton]:
        """Get button info by function_id."""
        for category in ALL_CATEGORIES:
            for btn in category.buttons:
                if btn.function_id == function_id:
                    return btn
        return None

    def _on_search(self, query: str) -> None:
        """Handle search query changes."""
        self.state.search_query = query.lower().strip()

        # Count matching buttons
        visible_count = 0
        total_count = 0

        for frame in self.category_frames:
            category_visible = 0
            for btn_widget in frame.buttons:
                total_count += 1
                matches = self._button_matches_search(btn_widget.button, self.state.search_query)
                btn_widget.set_visible(matches)
                if matches:
                    visible_count += 1
                    category_visible += 1

            # Hide category if no buttons match
            if category_visible == 0 and self.state.search_query:
                frame.pack_forget()
            else:
                frame.pack(fill="x", pady=(0, SPACING["md"]))

        # Update search bar count
        if self.state.search_query:
            self.search_bar.set_result_count(visible_count, total_count)
        else:
            self.search_bar.clear_result_count()

    def _button_matches_search(self, button: CommandButton, query: str) -> bool:
        """Check if a button matches the search query."""
        if not query:
            return True
        return query in button.name.lower() or query in button.description.lower()

    def _on_button_click(self, button: CommandButton) -> None:
        """Handle command button click."""
        if self.is_running:
            self._show_message("Please wait for the current command to finish.", "info")
            return

        # Check datapack warning
        if self.state.settings.use_datapack_mode and button.function_id:
            if not self.state.datapack_warning_shown and not check_any_world_has_datapack():
                self.state.datapack_warning_shown = True
                result = self._ask_yes_no(
                    "Datapack Not Found",
                    "The Maricraft datapack was not found in any Minecraft world.\n\n"
                    "Commands may not work without the datapack installed.\n\n"
                    "Would you like to install the datapack now?"
                )
                if result:
                    self._show_install_datapack()
                    return

            # Send function call
            function_cmd = f"/function {button.function_id}"
            self._execute_commands([function_cmd], button.name)
        else:
            # Legacy mode
            self._execute_commands(button.commands, button.name)

    def _on_favorite_toggle(self, function_id: str) -> bool:
        """Handle favorite star toggle. Returns new favorite state."""
        new_state = self.state.toggle_favorite(function_id)
        self.favorites_bar.update_favorites(self.state.favorites)
        self.state_manager.schedule_save(self)
        return new_state

    def _on_favorite_click(self, function_id: str) -> None:
        """Handle click on favorite in favorites bar."""
        button = self._get_button_info(function_id)
        if button:
            self._on_button_click(button)

    def _execute_commands(self, commands: list[str], name: str) -> None:
        """Execute commands in Minecraft."""
        self.is_running = True
        self.stop_btn.pack(side="right", padx=(0, SPACING["sm"]))
        self.stop_event.clear()

        settings = Settings(
            chat_key=self.state.settings.chat_key,
            delay_ms=self.state.settings.delay_ms,
            press_escape_first=True,
        )

        logger = Logger(DEFAULT_LOG_PATH)
        self.automator.logger = logger

        def worker() -> None:
            try:
                self._set_status(f"Running: {name}...")
                self.automator.run_commands(commands, settings)
            finally:
                logger.close()
                self.after(0, self._on_commands_complete)

        threading.Thread(target=worker, daemon=True).start()

    def _on_commands_complete(self) -> None:
        """Called when command execution completes."""
        self.is_running = False
        self.stop_btn.pack_forget()
        if not self.stop_event.is_set():
            self._set_status("Ready - Click a button to send commands!")

    def _on_stop(self) -> None:
        """Handle stop button click."""
        self.stop_event.set()
        self._set_status("Stopping...")

    def _set_status(self, message: str) -> None:
        """Thread-safe status update."""
        def update():
            self.status_bar.set_status(message)
        self.after(0, update)

    def _on_configure(self, event) -> None:
        """Handle window configure events (resize/move)."""
        if event.widget == self:
            self.state.window.width = self.winfo_width()
            self.state.window.height = self.winfo_height()
            self.state.window.x = self.winfo_x()
            self.state.window.y = self.winfo_y()
            self.state_manager.schedule_save(self)

    def _on_close(self) -> None:
        """Handle window close."""
        self.state_manager.save()
        self.destroy()

    def _check_for_updates_async(self) -> None:
        """Check for updates in background."""
        def check():
            result = check_for_update()
            if result:
                self.after(0, lambda: self._show_update_banner(result))

        threading.Thread(target=check, daemon=True).start()

    def _show_update_banner(self, update_info: Tuple[str, str]) -> None:
        """Show update available banner."""
        version, url = update_info
        self.update_available = update_info

        banner = ctk.CTkFrame(
            self.update_banner,
            fg_color=COLORS["warning"],
            corner_radius=RADIUS["md"],
        )
        banner.pack(fill="x", pady=(0, SPACING["sm"]))

        # Message
        msg = ctk.CTkLabel(
            banner,
            text=f"Update available: v{version}",
            font=FONTS["body"],
            text_color=COLORS["text_dark"],
        )
        msg.pack(side="left", padx=SPACING["md"], pady=SPACING["sm"])

        # Close button
        close_btn = ctk.CTkButton(
            banner,
            text="X",
            width=30,
            height=30,
            corner_radius=RADIUS["sm"],
            fg_color="transparent",
            hover_color=COLORS["danger"],
            text_color=COLORS["text_dark"],
            command=banner.destroy,
        )
        close_btn.pack(side="right", padx=SPACING["xs"])

        # Download button
        download_btn = ctk.CTkButton(
            banner,
            text="Download",
            width=100,
            height=30,
            corner_radius=RADIUS["sm"],
            fg_color=COLORS["success"],
            hover_color=COLORS["primary"],
            command=lambda: webbrowser.open(url),
        )
        download_btn.pack(side="right", padx=SPACING["sm"])

    def _show_settings(self) -> None:
        """Show settings dialog."""
        from .components.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self, self.state, self.state_manager)
        dialog.grab_set()

    def _show_install_datapack(self) -> None:
        """Show datapack installation dialog."""
        from .components.install_dialog import InstallDatapackDialog
        dialog = InstallDatapackDialog(self)
        dialog.grab_set()

    def _show_message(self, message: str, msg_type: str = "info") -> None:
        """Show a message dialog."""
        from tkinter import messagebox
        if msg_type == "info":
            messagebox.showinfo("Maricraft", message)
        elif msg_type == "warning":
            messagebox.showwarning("Maricraft", message)
        elif msg_type == "error":
            messagebox.showerror("Maricraft", message)

    def _ask_yes_no(self, title: str, message: str) -> bool:
        """Show a yes/no dialog."""
        from tkinter import messagebox
        return messagebox.askyesno(title, message)


def main() -> None:
    """Application entry point."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
