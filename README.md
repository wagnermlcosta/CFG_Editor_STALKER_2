# CFG Editor STALKER 2

A simple GUI tool to batch-edit numeric variables in STALKER 2-style `.cfg` files.  
It supports applying a single arithmetic operation to a chosen variable name within the whole file or a specific line range, while preserving numeric formatting and optional percentage suffixes.

Built with Python and Tkinter (no paid dependencies), and can be bundled into a portable Windows executable.

## Features

- Select a `.cfg` file
- Target a specific variable name (e.g., `BaseDamage`)
- Single operation per run:
  - Multiply, Add, Subtract, Divide, Set
- Scope control:
  - Entire file, or
  - Line range (1-based, inclusive): start and end
- Ignore commented lines option (lines beginning with `//`)
- Preserve numeric format:
  - Integers remain integers
  - Floats keep the same number of decimals
  - Percent values (e.g., `10%`) are supported and the `%` suffix is preserved after applying the operation
- Preview mode shows how many matches will be changed and a small before/after sample
- Apply mode updates and saves the file
- Optional automatic `.bak` backup before saving
- Restore from backup button

## Project Structure

```
.
├─ tools/
│  └─ cfg_editor_gui.py     # Tkinter GUI tool
├─ PlayerWeaponSettingsPrototypes.cfg  # Example/working CFG file
├─ LICENSE
├─ README.md
└─ cfg_editor_gui.spec      # PyInstaller spec generated during build
```

## Requirements

- Windows with Python 3.10+ (tested on Python 3.13)
- Tkinter is included with standard Python installers for Windows
- No extra libraries required for running from source

## Running from Source

1) Ensure Python is installed and on PATH.
2) Open a terminal in the project folder.
3) Run:
   ```
   python tools/cfg_editor_gui.py
   ```

The GUI window "CFG Variable Editor (Tkinter)" should appear.

## Usage

1) In the GUI:
   - File: Browse and select your `.cfg`
   - Variable name: e.g., `BaseDamage`
   - Operation: Choose one of Multiply/Add/Subtract/Divide/Set
   - Value: Enter the number to use with the operation
   - Scope: Entire file or Line range (Start/End are inclusive, 1-based)
   - Options:
     - Ignore commented lines (//)
     - Create .bak backup before Apply

2) Click Preview
   - Shows the number of matches and up to ~20 before/after samples.
   - NOTE: Preview does not modify the file.

3) Click Apply
   - Creates a backup if the option is enabled (same path + `.bak`)
   - Applies changes to the file and prints a short sample of updates.

4) Restore from backup (optional)
   - Replaces the current file with the `.bak` copy.

### Numeric Formatting Rules

- If the original value is an integer (e.g., `150`), the result stays integer.
- If the original value is a float (e.g., `150.0` or `3.30`), the same number of decimal places is preserved.
- If the original value has a percent sign (e.g., `10%`), the operation is applied to the numeric part and `%` is reattached.

### Comments and Matching Rules

- When "Ignore commented lines (//)" is enabled, lines starting with `//` are ignored (not modified).
- Variable matching is exact and case-sensitive.
- Only lines matching this pattern are considered:
  ```
  <spaces>VariableName = <number>[%]<spaces>
  ```
  Examples:
  - `   BaseDamage = 20.0`
  - `   ChanceBleedingPerShot = 10%`

Lines with extra content beyond the number (e.g., `// comments at end`) will not match.

## Building a Portable Executable (Windows)

1) Install PyInstaller:
   ```
   python -m pip install --user pyinstaller
   ```
2) Build:
   ```
   python -m PyInstaller --onefile --windowed --name cfg_editor_gui tools/cfg_editor_gui.py
   ```
3) The executable will be created at:
   ```
   dist/cfg_editor_gui.exe
   ```

If Windows Defender SmartScreen warns, click "More info" > "Run anyway".

## Notes and Limitations

- One operation per execution (by design).
- Division by zero is safely ignored (no change applied).
- This tool is tailored for CFG lines following the simple `Var = Number[%]` structure.
- Always keep backups of your game config files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
