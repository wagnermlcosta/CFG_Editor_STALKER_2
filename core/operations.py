"""
Mathematical operations for CFG file editing.
Provides functions for performing mathematical operations on numeric values.
"""

from typing import Union, Tuple
from enum import Enum

class OperationType(Enum):
    """Enumeration of supported operation types."""
    REPLACE = "replace"
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class MathOperations:
    """Class containing mathematical operations for CFG editing."""
    
    @staticmethod
    def apply_operation(old_value: Union[int, float], operation: OperationType, operand: Union[int, float]) -> Tuple[Union[int, float], bool]:
        """
        Apply a mathematical operation to a value.
        
        Args:
            old_value: The original value
            operation: The operation to perform
            operand: The value to use in the operation
            
        Returns:
            Tuple of (new_value, success)
        """
        try:
            if operation == OperationType.REPLACE:
                return operand, True
            elif operation == OperationType.ADD:
                return old_value + operand, True
            elif operation == OperationType.SUBTRACT:
                return old_value - operand, True
            elif operation == OperationType.MULTIPLY:
                return old_value * operand, True
            elif operation == OperationType.DIVIDE:
                if operand == 0:
                    return old_value, False  # Division by zero
                return old_value / operand, True
            else:
                return old_value, False  # Unknown operation
        except Exception:
            return old_value, False
    
    @staticmethod
    def validate_numeric_value(value_str: str) -> Tuple[Union[int, float], bool]:
        """
        Validate and convert a string to a numeric value.
        
        Args:
            value_str: String representation of the value
            
        Returns:
            Tuple of (numeric_value, is_valid)
        """
        try:
            # Try to convert to int first
            if '.' not in value_str:
                return int(value_str), True
            else:
                return float(value_str), True
        except ValueError:
            return 0, False
    
    @staticmethod
    def format_numeric_value(value: Union[int, float]) -> str:
        """
        Format a numeric value for output.
        
        Args:
            value: The numeric value to format
            
        Returns:
            Formatted string representation
        """
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)
    
    @staticmethod
    def get_operation_description(operation: OperationType, operand: Union[int, float]) -> str:
        """
        Get a human-readable description of an operation.
        
        Args:
            operation: The operation type
            operand: The operand value
            
        Returns:
            Description string
        """
        if operation == OperationType.REPLACE:
            return f"Replace with {operand}"
        elif operation == OperationType.ADD:
            return f"Add {operand}"
        elif operation == OperationType.SUBTRACT:
            return f"Subtract {operand}"
        elif operation == OperationType.MULTIPLY:
            return f"Multiply by {operand}"
        elif operation == OperationType.DIVIDE:
            return f"Divide by {operand}"
        else:
            return "Unknown operation"

