#!/usr/bin/env python3
"""
Stalker 2 CFG Editor
A GUI application for editing Stalker 2 configuration files with mathematical operations.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

from gui.themes import DarkTheme

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main():
    """Main entry point of the application."""
    try:
        # Create the main window
        root = tk.Tk()
        DarkTheme.configure_widget(root, "root")
        app = MainWindow(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

