import json
from tkinter import messagebox
from pathlib import Path
import sys
from app.constants import EMBEDDED_LANG_CONFIG, LANG_FILE

def get_exe_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent

class LanguageManager:
    def __init__(self):
        self.exe_dir = get_exe_dir()
        self.config_path = self.exe_dir / ".cfg_value_modifier_config.json"
        self.languages = self.load_language_definitions()
        self.current_lang = self.load_language()

    def load_language_definitions(self):
        try:
            with open(self.exe_dir / LANG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Language file {LANG_FILE} not found.")
            return {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error decoding language file {LANG_FILE}.")
            return {}

    def load_language(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("language") in self.languages:
                        return data["language"]
            except Exception:
                pass
        return EMBEDDED_LANG_CONFIG.get("language", "en")

    def save_language(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"language": self.current_lang}, f)
        except Exception:
            pass

    def get_translation(self, key):
        return self.languages.get(self.current_lang, {}).get(key, key)

    def toggle_language(self):
        self.current_lang = "pt" if self.current_lang == "en" else "en"
        self.save_language()
