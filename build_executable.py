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
    project_root = Path(__file__).parent.resolve()
    dist_path = project_root / "dist"
    build_path = project_root / "build"
    icon_path = project_root / "app_icon.ico"
    version_file_path = project_root / "version_info.txt"

    # Clean up previous builds
    if dist_path.exists():
        shutil.rmtree(dist_path)
    if build_path.exists():
        shutil.rmtree(build_path)

    try:
        subprocess.run([
            sys.executable,  # Use the current python interpreter
            "-m", "PyInstaller",
            "--windowed",
            f"--icon={icon_path}",
            f"--name=CFG_Editor_STALKER_2_{version}",
            "--distpath", str(dist_path),
            "--workpath", str(build_path),
            "--specpath", str(build_path),
            f"--version-file={version_file_path}",
            "cfg_value_modifier.py"
        ], check=True)
        print("Executable built successfully!")
        print(f"Output folder: {dist_path.resolve()}")
        
        # Clean up build directory
        shutil.rmtree(build_path)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

if __name__ == "__main__":
    version = get_version()
    build_executable(version)
