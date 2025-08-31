# Repository Guidelines

## Project Structure & Module Organization
- `maricraft/`: Python package for the app.
  - `ui.py`: Tkinter UI and macOS automation (`osascript`, `pbcopy/pbpaste`).
  - `__main__.py`: Entry point (`python -m maricraft`).
  - `__init__.py`: Package init.
- `documentation/`: Reference material (not required to run the app).
- `log.txt`: Overwritten on each run with execution details.

## Build, Test, and Development Commands
- Run UI (recommended): `uv run python -m maricraft`
- Run without uv: `python -m maricraft` (Python 3.10+ with `tkinter` on macOS).
- Dev tips:
  - Logs: tail during a run with `tail -f log.txt`.
  - If macOS doesn’t prompt for Accessibility, enable Terminal/`osascript` in System Settings → Privacy & Security → Accessibility.

## Coding Style & Naming Conventions
- Python only; stdlib-only by design (avoid new dependencies).
- Indentation: 4 spaces; keep lines ≤ 100 chars.
- Types: prefer annotations (e.g., `threading.Event | None`), dataclasses for config (`Settings`).
- Naming: modules and functions `snake_case`, classes `CapWords`, constants `UPPER_CASE`.
- Logs: concise, present tense; do not leak personal data.

## Testing Guidelines
- Current state: no automated tests. Prefer incremental coverage of non-UI logic.
- Unit tests: mock `_osascript`, `pbcopy/pbpaste`, and sleeps. Suggested layout: `tests/test_automator.py`.
- Example: verify `run_commands` filters blank/`#` lines and restores clipboard.
- Run (if added): `pytest -q` and aim to cover MacAutomator behaviors; UI can be smoke-tested manually.

## Commit & Pull Request Guidelines
- Commits: imperative mood; keep subjects focused. Conventional Commits are welcome (`feat:`, `fix:`, `refactor:`).
- PRs: include summary, rationale, and testing notes. For bug fixes, add macOS version, Minecraft version, and repro steps. Screenshots/log snippets help.
- Scope: avoid bundling unrelated changes; keep PRs small and reviewable.

## Security & Configuration Tips (macOS)
- Accessibility: app requires Accessibility permissions to send keystrokes.
- Safety: only use where chat macros are allowed. `log.txt` is ephemeral and should not contain secrets.
- Platform: functionality targets Minecraft Java on macOS; focusing tries `Minecraft`, `java`, `javaw`.
