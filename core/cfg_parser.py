"""
CFG file parser for Stalker 2 configuration files.
Handles parsing, variable identification, and value manipulation.
"""

import re
from typing import List, Tuple, Optional, Dict, Any

from core.operations import MathOperations, OperationType

class CFGParser:
    """Parser for Stalker 2 CFG files."""
    
    # Regex pattern to match variable assignments
    VARIABLE_PATTERN = r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$'
    
    def __init__(self):
        self.lines = []
        self.file_path = None
        
    def load_file(self, file_path: str) -> bool:
        """
        Load a CFG file.
        
        Args:
            file_path: Path to the CFG file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.lines = file.readlines()
            self.file_path = file_path
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def save_file(self, file_path: Optional[str] = None) -> bool:
        """
        Save the CFG file.
        
        Args:
            file_path: Optional path to save to (uses original path if None)
            
        Returns:
            True if successful, False otherwise
        """
        save_path = file_path or self.file_path
        if not save_path:
            return False
            
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.writelines(self.lines)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def get_content(self) -> str:
        """
        Get the current content as a string.
        
        Returns:
            The file content as a string
        """
        return ''.join(self.lines)
    
    def set_content(self, content: str):
        """
        Set the content from a string.
        
        Args:
            content: The new content as a string
        """
        self.lines = [line + '\n' for line in content.splitlines()]
    
    def find_variables(self, variable_name: str, start_line: int = 1, end_line: Optional[int] = None) -> List[Tuple[int, str, str, str]]:
        """
        Find all occurrences of a variable within a line range.
        
        Args:
            variable_name: Name of the variable to find
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based, inclusive). If None, search to end of file
            
        Returns:
            List of tuples: (line_number, indentation, variable_name, value)
        """
        results = []
        end_idx = len(self.lines) if end_line is None else min(end_line, len(self.lines))
        start_idx = max(0, start_line - 1)
        
        for i in range(start_idx, end_idx):
            line = self.lines[i]
            match = re.match(self.VARIABLE_PATTERN, line)
            if match:
                indent, var_name, value = match.groups()
                if var_name == variable_name:
                    results.append((i + 1, indent, var_name, value))
        
        return results
    
    def update_variable(self, variable_name: str, new_value: str, start_line: int = 1, end_line: Optional[int] = None) -> int:
        """
        Update all occurrences of a variable within a line range.
        
        Args:
            variable_name: Name of the variable to update
            new_value: New value for the variable
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based, inclusive). If None, update to end of file
            
        Returns:
            Number of variables updated
        """
        updated_count = 0
        if end_line is None:
            end_idx = len(self.lines)
        else:
            end_idx = min(end_line, len(self.lines))
        start_idx = max(0, start_line - 1)
        
        for i in range(start_idx, end_idx):
            line = self.lines[i]
            match = re.match(self.VARIABLE_PATTERN, line)
            if match:
                indent, var_name, old_value = match.groups()
                if var_name == variable_name:
                    # Preserve indentation and any comments/trailing content
                    self.lines[i] = f"{indent}{var_name} = {new_value}\n"
                    updated_count += 1
        
        return updated_count
    
    def apply_mathematical_operation(self, variable_name: str, operation: str, value: float, start_line: int = 1, end_line: Optional[int] = None) -> Tuple[int, List[str]]:
        """
        Apply a mathematical operation to all occurrences of a variable.
        
        Args:
            variable_name: Name of the variable to modify
            operation: Operation type ('add', 'subtract', 'multiply', 'divide')
            value: Value to use in the operation
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based, inclusive). If None, apply to end of file
            
        Returns:
            Tuple of (number_of_changes, list_of_error_messages)
        """
        changes = 0
        errors = []
        if end_line is None:
            end_idx = len(self.lines)
        else:
            end_idx = min(end_line, len(self.lines))
        start_idx = max(0, start_line - 1)
        
        for i in range(start_idx, end_idx):
            line = self.lines[i]
            match = re.match(self.VARIABLE_PATTERN, line)
            if match:
                indent, var_name, old_value_str = match.groups()
                if var_name == variable_name:
                    try:
                        old_value, is_valid = MathOperations.validate_numeric_value(old_value_str)
                        if not is_valid:
                            errors.append(f"Line {i + 1}: Invalid numeric value '{old_value_str}'")
                            continue

                        op_type = OperationType(operation)
                        new_value, success = MathOperations.apply_operation(old_value, op_type, value)
                        
                        if not success:
                            errors.append(f"Line {i + 1}: Operation '{operation}' failed for value '{old_value_str}'")
                            continue
                        
                        new_value_str = MathOperations.format_numeric_value(new_value)
                        
                        # Update the line
                        self.lines[i] = f"{indent}{var_name} = {new_value_str}\n"
                        changes += 1
                        
                    except ValueError:
                        errors.append(f"Line {i + 1}: Invalid numeric value '{old_value_str}'")
                    except Exception as e:
                        errors.append(f"Line {i + 1}: Error processing value - {str(e)}")
        
        return changes, errors
    
    def preview_changes(self, variable_name: str, operation: str, value: float, start_line: int = 1, end_line: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Preview changes without applying them.
        
        Args:
            variable_name: Name of the variable to modify
            operation: Operation type ('replace', 'add', 'subtract', 'multiply', 'divide')
            value: Value to use in the operation
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based, inclusive). If None, preview to end of file
            
        Returns:
            List of dictionaries with change information
        """
        changes = []
        if end_line is None:
            end_idx = len(self.lines)
        else:
            end_idx = min(end_line, len(self.lines))
        start_idx = max(0, start_line - 1)
        
        for i in range(start_idx, end_idx):
            line = self.lines[i]
            match = re.match(self.VARIABLE_PATTERN, line)
            if match:
                indent, var_name, old_value_str = match.groups()
                if var_name == variable_name:
                    try:
                        old_value, is_valid = MathOperations.validate_numeric_value(old_value_str)
                        if not is_valid:
                            continue

                        op_type = OperationType(operation)
                        new_value, success = MathOperations.apply_operation(old_value, op_type, value)

                        if not success:
                            continue

                        new_value_str = MathOperations.format_numeric_value(new_value)
                        
                        changes.append({
                            'line_number': i + 1,
                            'old_line': line.rstrip(),
                            'new_line': f"{indent}{var_name} = {new_value_str}",
                            'old_value': old_value,
                            'new_value': new_value
                        })
                        
                    except ValueError:
                        continue  # Skip invalid values
        
        return changes