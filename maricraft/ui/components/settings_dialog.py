"""Settings dialog component."""

from __future__ import annotations

import customtkinter as ctk

from ..state import AppState, StateManager
from ..theme import COLORS, FONTS, RADIUS, SPACING


class SettingsDialog(ctk.CTkToplevel):
    """Settings configuration dialog."""

    def __init__(self, parent, app_state: AppState, state_manager: StateManager):
        super().__init__(parent)

        self.app_state = app_state
        self.state_manager = state_manager

        # Window setup
        self.title("Settings")
        self.geometry("400x400")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["background"])

        # Center on parent
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 400) // 2
        self.geometry(f"+{x}+{y}")

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the settings UI."""
        # Main container
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["xl"])

        # Title
        title = ctk.CTkLabel(
            main,
            text="Settings",
            font=FONTS["heading"],
            text_color=COLORS["text"],
        )
        title.pack(anchor="w", pady=(0, SPACING["lg"]))

        # Chat key setting
        chat_frame = ctk.CTkFrame(main, fg_color="transparent")
        chat_frame.pack(fill="x", pady=SPACING["sm"])

        ctk.CTkLabel(
            chat_frame,
            text="Chat key:",
            font=FONTS["body"],
            text_color=COLORS["text"],
        ).pack(side="left")

        self.chat_key_var = ctk.StringVar(value=self.app_state.settings.chat_key)

        chat_options = ctk.CTkFrame(chat_frame, fg_color="transparent")
        chat_options.pack(side="right")

        ctk.CTkRadioButton(
            chat_options,
            text="T",
            variable=self.chat_key_var,
            value="t",
            font=FONTS["body"],
            text_color=COLORS["text"],
            fg_color=COLORS["primary"],
        ).pack(side="left", padx=SPACING["sm"])

        ctk.CTkRadioButton(
            chat_options,
            text="/",
            variable=self.chat_key_var,
            value="/",
            font=FONTS["body"],
            text_color=COLORS["text"],
            fg_color=COLORS["primary"],
        ).pack(side="left")

        # Delay setting
        delay_frame = ctk.CTkFrame(main, fg_color="transparent")
        delay_frame.pack(fill="x", pady=SPACING["sm"])

        ctk.CTkLabel(
            delay_frame,
            text="Command delay (ms):",
            font=FONTS["body"],
            text_color=COLORS["text"],
        ).pack(side="left")

        self.delay_var = ctk.StringVar(value=str(self.app_state.settings.delay_ms))
        self.delay_entry = ctk.CTkEntry(
            delay_frame,
            textvariable=self.delay_var,
            width=80,
            font=FONTS["body"],
            fg_color=COLORS["surface"],
            border_color=COLORS["surface_light"],
            text_color=COLORS["text"],
        )
        self.delay_entry.pack(side="right")

        # Help text for delay
        help_text = ctk.CTkLabel(
            main,
            text="Increase delay if commands are missed.\nDecrease for faster execution.",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
            justify="left",
        )
        help_text.pack(anchor="w", pady=(SPACING["xs"], SPACING["lg"]))

        # Appearance mode
        appearance_frame = ctk.CTkFrame(main, fg_color="transparent")
        appearance_frame.pack(fill="x", pady=SPACING["sm"])

        ctk.CTkLabel(
            appearance_frame,
            text="Appearance:",
            font=FONTS["body"],
            text_color=COLORS["text"],
        ).pack(side="left")

        self.appearance_var = ctk.StringVar(value=self.app_state.appearance.mode)
        appearance_menu = ctk.CTkOptionMenu(
            appearance_frame,
            variable=self.appearance_var,
            values=["dark", "light", "system"],
            font=FONTS["body"],
            fg_color=COLORS["surface"],
            button_color=COLORS["surface_light"],
            button_hover_color=COLORS["hover"],
            dropdown_fg_color=COLORS["surface"],
            dropdown_hover_color=COLORS["surface_light"],
            text_color=COLORS["text"],
            command=self._on_appearance_change,
        )
        appearance_menu.pack(side="right")

        # Datapack mode toggle
        datapack_frame = ctk.CTkFrame(main, fg_color="transparent")
        datapack_frame.pack(fill="x", pady=SPACING["sm"])

        ctk.CTkLabel(
            datapack_frame,
            text="Use datapack mode:",
            font=FONTS["body"],
            text_color=COLORS["text"],
        ).pack(side="left")

        self.datapack_var = ctk.BooleanVar(value=self.app_state.settings.use_datapack_mode)
        ctk.CTkSwitch(
            datapack_frame,
            text="",
            variable=self.datapack_var,
            fg_color=COLORS["surface_light"],
            progress_color=COLORS["success"],
        ).pack(side="right")

        # Auto-install datapack toggle
        auto_install_frame = ctk.CTkFrame(main, fg_color="transparent")
        auto_install_frame.pack(fill="x", pady=SPACING["sm"])

        ctk.CTkLabel(
            auto_install_frame,
            text="Auto-install datapack:",
            font=FONTS["body"],
            text_color=COLORS["text"],
        ).pack(side="left")

        self.auto_install_var = ctk.BooleanVar(value=self.app_state.settings.auto_install_datapack)
        ctk.CTkSwitch(
            auto_install_frame,
            text="",
            variable=self.auto_install_var,
            fg_color=COLORS["surface_light"],
            progress_color=COLORS["success"],
        ).pack(side="right")

        # Buttons
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(SPACING["xl"], 0))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            font=FONTS["body"],
            width=100,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["hover"],
            command=self.destroy,
        ).pack(side="right")

        ctk.CTkButton(
            btn_frame,
            text="Save",
            font=FONTS["body"],
            width=100,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["success"],
            command=self._save,
        ).pack(side="right", padx=(0, SPACING["sm"]))

    def _on_appearance_change(self, value: str) -> None:
        """Preview appearance change."""
        ctk.set_appearance_mode(value)

    def _save(self) -> None:
        """Save settings and close."""
        # Validate delay
        try:
            delay = int(self.delay_var.get())
            if delay < 50 or delay > 500:
                raise ValueError()
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("Invalid", "Delay must be a number between 50 and 500")
            return

        # Update state
        self.app_state.settings.chat_key = self.chat_key_var.get()
        self.app_state.settings.delay_ms = delay
        self.app_state.settings.use_datapack_mode = self.datapack_var.get()
        self.app_state.settings.auto_install_datapack = self.auto_install_var.get()
        self.app_state.appearance.mode = self.appearance_var.get()

        # Save and close
        self.state_manager.save()
        self.destroy()
