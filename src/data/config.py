"""Configuration module for file path resolution and management."""
import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration class for managing file locations and paths."""

    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            data_file: Optional custom path for the todo data file
        """
        self._data_file = data_file

    def get_data_file_path(self) -> Path:
        """
        Get the path for the todo data file.

        Returns:
            Path to the data file
        """
        if self._data_file:
            # Use custom file if provided
            file_path = Path(self._data_file).expanduser().resolve()
            # Validate the path to prevent directory traversal
            self._validate_path(file_path)
            return file_path
        else:
            # Use environment variable if set
            env_file = os.getenv('TODO_FILE')
            if env_file:
                file_path = Path(env_file).expanduser().resolve()
                # Validate the path to prevent directory traversal
                self._validate_path(file_path)
                return file_path
            else:
                # Use default location: ~/.todo/todos.json
                home_dir = Path.home()
                todo_dir = home_dir / '.todo'
                todo_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
                return todo_dir / 'todos.json'

    def _validate_path(self, path: Path) -> None:
        """
        Validate that the path is safe and doesn't contain directory traversal.

        Args:
            path: Path to validate
        """
        # Convert to string to check for unsafe patterns
        path_str = str(path)

        # Check for directory traversal patterns
        if '..' in path.parts:
            raise ValueError("Path contains directory traversal ('..') which is not allowed")

        # Additional check for common unsafe patterns
        unsafe_patterns = ['../', '..\\', '/..', '\\..']
        for pattern in unsafe_patterns:
            if pattern in path_str:
                raise ValueError(f"Path contains unsafe pattern '{pattern}' which is not allowed")

    def validate_file_path(self, file_path: Path) -> bool:
        """
        Validate that the file path is safe and accessible.

        Args:
            file_path: Path to validate

        Returns:
            True if path is valid and accessible, False otherwise
        """
        try:
            # Check if parent directory exists and is writable
            parent_dir = file_path.parent
            parent_dir.mkdir(parents=True, exist_ok=True)

            # Check if file exists and is readable/writable, or if we can create it
            if file_path.exists():
                return os.access(file_path, os.R_OK | os.W_OK)
            else:
                # Check if we can create the file in the directory
                return os.access(parent_dir, os.W_OK)
        except (OSError, AttributeError):
            return False

    def get_default_data_file_path(self) -> Path:
        """
        Get the default path for the todo data file.

        Returns:
            Default path to the data file
        """
        home_dir = Path.home()
        todo_dir = home_dir / '.todo'
        todo_dir.mkdir(exist_ok=True)
        return todo_dir / 'todos.json'