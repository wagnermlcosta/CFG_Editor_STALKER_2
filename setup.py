
import sys
from cx_Freeze import setup, Executable
import re
from pathlib import Path

def get_version():
    """Extracts version from version_info.txt file"""
    version_file = Path("version_info.txt")
    if not version_file.exists():
        raise RuntimeError("version_info.txt not found!")
    
    content = version_file.read_text(encoding="utf-8")
    
    match = re.search(r"prodvers=\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)", content)
    if match:
        return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    else:
        raise RuntimeError("Version not found in version_info.txt!")

VERSION = get_version()

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["tkinter", "re", "json", "os", "sys", "pathlib"],
    "include_files": ["app_icon.ico", "language_config.json"],
    "build_exe": f"build/CFG_Editor_STALKER_2_v{VERSION}"
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

# Define the executables
executables = [
    Executable(
        "cfg_value_modifier.py",
        base=base,
        target_name="CFG_Editor_STALKER_2.exe",
        icon="app_icon.ico",
        shortcut_name="CFG Editor STALKER 2",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name="CFG_Editor_STALKER_2",
    version=VERSION,
    description="CFG Editor for STALKER 2",
    options={"build_exe": build_exe_options},
    executables=executables,
)
