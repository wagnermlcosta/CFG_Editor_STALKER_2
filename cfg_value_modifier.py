import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os

class CFGValueModifierApp:
    LANG_FILE = "language_config.json"
    # New path for external config file to persist language preference
    import sys
    import pathlib

    if getattr(sys, 'frozen', False):
        # Executável PyInstaller
        exe_dir = pathlib.Path(sys.executable).parent
    else:
        # Execução normal do script
        exe_dir = pathlib.Path(__file__).parent

    CONFIG_PATH = exe_dir / ".cfg_value_modifier_config.json"

    def __init__(self, root):
        self.root = root
        self.root.title("CFG Value Modifier")
        self.root.geometry("520x430")
        self.root.configure(bg="#2e2e2e")  # Dark theme background

        style = ttk.Style(self.root)
        self.set_dark_theme(style)

        # Load language preference
        self.languages = {
            "en": {
                "title": "CFG Value Modifier",
                "file_label": "CFG File:",
                "select_button": "Select",
                "key_label": "Key:",
                "operation_label": "Operation:",
                "replace_only": "Replace value without operation",
                "value_label": "Value:",
                "line_start_label": "Start line (optional):",
                "line_end_label": "End line (optional):",
                "modify_button": "Modify Values",
                "error_no_file": "Please select a .cfg file.",
                "error_no_key": "Please enter the key.",
                "error_no_value": "Please enter the value.",
                "error_invalid_value": "Invalid value. Please enter a valid number.",
                "error_invalid_line": "Invalid start or end line. Please enter valid integers.",
                "error_read_file": "Error reading file: {}",
                "error_save_file": "Error saving file: {}",
                "success_modify": "Values modified successfully.",
                "error_div_zero": "Division by zero is not allowed.",
                "language_button": "Português"
            },
            "pt": {
                "title": "Modificador de Valores CFG",
                "file_label": "Arquivo .cfg:",
                "select_button": "Selecionar",
                "key_label": "Chave:",
                "operation_label": "Operação:",
                "replace_only": "Substituir valor sem operação",
                "value_label": "Valor:",
                "line_start_label": "Linha inicial (opcional):",
                "line_end_label": "Linha final (opcional):",
                "modify_button": "Modificar Valores",
                "error_no_file": "Por favor, selecione um arquivo .cfg.",
                "error_no_key": "Por favor, informe a chave.",
                "error_no_value": "Por favor, informe o valor.",
                "error_invalid_value": "Valor inválido. Informe um número válido.",
                "error_invalid_line": "Linha inicial ou final inválida. Informe números inteiros válidos.",
                "error_read_file": "Erro ao ler o arquivo: {}",
                "error_save_file": "Erro ao salvar o arquivo: {}",
                "success_modify": "Valores modificados com sucesso.",
                "error_div_zero": "Divisão por zero não é permitida.",
                "language_button": "English"
            }
        }

        self.current_lang = self.load_language()

        # Variables
        self.file_path = tk.StringVar()
        self.key = tk.StringVar()
        self.operation = tk.StringVar(value="+")
        self.replace_only = tk.BooleanVar(value=False)
        self.value = tk.StringVar()
        self.line_start = tk.StringVar()
        self.line_end = tk.StringVar()

        # Layout
        self.create_widgets()
        self.update_texts()

    def set_dark_theme(self, style):
        style.theme_use('clam')
        style.configure('.', background='#2e2e2e', foreground='white', fieldbackground='#3e3e3e')
        style.configure('TButton', background='#444444', foreground='white')
        style.map('TButton', background=[('active', '#555555')])
        style.configure('TEntry', fieldbackground='#3e3e3e', foreground='white')
        style.configure('TLabel', background='#2e2e2e', foreground='white')
        style.configure('TCheckbutton', background='#2e2e2e', foreground='white')
        style.configure('TCombobox', fieldbackground='#3e3e3e', foreground='white')

    def create_widgets(self):
        padding_opts = {'padx': 10, 'pady': 5}

        # File selection
        self.file_label = ttk.Label(self.root)
        self.file_label.grid(row=0, column=0, sticky='w', **padding_opts)
        self.file_entry = ttk.Entry(self.root, textvariable=self.file_path, width=40)
        self.file_entry.grid(row=0, column=1, **padding_opts)
        self.select_button = ttk.Button(self.root, command=self.select_file)
        self.select_button.grid(row=0, column=2, **padding_opts)

        # Key input
        self.key_label = ttk.Label(self.root)
        self.key_label.grid(row=1, column=0, sticky='w', **padding_opts)
        self.key_entry = ttk.Entry(self.root, textvariable=self.key)
        self.key_entry.grid(row=1, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Operation selection
        self.operation_label = ttk.Label(self.root)
        self.operation_label.grid(row=2, column=0, sticky='w', **padding_opts)
        self.op_combo = ttk.Combobox(self.root, textvariable=self.operation, values=["+", "-", "*", "/"], state="readonly", width=3)
        self.op_combo.grid(row=2, column=1, sticky='w', **padding_opts)

        # Replace only checkbox
        self.replace_check = ttk.Checkbutton(self.root, variable=self.replace_only, style='TCheckbutton')
        self.replace_check.grid(row=2, column=2, sticky='w', padx=10, pady=5)

        # Value input
        self.value_label = ttk.Label(self.root)
        self.value_label.grid(row=3, column=0, sticky='w', **padding_opts)
        self.value_entry = ttk.Entry(self.root, textvariable=self.value)
        self.value_entry.grid(row=3, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Line start input
        self.line_start_label = ttk.Label(self.root)
        self.line_start_label.grid(row=4, column=0, sticky='w', **padding_opts)
        self.line_start_entry = ttk.Entry(self.root, textvariable=self.line_start)
        self.line_start_entry.grid(row=4, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Line end input
        self.line_end_label = ttk.Label(self.root)
        self.line_end_label.grid(row=5, column=0, sticky='w', **padding_opts)
        self.line_end_entry = ttk.Entry(self.root, textvariable=self.line_end)
        self.line_end_entry.grid(row=5, column=1, columnspan=2, sticky='ew', **padding_opts)

        # Execute button
        self.modify_button = ttk.Button(self.root, command=self.modify_values)
        self.modify_button.grid(row=6, column=0, columnspan=3, pady=20)

        # Language toggle button
        self.lang_button = ttk.Button(self.root, command=self.toggle_language)
        self.lang_button.grid(row=7, column=0, columnspan=3, pady=5)

        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=0)

    def update_texts(self):
        lang = self.languages[self.current_lang]
        self.root.title(lang["title"])
        self.file_label.config(text=lang["file_label"])
        self.select_button.config(text=lang["select_button"])
        self.key_label.config(text=lang["key_label"])
        self.operation_label.config(text=lang["operation_label"])
        self.replace_check.config(text=lang["replace_only"])
        self.value_label.config(text=lang["value_label"])
        self.line_start_label.config(text=lang["line_start_label"])
        self.line_end_label.config(text=lang["line_end_label"])
        self.modify_button.config(text=lang["modify_button"])
        self.lang_button.config(text=lang["language_button"])

    def toggle_language(self):
        self.current_lang = "pt" if self.current_lang == "en" else "en"
        self.save_language()
        self.update_texts()

    def load_language(self):
        # Check external config file first
        if self.CONFIG_PATH.exists():
            try:
                with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("language") in self.languages:
                        return data["language"]
            except Exception:
                pass
        # Fallback to embedded default
        return self.EMBEDDED_LANG_CONFIG.get("language", "en")

    def save_language(self):
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump({"language": self.current_lang}, f)
        except Exception:
            pass

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("CFG files", "*.cfg"), ("All files", "*.*")])
        if file:
            self.file_path.set(file)

    def modify_values(self):
        lang = self.languages[self.current_lang]

        file_path = self.file_path.get()
        key = self.key.get().strip()
        operation = self.operation.get()
        value_str = self.value.get().strip()
        line_start_str = self.line_start.get().strip()
        line_end_str = self.line_end.get().strip()
        replace_only = self.replace_only.get()

        if not file_path:
            messagebox.showerror(lang["title"], lang["error_no_file"])
            return
        if not key:
            messagebox.showerror(lang["title"], lang["error_no_key"])
            return
        if not value_str:
            messagebox.showerror(lang["title"], lang["error_no_value"])
            return

        try:
            if replace_only:
                value_num = value_str
            else:
                value_num = float(value_str)
        except ValueError:
            messagebox.showerror(lang["title"], lang["error_invalid_value"])
            return

        try:
            line_start = int(line_start_str) if line_start_str else 1
            line_end = int(line_end_str) if line_end_str else None
        except ValueError:
            messagebox.showerror(lang["title"], lang["error_invalid_line"])
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            messagebox.showerror(lang["title"], lang["error_read_file"].format(e))
            return

        if line_end is None or line_end > len(lines):
            line_end = len(lines)

        # Regex to match lines like "Key = value"
        pattern = re.compile(rf"^(\s*{re.escape(key)}\s*=\s*)(.+?)(\s*)$", re.IGNORECASE)

        modified_lines = []
        for i, line in enumerate(lines, start=1):
            if i < line_start or i > line_end:
                modified_lines.append(line)
                continue

            match = pattern.match(line)
            if match:
                prefix = match.group(1)
                current_value = match.group(2)
                suffix = match.group(3)

                if replace_only:
                    new_value_str = value_num
                else:
                    try:
                        current_value_num = float(current_value)
                    except ValueError:
                        modified_lines.append(line)
                        continue

                    new_value = self.apply_operation(current_value_num, value_num, operation)
                    new_value_str = str(int(new_value)) if new_value.is_integer() else str(new_value)

                # Preserve original line ending by using the existing suffix
                new_line = f"{prefix}{new_value_str}{suffix}"
                modified_lines.append(new_line)
            else:
                modified_lines.append(line)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(modified_lines)
            success_msg = lang["success_modify"]
            messagebox.showinfo(lang["title"], success_msg)
        except Exception as e:
            error_msg = lang["error_save_file"].format(e)
            messagebox.showerror(lang["title"], error_msg)

    def apply_operation(self, current, value, operation):
        lang = self.languages[self.current_lang]
        if operation == "+":
            return current + value
        elif operation == "-":
            return current - value
        elif operation == "*":
            return current * value
        elif operation == "/":
            if value == 0:
                messagebox.showerror(lang["title"], lang["error_div_zero"])
                return current
            return current / value
        else:
            return current

if __name__ == "__main__":
    root = tk.Tk()
    app = CFGValueModifierApp(root)
    root.mainloop()
