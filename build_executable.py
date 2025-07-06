
import os
import shutil
import subprocess
import re
import sys
from pathlib import Path
from datetime import datetime

def update_version_info_file(version_str, current_year):
    """Updates the version_info.txt file with the given version and current year."""
    version_file = Path("version_info.txt")
    if not version_file.exists():
        print("Error: version_info.txt not found for update!")
        return False

    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Update version numbers
    version_tuple = tuple(map(int, version_str.split('.')))
    new_version_tuple_str = str(version_tuple)

    content = re.sub(r"filevers=\(.*?\)", f"filevers={new_version_tuple_str}", content)
    content = re.sub(r"prodvers=\(.*?\)", f"prodvers={new_version_tuple_str}", content)
    content = re.sub(r"StringStruct\(u'FileVersion', u'.*?'\)", f"StringStruct(u'FileVersion', u'{version_str}')", content)
    content = re.sub(r"StringStruct\(u'ProductVersion', u'.*?'\)", f"StringStruct(u'ProductVersion', u'{version_str}')", content)

    # Update copyright year
    content = re.sub(r"Copyright \(C\) wagnermlcosta \d{4}", f"Copyright (C) wagnermlcosta {current_year}", content)

    with open(version_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("--> Updated version_info.txt with current version and copyright year.")
    return True



def get_version():
    """Extracts version from version_info.txt file"""
    version_file = Path("version_info.txt")
    if not version_file.exists():
        print("Error: version_info.txt not found!")
        sys.exit(1)
    
    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Corrected regex
    prodvers_line_match = re.search(r"^\s*prodvers=\(.*\),", content, re.MULTILINE)
    if prodvers_line_match:
        version_numbers_match = re.search(r"\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\),", prodvers_line_match.group(0))
        if version_numbers_match:
            return f"{version_numbers_match.group(1)}.{version_numbers_match.group(2)}.{version_numbers_match.group(3)}.{version_numbers_match.group(4)}"
        else:
            print("Error: Version numbers not found in prodvers line!")
            sys.exit(1)
    else:
        print("Error: prodvers line not found in version_info.txt!")
        sys.exit(1)

def build_executable(version):
    """Builds executable using PyInstaller"""
    project_root = Path(__file__).parent.resolve()
    dist_path = project_root / "dist"
    build_path = project_root / "build"
    icon_path = project_root / "app_icon.ico"
    version_file_path = project_root / "version_info.txt"

    if dist_path.exists():
        shutil.rmtree(dist_path)
    if build_path.exists():
        shutil.rmtree(build_path)

    try:
        print(f"--> Building executable v{version}...")
        subprocess.run([
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            f"--icon={icon_path}",
            f"--name=CFG_Editor_STALKER_2_{version}",
            "--distpath", str(dist_path),
            "--workpath", str(build_path),
            "--specpath", str(build_path),
            f"--version-file={version_file_path}",
            "--add-data", f"{project_root / 'language_config.json'}{os.pathsep}.",
            "cfg_value_modifier.py"
        ], check=True)
        print("--> Executable built successfully!")
        
        shutil.rmtree(build_path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False



if __name__ == "__main__":
    main_version = get_version()
    current_year = datetime.now().year
    if update_version_info_file(main_version, current_year):
        if build_executable(main_version):
            print("\nBuild process completed successfully!")
        else:
            print("\nBuild process failed.")
            sys.exit(1)
    else:
        sys.exit(1)
