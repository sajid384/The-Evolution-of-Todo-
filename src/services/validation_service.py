"""Validation service for input and business rule validation."""
from typing import Optional
from core.exceptions import InvalidTaskError


class ValidationService:
    """Service for validating inputs and business rules."""

    @staticmethod
    def validate_task_title(title: Optional[str]) -> None:
        """Validate that a task title is not empty."""
        if not title or not title.strip():
            raise InvalidTaskError("Task title cannot be empty")

    @staticmethod
    def validate_task_id(task_id: int) -> None:
        """Validate that a task ID is a positive integer."""
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskError(f"Task ID must be a positive integer, got: {task_id}")

    @staticmethod
    def validate_optional_string(value: Optional[str], field_name: str) -> None:
        """Validate an optional string field."""
        if value is not None and not isinstance(value, str):
            raise InvalidTaskError(f"{field_name} must be a string if provided")