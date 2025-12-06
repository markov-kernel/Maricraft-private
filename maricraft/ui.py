"""Tkinter UI for Maricraft - Kid-friendly Minecraft command helper."""

from __future__ import annotations

import threading
from typing import Optional

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
from .logger import Logger
from .settings import Settings


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
        self.root.title("Maricraft Helper")
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

        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build all UI widgets."""
        pad = 10

        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=pad, pady=pad)

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

    def _on_button_click(self, cmd_button: CommandButton) -> None:
        """Handle command button click."""
        if self.is_running:
            messagebox.showinfo("Busy", "Please wait for the current command to finish.")
            return

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


def main() -> None:
    """Application entry point."""
    if tk is None:
        raise SystemExit("tkinter is required to run the UI.")
    root = tk.Tk()
    App(root)
    root.mainloop()
