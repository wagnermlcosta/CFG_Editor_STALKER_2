# Stalker 2 CFG Editor

A GUI application for editing Stalker 2 configuration files with mathematical operations.

---

## For Users: How to Use the Application

### Installation

No installation required. This is a portable application.

1.  Go to the [**Releases**](https://github.com/wagnermlcosta/CFG_Editor_STALKER_2/releases) page of this repository.
2.  Download the latest `CFG_Editor_STALKER_2.zip` file.
3.  Unzip the file.
4.  Run `CFG_Editor_STALKER_2.exe`.

### Features

*   **Load and Edit**: Open and modify `.cfg` files with ease.
*   **Math Operations**: Apply mathematical operations (add, subtract, multiply, divide) to variables.
*   **Value Replacement**: Replace variable values directly.
*   **Targeted Processing**: Apply changes to the entire file or specify a precise line range.
*   **Format Preservation**: Keeps your file formatting, indentation, and comments intact.
*   **Automatic Backups**: Automatically creates a backup of your file before saving changes.
*   **Modern Interface**: A clean, dark-themed UI.

### How to Use

1.  Run the application.
2.  Use **File > Open CFG File...** to load your configuration file.
3.  In the **Operations Panel** on the right:
    *   Enter the **Variable Name** you want to modify.
    *   Select the **Operation Type** (e.g., `Multiply (×)`).
    *   Enter the **Value** to apply.
    *   (Optional) Check **Apply to specific range** and set the start/end lines.
4.  Click **Preview Changes** to see a summary of what will be modified.
5.  Click **Apply Changes** to perform the operation.
6.  Use **File > Save** or **File > Save As...** to save your work.

---

## For Developers: Running from Source

### System Requirements

*   Python 3.8 or higher
*   `tkinter` (usually included with Python, but may require separate installation on Linux).

### Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/wagnermlcosta/CFG_Editor_STALKER_2.git
    cd CFG_Editor_STALKER_2
    ```

2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    *Note: `requirements.txt` only contains `pyinstaller` for building the executable. The application itself has no external dependencies.*

3.  **Run the application:**
    *   **Windows:** `python main.py`
    *   **Linux/macOS:** `python3 main.py`

### Building the Executable

To create the standalone `.exe` file:

1.  Ensure `pyinstaller` is installed (`pip install -r requirements.txt`).
2.  Run the build command:
    ```sh
    pyi-makespec --name CFG_Editor_STALKER_2 --onefile --windowed main.py
    pyinstaller CFG_Editor_STALKER_2.spec
    ```
3.  The final executable will be located in the `dist/` directory.
