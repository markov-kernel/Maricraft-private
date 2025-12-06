"""Command button widget with favorite star."""

from __future__ import annotations

from typing import Callable, Optional

import customtkinter as ctk

from ...commands import CommandButton
from ..theme import COLORS, FONTS, RADIUS, SPACING, calculate_text_color, lighten_color


class CommandButtonWidget(ctk.CTkFrame):
    """A styled command button with optional favorite star."""

    def __init__(
        self,
        parent,
        button: CommandButton,
        on_click: Callable[[CommandButton], None],
        on_favorite_toggle: Optional[Callable[[str], bool]] = None,
        is_favorite: bool = False,
        show_star: bool = True,
        compact: bool = False,
    ):
        super().__init__(parent, fg_color="transparent")

        self.button = button
        self.on_click = on_click
        self.on_favorite_toggle = on_favorite_toggle
        self._is_favorite = is_favorite
        self._visible = True

        # Calculate colors
        bg_color = button.color
        text_color = calculate_text_color(bg_color)
        hover_color = lighten_color(bg_color, 25)

        # Button dimensions
        if compact:
            width = 100
            height = 35
            font = FONTS["button_small"]
        else:
            width = 140
            height = 45
            font = FONTS["button"]

        # Main button
        self.btn = ctk.CTkButton(
            self,
            text=button.name,
            font=font,
            width=width,
            height=height,
            corner_radius=RADIUS["md"],
            fg_color=bg_color,
            hover_color=hover_color,
            text_color=text_color,
            command=self._handle_click,
        )
        self.btn.pack(side="left", fill="both", expand=True)

        # Favorite star (if enabled)
        if show_star and on_favorite_toggle:
            self.star_btn = ctk.CTkButton(
                self,
                text=self._get_star_text(),
                font=("Segoe UI", 14),
                width=30,
                height=height,
                corner_radius=RADIUS["sm"],
                fg_color="transparent",
                hover_color=COLORS["surface_light"],
                text_color=self._get_star_color(),
                command=self._toggle_favorite,
            )
            self.star_btn.pack(side="right", padx=(SPACING["xs"], 0))
        else:
            self.star_btn = None

        # Tooltip
        self._setup_tooltip()

    def _get_star_text(self) -> str:
        """Get star character based on favorite state."""
        return "\u2605" if self._is_favorite else "\u2606"  # Filled vs empty star

    def _get_star_color(self) -> str:
        """Get star color based on favorite state."""
        return COLORS["favorite"] if self._is_favorite else COLORS["text_secondary"]

    def _handle_click(self) -> None:
        """Handle button click."""
        self.on_click(self.button)

    def _toggle_favorite(self) -> None:
        """Toggle favorite state."""
        if self.on_favorite_toggle:
            self._is_favorite = self.on_favorite_toggle(self.button.function_id)
            self._update_star()

    def _update_star(self) -> None:
        """Update star appearance."""
        if self.star_btn:
            self.star_btn.configure(
                text=self._get_star_text(),
                text_color=self._get_star_color(),
            )

    def set_favorite(self, is_favorite: bool) -> None:
        """Set favorite state externally."""
        self._is_favorite = is_favorite
        self._update_star()

    def set_visible(self, visible: bool) -> None:
        """Show or hide the button."""
        if visible and not self._visible:
            self.pack(side="left", padx=SPACING["xs"], pady=SPACING["xs"])
            self._visible = True
        elif not visible and self._visible:
            self.pack_forget()
            self._visible = False

    def _setup_tooltip(self) -> None:
        """Set up hover tooltip."""
        from .tooltip import ToolTip
        ToolTip(self.btn, self.button.description)
