"""
Validation utilities for CFG file editing.
Provides functions for validating user input and file operations.
"""

import os
import re
from typing import Tuple, Optional

class Validator:
    """Validation utilities for the CFG editor."""
    
    @staticmethod
    def validate_file_path(file_path: str) -> Tuple[bool, str]:
        """
        Validate a file path.
        
        Args:
            file_path: Path to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_path:
            return False, "File path cannot be empty"
        
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        if not os.path.isfile(file_path):
            return False, "Path is not a file"
        
        if not file_path.lower().endswith('.cfg'):
            return False, "File must have .cfg extension"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1)  # Try to read one character
        except Exception as e:
            return False, f"Cannot read file: {str(e)}"
        
        return True, ""
    
    @staticmethod
    def validate_variable_name(variable_name: str) -> Tuple[bool, str]:
        """
        Validate a variable name.
        
        Args:
            variable_name: Variable name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not variable_name:
            return False, "Variable name cannot be empty"
        
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', variable_name):
            return False, "Variable name must start with letter or underscore and contain only letters, numbers, and underscores"
        
        return True, ""
    
    @staticmethod
    def validate_numeric_value(value_str: str) -> Tuple[bool, str, Optional[float]]:
        """
        Validate a numeric value string.
        
        Args:
            value_str: String representation of the value
            
        Returns:
            Tuple of (is_valid, error_message, numeric_value)
        """
        if not value_str:
            return False, "Value cannot be empty", None
        
        try:
            numeric_value = float(value_str)
            return True, "", numeric_value
        except ValueError:
            return False, "Value must be a valid number", None
    
    @staticmethod
    def validate_line_range(start_line: str, end_line: str, total_lines: int) -> Tuple[bool, str, Optional[int], Optional[int]]:
        """
        Validate a line range.
        
        Args:
            start_line: Starting line number as string
            end_line: Ending line number as string
            total_lines: Total number of lines in the file
            
        Returns:
            Tuple of (is_valid, error_message, start_int, end_int)
        """
        # Validate start line
        if start_line:
            try:
                start_int = int(start_line)
                if start_int < 1:
                    return False, "Start line must be greater than 0", None, None
                if start_int > total_lines:
                    return False, f"Start line cannot be greater than total lines ({total_lines})", None, None
            except ValueError:
                return False, "Start line must be a valid integer", None, None
        else:
            start_int = 1
        
        # Validate end line
        if end_line:
            try:
                end_int = int(end_line)
                if end_int < 1:
                    return False, "End line must be greater than 0", None, None
                if end_int > total_lines:
                    return False, f"End line cannot be greater than total lines ({total_lines})", None, None
                if end_int < start_int:
                    return False, "End line cannot be less than start line", None, None
            except ValueError:
                return False, "End line must be a valid integer", None, None
        else:
            end_int = total_lines
        
        return True, "", start_int, end_int
    
    @staticmethod
    def validate_operation_type(operation: str) -> Tuple[bool, str]:
        """
        Validate an operation type.
        
        Args:
            operation: Operation type to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_operations = ['replace', 'add', 'subtract', 'multiply', 'divide']
        
        if not operation:
            return False, "Operation type cannot be empty"
        
        if operation.lower() not in valid_operations:
            return False, f"Operation must be one of: {', '.join(valid_operations)}"
        
        return True, ""

