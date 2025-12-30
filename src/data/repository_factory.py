"""Repository factory for creating repository instances."""
from typing import Optional
from data.repository import TaskRepository
from data.file_repository import FileTaskRepository
from data.config import Config
from data.id_generator import SequentialIDGenerator


class RepositoryFactory:
    """Factory for creating repository instances."""

    @staticmethod
    def create_repository(repository_type: str = "file", config: Optional[Config] = None, id_generator: Optional[SequentialIDGenerator] = None):
        """
        Create a repository instance based on the specified type.

        Args:
            repository_type: Type of repository ("in_memory" or "file")
            config: Configuration object for file repository
            id_generator: ID generator instance

        Returns:
            Repository instance
        """
        if id_generator is None:
            id_generator = SequentialIDGenerator()

        if repository_type == "in_memory":
            return TaskRepository()
        elif repository_type == "file":
            if config is None:
                # Create default config if none provided
                from data.config import Config
                config = Config()
            return FileTaskRepository(config, id_generator)
        else:
            raise ValueError(f"Unknown repository type: {repository_type}")