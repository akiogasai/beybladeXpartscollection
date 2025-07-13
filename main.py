"""Main entry point for Beyblade X Collection Manager."""

import tkinter as tk
from tkinter import messagebox
import logging
from ui.modern_main_window import ModernMainWindow


def main():
    """Main application entry point."""
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info("Application starting...")
        
        app = ModernMainWindow()
        logging.info("Starting main loop...")
        app.run()
        
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")


if __name__ == "__main__":
    main()
