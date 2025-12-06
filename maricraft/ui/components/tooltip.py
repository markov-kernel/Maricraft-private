"""Tooltip component for hover hints."""

from __future__ import annotations

from typing import Optional

import customtkinter as ctk

from ..theme import COLORS, FONTS, RADIUS, SPACING


class ToolTip:
    """Simple tooltip that appears on hover."""

    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tooltip_window: Optional[ctk.CTkToplevel] = None

        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, event) -> None:
        """Show the tooltip."""
        if self.tooltip_window:
            return

        # Position tooltip below and to the right of cursor
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Create tooltip window
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Remove window decorations and make it float
        self.tooltip_window.attributes("-topmost", True)

        # Tooltip frame
        frame = ctk.CTkFrame(
            self.tooltip_window,
            fg_color=COLORS["surface_light"],
            corner_radius=RADIUS["sm"],
            border_width=1,
            border_color=COLORS["text_secondary"],
        )
        frame.pack(fill="both", expand=True)

        # Tooltip text
        label = ctk.CTkLabel(
            frame,
            text=self.text,
            font=FONTS["small"],
            text_color=COLORS["text"],
            wraplength=250,
            justify="left",
        )
        label.pack(padx=SPACING["sm"], pady=SPACING["xs"])

    def _hide(self, event) -> None:
        """Hide the tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
