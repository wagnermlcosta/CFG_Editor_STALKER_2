import sys
from cx_Freeze import setup, Executable
import os

# Base para ocultar console no Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Arquivos adicionais a incluir
includefiles = ["language_config.json", "version.txt"]

# Opções do build
build_exe_options = {
    "packages": [],
    "include_files": includefiles,
    "include_msvcr": True,
}

setup(
    name="cfg_value_modifier",
    version="1.0",
    description="Executável standalone do cfg_value_modifier",
    options={"build_exe": build_exe_options},
    executables=[Executable("cfg_value_modifier.py", base=base)]
)
