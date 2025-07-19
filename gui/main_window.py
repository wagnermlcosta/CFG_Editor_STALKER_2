"""
Main window for the Stalker 2 CFG Editor.
Integrates all components and handles the main application logic.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

from gui.themes import DarkTheme
from gui.editor_widget import CFGEditor
from gui.operations_panel import OperationsPanel
from core.cfg_parser import CFGParser
from core.file_handler import FileHandler
from core.validator import Validator

class MainWindow:
    """Main application window."""
    
    STATUS_TIMEOUT_MS = 5000  # 5 seconds
    
    def __init__(self, root):
        self.root = root
        self.cfg_parser = CFGParser()
        self.file_handler = FileHandler()
        self.current_file_path = None
        self.is_modified = False
        
        self.setup_window()
        self.create_menu()
        self.create_widgets()
        self.setup_layout()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("Stalker 2 CFG Editor")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure dark theme
        DarkTheme.configure_widget(self.root, "root")
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Create the application menu."""
        menubar = tk.Menu(self.root)
        DarkTheme.configure_widget(menubar, "menu")
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        DarkTheme.configure_widget(file_menu, "menu")
        file_menu.add_command(label="Open CFG File...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        DarkTheme.configure_widget(edit_menu, "menu")
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        DarkTheme.configure_widget(help_menu, "menu")
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_file_as())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
    
    def create_widgets(self):
        """Create the main widgets."""
        # Main container
        self.main_frame = tk.Frame(self.root)
        DarkTheme.configure_widget(self.main_frame, "frame")
        
        # File path display
        self.file_frame = tk.Frame(self.main_frame)
        DarkTheme.configure_widget(self.file_frame, "frame")
        
        file_label = tk.Label(self.file_frame, text="File:")
        DarkTheme.configure_widget(file_label, "label")
        file_label.pack(side='left', padx=(5, 5))
        
        self.file_path_var = tk.StringVar(value="No file loaded")
        self.file_path_label = tk.Label(self.file_frame, textvariable=self.file_path_var, 
                                       font=("Consolas", 9), anchor='w')
        DarkTheme.configure_widget(self.file_path_label, "label")
        self.file_path_label.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        load_button = tk.Button(self.file_frame, text="Load CFG File", command=self.open_file)
        DarkTheme.configure_widget(load_button, "button")
        load_button.pack(side='right', padx=5)
        
        # Content area
        self.content_frame = tk.Frame(self.main_frame)
        DarkTheme.configure_widget(self.content_frame, "frame")
        
        # Text editor
        self.editor = CFGEditor(self.content_frame)
        
        # Operations panel
        self.operations_panel = OperationsPanel(self.content_frame, 
                                               on_apply_callback=self.apply_operation,
                                               on_preview_callback=self.preview_operation)
        
        # Status bar
        self.status_frame = tk.Frame(self.main_frame, height=25)
        DarkTheme.configure_widget(self.status_frame, "frame")
        self.status_frame.configure(bg=DarkTheme.STATUS_BG)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                    anchor='w', font=("Arial", 9))
        self.status_label.configure(bg=DarkTheme.STATUS_BG, fg=DarkTheme.STATUS_FG)
        self.status_label.pack(side='left', fill='x', expand=True, padx=5)
        
        # Line/column info
        self.position_var = tk.StringVar(value="Line: 1, Column: 1")
        self.position_label = tk.Label(self.status_frame, textvariable=self.position_var, 
                                      font=("Arial", 9))
        self.position_label.configure(bg=DarkTheme.STATUS_BG, fg=DarkTheme.STATUS_FG)
        self.position_label.pack(side='right', padx=5)
        
        # Bind text change events
        self.editor.text_widget.bind('<KeyRelease>', self.on_text_change)
        self.editor.text_widget.bind('<Button-1>', self.update_position)
    
    def setup_layout(self):
        """Setup the widget layout."""
        self.main_frame.pack(fill='both', expand=True)
        
        # File frame at top
        self.file_frame.pack(fill='x', padx=5, pady=5)
        
        # Content frame in middle
        self.content_frame.pack(fill='both', expand=True, padx=5, pady=(0, 5))
        
        # Editor on the left
        self.editor.pack(side='left', fill='both', expand=True)
        
        # Operations panel on the right
        self.operations_panel.pack(side='right', fill='y', padx=(5, 0))
        
        # Status bar at bottom
        self.status_frame.pack(fill='x', side='bottom')
    
    def open_file(self):
        """Open a CFG file."""
        if self.is_modified:
            result = messagebox.askyesnocancel("Unsaved Changes", 
                                             "You have unsaved changes. Do you want to save before opening a new file?")
            if result is True:
                if not self.save_file():
                    return
            elif result is None:
                return
        
        file_path = filedialog.askopenfilename(
            title="Open CFG File",
            filetypes=[("CFG files", "*.cfg"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load a CFG file into the editor."""
        # Validate file
        valid, error = Validator.validate_file_path(file_path)
        if not valid:
            messagebox.showerror("Error", f"Cannot load file: {error}")
            return False
        
        # Load file content
        success, content = self.file_handler.read_file_content(file_path)
        if not success:
            messagebox.showerror("Error", f"Failed to read file: {content}")
            return False
        
        # Load into parser
        if not self.cfg_parser.load_file(file_path):
            messagebox.showerror("Error", "Failed to parse CFG file")
            return False
        
        # Update editor
        self.editor.set_content(content)
        
        # Update UI
        self.current_file_path = file_path
        self.file_path_var.set(file_path)
        self.is_modified = False
        self.update_title()
        self.update_status("File loaded successfully")
        
        return True
    
    def save_file(self):
        """Save the current file."""
        if not self.current_file_path:
            return self.save_file_as()
        
        return self.save_to_file(self.current_file_path)
    
    def save_file_as(self):
        """Save the file with a new name."""
        file_path = filedialog.asksaveasfilename(
            title="Save CFG File",
            defaultextension=".cfg",
            filetypes=[("CFG files", "*.cfg"), ("All files", "*.*")]
        )
        
        if file_path:
            return self.save_to_file(file_path)
        
        return False
    
    def save_to_file(self, file_path):
        """Save content to a specific file."""
        content = self.editor.get_content()
        
        # Update parser content
        self.cfg_parser.set_content(content)
        
        # Save file
        success, result = self.file_handler.write_file_content(file_path, content)
        if not success:
            messagebox.showerror("Error", f"Failed to save file: {result}")
            return False
        
        # Update UI
        self.current_file_path = file_path
        self.file_path_var.set(file_path)
        self.is_modified = False
        self.update_title()
        
        if result:  # Backup was created
            self.update_status(f"File saved successfully. Backup created: {os.path.basename(result)}")
        else:
            self.update_status("File saved successfully")
        
        return True
    
    def preview_operation(self, operation_data):
        """Preview the changes from an operation."""
        if not self.current_file_path:
            self.operations_panel.update_status("No file loaded", "error")
            return
        
        # Update parser with current content
        self.cfg_parser.set_content(self.editor.get_content())
        
        # Get operation parameters
        variable_name = operation_data['variable_name']
        operation = operation_data['operation']
        
        if operation == 'replace':
            value = operation_data['value']
        else:
            value = float(operation_data['value'])
        
        # Get line range
        start_line = 1
        end_line = None
        if operation_data['use_range']:
            if operation_data['start_line']:
                start_line = int(operation_data['start_line'])
            if operation_data['end_line']:
                end_line = int(operation_data['end_line'])
        
        # Preview changes
        changes = self.cfg_parser.preview_changes(variable_name, operation, value, start_line, end_line)
        
        if not changes:
            self.operations_panel.update_status(f"No occurrences of variable '{variable_name}' found in the specified range", "warning")
            return
        
        # Display preview
        preview_text = f"Preview: {len(changes)} change(s) will be made:\n\n"
        for change in changes[:10]:  # Limit to first 10 changes
            preview_text += f"Line {change['line_number']}: {change['old_value']} → {change['new_value']}\n"
        
        if len(changes) > 10:
            preview_text += f"... and {len(changes) - 10} more changes\n"
        
        self.operations_panel.update_status(preview_text, "info")
    
    def apply_operation(self, operation_data):
        """Apply the mathematical operation."""
        if not self.current_file_path:
            self.operations_panel.update_status("No file loaded", "error")
            return
        
        # Update parser with current content
        self.cfg_parser.set_content(self.editor.get_content())
        
        # Get operation parameters
        variable_name = operation_data['variable_name']
        operation = operation_data['operation']
        
        if operation == 'replace':
            value = operation_data['value']
        else:
            value = float(operation_data['value'])
        
        # Get line range
        start_line = 1
        end_line = None
        if operation_data['use_range']:
            if operation_data['start_line']:
                start_line = int(operation_data['start_line'])
            if operation_data['end_line']:
                end_line = int(operation_data['end_line'])
        
        # Apply operation
        if operation == 'replace':
            changes = self.cfg_parser.update_variable(variable_name, str(value), start_line, end_line)
            errors = []
        else:
            changes, errors = self.cfg_parser.apply_mathematical_operation(variable_name, operation, value, start_line, end_line)
        
        # Update editor with new content
        self.editor.set_content(self.cfg_parser.get_content())
        
        # Update status
        if changes > 0:
            self.operations_panel.update_status(f"Successfully applied operation to {changes} occurrence(s) of '{variable_name}'", "success")
            self.is_modified = True
            self.update_title()
        else:
            self.operations_panel.update_status(f"No occurrences of variable '{variable_name}' found in the specified range", "warning")
        
        # Display errors if any
        for error in errors:
            self.operations_panel.update_status(error, "error")
    
    def undo(self):
        """Undo the last change."""
        try:
            self.editor.text_widget.edit_undo()
            self.on_text_change()
        except tk.TclError:
            pass  # Nothing to undo
    
    def redo(self):
        """Redo the last undone change."""
        try:
            self.editor.text_widget.edit_redo()
            self.on_text_change()
        except tk.TclError:
            pass  # Nothing to redo
    
    def on_text_change(self, event=None):
        """Handle text changes."""
        self.is_modified = True
        self.update_title()
        self.update_position()
    
    def update_position(self, event=None):
        """Update cursor position display."""
        try:
            cursor_pos = self.editor.text_widget.index(tk.INSERT)
            line, column = cursor_pos.split('.')
            self.position_var.set(f"Line: {line}, Column: {int(column) + 1}")
        except tk.TclError:
            pass
    
    def update_title(self):
        """Update the window title."""
        title = "Stalker 2 CFG Editor"
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path)
            title += f" - {filename}"
            if self.is_modified:
                title += " *"
        self.root.title(title)
    
    def update_status(self, message):
        """Update the status bar."""
        self.status_var.set(message)
        self.root.after(self.STATUS_TIMEOUT_MS, lambda: self.status_var.set("Ready"))  # Clear after 5 seconds
    
    def show_about(self):
        """Show the about dialog."""
        about_text = """Stalker 2 CFG Editor
        
A GUI application for editing Stalker 2 configuration files with mathematical operations.
        
Features:
• Load and edit .cfg files
• Apply mathematical operations to variables
• Process specific line ranges
• Preserve file formatting and indentation
• Dark theme interface
        
Developed for Stalker 2 modding community."""
        
        messagebox.showinfo("About", about_text)
    
    def on_closing(self):
        """Handle window closing."""
        if self.is_modified:
            result = messagebox.askyesnocancel("Unsaved Changes", 
                                             "You have unsaved changes. Do you want to save before exiting?")
            if result is True:
                if not self.save_file():
                    return
            elif result is None:
                return
        
        self.root.destroy()

