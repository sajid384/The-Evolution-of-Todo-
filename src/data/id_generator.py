"""ID generator service for creating unique task IDs."""
from typing import Protocol


class IDGenerator(Protocol):
    """Protocol for ID generation service."""

    def get_next_id(self) -> int:
        """Generate and return the next unique ID."""


class SequentialIDGenerator:
    """Sequential ID generator that provides unique IDs."""

    def __init__(self):
        self._current_id = 1

    def get_next_id(self) -> int:
        """Generate and return the next unique ID."""
        current_id = self._current_id
        self._current_id += 1
        return current_id

    def set_next_id(self, next_id: int) -> None:
        """Set the next ID to be generated."""
        if next_id >= self._current_id:
            self._current_id = next_id