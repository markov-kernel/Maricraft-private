"""Search bar component with real-time filtering."""

from __future__ import annotations

from typing import Callable, Optional

import customtkinter as ctk

from ..theme import COLORS, FONTS, RADIUS, SPACING


class SearchBar(ctk.CTkFrame):
    """Search bar with placeholder, clear button, and result count."""

    def __init__(
        self,
        parent,
        on_search: Callable[[str], None],
        placeholder: str = "Search...",
    ):
        super().__init__(parent, fg_color="transparent")

        self.on_search = on_search
        self._debounce_id: Optional[str] = None

        # Search icon (using Unicode)
        search_icon = ctk.CTkLabel(
            self,
            text="\U0001F50D",  # Magnifying glass emoji
            font=("Segoe UI", 14),
            text_color=COLORS["text_secondary"],
        )
        search_icon.pack(side="left", padx=(0, SPACING["sm"]))

        # Search entry
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            font=FONTS["body"],
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["surface"],
            border_color=COLORS["surface_light"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["text_secondary"],
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<KeyRelease>", self._on_key_release)

        # Clear button (hidden initially)
        self.clear_btn = ctk.CTkButton(
            self,
            text="\u2715",  # X symbol
            font=("Segoe UI", 14),
            width=35,
            height=35,
            corner_radius=RADIUS["sm"],
            fg_color="transparent",
            hover_color=COLORS["surface_light"],
            text_color=COLORS["text_secondary"],
            command=self._clear,
        )
        # Hidden by default

        # Result count label (hidden initially)
        self.result_label = ctk.CTkLabel(
            self,
            text="",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        )
        # Hidden by default

    def _on_key_release(self, event) -> None:
        """Handle key release with debounce."""
        # Cancel previous debounce
        if self._debounce_id:
            self.after_cancel(self._debounce_id)

        # Schedule new search after 150ms
        self._debounce_id = self.after(150, self._do_search)

    def _do_search(self) -> None:
        """Perform the search."""
        query = self.entry.get()
        self.on_search(query)

        # Show/hide clear button
        if query:
            self.clear_btn.pack(side="left", padx=(SPACING["xs"], 0))
        else:
            self.clear_btn.pack_forget()
            self.result_label.pack_forget()

    def _clear(self) -> None:
        """Clear the search."""
        self.entry.delete(0, "end")
        self.clear_btn.pack_forget()
        self.result_label.pack_forget()
        self.on_search("")

    def set_result_count(self, visible: int, total: int) -> None:
        """Show result count."""
        self.result_label.configure(text=f"{visible} of {total}")
        self.result_label.pack(side="left", padx=(SPACING["sm"], 0))

    def clear_result_count(self) -> None:
        """Hide result count."""
        self.result_label.pack_forget()

    def get_query(self) -> str:
        """Get current search query."""
        return self.entry.get()
