"""Debug tools for testing paste and typing mechanisms."""

from __future__ import annotations

import argparse
import subprocess
import time

from .constants import KEY_V, KEY_N, KEY_SPACE, KEY_DELETE


def osascript(script: str) -> subprocess.CompletedProcess[bytes]:
    """Execute an AppleScript and return the result."""
    return subprocess.run(
        ["osascript", "-"],
        input=script.encode("utf-8"),
        capture_output=True,
        check=False,
    )


def focus_textedit_new() -> None:
    """Open TextEdit and create/clear a document."""
    script = r'''
    tell application "TextEdit"
        activate
        if not (exists document 1) then make new document
        set text of front document to ""
    end tell
    '''
    osascript(script)
    time.sleep(0.2)


def set_clipboard(text: str) -> None:
    """Set clipboard content using pbcopy."""
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=False)


def get_textedit_text() -> str:
    """Get the text content from the frontmost TextEdit document."""
    script = r'''
    try
        tell application "TextEdit"
            set t to text of front document
        end tell
        return t
    on error
        return ""
    end try
    '''
    proc = osascript(script)
    return (proc.stdout or b"").decode("utf-8", "ignore")


def paste_via_system_events() -> None:
    """Paste from clipboard using multiple Cmd+V variants."""
    variants = [
        f'tell application "System Events" to key code {KEY_V} using {{command down}}',
        'tell application "System Events" to keystroke "v" using {command down}',
        rf'''
        tell application "System Events"
            key down command
            delay 0.02
            key code {KEY_V}
            delay 0.02
            key up command
        end tell
        ''',
    ]
    for s in variants:
        osascript(s)
        time.sleep(0.04)


def type_tilde_safe() -> None:
    """Type a tilde character safely using Option+n then Space."""
    script = rf'''
    tell application "System Events"
        key down option
        key code {KEY_N}
        key up option
        key code {KEY_SPACE}
        key code {KEY_SPACE}
        key code {KEY_DELETE}
    end tell
    '''
    osascript(script)


def main() -> None:
    """Main entry point for debug tools CLI."""
    ap = argparse.ArgumentParser(description="Maricraft debug tools")
    ap.add_argument(
        "mode",
        choices=["paste-test", "type-tilde-test"],
        help="Test mode",
    )
    ap.add_argument(
        "--text",
        dest="text",
        default="/execute at @p run fill ~-1 ~ ~-1 ~1 ~1 ~1 air",
        help="Text to paste/type",
    )
    args = ap.parse_args()

    focus_textedit_new()
    time.sleep(0.2)

    if args.mode == "paste-test":
        print("[debug] Paste test to TextEdit…")
        set_clipboard(args.text)
        time.sleep(0.1)
        paste_via_system_events()
        time.sleep(0.2)
        got = get_textedit_text()
        print("[debug] Expected:", args.text)
        print("[debug]   Actual:", got)
        print("[debug]   Match:", got == args.text)
    else:
        print("[debug] Type tilde-safe test to TextEdit…")
        # Type everything by keystroke, but for '~' insert safely
        parts = args.text.split("~")
        for i, seg in enumerate(parts):
            if seg:
                esc = seg.replace("\\", "\\\\").replace('"', '\\"')
                osascript(f'tell application "System Events" to keystroke "{esc}"')
            if i < len(parts) - 1:
                type_tilde_safe()
            time.sleep(0.02)
        time.sleep(0.2)
        got = get_textedit_text()
        print("[debug] Expected:", args.text)
        print("[debug]   Actual:", got)
        print("[debug]   Match:", got == args.text)


if __name__ == "__main__":
    main()
