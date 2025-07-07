import tkinter as tk
from tkinter import ttk
from app.constants import (
    DARK_THEME_BG, OPERATIONS, STYLE_BACKGROUND, STYLE_BUTTON_ACTIVE_BACKGROUND, 
    STYLE_BUTTON_BACKGROUND, STYLE_FIELD_BACKGROUND, STYLE_FOREGROUND, STYLE_THEME, 
    WINDOW_GEOMETRY, WINDOW_TITLE
)

class MainWindow:
    def __init__(self, root, lang_manager):
        self.root = root
        self.lang_manager = lang_manager
        self.setup_window()
        self.create_styles()
        self.create_variables()
        self.create_widgets()
        self.update_texts()

    def setup_window(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.configure(bg=DARK_THEME_BG)

    def create_styles(self):
        style = ttk.Style(self.root)
        style.theme_use(STYLE_THEME)
        style.configure('.', background=STYLE_BACKGROUND, foreground=STYLE_FOREGROUND, fieldbackground=STYLE_FIELD_BACKGROUND)
        style.configure('TButton', background=STYLE_BUTTON_BACKGROUND, foreground=STYLE_FOREGROUND)
        style.map('TButton', background=[('active', STYLE_BUTTON_ACTIVE_BACKGROUND)])
        style.configure('TEntry', fieldbackground=STYLE_FIELD_BACKGROUND, foreground=STYLE_FOREGROUND)
        style.configure('TLabel', background=STYLE_BACKGROUND, foreground=STYLE_FOREGROUND)
        style.configure('TCheckbutton', background=STYLE_BACKGROUND, foreground=STYLE_FOREGROUND)
        style.configure('TCombobox', fieldbackground=STYLE_FIELD_BACKGROUND, foreground=STYLE_FOREGROUND)

    def create_variables(self):
        self.file_path = tk.StringVar()
        self.key = tk.StringVar()
        self.operation = tk.StringVar(value="+")
        self.replace_only = tk.BooleanVar(value=False)
        self.value = tk.StringVar()
        self.line_start = tk.StringVar()
        self.line_end = tk.StringVar()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=(10, 5))
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        padding_opts = {'padx': 10, 'pady': 5}

        # File selection
        self.file_label = ttk.Label(main_frame)
        self.file_label.grid(row=0, column=0, sticky='w', **padding_opts)
        self.file_entry = ttk.Entry(main_frame, textvariable=self.file_path, width=40)
        self.file_entry.grid(row=0, column=1, **padding_opts)
        self.select_button = ttk.Button(main_frame)
        self.select_button.grid(row=0, column=2, **padding_opts)

        # Key input
        self.key_label = ttk.Label(main_frame)
        self.key_label.grid(row=1, column=0, sticky='w', **padding_opts)
        self.key_entry = ttk.Entry(main_frame, textvariable=self.key)
        self.key_entry.grid(row=1, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Operation selection
        self.operation_label = ttk.Label(main_frame)
        self.operation_label.grid(row=2, column=0, sticky='w', **padding_opts)
        self.op_combo = ttk.Combobox(main_frame, textvariable=self.operation, values=OPERATIONS, state="readonly", width=3)
        self.op_combo.grid(row=2, column=1, sticky='w', **padding_opts)

        # Replace only checkbox
        self.replace_check = ttk.Checkbutton(main_frame, variable=self.replace_only, style='TCheckbutton')
        self.replace_check.grid(row=2, column=2, sticky='w', padx=10, pady=5)

        # Value input
        self.value_label = ttk.Label(main_frame)
        self.value_label.grid(row=3, column=0, sticky='w', **padding_opts)
        self.value_entry = ttk.Entry(main_frame, textvariable=self.value)
        self.value_entry.grid(row=3, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Line start input
        self.line_start_label = ttk.Label(main_frame)
        self.line_start_label.grid(row=4, column=0, sticky='w', **padding_opts)
        self.line_start_entry = ttk.Entry(main_frame, textvariable=self.line_start)
        self.line_start_entry.grid(row=4, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Line end input
        self.line_end_label = ttk.Label(main_frame)
        self.line_end_label.grid(row=5, column=0, sticky='w', **padding_opts)
        self.line_end_entry = ttk.Entry(main_frame, textvariable=self.line_end)
        self.line_end_entry.grid(row=5, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Execute button
        self.modify_button = ttk.Button(main_frame)
        self.modify_button.grid(row=6, column=0, columnspan=3, pady=20)

        # Status bar
        self.status_bar = ttk.Label(self.root, text="", anchor='w', relief='sunken')
        self.status_bar.grid(row=1, column=0, sticky='ew')

        main_frame.grid_columnconfigure(1, weight=1)

    def update_texts(self):
        self.root.title(self.lang_manager.get_translation("title"))
        self.file_label.config(text=self.lang_manager.get_translation("file_label"))
        self.select_button.config(text=self.lang_manager.get_translation("select_button"))
        self.key_label.config(text=self.lang_manager.get_translation("key_label"))
        self.operation_label.config(text=self.lang_manager.get_translation("operation_label"))
        self.replace_check.config(text=self.lang_manager.get_translation("replace_only"))
        self.value_label.config(text=self.lang_manager.get_translation("value_label"))
        self.line_start_label.config(text=self.lang_manager.get_translation("line_start_label"))
        self.line_end_label.config(text=self.lang_manager.get_translation("line_end_label"))
        self.modify_button.config(text=self.lang_manager.get_translation("modify_button"))

    def show_status_message(self, message, duration=3000):
        self.status_bar.config(text=message)
        self.root.after(duration, lambda: self.status_bar.config(text=""))
