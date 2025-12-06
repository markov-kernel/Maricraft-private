"""Datapack installation dialog."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Optional

import customtkinter as ctk

from ...datapack import (
    get_all_minecraft_instances,
    list_worlds,
    list_bedrock_worlds,
    is_datapack_installed,
    is_behavior_pack_installed,
    install_datapack,
    install_behavior_pack,
)
from ..theme import COLORS, FONTS, RADIUS, SPACING


class InstallDatapackDialog(ctk.CTkToplevel):
    """Dialog for installing the Maricraft datapack to Minecraft worlds."""

    def __init__(self, parent):
        super().__init__(parent)

        # Window setup
        self.title("Install Maricraft Datapack")
        self.geometry("500x550")
        self.resizable(True, True)
        self.minsize(450, 450)
        self.configure(fg_color=COLORS["background"])

        # Center on parent
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 500) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 550) // 2
        self.geometry(f"+{x}+{y}")

        # Get instances
        self.instances = get_all_minecraft_instances()
        self.world_vars: List[Tuple[ctk.BooleanVar, str, Path]] = []
        self.current_version: Optional[str] = None
        self.current_saves_path: Optional[Path] = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the dialog UI."""
        if not self.instances:
            self._show_no_instances()
            return

        # Main container
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])

        # Instance selector
        ctk.CTkLabel(
            main,
            text="Select Minecraft instance:",
            font=FONTS["heading"],
            text_color=COLORS["text"],
        ).pack(anchor="w", pady=(0, SPACING["sm"]))

        # Build display names with version
        self.instance_display_names = []
        for name, _path, version in self.instances:
            if version:
                self.instance_display_names.append(f"{name} (v{version})")
            else:
                self.instance_display_names.append(name)

        self.instance_var = ctk.StringVar(
            value=self.instance_display_names[0] if self.instance_display_names else ""
        )

        instance_menu = ctk.CTkOptionMenu(
            main,
            variable=self.instance_var,
            values=self.instance_display_names,
            font=FONTS["body"],
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["surface"],
            button_color=COLORS["surface_light"],
            button_hover_color=COLORS["hover"],
            dropdown_fg_color=COLORS["surface"],
            dropdown_hover_color=COLORS["surface_light"],
            text_color=COLORS["text"],
            command=self._on_instance_change,
        )
        instance_menu.pack(fill="x", pady=(0, SPACING["sm"]))

        # Version info label
        self.version_label = ctk.CTkLabel(
            main,
            text="",
            font=FONTS["body"],
            text_color=COLORS["success"],
        )
        self.version_label.pack(anchor="w", pady=(0, SPACING["md"]))

        # Worlds label
        ctk.CTkLabel(
            main,
            text="Worlds in this instance:",
            font=FONTS["heading"],
            text_color=COLORS["text"],
        ).pack(anchor="w", pady=(0, SPACING["sm"]))

        # Scrollable world list
        self.world_frame = ctk.CTkScrollableFrame(
            main,
            fg_color=COLORS["surface"],
            corner_radius=RADIUS["md"],
        )
        self.world_frame.pack(fill="both", expand=True)

        # Buttons frame
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(SPACING["md"], 0))

        # Select all / none
        ctk.CTkButton(
            btn_frame,
            text="Select All",
            font=FONTS["body"],
            width=100,
            height=35,
            corner_radius=RADIUS["sm"],
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["hover"],
            command=self._select_all,
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame,
            text="Select None",
            font=FONTS["body"],
            width=100,
            height=35,
            corner_radius=RADIUS["sm"],
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["hover"],
            command=self._select_none,
        ).pack(side="left", padx=(SPACING["sm"], 0))

        # Install / Cancel
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            font=FONTS["body"],
            width=100,
            height=35,
            corner_radius=RADIUS["sm"],
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["hover"],
            command=self.destroy,
        ).pack(side="right")

        ctk.CTkButton(
            btn_frame,
            text="Install",
            font=FONTS["body"],
            width=100,
            height=35,
            corner_radius=RADIUS["sm"],
            fg_color=COLORS["success"],
            hover_color=COLORS["primary"],
            command=self._install,
        ).pack(side="right", padx=(0, SPACING["sm"]))

        # Path info
        self.path_label = ctk.CTkLabel(
            main,
            text="",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"],
        )
        self.path_label.pack(anchor="w", pady=(SPACING["sm"], 0))

        # Initial load
        self._refresh_worlds()

    def _show_no_instances(self) -> None:
        """Show message when no Minecraft instances found."""
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["xl"])

        ctk.CTkLabel(
            main,
            text="Minecraft Not Found",
            font=FONTS["heading"],
            text_color=COLORS["danger"],
        ).pack(pady=SPACING["lg"])

        ctk.CTkLabel(
            main,
            text=(
                "Could not find any Minecraft installations.\n\n"
                "Checked locations:\n"
                "- %APPDATA%\\.minecraft\\saves (Vanilla)\n"
                "- CurseForge\\Minecraft\\Instances\\*\\saves\n\n"
                "Make sure Minecraft is installed and has at least one world."
            ),
            font=FONTS["body"],
            text_color=COLORS["text"],
            justify="left",
        ).pack()

        ctk.CTkButton(
            main,
            text="Close",
            font=FONTS["body"],
            width=100,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["primary"],
            command=self.destroy,
        ).pack(pady=SPACING["xl"])

    def _on_instance_change(self, value: str) -> None:
        """Handle instance selection change."""
        self._refresh_worlds()

    def _refresh_worlds(self) -> None:
        """Refresh the world list for selected instance."""
        # Clear existing
        for widget in self.world_frame.winfo_children():
            widget.destroy()
        self.world_vars.clear()

        # Get selected instance
        selected = self.instance_var.get()
        for idx, (name, path, version) in enumerate(self.instances):
            if self.instance_display_names[idx] == selected:
                self.current_saves_path = path
                self.current_version = version
                break

        if not self.current_saves_path:
            return

        # Check if this is Bedrock Edition
        is_bedrock = self.current_version == "bedrock"

        # Update labels
        if is_bedrock:
            self.version_label.configure(
                text="Detected: Minecraft Bedrock Edition",
                text_color=COLORS["success"],
            )
        elif self.current_version:
            self.version_label.configure(
                text=f"Detected: Minecraft {self.current_version}",
                text_color=COLORS["success"],
            )
        else:
            self.version_label.configure(
                text="Version: Unknown (using 1.20.x compatibility)",
                text_color=COLORS["warning"],
            )

        self.path_label.configure(text=f"Path: {self.current_saves_path}")

        # Get worlds - use appropriate function for edition
        if is_bedrock:
            worlds = list_bedrock_worlds()
        else:
            worlds = list_worlds(self.current_saves_path)

        if not worlds:
            ctk.CTkLabel(
                self.world_frame,
                text="No worlds found in this instance.",
                font=FONTS["body"],
                text_color=COLORS["text_secondary"],
            ).pack(pady=SPACING["lg"])
            return

        # Create checkboxes
        for world_name, world_path in worlds:
            var = ctk.BooleanVar(value=True)
            # Check if pack is installed - use appropriate function
            if is_bedrock:
                installed = is_behavior_pack_installed(world_path)
            else:
                installed = is_datapack_installed(world_path)

            row = ctk.CTkFrame(self.world_frame, fg_color="transparent")
            row.pack(fill="x", pady=SPACING["xs"])

            cb = ctk.CTkCheckBox(
                row,
                text=world_name,
                variable=var,
                font=FONTS["body"],
                text_color=COLORS["text"],
                fg_color=COLORS["primary"],
                hover_color=COLORS["hover"],
            )
            cb.pack(side="left", padx=SPACING["sm"])

            if installed:
                ctk.CTkLabel(
                    row,
                    text="(installed)",
                    font=FONTS["small"],
                    text_color=COLORS["success"],
                ).pack(side="left")

            self.world_vars.append((var, world_name, world_path))

    def _select_all(self) -> None:
        """Select all worlds."""
        for var, _, _ in self.world_vars:
            var.set(True)

    def _select_none(self) -> None:
        """Deselect all worlds."""
        for var, _, _ in self.world_vars:
            var.set(False)

    def _install(self) -> None:
        """Install datapack/behavior pack to selected worlds."""
        from tkinter import messagebox

        selected = [(name, path) for var, name, path in self.world_vars if var.get()]

        if not selected:
            messagebox.showinfo("No Selection", "Please select at least one world.")
            return

        is_bedrock = self.current_version == "bedrock"
        success = 0
        failed = 0

        for name, path in selected:
            if is_bedrock:
                # Bedrock Edition - install behavior pack
                if install_behavior_pack(path):
                    success += 1
                else:
                    failed += 1
            else:
                # Java Edition - install datapack
                if install_datapack(path, mc_version=self.current_version):
                    success += 1
                else:
                    failed += 1

        self.destroy()

        # Customize message for edition
        if is_bedrock:
            pack_type = "Behavior pack"
            reload_msg = "restart the world"
            version_info = " (Bedrock Edition)"
        else:
            pack_type = "Datapack"
            reload_msg = "run /reload or restart the world"
            version_info = f" (for Minecraft {self.current_version})" if self.current_version else ""

        if failed == 0:
            messagebox.showinfo(
                "Installation Complete",
                f"{pack_type} installed to {success} world(s){version_info}!\n\n"
                f"In Minecraft, {reload_msg} to activate."
            )
        else:
            messagebox.showwarning(
                "Partial Installation",
                f"Installed to {success} world(s), {failed} failed{version_info}.\n\n"
                f"In Minecraft, {reload_msg} to activate."
            )
