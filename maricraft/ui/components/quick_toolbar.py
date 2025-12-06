"""Quick access toolbar - floating window with favorite commands."""

from __future__ import annotations

from typing import Callable, List, Optional

import customtkinter as ctk

from ...commands import CommandButton
from ..state import get_state, get_state_manager
from ..theme import COLORS, FONTS, RADIUS, SPACING


class QuickToolbar(ctk.CTkToplevel):
    """Floating toolbar window showing favorite commands."""

    def __init__(
        self,
        parent,
        favorites: List[str],
        on_click: Callable[[str], None],
        get_button_info: Callable[[str], Optional[CommandButton]],
    ):
        super().__init__(parent)

        self.favorites = favorites
        self.on_click = on_click
        self.get_button_info = get_button_info
        self.state = get_state()
        self.state_manager = get_state_manager()
        self._dragging = False
        self._drag_start_x = 0
        self._drag_start_y = 0

        # Window setup
        self.title("Maricraft Quick Access")
        self.configure(fg_color=COLORS["background"])
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", self.state.quick_toolbar.always_on_top)

        # Restore position
        x = self.state.quick_toolbar.x
        y = self.state.quick_toolbar.y
        self.geometry(f"+{x}+{y}")

        self._build_ui()

        # Bind drag events
        self.bind("<Button-1>", self._start_drag)
        self.bind("<B1-Motion>", self._do_drag)
        self.bind("<ButtonRelease-1>", self._stop_drag)

    def _build_ui(self) -> None:
        """Build the toolbar UI."""
        # Main container with border effect
        main = ctk.CTkFrame(
            self,
            fg_color=COLORS["surface"],
            corner_radius=RADIUS["md"],
            border_width=1,
            border_color=COLORS["surface_light"],
        )
        main.pack(fill="both", expand=True, padx=2, pady=2)

        # Header bar (draggable)
        header = ctk.CTkFrame(main, fg_color=COLORS["surface_light"], height=30)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Title
        title = ctk.CTkLabel(
            header,
            text="\u2605 Quick Access",
            font=FONTS["small"],
            text_color=COLORS["favorite"],
        )
        title.pack(side="left", padx=SPACING["sm"])

        # Close button
        close_btn = ctk.CTkButton(
            header,
            text="\u2715",
            font=("Segoe UI", 10),
            width=25,
            height=25,
            corner_radius=RADIUS["sm"],
            fg_color="transparent",
            hover_color=COLORS["danger"],
            text_color=COLORS["text_secondary"],
            command=self._close,
        )
        close_btn.pack(side="right", padx=2, pady=2)

        # Pin button (toggle always on top)
        self.pin_btn = ctk.CTkButton(
            header,
            text="\U0001F4CC" if self.state.quick_toolbar.always_on_top else "\U0001F4CE",
            font=("Segoe UI", 10),
            width=25,
            height=25,
            corner_radius=RADIUS["sm"],
            fg_color="transparent",
            hover_color=COLORS["hover"],
            text_color=COLORS["text_secondary"],
            command=self._toggle_pin,
        )
        self.pin_btn.pack(side="right", padx=2, pady=2)

        # Button container
        self.button_container = ctk.CTkFrame(main, fg_color="transparent")
        self.button_container.pack(fill="both", expand=True, padx=SPACING["xs"], pady=SPACING["xs"])

        self._rebuild_buttons()

    def _rebuild_buttons(self) -> None:
        """Rebuild the favorite buttons."""
        # Clear existing
        for widget in self.button_container.winfo_children():
            widget.destroy()

        if not self.favorites:
            empty = ctk.CTkLabel(
                self.button_container,
                text="No favorites yet",
                font=FONTS["small"],
                text_color=COLORS["text_secondary"],
            )
            empty.pack(pady=SPACING["sm"])
            return

        # Create compact buttons in a grid (2 columns)
        for idx, function_id in enumerate(self.favorites):
            button_info = self.get_button_info(function_id)
            if button_info:
                btn = ctk.CTkButton(
                    self.button_container,
                    text=button_info.name[:12],  # Truncate long names
                    font=FONTS["button_small"],
                    width=80,
                    height=30,
                    corner_radius=RADIUS["sm"],
                    fg_color=button_info.color,
                    hover_color=COLORS["hover"],
                    command=lambda fid=function_id: self._on_button_click(fid),
                )
                row = idx // 2
                col = idx % 2
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

        # Make columns equal width
        self.button_container.columnconfigure(0, weight=1)
        self.button_container.columnconfigure(1, weight=1)

        # Update window size
        self.update_idletasks()
        width = max(180, self.button_container.winfo_reqwidth() + 20)
        height = self.button_container.winfo_reqheight() + 50  # header + padding
        self.geometry(f"{width}x{height}")

    def _on_button_click(self, function_id: str) -> None:
        """Handle button click."""
        self.on_click(function_id)

    def _start_drag(self, event) -> None:
        """Start window drag."""
        self._dragging = True
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _do_drag(self, event) -> None:
        """Perform window drag."""
        if self._dragging:
            x = self.winfo_x() + event.x - self._drag_start_x
            y = self.winfo_y() + event.y - self._drag_start_y
            self.geometry(f"+{x}+{y}")

    def _stop_drag(self, event) -> None:
        """Stop window drag and save position."""
        if self._dragging:
            self._dragging = False
            self.state.quick_toolbar.x = self.winfo_x()
            self.state.quick_toolbar.y = self.winfo_y()
            self.state_manager.schedule_save(self)

    def _toggle_pin(self) -> None:
        """Toggle always-on-top."""
        self.state.quick_toolbar.always_on_top = not self.state.quick_toolbar.always_on_top
        self.attributes("-topmost", self.state.quick_toolbar.always_on_top)
        self.pin_btn.configure(
            text="\U0001F4CC" if self.state.quick_toolbar.always_on_top else "\U0001F4CE"
        )
        self.state_manager.schedule_save(self)

    def _close(self) -> None:
        """Close the toolbar."""
        self.state.quick_toolbar.visible = False
        self.state_manager.save()
        self.destroy()

    def update_favorites(self, favorites: List[str]) -> None:
        """Update favorites and rebuild."""
        self.favorites = favorites
        self._rebuild_buttons()
