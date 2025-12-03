"""Tkinter UI for Maricraft chat macro runner."""

from __future__ import annotations

import json
import threading
from typing import Any, Dict, Optional

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    tk = None  # type: ignore[assignment]
    ttk = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]

try:
    from .hotkeys import HotkeyWatcher
except ImportError:
    HotkeyWatcher = None  # type: ignore[assignment,misc]

from .automator import MacAutomator, quartz_available
from .constants import (
    WINDOW_DEFAULT_WIDTH,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    DELAY_TURBO_MS,
    TELEPORT_BACK_COMMAND,
    AI_MODEL_OPTIONS,
    AI_DEFAULT_MODEL,
    AIMode,
    ChatKey,
    DEFAULT_LOG_PATH,
    UI_DELAY_MIN_MS,
    UI_DELAY_MAX_MS,
    UI_DELAY_INCREMENT,
)
from .logger import Logger
from .settings import Settings


class App:
    """Main Tkinter application for Maricraft."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Maricraft: Chat Macro Runner")
        self.root.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        self.stop_event = threading.Event()
        self.automator = MacAutomator(status_cb=self._set_status, stop_event=self.stop_event)
        self.hotkeys = None

        self._build_widgets()

        self.chat_key_var.set("t")
        self.delay_var.set(str(DELAY_TURBO_MS))
        self.escape_var.set(True)

    def _build_widgets(self) -> None:
        """Build all UI widgets."""
        pad = 8
        outer = ttk.Frame(self.root)
        outer.pack(fill=tk.BOTH, expand=True, padx=pad, pady=pad)

        nb = ttk.Notebook(outer)
        nb.pack(fill=tk.BOTH, expand=True)

        self.tab_commands = ttk.Frame(nb)
        nb.add(self.tab_commands, text="Commands")
        self._build_commands_tab(self.tab_commands, pad)

        self.tab_ai = ttk.Frame(nb)
        nb.add(self.tab_ai, text="AI")
        self._build_ai_tab(self.tab_ai, pad)

        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(outer, textvariable=self.status_var, anchor=tk.W)
        status.pack(fill=tk.X, pady=(pad, 0))

    def _build_commands_tab(self, frm: ttk.Frame, pad: int) -> None:
        opt = ttk.LabelFrame(frm, text="Options")
        opt.pack(fill=tk.X, padx=0, pady=(0, pad))

        row1 = ttk.Frame(opt)
        row1.pack(fill=tk.X, padx=0, pady=(pad // 2, 2))

        self.chat_key_var = tk.StringVar()
        ttk.Label(row1, text="Chat key:").pack(side=tk.LEFT, padx=(pad, 4))
        ttk.Radiobutton(row1, text="t", value="t", variable=self.chat_key_var).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(row1, text="/", value="/", variable=self.chat_key_var).pack(side=tk.LEFT)

        self.delay_var = tk.StringVar()
        ttk.Label(row1, text="Delay (ms):").pack(side=tk.LEFT, padx=(16, 4))
        self.delay_entry = ttk.Spinbox(
            row1,
            from_=UI_DELAY_MIN_MS,
            to=UI_DELAY_MAX_MS,
            increment=UI_DELAY_INCREMENT,
            textvariable=self.delay_var,
            width=6,
        )
        self.delay_entry.pack(side=tk.LEFT)

        self.escape_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(row1, text="Press Esc to resume first", variable=self.escape_var).pack(side=tk.LEFT, padx=(16, 4))

        row2 = ttk.Frame(opt)
        row2.pack(fill=tk.X, padx=0, pady=(2, pad // 2))

        self.quartz_var = tk.BooleanVar(value=False)
        quartz_text = "Quartz inject (fast)" + ("" if quartz_available() else " (unavailable)")
        ttk.Checkbutton(row2, text=quartz_text, variable=self.quartz_var).pack(side=tk.LEFT, padx=(pad, 8))

        txt_frame = ttk.LabelFrame(frm, text="Commands (one per line; blank/# lines ignored)")
        txt_frame.pack(fill=tk.BOTH, expand=True, pady=(0, pad))

        self.text = tk.Text(txt_frame, wrap=tk.NONE, undo=True)
        self.text.pack(fill=tk.BOTH, expand=True)

        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X)
        self.run_btn = ttk.Button(btns, text="Run", command=self.on_run)
        self.run_btn.pack(side=tk.LEFT)
        self.stop_btn = ttk.Button(btns, text="Stop", command=self.on_stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(8, 0))
        self.back_btn = ttk.Button(btns, text="Back 75", command=self.on_back_75)
        self.back_btn.pack(side=tk.LEFT, padx=(8, 0))

    def _build_ai_tab(self, frm: ttk.Frame, pad: int) -> None:
        try:
            from .ai_chat import AIChatController
        except ImportError:
            AIChatController = None

        top = ttk.Frame(frm)
        top.pack(fill=tk.X, pady=(0, pad))

        self.ai_mode = tk.StringVar(value=AIMode.CREATE.value)
        ttk.Label(top, text="Mode:").pack(side=tk.LEFT, padx=(pad, 4))
        ttk.Radiobutton(top, text="Create", variable=self.ai_mode, value=AIMode.CREATE.value).pack(side=tk.LEFT)
        ttk.Radiobutton(top, text="Debug", variable=self.ai_mode, value=AIMode.DEBUG.value).pack(side=tk.LEFT, padx=(4, 0))

        ttk.Label(top, text="Model:").pack(side=tk.LEFT, padx=(16, 4))
        self.ai_model = tk.StringVar(value=AI_DEFAULT_MODEL)
        self.ai_model_box = ttk.Combobox(top, textvariable=self.ai_model, width=40)
        self.ai_model_box["values"] = AI_MODEL_OPTIONS
        self.ai_model_box.pack(side=tk.LEFT)

        self.ai_require_params = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Require parameters", variable=self.ai_require_params).pack(side=tk.LEFT, padx=(12, 4))

        self.ai_attach_log = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Attach log.txt tail (debug)", variable=self.ai_attach_log).pack(side=tk.LEFT, padx=(12, 4))

        pw = ttk.PanedWindow(frm, orient=tk.HORIZONTAL)
        pw.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(pw)
        right = ttk.Frame(pw)
        pw.add(left, weight=3)
        pw.add(right, weight=2)

        lframe = ttk.LabelFrame(left, text="Chat")
        lframe.pack(fill=tk.BOTH, expand=True)
        self.ai_transcript = tk.Text(lframe, wrap=tk.WORD, state=tk.DISABLED)
        self.ai_transcript.pack(fill=tk.BOTH, expand=True)

        entry_row = ttk.Frame(left)
        entry_row.pack(fill=tk.X, pady=(pad, 0))
        self.ai_input = tk.Entry(entry_row)
        self.ai_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ai_send_btn = ttk.Button(entry_row, text="Send", command=self.on_ai_send)
        self.ai_send_btn.pack(side=tk.LEFT, padx=(8, 0))

        rframe = ttk.LabelFrame(right, text="Structured result")
        rframe.pack(fill=tk.BOTH, expand=True)
        self.ai_result = tk.Text(rframe, wrap=tk.NONE, height=12, state=tk.DISABLED)
        self.ai_result.pack(fill=tk.BOTH, expand=True)

        actions = ttk.Frame(right)
        actions.pack(fill=tk.X, pady=(pad, 0))
        self.ai_apply_btn = ttk.Button(actions, text="Apply to Commands", command=self.on_ai_apply, state=tk.DISABLED)
        self.ai_apply_btn.pack(side=tk.LEFT)
        self.ai_apply_run_btn = ttk.Button(actions, text="Apply & Run", command=self.on_ai_apply_run, state=tk.DISABLED)
        self.ai_apply_run_btn.pack(side=tk.LEFT, padx=(8, 0))
        self.ai_reset_btn = ttk.Button(actions, text="Reset Conversation", command=self.on_ai_reset)
        self.ai_reset_btn.pack(side=tk.LEFT, padx=(8, 0))

        self.ai_controller = AIChatController() if AIChatController else None
        self.ai_last_parsed = None
        self.ai_last_mode = None

    def _set_status(self, msg: str) -> None:
        """Thread-safe status update."""
        def _upd() -> None:
            self.status_var.set(msg)
        self.root.after(0, _upd)

    def on_run(self) -> None:
        """Handle Run button click."""
        delay = self._parse_delay()
        if delay is None:
            return

        settings = Settings.for_run(
            chat_key=self.chat_key_var.get(),
            delay_ms=delay,
            press_escape_first=self.escape_var.get(),
            use_quartz_injection=self.quartz_var.get() and quartz_available(),
        )

        lines = self.text.get("1.0", tk.END).splitlines()
        if not any(ln.strip() for ln in lines):
            messagebox.showinfo("Nothing to run", "Paste some commands first.")
            return

        self._start_command_run(lines, settings, teleport_back=True)

    def _parse_delay(self) -> Optional[int]:
        """Parse delay from UI, showing error on failure."""
        try:
            return int(self.delay_var.get())
        except ValueError:
            messagebox.showerror("Invalid delay", "Delay must be an integer (ms).")
            return None

    def _start_command_run(
        self,
        lines: list[str],
        settings: Settings,
        teleport_back: bool = False,
    ) -> None:
        """Start a command run in a background thread.

        Args:
            lines: Commands to execute
            settings: Run settings
            teleport_back: Whether to teleport back after completion
        """
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.stop_event.clear()

        logger = Logger(DEFAULT_LOG_PATH)
        self.automator.logger = logger

        if HotkeyWatcher:
            self.hotkeys = HotkeyWatcher(self.stop_event, logger=logger)
            self.hotkeys.start()

        def worker() -> None:
            try:
                self.automator.run_commands(lines, settings)
                if teleport_back:
                    self.automator.send_quick_command(TELEPORT_BACK_COMMAND, settings)
            finally:
                self.root.after(0, self._enable_run_btn)
                logger.close()
                if self.hotkeys:
                    self.hotkeys.stop()

        threading.Thread(target=worker, daemon=True).start()

    def _enable_run_btn(self) -> None:
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def on_stop(self) -> None:
        """Handle Stop button click."""
        self.stop_event.set()
        self._set_status("Stopping…")

    def on_back_75(self) -> None:
        """Handle Back 75 button click - quick teleport backwards."""
        delay = self._parse_delay() or DELAY_TURBO_MS

        settings = Settings.for_quick_command(
            chat_key=self.chat_key_var.get(),
            delay_ms=delay,
            press_escape_first=self.escape_var.get(),
        )

        self._start_command_run([TELEPORT_BACK_COMMAND], settings, teleport_back=False)

    def _ai_append_transcript(self, who: str, text: str) -> None:
        """Append a message to the AI chat transcript."""
        self.ai_transcript.configure(state=tk.NORMAL)
        self.ai_transcript.insert(tk.END, f"{who}: {text}\n")
        self.ai_transcript.see(tk.END)
        self.ai_transcript.configure(state=tk.DISABLED)

    def _ai_set_result(self, obj: Optional[Dict[str, Any]], raw: Optional[str], error: Optional[str]) -> None:
        """Set the AI result display."""
        self.ai_result.configure(state=tk.NORMAL)
        self.ai_result.delete("1.0", tk.END)
        if error:
            self.ai_result.insert(tk.END, f"Error: {error}\n\nRaw:\n{raw or ''}")
        else:
            self.ai_result.insert(tk.END, json.dumps(obj or {}, indent=2, ensure_ascii=False))
        self.ai_result.configure(state=tk.DISABLED)

    def _get_ai_config(self) -> Any:
        """Get the current AI configuration from UI state.

        Returns:
            AIConfig instance with current UI settings
        """
        from .ai_chat import AIConfig

        return AIConfig(
            model=self.ai_model.get().strip(),
            require_parameters=self.ai_require_params.get(),
            attach_log=self.ai_attach_log.get(),
        )

    def on_ai_send(self) -> None:
        """Handle AI Send button click."""
        if not self.ai_controller:
            messagebox.showerror(
                "Missing dependency",
                "AI features require 'openai-agents[litellm]' and 'python-dotenv'. Install via uv and try again."
            )
            return

        msg = self.ai_input.get().strip()
        if not msg:
            return
        self.ai_input.delete(0, tk.END)
        self._ai_append_transcript("You", msg)
        self.ai_send_btn.config(state=tk.DISABLED)
        self.ai_apply_btn.config(state=tk.DISABLED)
        self.ai_apply_run_btn.config(state=tk.DISABLED)

        mode_str = self.ai_mode.get()
        mode = AIMode.from_str(mode_str)
        self.ai_last_mode = mode
        cfg = self._get_ai_config()

        def worker() -> None:
            try:
                out = self.ai_controller.send(mode=mode_str, cfg=cfg, user_message=msg)
            except Exception as e:
                out = {"parsed": None, "raw": "", "error": str(e)}
            parsed, raw, err = out.get("parsed"), out.get("raw"), out.get("error")
            self.ai_last_parsed = parsed

            def done() -> None:
                self._ai_set_result(parsed, raw, err)
                if not err and parsed:
                    self.ai_apply_btn.config(state=tk.NORMAL)
                    self.ai_apply_run_btn.config(state=tk.NORMAL)
                self.ai_send_btn.config(state=tk.NORMAL)

            self.root.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    def on_ai_apply(self) -> None:
        """Apply AI-generated commands to the command editor."""
        if not self.ai_last_parsed:
            return

        # Get commands based on mode
        if self.ai_last_mode == AIMode.CREATE:
            commands = self.ai_last_parsed.get("commands", [])
        else:
            commands = self.ai_last_parsed.get("corrected_commands", [])
        text = "\n".join(commands) + ("\n" if commands else "")

        # Replace content in commands editor
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)

        # Apply overrides if present
        chat_key = self.ai_last_parsed.get("chat_key") if self.ai_last_parsed else None
        if chat_key in {ChatKey.T.value, ChatKey.SLASH.value}:
            self.chat_key_var.set(chat_key)
        if self.ai_last_parsed and isinstance(self.ai_last_parsed.get("delay_ms"), int):
            self.delay_var.set(str(self.ai_last_parsed.get("delay_ms")))

    def on_ai_apply_run(self) -> None:
        """Apply AI commands and immediately run them."""
        self.on_ai_apply()
        self.on_run()

    def on_ai_reset(self) -> None:
        """Reset the AI conversation and clear state."""
        # Clear UI
        self.ai_transcript.configure(state=tk.NORMAL)
        self.ai_transcript.delete("1.0", tk.END)
        self.ai_transcript.configure(state=tk.DISABLED)
        self.ai_result.configure(state=tk.NORMAL)
        self.ai_result.delete("1.0", tk.END)
        self.ai_result.configure(state=tk.DISABLED)

        # Clear state to prevent stale data
        self.ai_last_parsed = None
        self.ai_last_mode = None

        # Disable apply buttons since there's nothing to apply
        self.ai_apply_btn.config(state=tk.DISABLED)
        self.ai_apply_run_btn.config(state=tk.DISABLED)


def main() -> None:
    """Application entry point."""
    if tk is None:
        raise SystemExit("tkinter is required to run the UI.")
    root = tk.Tk()
    App(root)
    root.mainloop()
