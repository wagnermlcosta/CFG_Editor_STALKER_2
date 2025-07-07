import json
from tkinter import messagebox
from pathlib import Path
import sys
from app.constants import EMBEDDED_LANG_CONFIG, LANG_FILE

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # When running as a PyInstaller executable, files are extracted to sys._MEIPASS
        return Path(sys._MEIPASS)
    else:
        # When running from source, the language file is in the project root
        return Path(__file__).parent.parent.parent

class LanguageManager:
    def __init__(self):
        self.base_dir = get_base_dir()
        self.languages = self.load_language_definitions()
        self.current_lang = "en"

    def load_language_definitions(self):
        try:
            with open(self.base_dir / LANG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Language file {LANG_FILE} not found.")
            return {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error decoding language file {LANG_FILE}.")
            return {}

    def load_language(self):
        return EMBEDDED_LANG_CONFIG.get("language", "en")

    def save_language(self):
        pass

    def get_translation(self, key):
        return self.languages.get(self.current_lang, {}).get(key, key)

    def toggle_language(self):
        pass
