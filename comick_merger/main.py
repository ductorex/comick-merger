"""Main entry point for the GUI application."""

import sys
from comick_merger.gui import main as gui_main


def main():
    """Launch the GUI application."""
    return gui_main()


if __name__ == "__main__":
    sys.exit(main())
