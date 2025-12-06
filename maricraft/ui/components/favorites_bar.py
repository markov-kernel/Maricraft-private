"""Favorites bar showing pinned command buttons."""

from __future__ import annotations

from typing import Callable, List, Optional

import customtkinter as ctk

from ...commands import CommandButton
from ..theme import COLORS, FONTS, RADIUS, SPACING


class FavoritesBar(ctk.CTkFrame):
    """Horizontal bar displaying favorite commands."""

    def __init__(
        self,
        parent,
        favorites: List[str],
        on_click: Callable[[str], None],
        get_button_info: Callable[[str], Optional[CommandButton]],
    ):
        super().__init__(
            parent,
            fg_color=COLORS["surface"],
            corner_radius=RADIUS["md"],
            height=50,
        )

        self.favorites = favorites
        self.on_click = on_click
        self.get_button_info = get_button_info
        self.favorite_buttons: List[ctk.CTkButton] = []

        # Star icon
        self.star_label = ctk.CTkLabel(
            self,
            text="\u2605",  # Filled star
            font=("Segoe UI", 16),
            text_color=COLORS["favorite"],
        )
        self.star_label.pack(side="left", padx=SPACING["md"])

        # Favorites container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="left", fill="both", expand=True, padx=SPACING["xs"])

        # Empty message
        self.empty_label = ctk.CTkLabel(
            self.container,
            text="Click \u2606 on any command to add favorites",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        )

        self._rebuild_favorites()

    def _rebuild_favorites(self) -> None:
        """Rebuild the favorites display."""
        # Clear existing buttons
        for btn in self.favorite_buttons:
            btn.destroy()
        self.favorite_buttons.clear()
        self.empty_label.pack_forget()

        if not self.favorites:
            self.empty_label.pack(side="left", pady=SPACING["sm"])
            return

        # Create compact buttons for each favorite
        for function_id in self.favorites:
            button_info = self.get_button_info(function_id)
            if button_info:
                btn = ctk.CTkButton(
                    self.container,
                    text=button_info.name,
                    font=FONTS["button_small"],
                    width=90,
                    height=32,
                    corner_radius=RADIUS["sm"],
                    fg_color=button_info.color,
                    hover_color=COLORS["hover"],
                    command=lambda fid=function_id: self.on_click(fid),
                )
                btn.pack(side="left", padx=SPACING["xs"], pady=SPACING["xs"])
                self.favorite_buttons.append(btn)

    def update_favorites(self, favorites: List[str]) -> None:
        """Update the favorites list and rebuild display."""
        self.favorites = favorites
        self._rebuild_favorites()

    def add_favorite(self, function_id: str) -> None:
        """Add a favorite."""
        if function_id not in self.favorites:
            self.favorites.append(function_id)
            self._rebuild_favorites()

    def remove_favorite(self, function_id: str) -> None:
        """Remove a favorite."""
        if function_id in self.favorites:
            self.favorites.remove(function_id)
            self._rebuild_favorites()
