"""Entry point for Maricraft."""

import sys
import traceback


def run():
    """Run the application with error handling."""
    try:
        from .ui import main
        main()
    except Exception as e:
        # Show error in a message box if possible
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Maricraft Error",
                f"An error occurred:\n\n{type(e).__name__}: {e}\n\nRun DEBUG_MARICRAFT.bat for details."
            )
            root.destroy()
        except:
            pass

        # Also print to console
        print("\n" + "=" * 50)
        print("MARICRAFT ERROR")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50 + "\n")

        # Keep window open
        input("Press Enter to close...")
        sys.exit(1)


# Run when executed as module (python -m maricraft)
run()
