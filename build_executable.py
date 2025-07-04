import os
import shutil
import subprocess
import re
import sys
from pathlib import Path

def get_version():
    """Extracts version from version_info.txt file"""
    version_file = Path("version_info.txt")
    if not version_file.exists():
        print("Error: version_info.txt not found!")
        sys.exit(1)
    
    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Search for pattern: prodvers=(MAJOR, MINOR, PATCH, BUILD)
    match = re.search(r"prodvers=\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)", content)
    if match:
        return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    else:
        print("Error: Version not found in version_info.txt!")
        sys.exit(1)

def build_executable(version):
    """Builds executable using PyInstaller"""
    try:
        subprocess.run([
            "pyinstaller",
            "--onedir",
            "--windowed",
            "--icon=app_icon.ico",
            f"--name=CFG_Editor_STALKER_2_{version}",
            "cfg_value_modifier.py"
        ], check=True)
        print("Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

if __name__ == "__main__":
    version = get_version()
    build_executable(version)
