"""Tkinter UI for Maricraft - Kid-friendly Minecraft command helper."""

from __future__ import annotations

import threading
import webbrowser
from typing import Optional

from .version import UpdateInfo

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    tk = None  # type: ignore[assignment]
    ttk = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]

from .automator import WindowsAutomator
from .commands import ALL_CATEGORIES, CommandButton
from .constants import (
    WINDOW_DEFAULT_WIDTH,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    UI_DELAY_MIN_MS,
    UI_DELAY_MAX_MS,
    UI_DELAY_DEFAULT_MS,
    BUTTONS_PER_ROW,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    DEFAULT_LOG_PATH,
)
from .datapack import (
    check_any_world_has_datapack,
    get_minecraft_saves_path,
    get_all_minecraft_instances,
    list_worlds,
    is_datapack_installed,
    install_datapack,
    DATAPACK_NAME,
)
from .logger import Logger
from .settings import Settings
from .version import __version__, check_for_update
from .updater import (
    is_frozen,
    is_update_downloaded,
    download_update_async,
    perform_update,
    cleanup_downloaded_update,
)


class ToolTip:
    """Simple tooltip that appears on hover."""

    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tooltip_window: Optional[tk.Toplevel] = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, _event: tk.Event) -> None:
        if self.tooltip_window:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#FFFFD0",
            foreground="#000000",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 10),
            padx=6,
            pady=4,
        )
        label.pack()

    def _hide(self, _event: tk.Event) -> None:
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class ScrollableFrame(ttk.Frame):
    """A scrollable frame container."""

    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_canvas_configure(self, event: tk.Event) -> None:
        # Make the inner frame expand to fill the canvas width
        self.canvas.itemconfig(self.canvas_frame, width=event.width)


