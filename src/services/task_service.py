"""Task service for handling business logic operations."""
from datetime import datetime
from typing import List, Optional
from core.task import Task
from core.exceptions import TaskNotFoundError, InvalidTaskError
from data.repository import TaskRepository
from data.id_generator import SequentialIDGenerator


class TaskService:
    """Service for managing tasks with business logic."""

    def __init__(self, repository: TaskRepository, id_generator: SequentialIDGenerator):
        self.repository = repository
        self.id_generator = id_generator

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with the given title and optional description."""
        # Validate title
        if not title or not title.strip():
            raise InvalidTaskError("Task title cannot be empty")

        # Generate unique ID
        task_id = self.id_generator.get_next_id()

        # Create and store the task
        task = Task(
            id=task_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False,
            created_at=datetime.now()
        )

        return self.repository.add_task(task)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.repository.get_all_tasks()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """Update an existing task with new title and/or description."""
        # Get the existing task
        existing_task = self.repository.get_task(task_id)

        # Use existing values if not provided
        new_title = title.strip() if title is not None else existing_task.title
        new_description = description.strip() if description is not None else existing_task.description

        # Validate title
        if not new_title or not new_title.strip():
            raise InvalidTaskError("Task title cannot be empty")

        # Create updated task
        updated_task = Task(
            id=existing_task.id,
            title=new_title,
            description=new_description,
            completed=existing_task.completed,
            created_at=existing_task.created_at
        )

        return self.repository.update_task(task_id, updated_task)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        return self.repository.delete_task(task_id)

    def mark_task_complete(self, task_id: int) -> Task:
        """Mark a task as complete."""
        from datetime import datetime
        existing_task = self.repository.get_task(task_id)
        updated_task = Task(
            id=existing_task.id,
            title=existing_task.title,
            description=existing_task.description,
            completed=True,
            created_at=existing_task.created_at,
            completed_at=datetime.now()
        )
        return self.repository.update_task(task_id, updated_task)

    def mark_task_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete."""
        existing_task = self.repository.get_task(task_id)
        updated_task = Task(
            id=existing_task.id,
            title=existing_task.title,
            description=existing_task.description,
            completed=False,
            created_at=existing_task.created_at,
            completed_at=None
        )
        return self.repository.update_task(task_id, updated_task)

    def toggle_task_status(self, task_id: int) -> Task:
        """Toggle the completion status of a task."""
        from datetime import datetime
        existing_task = self.repository.get_task(task_id)
        new_status = not existing_task.completed
        completed_at = datetime.now() if new_status else None
        updated_task = Task(
            id=existing_task.id,
            title=existing_task.title,
            description=existing_task.description,
            completed=new_status,
            created_at=existing_task.created_at,
            completed_at=completed_at
        )
        return self.repository.update_task(task_id, updated_task)