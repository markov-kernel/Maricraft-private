"""Category frame containing command buttons."""

from __future__ import annotations

from typing import Callable, List

import customtkinter as ctk

from ...commands import CommandCategory, CommandButton
from ..theme import COLORS, FONTS, RADIUS, SPACING, get_category_color
from .command_button import CommandButtonWidget


class CategoryFrame(ctk.CTkFrame):
    """A collapsible frame containing command buttons for a category."""

    def __init__(
        self,
        parent,
        category: CommandCategory,
        on_button_click: Callable[[CommandButton], None],
        on_favorite_toggle: Callable[[str], bool],
        is_favorite_fn: Callable[[str], bool],
    ):
        super().__init__(
            parent,
            fg_color=COLORS["surface"],
            corner_radius=RADIUS["lg"],
        )

        self.category = category
        self.on_button_click = on_button_click
        self.on_favorite_toggle = on_favorite_toggle
        self.is_favorite_fn = is_favorite_fn
        self.buttons: List[CommandButtonWidget] = []
        self._expanded = True

        # Category color
        cat_color = get_category_color(category.name)

        # Header with category name and toggle
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=SPACING["md"], pady=(SPACING["md"], SPACING["sm"]))

        # Color accent bar
        accent = ctk.CTkFrame(
            self.header,
            fg_color=cat_color,
            width=4,
            height=30,
            corner_radius=2,
        )
        accent.pack(side="left", padx=(0, SPACING["sm"]))

        # Category label
        self.label = ctk.CTkLabel(
            self.header,
            text=category.name,
            font=FONTS["heading"],
            text_color=COLORS["text"],
        )
        self.label.pack(side="left")

        # Button count
        self.count_label = ctk.CTkLabel(
            self.header,
            text=f"({len(category.buttons)})",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        )
        self.count_label.pack(side="left", padx=(SPACING["sm"], 0))

        # Toggle button
        self.toggle_btn = ctk.CTkButton(
            self.header,
            text="\u25BC",  # Down arrow
            font=("Segoe UI", 12),
            width=30,
            height=30,
            corner_radius=RADIUS["sm"],
            fg_color="transparent",
            hover_color=COLORS["surface_light"],
            text_color=COLORS["text_secondary"],
            command=self._toggle_expand,
        )
        self.toggle_btn.pack(side="right")

        # Button container (uses grid layout with wrapping)
        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["md"]))

        # Create buttons
        self._create_buttons()

        # Re-layout on resize
        self.bind("<Configure>", self._on_resize)

    def _create_buttons(self) -> None:
        """Create command buttons for this category."""
        for button in self.category.buttons:
            is_fav = self.is_favorite_fn(button.function_id) if button.function_id else False

            btn_widget = CommandButtonWidget(
                self.button_container,
                button=button,
                on_click=self.on_button_click,
                on_favorite_toggle=self.on_favorite_toggle,
                is_favorite=is_fav,
            )
            self.buttons.append(btn_widget)

        # Initial layout
        self._layout_buttons()

    def _on_resize(self, event=None) -> None:
        """Handle resize to re-layout buttons."""
        if event and event.widget == self:
            self._layout_buttons()

    def _layout_buttons(self) -> None:
        """Layout buttons in a responsive grid."""
        if not self.buttons:
            return

        # Calculate columns based on container width
        container_width = self.winfo_width()
        if container_width < 50:  # Not yet sized
            container_width = 800  # Default

        button_width = 180  # Button + star + padding
        columns = max(2, min(6, (container_width - 20) // button_width))

        # Place buttons in grid
        for idx, btn_widget in enumerate(self.buttons):
            if btn_widget._visible:
                row = idx // columns
                col = idx % columns
                btn_widget.grid(row=row, column=col, padx=SPACING["xs"], pady=SPACING["xs"], sticky="w")

        # Configure column weights for even distribution
        for col in range(columns):
            self.button_container.columnconfigure(col, weight=1)

    def _toggle_expand(self) -> None:
        """Toggle category expansion."""
        self._expanded = not self._expanded

        if self._expanded:
            self.button_container.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["md"]))
            self.toggle_btn.configure(text="\u25BC")  # Down arrow
        else:
            self.button_container.pack_forget()
            self.toggle_btn.configure(text="\u25B6")  # Right arrow

    def update_button_favorites(self) -> None:
        """Update favorite state of all buttons."""
        for btn_widget in self.buttons:
            if btn_widget.button.function_id:
                is_fav = self.is_favorite_fn(btn_widget.button.function_id)
                btn_widget.set_favorite(is_fav)
