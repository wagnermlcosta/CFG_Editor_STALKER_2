import tkinter as tk
from tkinter import filedialog, messagebox
from app.core.file_operations import process_lines
from app.lang.language_manager import LanguageManager
from app.ui.main_window import MainWindow
from app.constants import FILE_TYPES

class CFGValueModifierApp:
    def __init__(self, root):
        self.root = root
        self.lang_manager = LanguageManager()
        self.ui = MainWindow(root, self.lang_manager)
        self.setup_callbacks()

    def setup_callbacks(self):
        self.ui.select_button.config(command=self.select_file)
        self.ui.modify_button.config(command=self.modify_values)

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=FILE_TYPES)
        if file:
            self.ui.file_path.set(file)

    def _validate_inputs(self):
        file_path = self.ui.file_path.get()
        key = self.ui.key.get().strip()
        value_str = self.ui.value.get().strip()
        line_start_str = self.ui.line_start.get().strip()
        line_end_str = self.ui.line_end.get().strip()
        replace_only = self.ui.replace_only.get()
        operation = self.ui.operation.get()

        if not file_path:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_no_file"))
            return None
        if not key:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_no_key"))
            return None
        if not value_str:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_no_value"))
            return None

        try:
            value_num = float(value_str) if not replace_only else value_str
        except ValueError:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_invalid_value"))
            return None

        if operation == "/" and not replace_only and value_num == 0:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_div_zero"))
            return None

        try:
            line_start = int(line_start_str) if line_start_str else 1
            line_end = int(line_end_str) if line_end_str else float('inf')
        except ValueError:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_invalid_line"))
            return None

        return {
            "file_path": file_path, "key": key, "operation": operation,
            "value_num": value_num, "line_start": line_start, "line_end": line_end,
            "replace_only": replace_only
        }

    def modify_values(self):
        config = self._validate_inputs()
        if not config:
            return

        try:
            with open(config["file_path"], "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_read_file").format(e))
            return

        modified_lines = process_lines(lines, config)

        try:
            with open(config["file_path"], "w", encoding="utf-8") as f:
                f.writelines(modified_lines)
            self.ui.show_status_message(self.lang_manager.get_translation("success_modify"))
        except Exception as e:
            messagebox.showerror(self.lang_manager.get_translation("title"), self.lang_manager.get_translation("error_save_file").format(e))

    def toggle_language(self):
        pass
