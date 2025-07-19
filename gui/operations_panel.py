"""
Operations panel for the CFG editor.
Provides controls for mathematical operations and variable manipulation.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from gui.themes import DarkTheme

from core.validator import Validator

class OperationsPanel(tk.Frame):
    """Panel containing operation controls."""
    
    def __init__(self, parent, on_apply_callback=None, on_preview_callback=None):
        super().__init__(parent)
        
        self.on_apply_callback = on_apply_callback
        self.on_preview_callback = on_preview_callback
        
        # Configure frame
        DarkTheme.configure_widget(self, "frame")
        self.configure(width=300, relief='raised', borderwidth=1)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the panel widgets."""
        # Title
        title_label = tk.Label(self, text="Operations Panel", font=("Arial", 12, "bold"))
        DarkTheme.configure_widget(title_label, "label")
        title_label.pack(pady=(10, 20))
        
        # Variable name section
        var_frame = tk.Frame(self)
        DarkTheme.configure_widget(var_frame, "frame")
        var_frame.pack(fill='x', padx=10, pady=5)
        
        var_label = tk.Label(var_frame, text="Variable Name:")
        DarkTheme.configure_widget(var_label, "label")
        var_label.pack(anchor='w')
        
        self.var_name_entry = tk.Entry(var_frame, font=("Consolas", 10))
        DarkTheme.configure_widget(self.var_name_entry, "entry")
        self.var_name_entry.pack(fill='x', pady=(2, 0))
        
        # Operation type section
        op_frame = tk.Frame(self)
        DarkTheme.configure_widget(op_frame, "frame")
        op_frame.pack(fill='x', padx=10, pady=5)
        
        op_label = tk.Label(op_frame, text="Operation Type:")
        DarkTheme.configure_widget(op_label, "label")
        op_label.pack(anchor='w')
        
        self.operation_var = tk.StringVar(value="replace")
        operations = [
            ("Replace Value", "replace"),
            ("Add (+)", "add"),
            ("Subtract (-)", "subtract"),
            ("Multiply (×)", "multiply"),
            ("Divide (÷)", "divide")
        ]
        
        for text, value in operations:
            rb = tk.Radiobutton(op_frame, text=text, variable=self.operation_var, value=value)
            DarkTheme.configure_widget(rb, "label")
            rb.configure(selectcolor=DarkTheme.ACCENT, activebackground=DarkTheme.BACKGROUND)
            rb.pack(anchor='w', pady=1)
        
        # Value section
        value_frame = tk.Frame(self)
        DarkTheme.configure_widget(value_frame, "frame")
        value_frame.pack(fill='x', padx=10, pady=5)
        
        value_label = tk.Label(value_frame, text="Value:")
        DarkTheme.configure_widget(value_label, "label")
        value_label.pack(anchor='w')
        
        self.value_entry = tk.Entry(value_frame, font=("Consolas", 10))
        DarkTheme.configure_widget(self.value_entry, "entry")
        self.value_entry.pack(fill='x', pady=(2, 0))
        
        # Line range section
        range_frame = tk.LabelFrame(self, text="Line Range (Optional)", font=("Arial", 9))
        DarkTheme.configure_widget(range_frame, "labelframe")
        range_frame.pack(fill='x', padx=10, pady=10)
        
        self.use_range_var = tk.BooleanVar()
        range_check = tk.Checkbutton(range_frame, text="Apply to specific range", 
                                   variable=self.use_range_var, command=self.toggle_range)
        DarkTheme.configure_widget(range_check, "label")
        range_check.configure(selectcolor=DarkTheme.ACCENT, activebackground=DarkTheme.BACKGROUND)
        range_check.pack(anchor='w', padx=5, pady=5)
        
        # Start line
        start_frame = tk.Frame(range_frame)
        DarkTheme.configure_widget(start_frame, "frame")
        start_frame.pack(fill='x', padx=5, pady=2)
        
        start_label = tk.Label(start_frame, text="Start Line:")
        DarkTheme.configure_widget(start_label, "label")
        start_label.pack(side='left')
        
        self.start_line_entry = tk.Entry(start_frame, width=10, font=("Consolas", 10), state='disabled')
        DarkTheme.configure_widget(self.start_line_entry, "entry")
        self.start_line_entry.pack(side='right')
        
        # End line
        end_frame = tk.Frame(range_frame)
        DarkTheme.configure_widget(end_frame, "frame")
        end_frame.pack(fill='x', padx=5, pady=2)
        
        end_label = tk.Label(end_frame, text="End Line:")
        DarkTheme.configure_widget(end_label, "label")
        end_label.pack(side='left')
        
        self.end_line_entry = tk.Entry(end_frame, width=10, font=("Consolas", 10), state='disabled')
        DarkTheme.configure_widget(self.end_line_entry, "entry")
        self.end_line_entry.pack(side='right')
        
        # Buttons section
        button_frame = tk.Frame(self)
        DarkTheme.configure_widget(button_frame, "frame")
        button_frame.pack(fill='x', padx=10, pady=20)
        
        self.preview_button = tk.Button(button_frame, text="Preview Changes", 
                                       command=self.preview_changes)
        DarkTheme.configure_widget(self.preview_button, "button")
        self.preview_button.pack(fill='x', pady=2)
        
        self.apply_button = tk.Button(button_frame, text="Apply Changes", 
                                     command=self.apply_changes)
        DarkTheme.configure_widget(self.apply_button, "button")
        self.apply_button.pack(fill='x', pady=2)
        
        # Status section
        status_frame = tk.Frame(self)
        DarkTheme.configure_widget(status_frame, "frame")
        status_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        status_label = tk.Label(status_frame, text="Status:")
        DarkTheme.configure_widget(status_label, "label")
        status_label.pack(anchor='w')
        
        self.status_text = tk.Text(status_frame, height=8, wrap='word', state='disabled')
        DarkTheme.configure_widget(self.status_text, "text")
        self.status_text.pack(fill='both', expand=True)
        
        # Scrollbar for status text
        status_scroll = tk.Scrollbar(status_frame, command=self.status_text.yview)
        DarkTheme.configure_widget(status_scroll)
        self.status_text.configure(yscrollcommand=status_scroll.set)
        status_scroll.pack(side='right', fill='y')
    
    def toggle_range(self):
        """Toggle the line range entry fields."""
        if self.use_range_var.get():
            self.start_line_entry.configure(state='normal')
            self.end_line_entry.configure(state='normal')
        else:
            self.start_line_entry.configure(state='disabled')
            self.end_line_entry.configure(state='disabled')
            self.start_line_entry.delete(0, 'end')
            self.end_line_entry.delete(0, 'end')
    
    def get_operation_data(self):
        """Get the current operation data from the panel."""
        return {
            'variable_name': self.var_name_entry.get().strip(),
            'operation': self.operation_var.get(),
            'value': self.value_entry.get().strip(),
            'use_range': self.use_range_var.get(),
            'start_line': self.start_line_entry.get().strip() if self.use_range_var.get() else '',
            'end_line': self.end_line_entry.get().strip() if self.use_range_var.get() else ''
        }
    
    def validate_input(self):
        """Validate the current input."""
        data = self.get_operation_data()
        
        is_valid, error_msg = Validator.validate_variable_name(data['variable_name'])
        if not is_valid:
            return False, error_msg

        if data['operation'] != 'replace':
            is_valid, error_msg, _ = Validator.validate_numeric_value(data['value'])
            if not is_valid:
                return False, error_msg
        
        if data['use_range']:
            # We don't have total_lines here, so we'll just validate format
            if data['start_line']:
                try:
                    start = int(data['start_line'])
                    if start < 1:
                        return False, "Start line must be greater than 0"
                except ValueError:
                    return False, "Start line must be a valid integer"
            
            if data['end_line']:
                try:
                    end = int(data['end_line'])
                    if end < 1:
                        return False, "End line must be greater than 0"
                    if data['start_line'] and int(data['start_line']) > end:
                        return False, "End line must be greater than or equal to start line"
                except ValueError:
                    return False, "End line must be a valid integer"
        
        return True, ""
    
    def preview_changes(self):
        """Handle preview button click."""
        valid, error = self.validate_input()
        if not valid:
            self.update_status(f"Error: {error}", "error")
            return
        
        if self.on_preview_callback:
            self.on_preview_callback(self.get_operation_data())
    
    def apply_changes(self):
        """Handle apply button click."""
        valid, error = self.validate_input()
        if not valid:
            self.update_status(f"Error: {error}", "error")
            return
        
        if self.on_apply_callback:
            self.on_apply_callback(self.get_operation_data())
    
    def update_status(self, message, status_type="info"):
        """Update the status display."""
        self.status_text.configure(state='normal')
        
        # Color coding based on status type
        if status_type == "error":
            color = DarkTheme.ERROR
        elif status_type == "warning":
            color = DarkTheme.WARNING
        elif status_type == "success":
            color = DarkTheme.SUCCESS
        else:
            color = DarkTheme.FOREGROUND
        
        # Insert the message with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.status_text.insert('end', formatted_message)
        self.status_text.tag_add(status_type, f"end-{len(formatted_message)}c", 'end-1c')
        self.status_text.tag_configure(status_type, foreground=color)
        
        # Auto-scroll to bottom
        self.status_text.see('end')
        
        self.status_text.configure(state='disabled')
    
    def clear_status(self):
        """Clear the status display."""
        self.status_text.configure(state='normal')
        self.status_text.delete('1.0', 'end')
        self.status_text.configure(state='disabled')
