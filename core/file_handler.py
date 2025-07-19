"""
File handling utilities for CFG files.
Provides functions for loading, saving, and managing CFG files.
"""

import os
import shutil
from typing import Optional, Tuple
from datetime import datetime

class FileHandler:
    """File handling utilities for CFG files."""
    
    def __init__(self):
        self.current_file = None
        self.backup_dir = None
        
    def create_backup(self, file_path: str) -> Tuple[bool, str]:
        """
        Create a backup of the current file.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Tuple of (success, backup_path_or_error_message)
        """
        try:
            # Create backup directory if it doesn't exist
            backup_dir = os.path.join(os.path.dirname(file_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename with timestamp
            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{name}_backup_{timestamp}{ext}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Copy the file
            shutil.copy2(file_path, backup_path)
            
            return True, backup_path
            
        except Exception as e:
            return False, f"Failed to create backup: {str(e)}"
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            stat = os.stat(file_path)
            
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK)
            }
        except Exception as e:
            return {
                'path': file_path,
                'error': str(e)
            }
    
    def read_file_content(self, file_path: str) -> Tuple[bool, str]:
        """
        Read the content of a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            Tuple of (success, content_or_error_message)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return True, content
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                return True, content
            except Exception as e:
                return False, f"Failed to read file with alternative encoding: {str(e)}"
        except Exception as e:
            return False, f"Failed to read file: {str(e)}"
    
    def write_file_content(self, file_path: str, content: str, create_backup: bool = True) -> Tuple[bool, str]:
        """
        Write content to a file.
        
        Args:
            file_path: Path to the file to write
            content: Content to write
            create_backup: Whether to create a backup before writing
            
        Returns:
            Tuple of (success, error_message_or_backup_path)
        """
        try:
            backup_path = ""
            
            # Create backup if requested and file exists
            if create_backup and os.path.exists(file_path):
                success, result = self.create_backup(file_path)
                if success:
                    backup_path = result
                else:
                    return False, result
            
            # Write the content
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return True, backup_path
            
        except Exception as e:
            return False, f"Failed to write file: {str(e)}"
    
    def validate_file_access(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate that a file can be accessed for reading and writing.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        if not os.path.isfile(file_path):
            return False, "Path is not a file"
        
        if not os.access(file_path, os.R_OK):
            return False, "File is not readable"
        
        if not os.access(file_path, os.W_OK):
            return False, "File is not writable"
        
        return True, ""
    
    def get_line_count(self, file_path: str) -> int:
        """
        Get the number of lines in a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Number of lines in the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return sum(1 for _ in file)
        except Exception:
            return 0

