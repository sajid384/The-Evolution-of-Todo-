"""In-memory repository for storing tasks."""
from typing import Dict, List, Optional
from core.task import Task
from core.exceptions import TaskNotFoundError


class TaskRepository:
    """In-memory repository for managing tasks."""

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, task: Task) -> Task:
        """Add a new task to the repository."""
        if task.id in self._tasks:
            raise ValueError(f"Task with ID {task.id} already exists")
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: int) -> Task:
        """Get a task by its ID."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self._tasks.values())

    def update_task(self, task_id: int, updated_task: Task) -> Task:
        """Update an existing task."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]
        return True

    def get_next_id(self) -> int:
        """Get the next available ID and increment the counter."""
        current_id = self._next_id
        self._next_id += 1
        return current_id