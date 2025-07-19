"""
Theme configuration for the Stalker 2 CFG Editor.
Provides dark theme colors and styling.
"""

import tkinter as tk

class DarkTheme:
    """Dark theme color scheme and styling configuration."""
    
    # Main colors
    BACKGROUND = "#2b2b2b"
    FOREGROUND = "#ffffff"
    
    # UI element colors
    BUTTON_BG = "#404040"
    BUTTON_FG = "#ffffff"
    BUTTON_ACTIVE_BG = "#505050"
    
    ENTRY_BG = "#3c3c3c"
    ENTRY_FG = "#ffffff"
    ENTRY_SELECT_BG = "#4a9eff"
    
    TEXT_BG = "#2b2b2b"
    TEXT_FG = "#ffffff"
    TEXT_SELECT_BG = "#4a9eff"
    TEXT_INSERT_BG = "#ffffff"
    
    # Frame and border colors
    FRAME_BG = "#2b2b2b"
    BORDER_COLOR = "#555555"
    
    # Menu colors
    MENU_BG = "#3c3c3c"
    MENU_FG = "#ffffff"
    MENU_ACTIVE_BG = "#4a9eff"
    
    # Status bar colors
    STATUS_BG = "#404040"
    STATUS_FG = "#ffffff"
    
    # Accent colors
    ACCENT = "#4a9eff"
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    ERROR = "#f44336"
    
    @classmethod
    def configure_widget(cls, widget, widget_type="default"):
        """
        Configure a widget with dark theme colors.
        
        Args:
            widget: The tkinter widget to configure
            widget_type: Type of widget for specific styling
        """
        if widget_type == "root":
            widget.configure(bg=cls.BACKGROUND)
        elif widget_type == "button":
            widget.configure(
                bg=cls.BUTTON_BG,
                fg=cls.BUTTON_FG,
                activebackground=cls.BUTTON_ACTIVE_BG,
                activeforeground=cls.BUTTON_FG,
                relief="flat",
                borderwidth=1,
                highlightthickness=0
            )
        elif widget_type == "entry":
            widget.configure(
                bg=cls.ENTRY_BG,
                fg=cls.ENTRY_FG,
                selectbackground=cls.ENTRY_SELECT_BG,
                insertbackground=cls.TEXT_INSERT_BG,
                relief="flat",
                borderwidth=1,
                highlightthickness=0
            )
        elif widget_type == "text":
            widget.configure(
                bg=cls.TEXT_BG,
                fg=cls.TEXT_FG,
                selectbackground=cls.TEXT_SELECT_BG,
                insertbackground=cls.TEXT_INSERT_BG,
                relief="flat",
                borderwidth=1,
                highlightthickness=0
            )
        elif widget_type == "frame":
            widget.configure(
                bg=cls.FRAME_BG,
                relief="flat",
                borderwidth=0
            )
        elif widget_type == "labelframe":
            widget.configure(
                bg=cls.FRAME_BG,
                fg=cls.FOREGROUND,
                relief="solid",
                borderwidth=1
            )
        elif widget_type == "label":
            widget.configure(
                bg=cls.BACKGROUND,
                fg=cls.FOREGROUND
            )
        elif widget_type == "menu":
            widget.configure(
                bg=cls.MENU_BG,
                fg=cls.MENU_FG,
                activebackground=cls.MENU_ACTIVE_BG,
                activeforeground=cls.MENU_FG
            )
        elif widget_type == "scrollbar":
            widget.configure(
                bg=cls.BACKGROUND,
                troughcolor=cls.BUTTON_BG,
                activebackground=cls.BUTTON_ACTIVE_BG,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            # Default configuration
            # Attempt to configure background and foreground, if supported
            try:
                widget.configure(bg=cls.BACKGROUND)
            except tk.TclError:
                pass
            try:
                widget.configure(fg=cls.FOREGROUND)
            except tk.TclError:
                pass

