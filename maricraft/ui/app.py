"""Main application window for Maricraft."""

from __future__ import annotations

import threading
import webbrowser
from typing import Optional, Callable

import customtkinter as ctk

from ..automator import WindowsAutomator
from ..commands import ALL_CATEGORIES, CommandButton
from ..constants import DEFAULT_LOG_PATH
from ..datapack import check_any_world_has_datapack
from ..logger import Logger
from ..settings import Settings
from ..version import __version__, check_for_update, UpdateInfo
from ..updater import (
    is_frozen,
    is_update_downloaded,
    download_update_async,
    perform_update,
    cleanup_downloaded_update,
)

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
        self.app_state_manager = get_state_manager()
        self.app_state = self.app_state_manager.load()

        # Configure appearance
        ctk.set_appearance_mode(self.app_state.appearance.mode)
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
        self.update_available: Optional[UpdateInfo] = None
        self.update_downloaded = False
        self.update_banner_widget: Optional[ctk.CTkFrame] = None
        self.category_frames: list[CategoryFrame] = []
        self.all_buttons: list[CommandButtonWidget] = []

        # Build UI
        self._build_ui()

        # Bind events
        self.bind("<Configure>", self._on_configure)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Check for updates
        self.after(1000, self._check_for_updates_async)

        # Auto-install datapacks
        if self.app_state.settings.auto_install_datapack:
            self.after(500, self._auto_install_datapacks)

    def _setup_window_geometry(self) -> None:
        """Set up window size and position from saved state."""
        w = self.app_state.window
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
            favorites=self.app_state.favorites,
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
                is_favorite_fn=self.app_state.is_favorite,
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
        self.app_state.search_query = query.lower().strip()

        # Count matching buttons
        visible_count = 0
        total_count = 0

        for frame in self.category_frames:
            category_visible = 0
            for btn_widget in frame.buttons:
                total_count += 1
                matches = self._button_matches_search(btn_widget.button, self.app_state.search_query)
                btn_widget.set_visible(matches)
                if matches:
                    visible_count += 1
                    category_visible += 1

            # Hide category if no buttons match
            if category_visible == 0 and self.app_state.search_query:
                frame.pack_forget()
            else:
                frame.pack(fill="x", pady=(0, SPACING["md"]))
                # Re-layout visible buttons in grid
                frame._layout_buttons()

        # Update search bar count
        if self.app_state.search_query:
            self.search_bar.set_result_count(visible_count, total_count)
        else:
            self.search_bar.clear_result_count()

    def _button_matches_search(self, button: CommandButton, query: str) -> bool:
        """Check if a button matches the search query."""
        if not query:
            return True
        return query in button.name.lower() or query in button.description.lower()

    def _detect_bedrock_window(self) -> bool:
        """Check if Minecraft Bedrock Edition is the active window.

        Detection strategy:
        - Java Edition titles always include version: "Minecraft 1.20.1", "Minecraft* 1.21.1"
        - Bedrock titles are just "Minecraft" or contain "for Windows"
        """
        try:
            import re
            import pygetwindow as gw

            active = gw.getActiveWindow()
            if active and active.title:
                title = active.title.strip()

                # Explicit Bedrock indicators
                if "for Windows" in title:
                    return True

                # Java Edition has version number: "Minecraft 1.20.1" or "Minecraft* 1.21.1"
                # Pattern: "Minecraft" optionally followed by "*" then space and version
                java_pattern = r"^Minecraft\*?\s+\d+\.\d+"
                if re.match(java_pattern, title):
                    return False  # It's Java Edition

                # Title is exactly "Minecraft" (no version) = Bedrock
                if title == "Minecraft":
                    return True

        except Exception:
            pass
        return False

    def _on_button_click(self, button: CommandButton) -> None:
        """Handle command button click."""
        if self.is_running:
            self._show_message("Please wait for the current command to finish.", "info")
            return

        # Detect which edition is active
        is_bedrock = self._detect_bedrock_window()

        if is_bedrock:
            # Bedrock Edition: use bedrock_commands if available, otherwise fall back
            commands = button.bedrock_commands if button.bedrock_commands else button.commands
            self._execute_commands(commands, button.name)
        else:
            # Java Edition: use datapack function if enabled, otherwise legacy mode
            if self.app_state.settings.use_datapack_mode and button.function_id:
                if not self.app_state.datapack_warning_shown and not check_any_world_has_datapack():
                    self.app_state.datapack_warning_shown = True
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
        new_state = self.app_state.toggle_favorite(function_id)
        self.favorites_bar.update_favorites(self.app_state.favorites)
        self.app_state_manager.schedule_save(self)
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
            chat_key=self.app_state.settings.chat_key,
            delay_ms=self.app_state.settings.delay_ms,
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
            self.app_state.window.width = self.winfo_width()
            self.app_state.window.height = self.winfo_height()
            self.app_state.window.x = self.winfo_x()
            self.app_state.window.y = self.winfo_y()
            self.app_state_manager.schedule_save(self)

    def _on_close(self) -> None:
        """Handle window close."""
        self.app_state_manager.save()
        self.destroy()

    def _auto_install_datapacks(self) -> None:
        """Auto-install/update datapacks in background."""
        def worker():
            from ..datapack import auto_install_all_datapacks
            results = auto_install_all_datapacks()

            # Build status message
            installed = len(results["installed"])
            updated = len(results["updated"])

            if installed or updated:
                parts = []
                if installed:
                    parts.append(f"installed in {installed} world(s)")
                if updated:
                    parts.append(f"updated in {updated} world(s)")
                message = f"Datapack {' and '.join(parts)}"
                self.after(0, lambda: self._set_status(message))

        threading.Thread(target=worker, daemon=True).start()

    def _check_for_updates_async(self) -> None:
        """Check for updates and download silently in background."""
        def check():
            result = check_for_update()
            if result:
                self.update_available = result

                # If running as .exe and exe_download_url available, download silently
                if is_frozen() and result.exe_download_url:
                    def on_download_complete(success: bool, error: str) -> None:
                        if success:
                            self.update_downloaded = True
                        # Show banner whether download succeeded or not
                        self.after(0, lambda: self._show_update_banner(result))

                    download_update_async(result, on_download_complete)
                else:
                    # Not frozen or no exe URL, just show banner
                    self.after(0, lambda: self._show_update_banner(result))

        threading.Thread(target=check, daemon=True).start()

    def _show_update_banner(self, update_info: UpdateInfo) -> None:
        """Show update available/ready banner."""
        # Remove existing banner if any
        if self.update_banner_widget:
            self.update_banner_widget.destroy()

        # Choose colors based on download status
        if self.update_downloaded:
            bg_color = COLORS["success"]
            message = f"Update ready: v{update_info.version}"
        else:
            bg_color = COLORS["warning"]
            message = f"Update available: v{update_info.version}"

        banner = ctk.CTkFrame(
            self.update_banner,
            fg_color=bg_color,
            corner_radius=RADIUS["md"],
        )
        banner.pack(fill="x", pady=(0, SPACING["sm"]))
        self.update_banner_widget = banner

        # Message
        msg = ctk.CTkLabel(
            banner,
            text=message,
            font=FONTS["body"],
            text_color=COLORS["text_dark"],
        )
        msg.pack(side="left", padx=SPACING["md"], pady=SPACING["sm"])

        # Close button
        def on_close():
            banner.destroy()
            if self.update_downloaded:
                cleanup_downloaded_update()
                self.update_downloaded = False
            self.update_banner_widget = None

        close_btn = ctk.CTkButton(
            banner,
            text="X",
            width=30,
            height=30,
            corner_radius=RADIUS["sm"],
            fg_color="transparent",
            hover_color=COLORS["danger"],
            text_color=COLORS["text_dark"],
            command=on_close,
        )
        close_btn.pack(side="right", padx=SPACING["xs"])

        # Download button (browser fallback)
        download_btn = ctk.CTkButton(
            banner,
            text="Download",
            width=100,
            height=30,
            corner_radius=RADIUS["sm"],
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["hover"],
            text_color=COLORS["text"],
            command=lambda: webbrowser.open(update_info.download_url),
        )
        download_btn.pack(side="right", padx=SPACING["sm"])

        # Install Now button (only if update is downloaded and running as .exe)
        if self.update_downloaded and is_frozen():
            install_btn = ctk.CTkButton(
                banner,
                text="Install Now",
                width=120,
                height=30,
                corner_radius=RADIUS["sm"],
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"] if "primary_dark" in COLORS else COLORS["primary"],
                text_color="white",
                command=self._start_auto_update,
            )
            install_btn.pack(side="right", padx=SPACING["sm"])

    def _start_auto_update(self) -> None:
        """Start the auto-update installation process."""
        if not self.update_available:
            return

        # Confirm with user
        notes = self.update_available.release_notes
        notes_text = f"\n\nWhat's new: {notes}" if notes else ""

        result = self._ask_yes_no(
            "Install Update",
            f"Install Maricraft v{self.update_available.version}?{notes_text}\n\n"
            "The app will close and reopen automatically."
        )

        if not result:
            return

        # Show progress dialog
        self._show_install_progress()

    def _show_install_progress(self) -> None:
        """Show progress dialog during installation."""
        if not self.update_available:
            return

        # Create progress window
        progress_window = ctk.CTkToplevel(self)
        progress_window.title("Installing Update")
        progress_window.geometry("350x150")
        progress_window.resizable(False, False)
        progress_window.transient(self)
        progress_window.grab_set()

        # Center on parent
        progress_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 350) // 2
        y = self.winfo_y() + (self.winfo_height() - 150) // 2
        progress_window.geometry(f"+{x}+{y}")

        # Content
        frame = ctk.CTkFrame(progress_window, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            frame,
            text=f"Installing Maricraft v{self.update_available.version}",
            font=FONTS["heading"],
        )
        title.pack(pady=(0, 10))

        status_label = ctk.CTkLabel(frame, text="Verifying download...")
        status_label.pack()

        progress = ctk.CTkProgressBar(frame, width=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()

        def progress_callback(stage: str, current: int, total: int) -> None:
            self.after(0, lambda: status_label.configure(text=stage))

        def do_install() -> None:
            # Import here to avoid circular import
            from ..updater import get_download_path, get_current_exe_path, get_backup_path
            from ..updater import verify_hash, create_updater_script
            import subprocess
            import sys

            update_info = self.update_available
            current_exe = get_current_exe_path()

            if current_exe is None:
                self.after(0, lambda: self._show_install_error(
                    progress_window, "Auto-update only works when running as MariCraft.exe"))
                return

            download_path = get_download_path()
            if not download_path.exists():
                self.after(0, lambda: self._show_install_error(
                    progress_window, "Update file not found. Please try again."))
                return

            # Verify hash
            self.after(0, lambda: status_label.configure(text="Verifying download..."))
            if update_info.sha256:
                success, error = verify_hash(download_path, update_info.sha256)
                if not success:
                    download_path.unlink()
                    self.after(0, lambda: self._show_install_error(progress_window, f"Security check failed: {error}"))
                    return

            # Create updater script
            self.after(0, lambda: status_label.configure(text="Preparing installation..."))
            backup_path = get_backup_path(current_exe)
            try:
                import os
                script_path = create_updater_script(current_exe, download_path, backup_path, os.getpid())
            except Exception as e:
                download_path.unlink()
                self.after(0, lambda: self._show_install_error(progress_window, f"Could not create updater: {e}"))
                return

            # Launch updater script
            self.after(0, lambda: status_label.configure(text="Launching updater..."))

            CREATE_NEW_CONSOLE = 0x00000010
            subprocess.Popen(
                ['cmd.exe', '/c', str(script_path)],
                creationflags=CREATE_NEW_CONSOLE,
                close_fds=True,
            )

            # Exit from main thread
            def exit_app():
                self.destroy()
                sys.exit(0)

            self.after(100, exit_app)

        # Run installation in background
        threading.Thread(target=do_install, daemon=True).start()

    def _show_install_error(self, dialog: ctk.CTkToplevel, error: str) -> None:
        """Show installation error and close dialog."""
        dialog.destroy()
        self._show_message(
            f"Could not install update:\n\n{error}\n\n"
            "You can download the update manually instead.",
            "error"
        )

    def _show_settings(self) -> None:
        """Show settings dialog."""
        from .components.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self, self.app_state, self.app_state_manager)
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