class App:
    """Main Tkinter application for Maricraft."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(f"Maricraft Helper v{__version__}")
        self.root.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Set a nice background color
        style = ttk.Style()
        style.configure("Category.TLabelframe.Label", font=("Segoe UI", 12, "bold"))

        self.stop_event = threading.Event()
        self.automator = WindowsAutomator(status_cb=self._set_status, stop_event=self.stop_event)
        self.is_running = False

        # Settings
        self.chat_key = "t"
        self.delay_ms = UI_DELAY_DEFAULT_MS

        # Datapack mode
        self.use_datapack_mode = True
        self.datapack_warning_shown = False

        # Update state
        self.update_available: Optional[UpdateInfo] = None
        self.update_downloaded = False
        self.update_banner_frame: Optional[tk.Frame] = None

        self._build_widgets()

        # Check for updates in background after 1 second
        self.root.after(1000, self._check_for_updates_async)

    def _build_widgets(self) -> None:
        """Build all UI widgets."""
        pad = 10

        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=pad, pady=pad)

        # Update banner placeholder (will be shown if update available)
        self.update_banner_container = ttk.Frame(main_frame)
        self.update_banner_container.pack(fill=tk.X, pady=(0, 5))

        # Header with title and settings
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, pad))

        title_label = ttk.Label(
            header,
            text="Maricraft Helper",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.pack(side=tk.LEFT)

        # Settings button
        settings_btn = ttk.Button(header, text="Settings", command=self._show_settings)
        settings_btn.pack(side=tk.RIGHT)

        # Install Datapack button
        datapack_btn = ttk.Button(header, text="Install Datapack", command=self._show_install_datapack)
        datapack_btn.pack(side=tk.RIGHT, padx=(0, 8))

        # Stop button (hidden until running)
        self.stop_btn = ttk.Button(header, text="STOP", command=self.on_stop)
        self.stop_btn.pack(side=tk.RIGHT, padx=(0, 8))
        self.stop_btn.pack_forget()  # Hide initially

        # Scrollable button area
        scroll_frame = ScrollableFrame(main_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        # Build button categories
        self._build_button_categories(scroll_frame.scrollable_frame)

        # Status bar
        self.status_var = tk.StringVar(value="Ready - Click a button to send commands!")
        status = ttk.Label(main_frame, textvariable=self.status_var, anchor=tk.W, font=("Segoe UI", 10))
        status.pack(fill=tk.X, pady=(pad, 0))

    def _build_button_categories(self, parent: ttk.Frame) -> None:
        """Build button grid organized by category."""
        for category in ALL_CATEGORIES:
            # Category frame with label
            cat_frame = ttk.LabelFrame(
                parent,
                text=f"  {category.name}  ",
                style="Category.TLabelframe",
            )
            cat_frame.pack(fill=tk.X, padx=5, pady=(0, 15))

            # Button grid inside category
            buttons_frame = ttk.Frame(cat_frame)
            buttons_frame.pack(fill=tk.X, padx=10, pady=10)

            for idx, button in enumerate(category.buttons):
                row = idx // BUTTONS_PER_ROW
                col = idx % BUTTONS_PER_ROW

                btn = self._create_command_button(buttons_frame, button)
                btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew")

            # Make columns expand evenly
            for col in range(BUTTONS_PER_ROW):
                buttons_frame.columnconfigure(col, weight=1)

    def _create_command_button(self, parent: ttk.Frame, cmd_button: CommandButton) -> tk.Button:
        """Create a styled command button."""
        # Determine text color based on background brightness
        bg_color = cmd_button.color
        # Simple brightness check
        r = int(bg_color[1:3], 16)
        g = int(bg_color[3:5], 16)
        b = int(bg_color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        fg_color = "#000000" if brightness > 128 else "#FFFFFF"

        btn = tk.Button(
            parent,
            text=cmd_button.name,
            bg=bg_color,
            fg=fg_color,
            activebackground=self._lighten_color(bg_color),
            activeforeground=fg_color,
            font=("Segoe UI", 11, "bold"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            relief=tk.RAISED,
            cursor="hand2",
            command=lambda: self._on_button_click(cmd_button),
        )

        # Add tooltip
        ToolTip(btn, cmd_button.description)

        return btn

    def _lighten_color(self, hex_color: str) -> str:
        """Lighten a hex color for hover effect."""
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _detect_bedrock_window(self) -> bool:
        """Check if Minecraft Bedrock Edition is the active window.

        Uses process name detection which is more reliable than window titles.
        Works with GDK (Xbox App) and UWP (Microsoft Store) versions.
        """
        try:
            import ctypes
            import psutil
            from ctypes import wintypes

            # Get Active Window Handle
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if not hwnd:
                return False

            # Get Process ID from Window
            pid = wintypes.DWORD()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            if pid.value > 0:
                try:
                    proc = psutil.Process(pid.value)
                    proc_name = proc.name().lower()

                    # Primary: The actual Bedrock executable
                    if proc_name == "minecraft.windows.exe":
                        return True

                    # Secondary: UWP Frame Host (check title)
                    if proc_name == "applicationframehost.exe":
                        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                        buff = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                        if buff.value == "Minecraft":
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception:
            pass
        return False

    def _on_button_click(self, cmd_button: CommandButton) -> None:
        """Handle command button click."""
        if self.is_running:
            messagebox.showinfo("Busy", "Please wait for the current command to finish.")
            return

        # Detect which edition is active
        is_bedrock = self._detect_bedrock_window()

        if is_bedrock:
            # Bedrock Edition: use bedrock_commands if available, otherwise fall back
            commands = cmd_button.bedrock_commands if cmd_button.bedrock_commands else cmd_button.commands
            self._execute_commands(commands, cmd_button.name)
        elif self.use_datapack_mode and cmd_button.function_id:
            # Java Edition with datapack mode
            # Check if datapack is installed (only warn once per session)
            if not self.datapack_warning_shown and not check_any_world_has_datapack():
                self.datapack_warning_shown = True
                result = messagebox.askyesno(
                    "Datapack Not Found",
                    "The Maricraft datapack was not found in any Minecraft world.\n\n"
                    "Commands may not work without the datapack installed.\n\n"
                    "Click 'Yes' to install the datapack now.\n"
                    "Click 'No' to try anyway (may not work).",
                    icon=messagebox.WARNING
                )
                if result:
                    self._show_install_datapack()
                    return

            # Send single function call
            function_cmd = f"/function {cmd_button.function_id}"
            self._execute_commands([function_cmd], cmd_button.name)
        else:
            # Legacy mode: send all raw commands
            self._execute_commands(cmd_button.commands, cmd_button.name)

    def _execute_commands(self, commands: list[str], name: str) -> None:
        """Execute a list of commands in Minecraft."""
        self.is_running = True
        self.stop_btn.pack(side=tk.RIGHT, padx=(0, 8))
        self.stop_event.clear()

        settings = Settings(
            chat_key=self.chat_key,
            delay_ms=self.delay_ms,
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
                self.root.after(0, self._on_commands_complete)

        threading.Thread(target=worker, daemon=True).start()

    def _on_commands_complete(self) -> None:
        """Called when command execution is complete."""
        self.is_running = False
        self.stop_btn.pack_forget()
        if not self.stop_event.is_set():
            self._set_status("Ready - Click a button to send commands!")

    def on_stop(self) -> None:
        """Handle Stop button click."""
        self.stop_event.set()
        self._set_status("Stopping...")

    def _set_status(self, msg: str) -> None:
        """Thread-safe status update."""
        def _upd() -> None:
            self.status_var.set(msg)
        self.root.after(0, _upd)

    def _show_settings(self) -> None:
        """Show settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("300x180")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 180) // 2
        dialog.geometry(f"+{x}+{y}")

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Chat key setting
        ttk.Label(frame, text="Chat key:").grid(row=0, column=0, sticky="w", pady=5)
        chat_key_var = tk.StringVar(value=self.chat_key)
        chat_frame = ttk.Frame(frame)
        chat_frame.grid(row=0, column=1, sticky="w", pady=5)
        ttk.Radiobutton(chat_frame, text="T", value="t", variable=chat_key_var).pack(side=tk.LEFT)
        ttk.Radiobutton(chat_frame, text="/", value="/", variable=chat_key_var).pack(side=tk.LEFT, padx=(10, 0))

        # Delay setting
        ttk.Label(frame, text="Delay (ms):").grid(row=1, column=0, sticky="w", pady=5)
        delay_var = tk.StringVar(value=str(self.delay_ms))
        delay_spinbox = ttk.Spinbox(
            frame,
            from_=UI_DELAY_MIN_MS,
            to=UI_DELAY_MAX_MS,
            textvariable=delay_var,
            width=10,
        )
        delay_spinbox.grid(row=1, column=1, sticky="w", pady=5)

        # Help text
        help_text = ttk.Label(
            frame,
            text="Increase delay if commands are missed.\nDecrease for faster execution.",
            font=("Segoe UI", 9),
            foreground="gray",
        )
        help_text.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="w")

        # Save button
        def save() -> None:
            self.chat_key = chat_key_var.get()
            try:
                self.delay_ms = int(delay_var.get())
            except ValueError:
                messagebox.showerror("Invalid", "Delay must be a number")
                return
            dialog.destroy()

        ttk.Button(frame, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=(20, 0))

    def _check_for_updates_async(self) -> None:
        """Check for updates and download silently in background."""
        def check() -> None:
            result = check_for_update()
            if result:
                self.update_available = result

                # If running as .exe and exe_download_url available, download silently
                if is_frozen() and result.exe_download_url:
                    def on_download_complete(success: bool, error: str) -> None:
                        if success:
                            self.update_downloaded = True
                            self.root.after(0, lambda: self._show_update_banner(result))
                        else:
                            # Download failed, just show browser download option
                            self.root.after(0, lambda: self._show_update_banner(result))

                    download_update_async(result, on_download_complete)
                else:
                    # Not frozen or no exe URL, just show banner with browser download
                    self.root.after(0, lambda: self._show_update_banner(result))

        threading.Thread(target=check, daemon=True).start()

    def _show_update_banner(self, update_info: UpdateInfo) -> None:
        """Show update available/ready banner."""
        # Remove any existing banner
        if self.update_banner_frame:
            self.update_banner_frame.destroy()

        # Choose banner color based on download status
        if self.update_downloaded:
            bg_color = "#D4EDDA"  # Green - ready to install
            fg_color = "#155724"
            icon_text = "v"
            message = f"Update ready: v{update_info.version}"
        else:
            bg_color = "#FFF3CD"  # Yellow - available
            fg_color = "#856404"
            icon_text = "!"
            message = f"Update available: v{update_info.version}"

        # Create banner frame
        banner = tk.Frame(self.update_banner_container, bg=bg_color, padx=10, pady=5)
        banner.pack(fill=tk.X)

        # Icon
        icon = tk.Label(banner, text=icon_text, bg=bg_color, fg=fg_color, font=("Segoe UI", 12, "bold"))
        icon.pack(side=tk.LEFT, padx=(0, 8))

        # Message
        msg = tk.Label(
            banner,
            text=message,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 10),
        )
        msg.pack(side=tk.LEFT)

        # Install Now button (only if update is downloaded and running as .exe)
        if self.update_downloaded and is_frozen():
            install_btn = ttk.Button(banner, text="Install Now", command=self._start_auto_update)
            install_btn.pack(side=tk.LEFT, padx=(10, 5))

        # Download button (browser fallback)
        download_btn = ttk.Button(banner, text="Download", command=self._open_download_page)
        download_btn.pack(side=tk.LEFT, padx=5)

        # Close button
        def on_close() -> None:
            banner.destroy()
            # Clean up downloaded file if user dismisses
            if self.update_downloaded:
                cleanup_downloaded_update()
                self.update_downloaded = False

        close_btn = tk.Button(
            banner,
            text="X",
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            command=on_close,
        )
        close_btn.pack(side=tk.RIGHT)

        self.update_banner_frame = banner

    def _open_download_page(self) -> None:
        """Open download URL in browser."""
        if self.update_available:
            webbrowser.open(self.update_available.download_url)

    def _start_auto_update(self) -> None:
        """Start the auto-update installation process."""
        if not self.update_available:
            return

        # Confirm with user
        notes = self.update_available.release_notes
        notes_text = f"\n\nWhat's new: {notes}" if notes else ""

        result = messagebox.askyesno(
            "Install Update",
            f"Install Maricraft v{self.update_available.version}?{notes_text}\n\n"
            "The app will close and reopen automatically.",
            icon=messagebox.QUESTION
        )

        if not result:
            return

        # Show progress dialog
        self._show_install_progress_dialog()

    def _show_install_progress_dialog(self) -> None:
        """Show progress dialog during installation."""
        if not self.update_available:
            return

        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Installing Update")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)  # Prevent closing

        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 350) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        dialog.geometry(f"+{x}+{y}")

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            frame,
            text=f"Installing Maricraft v{self.update_available.version}",
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(0, 10))

        # Status label
        status_var = tk.StringVar(value="Verifying download...")
        ttk.Label(frame, textvariable=status_var).pack()

        # Progress bar
        progress = ttk.Progressbar(frame, mode='indeterminate', length=300)
        progress.pack(pady=10)
        progress.start()

        def progress_callback(stage: str, current: int, total: int) -> None:
            self.root.after(0, lambda: status_var.set(stage))

        def do_install() -> None:
            success, error = perform_update(
                self.update_available,
                progress_callback=progress_callback
            )

            if not success:
                self.root.after(0, lambda: self._show_install_error(dialog, error))

        # Run installation in background thread
        threading.Thread(target=do_install, daemon=True).start()

    def _show_install_error(self, dialog: tk.Toplevel, error: str) -> None:
        """Show installation error and close dialog."""
        dialog.destroy()
        messagebox.showerror(
            "Update Failed",
            f"Could not install update:\n\n{error}\n\n"
            "You can download the update manually instead."
        )

    def _show_install_datapack(self) -> None:
        """Show datapack installation dialog with instance selection."""
        from pathlib import Path

        # Get all Minecraft instances (vanilla + CurseForge)
        # Returns list of (name, saves_path, version) tuples
        instances = get_all_minecraft_instances()

        if not instances:
            messagebox.showerror(
                "Minecraft Not Found",
                "Could not find any Minecraft installations.\n\n"
                "Checked locations:\n"
                "- %APPDATA%\\.minecraft\\saves (Vanilla)\n"
                "- CurseForge\\Minecraft\\Instances\\*\\saves\n\n"
                "Make sure Minecraft is installed and has at least one world."
            )
            return

        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Install Maricraft Datapack")
        dialog.geometry("450x530")
        dialog.resizable(True, True)
        dialog.minsize(400, 430)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 450) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 530) // 2
        dialog.geometry(f"+{x}+{y}")

        frame = ttk.Frame(dialog, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        # Instance selector
        ttk.Label(
            frame,
            text="Select Minecraft instance:",
            font=("Segoe UI", 11),
        ).pack(anchor=tk.W, pady=(0, 5))

        # Build display names with version info
        instance_display_names = []
        for name, _path, version in instances:
            if version:
                instance_display_names.append(f"{name} (v{version})")
            else:
                instance_display_names.append(name)

        instance_var = tk.StringVar(value=instance_display_names[0] if instance_display_names else "")
        instance_combo = ttk.Combobox(
            frame,
            textvariable=instance_var,
            values=instance_display_names,
            state="readonly",
            width=50,
        )
        instance_combo.pack(fill=tk.X, pady=(0, 10))

        # Version info label
        version_label = ttk.Label(
            frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            foreground="#006600",
        )
        version_label.pack(anchor=tk.W, pady=(0, 10))

        # Worlds label
        ttk.Label(
            frame,
            text="Worlds in this instance:",
            font=("Segoe UI", 11),
        ).pack(anchor=tk.W, pady=(0, 5))

        # World list with checkboxes (scrollable)
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(list_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Current world checkboxes (mutable list for updates)
        world_vars: list[tuple[tk.BooleanVar, str, str]] = []

        # Path info label (will be updated)
        path_label = ttk.Label(
            frame,
            text="",
            font=("Segoe UI", 9),
            foreground="gray",
        )

        # Store current instance info for installation
        current_instance_info: dict = {"version": None, "saves_path": None}

        def refresh_worlds() -> None:
            """Refresh the world list based on selected instance."""
            # Clear existing checkboxes
            for widget in scrollable.winfo_children():
                widget.destroy()
            world_vars.clear()

            # Get selected instance (match by display name prefix)
            selected_display = instance_var.get()
            saves_path = None
            mc_version = None

            for idx, (name, path, version) in enumerate(instances):
                if instance_display_names[idx] == selected_display:
                    saves_path = path
                    mc_version = version
                    break

            if not saves_path:
                return

            # Store for installation
            current_instance_info["version"] = mc_version
            current_instance_info["saves_path"] = saves_path

            # Update version label
            if mc_version:
                version_label.config(
                    text=f"Detected: Minecraft {mc_version}",
                    foreground="#006600"
                )
            else:
                version_label.config(
                    text="Version: Unknown (using 1.20.x compatibility mode)",
                    foreground="#666600"
                )

            # Update path label
            path_label.config(text=f"Path: {saves_path}")

            # Get worlds for this instance
            worlds = list_worlds(saves_path)

            if not worlds:
                ttk.Label(
                    scrollable,
                    text="No worlds found in this instance.",
                    foreground="gray",
                ).pack(anchor=tk.W, pady=10)
                return

            # Create checkbox for each world
            for world_name, world_path in worlds:
                var = tk.BooleanVar(value=True)
                installed = is_datapack_installed(world_path)

                cb_frame = ttk.Frame(scrollable)
                cb_frame.pack(fill=tk.X, pady=2)

                cb = ttk.Checkbutton(cb_frame, text=world_name, variable=var)
                cb.pack(side=tk.LEFT)

                if installed:
                    ttk.Label(cb_frame, text="(installed)", foreground="green").pack(side=tk.LEFT, padx=(5, 0))

                world_vars.append((var, world_name, str(world_path)))

        # Bind instance change to refresh
        instance_combo.bind("<<ComboboxSelected>>", lambda e: refresh_worlds())

        # Initial load
        refresh_worlds()

        # Buttons frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        # Select all / none buttons
        def select_all() -> None:
            for var, _, _ in world_vars:
                var.set(True)

        def select_none() -> None:
            for var, _, _ in world_vars:
                var.set(False)

        ttk.Button(btn_frame, text="Select All", command=select_all).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Select None", command=select_none).pack(side=tk.LEFT, padx=(5, 0))

        # Install button
        def do_install() -> None:
            selected = [(name, Path(path)) for var, name, path in world_vars if var.get()]
            if not selected:
                messagebox.showinfo("No Selection", "Please select at least one world.")
                return

            mc_version = current_instance_info.get("version")
            success = 0
            failed = 0
            for name, path in selected:
                if install_datapack(path, mc_version=mc_version):
                    success += 1
                else:
                    failed += 1

            dialog.destroy()

            version_info = f" (for Minecraft {mc_version})" if mc_version else ""
            if failed == 0:
                messagebox.showinfo(
                    "Installation Complete",
                    f"Datapack installed to {success} world(s){version_info}!\n\n"
                    "In Minecraft, run /reload or restart the world to activate."
                )
            else:
                messagebox.showwarning(
                    "Partial Installation",
                    f"Installed to {success} world(s), {failed} failed{version_info}.\n\n"
                    "In Minecraft, run /reload or restart the world to activate."
                )

        ttk.Button(btn_frame, text="Install to Selected", command=do_install).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=(0, 5))

        # Path info (placed after buttons)
        path_label.pack(anchor=tk.W, pady=(10, 0))


def main() -> None:
    """Application entry point."""
    if tk is None:
        raise SystemExit("tkinter is required to run the UI.")
    root = tk.Tk()
    App(root)
    root.mainloop()
