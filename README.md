Maricraft — Minecraft Chat Macro Runner (macOS)

Quick UI to paste a list of chat commands and send them to Minecraft with one click. It brings the game to front, presses Escape to resume (optional), opens chat, pastes each line, presses Enter, and repeats.

Run with uv

- Prereqs: macOS, Minecraft Java running and focused at least once, Python available (system Python is fine), and `uv` installed.

Commands:

- Start the UI: `uv run python -m maricraft`

Defaults and speed

- Default mode is tuned for speed: typing (not paste), turbo timings, ASCII layout safe handling enabled. Delay defaults to 40 ms. You can further tweak Delay if needed.
- Optional: toggle "Quartz inject (fast)". On some setups this is ignored by the game; when enabled the app verifies injection and falls back to typing if it didn’t land.

AI Assistant (Create & Debug)

- Create new commands or debug failing ones from the AI tab.
- Add `.env` with `OPENROUTER_API_KEY=...` (OpenRouter key). Optional: `OR_SITE_URL`, `OR_APP_NAME` for attribution.
- Choose a model (e.g., `openrouter/openai/gpt-4o-mini`) and chat. The default model in the UI may need to be changed to a valid option. The app requests structured JSON via OpenRouter `response_format` and requires supported providers.
- Debug mode can attach the tail of `log.txt` for context. Use “Apply to Commands” or “Apply & Run”.

First-run permissions

- macOS will prompt for Accessibility control (to allow keystrokes). If it doesn’t, go to System Settings → Privacy & Security → Accessibility and enable Terminal (or the app you use to run `uv`) and `osascript` if shown.

Usage tips

- Chat key: default is `t`. Switch to `/` if you prefer opening chat with a leading slash.
- Delays: increase if commands are missed (e.g., to 250–300 ms).
- Lines starting with `#` and blank lines are ignored.
- Clipboard is preserved and restored when done.
- Logs: writes to `log.txt` in the working directory and overwrites on each Run.
- Back 75: Click this button to quickly teleport 75 blocks backward (useful after building ahead).

Emergency stop

- Press Space+Escape (either order, within 500ms) to immediately stop a running macro. This works globally even when Minecraft is focused.
- Requires Accessibility permissions for the Quartz event tap.

Notes

- Target process names tried: `Minecraft`, `java`, `javaw`. If the game window isn’t focused reliably, click the game once before running.
- Only use in contexts where macros are allowed.
- For fastest typing, enable "Quartz inject (fast)" in Options. This uses macOS Quartz to insert text directly (requires Accessibility permissions). If unavailable, the checkbox will indicate it.
