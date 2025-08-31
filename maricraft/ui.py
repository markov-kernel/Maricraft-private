import subprocess
import threading
import time
import shlex
import json
from dataclasses import dataclass

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except Exception:  # pragma: no cover
    tk = None
    ttk = None
    messagebox = None


@dataclass
class Settings:
    chat_key: str = "t"  # 't' or '/'
    delay_ms: int = 150
    press_escape_first: bool = True
    type_instead_of_paste: bool = True
    paste_repeats: int = 2
    force_ascii_layout: bool = False
    typing_segment_delay_ms: int = 8
    turbo_mode: bool = False


class MacAutomator:
    def __init__(self, status_cb=None, stop_event: threading.Event | None = None, logger=None):
        self.status_cb = status_cb or (lambda _msg: None)
        self.stop_event = stop_event or threading.Event()
        self.logger = logger

    def _osascript(self, script: str) -> subprocess.CompletedProcess:
        proc = subprocess.run(
            ["osascript", "-"],
            input=script.encode("utf-8"),
            capture_output=True,
            check=False,
        )
        if getattr(proc, "returncode", 0) != 0:
            self._log(
                f"osascript error rc={proc.returncode} stdout={proc.stdout.decode('utf-8', 'ignore').strip()} stderr={proc.stderr.decode('utf-8', 'ignore').strip()}"
            )
        return proc

    def _status(self, msg: str):
        self._log(msg)
        self.status_cb(msg)

    def _log(self, msg: str):
        try:
            if self.logger is not None:
                self.logger.log(msg)
        except Exception:
            pass

    def _sleep(self, ms: int):
        time.sleep(max(ms, 0) / 1000.0)

    # ===== Input source helpers (for reliable typing on non-US layouts) =====
    def _get_input_source_name(self) -> str:
        script = r'''
        try
            tell application "System Events"
                set n to name of current input source
            end tell
            return n
        on error
            return ""
        end try
        '''
        proc = self._osascript(script)
        try:
            return (proc.stdout or b"").decode("utf-8", "ignore").strip()
        except Exception:
            return ""

    def _set_input_source_by_name(self, name: str) -> bool:
        # Tries to switch the active keyboard layout by its display name.
        script = rf'''
        try
            tell application "System Events"
                set target to first input source whose name is "{name}"
                set current input source to target
                return name of current input source
            end tell
        on error
            return ""
        end try
        '''
        proc = self._osascript(script)
        out = (proc.stdout or b"").decode("utf-8", "ignore").strip()
        return out == name

    def _maybe_force_ascii_input(self) -> tuple[bool, str]:
        # Attempt to switch to an ASCII-friendly layout so characters like '~' and '-' are literal.
        # Try common names: "ABC" and "U.S.". Returns (changed, previous_name)
        prev = self._get_input_source_name()
        for candidate in ("ABC", "U.S.", "ABC - QWERTZ", "ABC QWERTZ"):
            if self._set_input_source_by_name(candidate):
                self._log(f"Switched input source to '{candidate}' from '{prev}'")
                return True, prev
        return False, prev

    def _restore_input_source(self, prev: str):
        if not prev:
            return
        ok = self._set_input_source_by_name(prev)
        self._log(f"Restored input source to '{prev}' => {'ok' if ok else 'failed'}")

    def _frontmost_process_name(self) -> str:
        script = r'''
        tell application "System Events"
            set pname to name of first process whose frontmost is true
        end tell
        return pname
        '''
        proc = self._osascript(script)
        try:
            out = proc.stdout.decode("utf-8", "ignore").strip()
            return out
        except Exception:
            return ""

    def focus_minecraft(self, attempts: int = 8, settle_ms: int = 250) -> bool:
        # Simple, robust focusing: activate Minecraft; then try explicit process names without list iteration
        simp_script = r'''
        try
            tell application "Minecraft" to activate
        end try
        delay 0.05
        try
            tell application "System Events" to set frontmost of process "Minecraft" to true
        end try
        try
            tell application "System Events" to set frontmost of process "java" to true
        end try
        try
            tell application "System Events" to set frontmost of process "javaw" to true
        end try
        '''

        for i in range(max(1, attempts)):
            self._osascript(simp_script)
            self._log(f"Focus attempt {i+1}/{attempts}: issued activate/raise")
            time.sleep(max(settle_ms, 0) / 1000.0)
            front = (self._frontmost_process_name() or "").lower()
            self._log(f"Frontmost after attempt {i+1}: '{front}'")
            if ("minecraft" in front and "launcher" not in front) or any(k == front for k in ("java", "javaw")):
                return True
        return False

    def key_escape(self):
        script = 'tell application "System Events" to key code 53'
        self._osascript(script)

    def keystroke(self, text: str):
        # Send literal characters robustly, handling embedded double quotes.
        # AppleScript does not support escaping quotes inside string literals; use `keystroke quote`.
        if '"' in text:
            parts = text.split('"')
            lines = ['tell application "System Events"']
            for i, seg in enumerate(parts):
                if seg:
                    seg_esc = seg.replace("\\", "\\\\").replace("\n", " ")
                    lines.append(f'    keystroke "{seg_esc}"')
                if i < len(parts) - 1:
                    lines.append('    keystroke quote')
            lines.append('end tell')
            script = "\n".join(lines)
            self._osascript(script)
        else:
            seg_esc = text.replace("\\", "\\\\").replace("\n", " ")
            script = f'tell application "System Events" to keystroke "{seg_esc}"'
            self._osascript(script)

    def _type_tilde(self):
        # On many non-US layouts, '~' is a dead key: Option+n then Space.
        # Some layouts require an extra Space to fully separate; we send Space twice
        # and then Delete once to avoid leaving an extra space.
        script = r'''
        tell application "System Events"
            key down option
            key code 45 -- 'n'
            key up option
            key code 49 -- space (commit tilde)
            key code 49 -- extra space to separate dead key
            key code 51 -- delete the extra space
        end tell
        '''
        self._osascript(script)
        # Small settle to ensure the next character doesn't combine
        self._sleep(20)

    def type_line_safely(self, text: str, per_segment_delay_ms: int = 10):
        # Type text but handle '~' explicitly with Option+n then Space to produce ASCII tilde
        parts = text.split("~")
        for i, seg in enumerate(parts):
            if seg:
                self.keystroke(seg)
            if i < len(parts) - 1:
                self._type_tilde()
            if per_segment_delay_ms:
                self._sleep(per_segment_delay_ms)

    def keycode(self, code: int):
        script = f'tell application "System Events" to key code {code}'
        self._osascript(script)

    def paste_from_clipboard(self):
        # Try multiple variants of Cmd+V with small gaps to maximize compatibility across layouts
        variants = [
            'tell application "System Events" to key code 9 using {command down}',
            'tell application "System Events" to keystroke "v" using {command down}',
            r'''
            tell application "System Events"
                key down command
                delay 0.02
                key code 9 -- 'v'
                delay 0.02
                key up command
            end tell
            ''',
        ]
        for idx, script in enumerate(variants, start=1):
            self._osascript(script)
            self._sleep(35)

    def poke_input(self):
        # Type a space then delete; helps some clients accept subsequent paste reliably
        script = r'''
        tell application "System Events"
            keystroke " "
            key code 51 -- delete
        end tell
        '''
        self._osascript(script)

    def select_all(self):
        script = 'tell application "System Events" to keystroke "a" using {command down}'
        self._osascript(script)

    def copy_selection(self):
        script = 'tell application "System Events" to keystroke "c" using {command down}'
        self._osascript(script)

    def set_clipboard(self, text: str):
        # Use pbcopy to avoid AppleScript string escaping limits
        try:
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=False)
        except Exception:
            pass

    def get_clipboard(self) -> str:
        try:
            out = subprocess.run(["pbpaste"], capture_output=True, check=False)
            return out.stdout.decode("utf-8", errors="ignore")
        except Exception:
            return ""

    def open_chat(self, chat_key: str):
        if chat_key == "/":
            self.keystroke("/")
        else:
            self.keystroke("t")

    def press_enter(self):
        # Return key
        self.keycode(36)

    def run_commands(self, commands: list[str], settings: Settings):
        # Save original clipboard
        original_clipboard = self.get_clipboard()
        # Save original input source; possibly switch for typing mode
        switched_layout = False
        prev_layout = ""
        try:
            self._status("Bringing Minecraft to front…")
            focused = self.focus_minecraft()
            if not focused:
                self._status("Could not focus Minecraft. Ensure Accessibility is enabled and the game window is visible, then try again.")
                return
            self._sleep(max(300, settings.delay_ms))

            # If typing, ensure ASCII-friendly layout to avoid dead keys (e.g., '~') or Unicode minus
            if settings.type_instead_of_paste and settings.force_ascii_layout:
                switched_layout, prev_layout = self._maybe_force_ascii_input()
                self._sleep(120)

            if settings.press_escape_first:
                self._status("Resuming game (Esc)…")
                self.key_escape()
                self._sleep(120)

            cleaned = [ln for ln in commands if ln.strip() and not ln.strip().startswith("#")]
            for idx, line in enumerate(cleaned, start=1):
                if self.stop_event.is_set():
                    self._status("Stopped by user.")
                    return

                # If chat was opened with '/', avoid inserting a duplicate leading slash
                line_to_send = line
                if settings.chat_key == "/" and line_to_send.startswith("/"):
                    line_to_send = line_to_send[1:]

                # Default to safe typing; paste path remains available if user disables typing
                use_typing = settings.type_instead_of_paste

                self._status(f"{idx}/{len(cleaned)}: Open chat…")
                self.open_chat(settings.chat_key)
                # Allow chat field to appear and focus; skip nudge for typing path
                if use_typing:
                    if settings.turbo_mode:
                        self._sleep(40)
                    else:
                        self._sleep(max(80, settings.delay_ms // 2))
                else:
                    self._sleep(max(220, settings.delay_ms))
                    self.poke_input()
                    self._sleep(max(90, settings.delay_ms // 3))
                mode_desc = "typed" if use_typing else "pasted"
                self._status(f"{idx}/{len(cleaned)}: Input line ({mode_desc})…")
                self._log(f"Command line: {line}")
                line_start = time.monotonic()
                if use_typing:
                    # Directly type characters to avoid paste issues
                    # Use safe tilde typing on non-US layouts
                    self.type_line_safely(line_to_send, per_segment_delay_ms=max(0, int(settings.typing_segment_delay_ms)))
                    if settings.turbo_mode:
                        self._sleep(30)
                    else:
                        self._sleep(max(60, settings.delay_ms // 2))
                else:
                    self.set_clipboard(line_to_send)
                    self._sleep(max(160, settings.delay_ms // 2))
                    # Paste once or more depending on reliability preference
                    reps = max(1, int(settings.paste_repeats))
                    for i in range(reps):
                        self.paste_from_clipboard()
                        # Small gap between repeated pastes
                        if i < reps - 1:
                            self._sleep(max(120, settings.delay_ms // 3))
                    self._sleep(max(120, settings.delay_ms // 2))

                    # Verify pasted content to avoid empty-send on longer lines
                    expected_field = ("/" + line_to_send) if settings.chat_key == "/" else line_to_send
                    verified = False
                    # Use a clipboard sentinel to detect copy failures
                    sentinel = f"__MARICRAFT_SENTINEL__{int(time.time()*1000)}__"
                    for attempt in range(3):
                        # Set sentinel and then try to copy field contents
                        self.set_clipboard(sentinel)
                        self._sleep(80)
                        self.select_all()
                        self._sleep(70)
                        self.copy_selection()
                        self._sleep(110)
                        got = self.get_clipboard()
                        if not got or got == sentinel:
                            self._log(f"Verify attempt {attempt+1}: copy failed (clipboard unchanged)")
                        else:
                            got_s = got.strip().replace("\r", "")
                            exp_s = expected_field.strip().replace("\r", "")
                            self._log(f"Verify attempt {attempt+1}: got_len={len(got_s)} match={got_s==exp_s}")
                            if got_s == exp_s:
                                verified = True
                                break
                        # Re-paste and try again with longer waits
                        self.set_clipboard(line_to_send)
                        self._sleep(120)
                        self.paste_from_clipboard()
                        self._sleep(200 + attempt * 100)
                    if not verified:
                        self._log("Paste verify failed; falling back to safe typing for this line")
                        # Clear any accidental partial content
                        self.poke_input()
                        self._sleep(60)
                        # Type with explicit handling for '~'
                        self.type_line_safely(line_to_send, per_segment_delay_ms=12)
                        self._sleep(max(140, settings.delay_ms // 2))

                dur_ms = int((time.monotonic() - line_start) * 1000)
                turbo_txt = " turbo" if settings.turbo_mode and use_typing else ""
                self._status(f"{idx}/{len(cleaned)}: Send… (typed_ms={dur_ms}{turbo_txt})")
                self.press_enter()

                # Safety delay between lines
                if settings.turbo_mode and use_typing:
                    self._sleep(40)
                else:
                    self._sleep(max(60, settings.delay_ms))

            self._status("Done.")
        finally:
            # Restore clipboard
            self.set_clipboard(original_clipboard)
            # Restore input source if changed
            if switched_layout:
                self._sleep(120)
                self._restore_input_source(prev_layout)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Maricraft: Chat Macro Runner")
        self.root.geometry("900x680")
        self.root.minsize(800, 520)

        self.stop_event = threading.Event()
        self.automator = MacAutomator(status_cb=self._set_status, stop_event=self.stop_event)

        # UI Elements
        self._build_widgets()

        # Defaults
        self.chat_key_var.set("t")
        self.delay_var.set("150")
        self.escape_var.set(True)

    def _build_widgets(self):
        pad = 8
        outer = ttk.Frame(self.root)
        outer.pack(fill=tk.BOTH, expand=True, padx=pad, pady=pad)

        nb = ttk.Notebook(outer)
        nb.pack(fill=tk.BOTH, expand=True)

        # Commands tab
        self.tab_commands = ttk.Frame(nb)
        nb.add(self.tab_commands, text="Commands")
        self._build_commands_tab(self.tab_commands, pad)

        # AI tab
        self.tab_ai = ttk.Frame(nb)
        nb.add(self.tab_ai, text="AI")
        self._build_ai_tab(self.tab_ai, pad)

        # Status
        self.status_var = tk.StringVar(value="Ready. The app will request Accessibility permissions on first use.")
        status = ttk.Label(outer, textvariable=self.status_var, anchor=tk.W)
        status.pack(fill=tk.X, pady=(pad, 0))

    def _build_commands_tab(self, frm: ttk.Frame, pad: int):
        # Options
        opt = ttk.LabelFrame(frm, text="Options")
        opt.pack(fill=tk.X, padx=0, pady=(0, pad))

        row1 = ttk.Frame(opt)
        row1.pack(fill=tk.X, padx=0, pady=(pad//2, 2))

        self.chat_key_var = tk.StringVar()
        ttk.Label(row1, text="Chat key:").pack(side=tk.LEFT, padx=(pad, 4))
        ttk.Radiobutton(row1, text="t", value="t", variable=self.chat_key_var).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(row1, text="/", value="/", variable=self.chat_key_var).pack(side=tk.LEFT)

        self.delay_var = tk.StringVar()
        ttk.Label(row1, text="Delay (ms):").pack(side=tk.LEFT, padx=(16, 4))
        self.delay_entry = ttk.Spinbox(row1, from_=30, to=1000, increment=5, textvariable=self.delay_var, width=6)
        self.delay_entry.pack(side=tk.LEFT)

        self.escape_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(row1, text="Press Esc to resume first", variable=self.escape_var).pack(side=tk.LEFT, padx=(16, 4))

        self.type_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(row1, text="Type text instead of paste", variable=self.type_var).pack(side=tk.LEFT, padx=(16, 4))

        self.fast_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row1, text="Fast mode (single paste)", variable=self.fast_var).pack(side=tk.LEFT, padx=(16, 4))

        # Second row: typing/ASCII/turbo controls
        row2 = ttk.Frame(opt)
        row2.pack(fill=tk.X, padx=0, pady=(2, pad//2))

        self.ascii_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row2, text="Force ASCII layout while typing", variable=self.ascii_var).pack(side=tk.LEFT, padx=(pad, 8))

        speed_frame = ttk.Frame(row2)
        speed_frame.pack(side=tk.LEFT, padx=(8, 0))
        ttk.Label(speed_frame, text="Typing seg (ms):").pack(side=tk.LEFT)
        self.type_seg_var = tk.StringVar(value="8")
        self.type_seg_entry = ttk.Spinbox(speed_frame, from_=0, to=50, increment=1, textvariable=self.type_seg_var, width=4)
        self.type_seg_entry.pack(side=tk.LEFT, padx=(4, 0))

        self.turbo_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row2, text="Turbo typing", variable=self.turbo_var, command=self.on_toggle_turbo).pack(side=tk.LEFT, padx=(16, 4))

        # Text area
        txt_frame = ttk.LabelFrame(frm, text="Commands (one per line; blank/# lines ignored)")
        txt_frame.pack(fill=tk.BOTH, expand=True, pady=(0, pad))

        self.text = tk.Text(txt_frame, wrap=tk.NONE, undo=True)
        self.text.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X)
        self.run_btn = ttk.Button(btns, text="Run", command=self.on_run)
        self.run_btn.pack(side=tk.LEFT)
        self.stop_btn = ttk.Button(btns, text="Stop", command=self.on_stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(8, 0))

    def _build_ai_tab(self, frm: ttk.Frame, pad: int):
        try:
            from .ai_chat import AIChatController
        except Exception:
            AIChatController = None

        # Top controls
        top = ttk.Frame(frm)
        top.pack(fill=tk.X, pady=(0, pad))

        self.ai_mode = tk.StringVar(value="create")
        ttk.Label(top, text="Mode:").pack(side=tk.LEFT, padx=(pad, 4))
        ttk.Radiobutton(top, text="Create", variable=self.ai_mode, value="create").pack(side=tk.LEFT)
        ttk.Radiobutton(top, text="Debug", variable=self.ai_mode, value="debug").pack(side=tk.LEFT, padx=(4, 0))

        ttk.Label(top, text="Model:").pack(side=tk.LEFT, padx=(16, 4))
        self.ai_model = tk.StringVar(value="openrouter/openai/gpt-5-mini")
        self.ai_model_box = ttk.Combobox(top, textvariable=self.ai_model, width=40)
        self.ai_model_box["values"] = (
            "openrouter/openai/gpt-5-mini",
            "openrouter/openai/gpt-4o-mini",
            "openrouter/meta-llama/llama-3.1-70b-instruct",
            "openrouter/mistralai/mistral-large",
        )
        self.ai_model_box.pack(side=tk.LEFT)

        self.ai_require_params = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Require parameters", variable=self.ai_require_params).pack(side=tk.LEFT, padx=(12, 4))

        self.ai_attach_log = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Attach log.txt tail (debug)", variable=self.ai_attach_log).pack(side=tk.LEFT, padx=(12, 4))

        # Middle: split chat/result
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

        # Controller
        self.ai_controller = None
        if AIChatController is not None:
            self.ai_controller = AIChatController(logger=getattr(self, "logger", None))
        self.ai_last_parsed = None
        self.ai_last_mode = None

    def _set_status(self, msg: str):
        # Thread-safe update
        def _upd():
            self.status_var.set(msg)
        self.root.after(0, _upd)

    def on_run(self):
        try:
            delay = int(self.delay_var.get())
        except ValueError:
            messagebox.showerror("Invalid delay", "Delay must be an integer (ms).")
            return

        settings = Settings(
            chat_key=self.chat_key_var.get(),
            delay_ms=delay,
            press_escape_first=self.escape_var.get(),
            type_instead_of_paste=self.type_var.get(),
            paste_repeats=(1 if getattr(self, 'fast_var', None) and self.fast_var.get() else 2),
            force_ascii_layout=(getattr(self, 'ascii_var', None) and self.ascii_var.get()),
            typing_segment_delay_ms=max(0, int(self.type_seg_var.get() or 0)),
            turbo_mode=self.turbo_var.get(),
        )

        # Enforce turbo overrides at run time for consistency
        if settings.turbo_mode:
            settings.delay_ms = min(settings.delay_ms, 40)
            settings.typing_segment_delay_ms = 0


        raw = self.text.get("1.0", tk.END)
        lines = raw.splitlines()
        if not any(ln.strip() for ln in lines):
            messagebox.showinfo("Nothing to run", "Paste some commands first.")
            return

        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.stop_event.clear()

        # Prepare logger (overwrite log.txt on each run)
        logger = Logger("log.txt")
        self.automator.logger = logger

        def worker():
            try:
                self.automator.run_commands(lines, settings)
            finally:
                self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))
                try:
                    logger.close()
                except Exception:
                    pass

        threading.Thread(target=worker, daemon=True).start()

    def on_stop(self):
        self.stop_event.set()
        self._set_status("Stopping…")

    def on_toggle_turbo(self):
        # Adjust UI to recommended turbo values when toggled on/off
        if self.turbo_var.get():
            try:
                self.delay_var.set("40")
            except Exception:
                pass
            try:
                self.type_seg_var.set("0")
            except Exception:
                pass
        else:
            # Restore a safer baseline if user used defaults
            if self.delay_var.get() == "40":
                self.delay_var.set("100")
            if self.type_seg_var.get() == "0":
                self.type_seg_var.set("8")

    # ===== AI Tab handlers =====
    def _ai_append_transcript(self, who: str, text: str):
        self.ai_transcript.configure(state=tk.NORMAL)
        self.ai_transcript.insert(tk.END, f"{who}: {text}\n")
        self.ai_transcript.see(tk.END)
        self.ai_transcript.configure(state=tk.DISABLED)

    def _ai_set_result(self, obj: dict | None, raw: str | None, error: str | None):
        self.ai_result.configure(state=tk.NORMAL)
        self.ai_result.delete("1.0", tk.END)
        if error:
            self.ai_result.insert(tk.END, f"Error: {error}\n\nRaw:\n{raw or ''}")
        else:
            self.ai_result.insert(tk.END, json.dumps(obj or {}, indent=2, ensure_ascii=False))
        self.ai_result.configure(state=tk.DISABLED)

    def _get_ai_config(self):
        from .ai_chat import AIConfig

        return AIConfig(
            model=self.ai_model.get().strip(),
            require_parameters=self.ai_require_params.get(),
            attach_log=self.ai_attach_log.get(),
        )

    def on_ai_send(self):
        if not self.ai_controller:
            messagebox.showerror("Missing dependency", "AI features require 'openai-agents[litellm]' and 'python-dotenv'. Install via uv and try again.")
            return

        msg = self.ai_input.get().strip()
        if not msg:
            return
        self.ai_input.delete(0, tk.END)
        self._ai_append_transcript("You", msg)
        self.ai_send_btn.config(state=tk.DISABLED)
        self.ai_apply_btn.config(state=tk.DISABLED)
        self.ai_apply_run_btn.config(state=tk.DISABLED)

        mode = self.ai_mode.get()
        self.ai_last_mode = mode
        cfg = self._get_ai_config()

        def worker():
            try:
                out = self.ai_controller.send(mode=mode, cfg=cfg, user_message=msg)
            except Exception as e:
                out = {"parsed": None, "raw": "", "error": str(e)}
            parsed, raw, err = out.get("parsed"), out.get("raw"), out.get("error")
            self.ai_last_parsed = parsed

            def done():
                self._ai_set_result(parsed, raw, err)
                if not err and parsed:
                    self.ai_apply_btn.config(state=tk.NORMAL)
                    self.ai_apply_run_btn.config(state=tk.NORMAL)
                self.ai_send_btn.config(state=tk.NORMAL)

            self.root.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    def on_ai_apply(self):
        if not self.ai_last_parsed:
            return
        if self.ai_last_mode == "create":
            commands = self.ai_last_parsed.get("commands", [])
            text = "\n".join(commands) + ("\n" if commands else "")
        else:
            commands = self.ai_last_parsed.get("corrected_commands", [])
            text = "\n".join(commands) + ("\n" if commands else "")

        # Replace content in commands editor
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)

        # Apply overrides if present
        chat_key = self.ai_last_parsed.get("chat_key") if self.ai_last_parsed else None
        if chat_key in {"t", "/"}:
            self.chat_key_var.set(chat_key)
        if self.ai_last_parsed and isinstance(self.ai_last_parsed.get("delay_ms"), int):
            self.delay_var.set(str(self.ai_last_parsed.get("delay_ms")))

    def on_ai_apply_run(self):
        self.on_ai_apply()
        self.on_run()

    def on_ai_reset(self):
        self.ai_transcript.configure(state=tk.NORMAL)
        self.ai_transcript.delete("1.0", tk.END)
        self.ai_transcript.configure(state=tk.DISABLED)
        self.ai_result.configure(state=tk.NORMAL)
        self.ai_result.delete("1.0", tk.END)
        self.ai_result.configure(state=tk.DISABLED)


def main():
    if tk is None:
        raise SystemExit("tkinter is required to run the UI.")
    root = tk.Tk()
    App(root)
    root.mainloop()


class Logger:
    def __init__(self, path: str = "log.txt"):
        self.path = path
        # Overwrite on each run
        self._fp = open(self.path, "w", encoding="utf-8")
        self.log("=== Maricraft run started ===")

    def log(self, msg: str):
        try:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            self._fp.write(f"[{ts}] {msg}\n")
            self._fp.flush()
        except Exception:
            pass

    def close(self):
        try:
            self.log("=== Maricraft run finished ===")
            self._fp.close()
        except Exception:
            pass
