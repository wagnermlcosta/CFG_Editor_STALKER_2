"""
Text editor widget for CFG files.
Provides a text editor with line numbers and syntax highlighting.
"""

import tkinter as tk
from tkinter import scrolledtext
from gui.themes import DarkTheme

class LineNumberText(tk.Text):
    """Text widget with line numbers."""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Create line number widget
        self.line_numbers = tk.Text(parent, width=4, padx=3, takefocus=0,
                                   border=0, state='disabled', wrap='none')
        
        # Configure colors for line numbers
        DarkTheme.configure_widget(self.line_numbers, "text")
        self.line_numbers.configure(fg="#888888")
        
        # Bind events
        self.bind('<KeyPress>', self.on_key_press)
        self.bind('<Button-1>', self.on_click)
        self.bind('<MouseWheel>', self.on_mousewheel)
        self.bind('<Button-4>', self.on_mousewheel)
        self.bind('<Button-5>', self.on_mousewheel)
        
        # Update line numbers initially
        self.update_line_numbers()
    
    def on_key_press(self, event):
        """Handle key press events."""
        self.after_idle(self.update_line_numbers)
    
    def on_click(self, event):
        """Handle mouse click events."""
        self.after_idle(self.update_line_numbers)
    
    def on_mousewheel(self, event):
        """Handle mouse wheel events."""
        if event.num == 4 or event.delta > 0:
            self.line_numbers.yview_scroll(-1, "units")
            self.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.line_numbers.yview_scroll(1, "units")
            self.yview_scroll(1, "units")
        self.after_idle(self.update_line_numbers)
    
    def update_line_numbers(self):
        """Update the line numbers display."""
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        
        # Get the number of lines
        line_count = int(self.index('end-1c').split('.')[0])
        
        # Generate line numbers
        line_numbers = '\n'.join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert('1.0', line_numbers)
        
        self.line_numbers.config(state='disabled')
        
        # Sync scrolling
        self.line_numbers.yview_moveto(self.yview()[0])

class CFGEditor(tk.Frame):
    """CFG file editor widget with line numbers."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure frame
        DarkTheme.configure_widget(self, "frame")
        
        # Create text editor with line numbers
        self.text_widget = LineNumberText(self, wrap='none', undo=True, maxundo=50)
        DarkTheme.configure_widget(self.text_widget, "text")
        
        # Create scrollbars
        self.v_scrollbar = tk.Scrollbar(self, orient='vertical', command=self.text_widget.yview)
        self.h_scrollbar = tk.Scrollbar(self, orient='horizontal', command=self.text_widget.xview)
        
        # Configure scrollbars
        DarkTheme.configure_widget(self.v_scrollbar)
        DarkTheme.configure_widget(self.h_scrollbar)
        
        # Configure text widget scrolling
        self.text_widget.configure(yscrollcommand=self.v_scrollbar.set,
                                  xscrollcommand=self.h_scrollbar.set)
        
        # Grid layout
        self.text_widget.line_numbers.grid(row=0, column=0, sticky='nsew')
        self.text_widget.grid(row=0, column=1, sticky='nsew')
        self.v_scrollbar.grid(row=0, column=2, sticky='ns')
        self.h_scrollbar.grid(row=1, column=0, columnspan=2, sticky='ew')
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Bind scrollbar to line numbers
        def on_text_scroll(*args):
            self.v_scrollbar.set(*args)
            self.text_widget.line_numbers.yview_moveto(args[0])
        
        self.text_widget.configure(yscrollcommand=on_text_scroll)
    
    def get_content(self):
        """Get the current content of the editor."""
        return self.text_widget.get('1.0', 'end-1c')
    
    def set_content(self, content):
        """Set the content of the editor."""
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', content)
        self.text_widget.update_line_numbers()
    
    def clear(self):
        """Clear the editor content."""
        self.text_widget.delete('1.0', 'end')
        self.text_widget.update_line_numbers()
    
    def get_line_count(self):
        """Get the number of lines in the editor."""
        return int(self.text_widget.index('end-1c').split('.')[0])
    
    def highlight_line(self, line_number):
        """Highlight a specific line."""
        # Remove existing highlights
        self.text_widget.tag_remove('highlight', '1.0', 'end')
        
        # Add highlight to the specified line
        start = f"{line_number}.0"
        end = f"{line_number}.end"
        self.text_widget.tag_add('highlight', start, end)
        self.text_widget.tag_configure('highlight', background=DarkTheme.ACCENT)
        
        # Scroll to the line
        self.text_widget.see(start)
    
    def remove_highlights(self):
        """Remove all line highlights."""
        self.text_widget.tag_remove('highlight', '1.0', 'end')

