# CFG Editor for STALKER 2

Python GUI application for modifying values in `.cfg` configuration files for games like STALKER.

## Features
- Intuitive dark theme interface.
- Mathematical operations on config values (`+`, `-`, `*`, `/`).
- Option to replace a value directly without any mathematical operation.
- Line-range specific modifications to target specific sections of a file.
- Standalone executable, no Python installation required to run.

## Installation

1.  Go to the [Releases page](https://github.com/wagnermlcosta/CFG_Editor_STALKER_2/releases).
2.  Download the `.exe` file from the latest release.
3.  Run the executable.

## Usage

1.  Launch the application.
2.  Click **"Select"** to choose a `.cfg` file.
3.  Enter the configuration **"Key"** you want to modify (e.g., `fov`).
4.  Choose the **"Operation"** (`+`, `-`, `*`, `/`) or check the **"Replace value without operation"** box.
5.  Enter the **"Value"** for the operation.
6.  (Optional) Specify a **"Start line"** and **"End line"** to limit the modification to a specific part of the file.
7.  Click **"Modify Values"** to apply the changes to the file.

## Building from Source

To create the executable from the source code:

1.  **Prerequisites:**
    *   Install [Python 3.13](https://www.python.org/downloads/) or later.

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/wagnermlcosta/CFG_Editor_STALKER_2.git
    cd CFG_Editor_STALKER_2
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements-dev.txt
    ```

4.  **Run the build command:**
    ```bash
    pyinstaller main.spec
    ```

This will generate the executable using PyInstaller. The final `.exe` file will be located in the `dist/` directory.

## License
MIT License - See [LICENSE](LICENSE)
