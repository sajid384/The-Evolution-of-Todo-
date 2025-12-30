"""Configuration service for managing file location and settings."""
from typing import Optional
from data.config import Config


class ConfigService:
    """Service for managing application configuration."""

    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize configuration service.

        Args:
            data_file: Optional custom path for the todo data file
        """
        self.config = Config(data_file)

    def get_data_file_path(self):
        """Get the path for the data file."""
        return self.config.get_data_file_path()

    def validate_file_path(self, file_path):
        """Validate that the file path is safe and accessible."""
        return self.config.validate_file_path(file_path)

    def get_default_data_file_path(self):
        """Get the default path for the data file."""
        return self.config.get_default_data_file_path()