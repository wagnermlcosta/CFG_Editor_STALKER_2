import os
import re
import shutil
from dataclasses import dataclass
from typing import Optional, Tuple, List

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


@dataclass
class PreviewChange:
    line_no: int
    original: str
    updated: str


NUMBER_WITH_OPTIONAL_PERCENT_RE = re.compile(
    r"""
    ^(?P<prefix>\s*)                                   # leading spaces
    (?P<var>[A-Za-z_][A-Za-z0-9_]*)                    # variable name
    \s*=\s*
    (?P<num>
        (?:
            \d+                                        # int
            (?:\.(\d+))?                               # optional decimals
        )
    )
    (?P<pct>\s*%)?                                     # optional percent (with possible space before %)
    (?P<suffix>\s*)$                                   # trailing spaces
    """,
    re.VERBOSE,
)

COMMENT_RE = re.compile(r"^\s*//")  # lines starting with //


def parse_number_format(num_str: str) -> Tuple[bool, int]:
    """
    Determine if num_str is int or float and how many decimal places it has.
    Returns: (is_int, decimals_count)
    """
    if "." in num_str:
        decimals = len(num_str.split(".")[1])
        return False, decimals
    return True, 0


def format_number(value: float, is_int: bool, decimals: int) -> str:
    """
    Format value respecting original numeric format:
    - if original was int, return int without decimal part
    - if original was float, keep the same number of decimals
    """
    if is_int:
        return str(int(round(value)))
    # format with fixed decimals, then strip unnecessary trailing zeros if decimals == 0 (shouldn't happen here)
    fmt = f"{{:.{decimals}f}}"
    return fmt.format(value)


def apply_operation(original_value: float, op: str, operand: float) -> float:
    if op == "Multiply":
        return original_value * operand
    if op == "Add":
        return original_value + operand
    if op == "Subtract":
        return original_value - operand
    if op == "Divide":
        # avoid division by zero
        return original_value / operand if operand != 0 else original_value
    if op == "Set":
        return operand
    return original_value


def process_lines(
    lines: List[str],
    var_name: str,
    op: str,
    operand: float,
    start_line: Optional[int],
    end_line: Optional[int],
    ignore_commented: bool,
    preview_only: bool,
) -> Tuple[List[str], int, List[PreviewChange]]:
    """
    Process lines in the specified inclusive range (1-based).
    Returns: (updated_lines, changes_count, preview_list)
    """
    updated = list(lines)
    total = len(lines)
    changes = 0
    previews: List[PreviewChange] = []

    # normalize range
    s_idx = 1 if start_line is None else max(1, start_line)
    e_idx = total if end_line is None else min(total, end_line)
    if s_idx > e_idx:
        return updated, 0, previews

    # regex for matching variable name exactly (case-sensitive by spec)
    # We'll match line fully with NUMBER_WITH_OPTIONAL_PERCENT_RE and then check var equality
    for i in range(s_idx, e_idx + 1):
        original_line = lines[i - 1]
        line = original_line.rstrip("\n")

        # ignore commented if checkbox is set
        if ignore_commented and COMMENT_RE.match(line):
            continue

        m = NUMBER_WITH_OPTIONAL_PERCENT_RE.match(line)
        if not m:
            continue
        if m.group("var") != var_name:
            continue

        num_str = m.group("num")
        pct = m.group("pct") or ""
        is_int, decimals = parse_number_format(num_str)

        try:
            numeric_value = float(num_str)
        except ValueError:
            continue

        new_value = apply_operation(numeric_value, op, operand)

        # Preserve numeric formatting
        out_num_str = format_number(new_value, is_int, decimals)

        # Rebuild line preserving prefix/suffix and percent suffix (with any space captured before %)
        prefix = m.group("prefix") or ""
        suffix = m.group("suffix") or ""
        rebuilt = f"{prefix}{var_name} = {out_num_str}{pct}{suffix}"

        if rebuilt != line:
            changes += 1
            previews.append(PreviewChange(i, original_line.rstrip('\n'), rebuilt))
            if not preview_only:
                # preserve the original newline if it had one
                newline = "\n" if original_line.endswith("\n") else ""
                updated[i - 1] = rebuilt + newline

    return updated, changes, previews


def make_backup(path: str) -> str:
    bak_path = path + ".bak"
    shutil.copy2(path, bak_path)
    return bak_path


