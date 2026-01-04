"""Entry point for Maricraft."""

import sys
import os
import traceback


def run():
    """Run the application with error handling."""
    try:
        # Support both module execution and direct/PyInstaller execution
        try:
            from .ui import main
        except ImportError:
            # Add parent directory to path for direct execution
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from maricraft.ui import main
        main()
    except Exception as e:
        # Show error in a message box if possible
        error_msg = f"{type(e).__name__}: {e}"
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Maricraft Error",
                f"An error occurred:\n\n{error_msg}\n\nRun DEBUG_MARICRAFT.bat for details."
            )
            root.destroy()
        except Exception:
            pass  # GUI error dialog failed, will print to console instead

        # Also print to console
        print("\n" + "=" * 50)
        print("MARICRAFT ERROR")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50 + "\n")

        # Keep window open (but don't crash if no stdin)
        try:
            input("Press Enter to close...")
        except (EOFError, RuntimeError):
            pass
        sys.exit(1)


if __name__ == "__main__":
    run()
