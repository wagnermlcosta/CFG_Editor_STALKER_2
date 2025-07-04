# CFG Editor for STALKER 2

Python GUI application for modifying values in .cfg configuration files.

## Features
- Intuitive dark theme interface
- Mathematical operations on config values (+, -, *, /)
- Line-range specific modifications
- English/Portuguese language switching
- Error handling for common issues

## Installation
```bash
git clone https://github.com/wagnermlcosta/CFG_Editor_STALKER_2.git
python cfg_value_modifier.py
```

## Usage
1. Select .cfg file
2. Enter target key
3. Choose operation (or select "Replace value without operation")
4. Enter modification value
5. (Optional) Specify line range
6. Click "Modify Values"

## Building Executable

To create the executable and required files:

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run the build script:
```bash
python build_executable.py
```

This will:
- Generate the executable using PyInstaller

## License
MIT License - See [LICENSE](LICENSE)
