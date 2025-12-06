"""Status bar component."""

from __future__ import annotations

import customtkinter as ctk

from ..theme import COLORS, FONTS, RADIUS, SPACING


class StatusBar(ctk.CTkFrame):
    """Bottom status bar showing current status message."""

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=COLORS["surface"],
            corner_radius=RADIUS["md"],
            height=40,
        )

        # Status icon (changes based on state)
        self.icon_label = ctk.CTkLabel(
            self,
            text="\u2713",  # Checkmark
            font=("Segoe UI", 14),
            text_color=COLORS["success"],
        )
        self.icon_label.pack(side="left", padx=SPACING["md"])

        # Status message
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=FONTS["body"],
            text_color=COLORS["text"],
            anchor="w",
        )
        self.status_label.pack(side="left", fill="x", expand=True)

    def set_status(self, message: str, status_type: str = "info") -> None:
        """Set status message with optional type for icon color."""
        self.status_label.configure(text=message)

        # Update icon based on type
        if status_type == "success" or "Ready" in message:
            self.icon_label.configure(text="\u2713", text_color=COLORS["success"])
        elif status_type == "error":
            self.icon_label.configure(text="\u2717", text_color=COLORS["danger"])
        elif status_type == "warning" or "Stopping" in message:
            self.icon_label.configure(text="\u26A0", text_color=COLORS["warning"])
        elif "Running" in message:
            self.icon_label.configure(text="\u23F3", text_color=COLORS["primary"])
        else:
            self.icon_label.configure(text="\u2139", text_color=COLORS["primary"])
