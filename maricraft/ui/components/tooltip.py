"""Tooltip component for hover hints."""

from __future__ import annotations

from typing import Optional

import customtkinter as ctk

from ..theme import COLORS, FONTS, RADIUS, SPACING


class ToolTip:
    """Simple tooltip that appears on hover."""

    def __init__(self, widget, text: str, delay_ms: int = 500):
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self.tooltip_window: Optional[ctk.CTkToplevel] = None
        self._after_id: Optional[str] = None

        # Bind events
        widget.bind("<Enter>", self._schedule_show, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<Button-1>", self._hide, add="+")
        widget.bind("<Destroy>", self._on_destroy, add="+")

    def _schedule_show(self, event) -> None:
        """Schedule tooltip to show after delay."""
        self._cancel_schedule()
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _cancel_schedule(self) -> None:
        """Cancel any scheduled tooltip."""
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self) -> None:
        """Show the tooltip."""
        self._after_id = None

        # Don't show if widget is gone or another tooltip exists
        if self.tooltip_window:
            return

        try:
            if not self.widget.winfo_exists():
                return
        except Exception:
            return

        # Position tooltip below and to the right of widget
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        except Exception:
            return

        # Create tooltip window
        try:
            self.tooltip_window = ctk.CTkToplevel(self.widget)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            self.tooltip_window.attributes("-topmost", True)

            # Bind leave on tooltip window itself (in case mouse moves onto it)
            self.tooltip_window.bind("<Leave>", self._hide)

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

        except Exception:
            self._cleanup_tooltip()

    def _hide(self, event=None) -> None:
        """Hide the tooltip."""
        self._cancel_schedule()
        self._cleanup_tooltip()

    def _cleanup_tooltip(self) -> None:
        """Safely destroy tooltip window."""
        if self.tooltip_window:
            try:
                self.tooltip_window.destroy()
            except Exception:
                pass
            self.tooltip_window = None

    def _on_destroy(self, event=None) -> None:
        """Clean up when widget is destroyed."""
        self._cancel_schedule()
        self._cleanup_tooltip()