def restore_backup(path: str) -> Tuple[bool, str]:
    bak_path = path + ".bak"
    if not os.path.isfile(bak_path):
        return False, "Backup file not found: " + bak_path
    shutil.copy2(bak_path, path)
    return True, f"Restored from backup: {bak_path} -> {path}"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CFG Variable Editor (Tkinter)")
        self.geometry("900x620")
        self.minsize(900, 620)

        # Variables
        self.file_path = tk.StringVar()
        self.var_name = tk.StringVar()
        self.operation = tk.StringVar(value="Multiply")
        self.value_str = tk.StringVar()
        self.scope_mode = tk.StringVar(value="entire")  # "entire" or "range"
        self.start_line = tk.StringVar()
        self.end_line = tk.StringVar()
        self.ignore_commented = tk.BooleanVar(value=True)
        self.create_backup = tk.BooleanVar(value=True)

        self._build_ui()
        self.text_output.insert(tk.END, "Ready.\n")

    def _build_ui(self):
        pad = {"padx": 8, "pady": 6}

        # File row
        row_file = ttk.Frame(self)
        row_file.pack(fill="x", **pad)
        ttk.Label(row_file, text="CFG File").pack(side="left")
        ttk.Entry(row_file, textvariable=self.file_path, width=80).pack(side="left", padx=6)
        ttk.Button(row_file, text="Browse...", command=self._browse_file).pack(side="left")

        # Variable / Operation row
        row_var = ttk.Frame(self)
        row_var.pack(fill="x", **pad)
        ttk.Label(row_var, text="Variable name").pack(side="left")
        ttk.Entry(row_var, textvariable=self.var_name, width=30).pack(side="left", padx=6)
        ttk.Label(row_var, text="Operation").pack(side="left", padx=(16, 4))
        op_combo = ttk.Combobox(row_var, textvariable=self.operation, values=["Multiply", "Add", "Subtract", "Divide", "Set"], state="readonly", width=12)
        op_combo.pack(side="left")
        ttk.Label(row_var, text="Value").pack(side="left", padx=(16, 4))
        ttk.Entry(row_var, textvariable=self.value_str, width=15).pack(side="left")

        # Scope frame
        frame_scope = ttk.LabelFrame(self, text="Scope")
        frame_scope.pack(fill="x", **pad)
        row_scope = ttk.Frame(frame_scope)
        row_scope.pack(fill="x", padx=6, pady=6)
        ttk.Radiobutton(row_scope, text="Entire file", value="entire", variable=self.scope_mode).pack(side="left")
        ttk.Radiobutton(row_scope, text="Line range", value="range", variable=self.scope_mode).pack(side="left", padx=(12, 0))
        ttk.Label(row_scope, text="Start").pack(side="left", padx=(24, 4))
        ttk.Entry(row_scope, textvariable=self.start_line, width=8).pack(side="left")
        ttk.Label(row_scope, text="End").pack(side="left", padx=(12, 4))
        ttk.Entry(row_scope, textvariable=self.end_line, width=8).pack(side="left")

        # Options
        row_opts = ttk.Frame(self)
        row_opts.pack(fill="x", **pad)
        ttk.Checkbutton(row_opts, text="Ignore commented lines (//)", variable=self.ignore_commented).pack(side="left")
        ttk.Checkbutton(row_opts, text="Create .bak backup before Apply", variable=self.create_backup).pack(side="left", padx=(16, 0))

        # Buttons
        row_btns = ttk.Frame(self)
        row_btns.pack(fill="x", **pad)
        ttk.Button(row_btns, text="Preview", command=self._on_preview).pack(side="left")
        ttk.Button(row_btns, text="Apply", command=self._on_apply).pack(side="left", padx=(8, 0))
        ttk.Button(row_btns, text="Restore from backup", command=self._on_restore).pack(side="left", padx=(8, 0))
        ttk.Button(row_btns, text="Close", command=self.destroy).pack(side="right")

        # Output
        ttk.Label(self, text="Output").pack(anchor="w", **pad)
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.text_output = tk.Text(text_frame, wrap="none", font=("Consolas", 10))
        self.text_output.pack(side="left", fill="both", expand=True)
        y_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_output.yview)
        y_scroll.pack(side="right", fill="y")
        self.text_output.configure(yscrollcommand=y_scroll.set)

    def _browse_file(self):
        path = filedialog.askopenfilename(title="Select CFG file", filetypes=[("CFG Files", "*.cfg"), ("All Files", "*.*")])
        if path:
            self.file_path.set(path)

    def _print(self, msg: str):
        self.text_output.insert(tk.END, msg + "\n")
        self.text_output.see(tk.END)

    def _validate_inputs(self) -> Optional[str]:
        if not self.file_path.get().strip():
            return "Please select a file."
        if not self.var_name.get().strip():
            return "Please enter a variable name."
        if self.operation.get() not in {"Multiply", "Add", "Subtract", "Divide", "Set"}:
            return "Please choose a valid operation."
        try:
            float(self.value_str.get().strip())
        except Exception:
            return "Value must be a number."
        if self.scope_mode.get() == "range":
            s = self.start_line.get().strip()
            e = self.end_line.get().strip()
            if not s or not e:
                return "Both start and end lines must be provided."
            try:
                s_val = int(s)
                e_val = int(e)
            except ValueError:
                return "Start/End must be integers."
            if s_val < 1 or e_val < 1:
                return "Start/End must be positive."
        return None

    def _collect_range(self) -> Tuple[Optional[int], Optional[int]]:
        if self.scope_mode.get() == "range":
            return int(self.start_line.get().strip()), int(self.end_line.get().strip())
        return None, None

    def _on_preview(self):
        err = self._validate_inputs()
        if err:
            messagebox.showerror("Validation", err)
            return

        with open(self.file_path.get(), "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        s_line, e_line = self._collect_range()
        updated, changes, previews = process_lines(
            lines=lines,
            var_name=self.var_name.get().strip(),
            op=self.operation.get(),
            operand=float(self.value_str.get().strip()),
            start_line=s_line,
            end_line=e_line,
            ignore_commented=self.ignore_commented.get(),
            preview_only=True,
        )

        self._print(f"[Preview] Matches to change: {changes}")
        for p in previews[:20]:
            self._print(f"Line {p.line_no}:")
            self._print(f"  - {p.original}")
            self._print(f"  + {p.updated}")
        if changes > 20:
            self._print(f"... and {changes - 20} more changes.")

    def _on_apply(self):
        err = self._validate_inputs()
        if err:
            messagebox.showerror("Validation", err)
            return

        with open(self.file_path.get(), "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        s_line, e_line = self._collect_range()
        updated, changes, previews = process_lines(
            lines=lines,
            var_name=self.var_name.get().strip(),
            op=self.operation.get(),
            operand=float(self.value_str.get().strip()),
            start_line=s_line,
            end_line=e_line,
            ignore_commented=self.ignore_commented.get(),
            preview_only=False,
        )

        if self.create_backup.get():
            try:
                bak = make_backup(self.file_path.get())
                self._print(f"Backup created: {bak}")
            except Exception as e:
                self._print(f"Failed to create backup: {e}")

        with open(self.file_path.get(), "w", encoding="utf-8", errors="replace") as f:
            f.writelines(updated)

        self._print(f"Saved file: {self.file_path.get()}")
        self._print(f"Applied changes: {changes}")
        for p in previews[:20]:
            self._print(f"Line {p.line_no}:")
            self._print(f"  - {p.original}")
            self._print(f"  + {p.updated}")
        if changes > 20:
            self._print(f"... and {changes - 20} more changes.")

    def _on_restore(self):
        path = self.file_path.get().strip()
        if not path:
            messagebox.showinfo("Info", "Please select a file.")
            return
        ok, msg = restore_backup(path)
        self._print(msg)


def build_gui():
    # Tkinter version uses App class
    return App()


def read_file_text(path: str) -> Tuple[bool, str, Optional[List[str]]]:
    if not os.path.isfile(path):
        return False, f"File not found: {path}", None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        return True, "OK", lines
    except Exception as e:
        return False, f"Error reading file: {e}", None


def write_file_text(path: str, lines: List[str]) -> Tuple[bool, str]:
    try:
        with open(path, "w", encoding="utf-8", errors="replace") as f:
            f.writelines(lines)
        return True, f"Saved file: {path}"
    except Exception as e:
        return False, f"Error writing file: {e}"


def parse_range(start_s: str, end_s: str) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    start = start_s.strip()
    end = end_s.strip()
    if start == "" and end == "":
        return None, None, None
    if start == "" or end == "":
        return None, None, "Both start and end lines must be provided."
    try:
        s_val = int(start)
        e_val = int(end)
    except ValueError:
        return None, None, "Start/End must be integers."
    if s_val < 1 or e_val < 1:
        return None, None, "Start/End must be positive."
    return s_val, e_val, None


def parse_operand(val_s: str) -> Tuple[Optional[float], Optional[str]]:
    try:
        return float(val_s.strip()), None
    except Exception:
        return None, "Value must be a number."


def main():
    app = build_gui()
    app.mainloop()


if __name__ == "__main__":
    main()
