"""File-based repository for storing tasks in JSON files."""
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from core.task import Task
from core.exceptions import TaskNotFoundError
from data.config import Config
from utils.file_utils import read_json_file, write_json_file, backup_file
from data.id_generator import SequentialIDGenerator


class FileTaskRepository:
    """File-based repository for managing tasks with JSON persistence."""

    def __init__(self, config: Config, id_generator: SequentialIDGenerator):
        self.config = config
        self.id_generator = id_generator
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
        self._data_file_path = self.config.get_data_file_path()
        self._load_from_file()

    def _load_from_file(self) -> None:
        """Load tasks from the JSON file."""
        try:
            data = read_json_file(self._data_file_path)
            if data is not None:
                self._tasks = {}
                max_id = 0
                invalid_tasks = []

                for i, task_dict in enumerate(data):
                    try:
                        # Parse datetime strings
                        created_at = task_dict['created_at']
                        if isinstance(created_at, str):
                            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

                        completed_at = task_dict.get('completed_at')
                        if completed_at and isinstance(completed_at, str):
                            completed_at = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                        elif completed_at is None:
                            completed_at = None

                        task = Task(
                            id=task_dict['id'],
                            title=task_dict['title'],
                            description=task_dict.get('description'),
                            completed=task_dict.get('completed', False),
                            created_at=created_at,
                            completed_at=completed_at
                        )
                        self._tasks[task.id] = task
                        if task.id > max_id:
                            max_id = task.id
                    except (KeyError, ValueError, TypeError) as task_error:
                        invalid_tasks.append((i, task_dict, str(task_error)))
                        print(f"Warning: Skipping invalid task at index {i}: {task_error}")

                if invalid_tasks:
                    backup_file(self._data_file_path)
                    print(f"Warning: {len(invalid_tasks)} invalid tasks were skipped. Backup created.")

                # Set the next ID based on the highest ID found
                self._next_id = max_id + 1
                self.id_generator.set_next_id(self._next_id)
            else:
                # File doesn't exist, initialize empty
                self._tasks = {}
                self._next_id = 1
                self.id_generator.set_next_id(1)
        except ValueError as e:
            # If there's an error loading the file, create a backup and start fresh
            backup_file(self._data_file_path)
            print(f"Warning: Could not load tasks from file due to invalid JSON: {e}")
            print("Creating backup and starting with empty task list.")
            self._tasks = {}
            self._next_id = 1
            self.id_generator.set_next_id(1)
        except PermissionError:
            print(f"Error: Permission denied when reading file {self._data_file_path}")
            print("Please check file permissions.")
            self._tasks = {}
            self._next_id = 1
            self.id_generator.set_next_id(1)
        except OSError as e:
            print(f"Error: Could not read file {self._data_file_path}: {e}")
            self._tasks = {}
            self._next_id = 1
            self.id_generator.set_next_id(1)
        except Exception as e:
            # For other unexpected errors, start fresh
            backup_file(self._data_file_path)
            print(f"Unexpected error loading tasks from file: {e}")
            print("Creating backup and starting with empty task list.")
            self._tasks = {}
            self._next_id = 1
            self.id_generator.set_next_id(1)

    def _save_to_file(self) -> None:
        """Save tasks to the JSON file."""
        try:
            data = []
            for task in self._tasks.values():
                task_dict = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'created_at': task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at)
                }
                if task.completed_at:
                    task_dict['completed_at'] = task.completed_at.isoformat() if hasattr(task.completed_at, 'isoformat') else str(task.completed_at)
                else:
                    task_dict['completed_at'] = None
                data.append(task_dict)

            write_json_file(self._data_file_path, data)
        except PermissionError:
            raise OSError(f"Permission denied when writing to file: {self._data_file_path}")
        except OSError as e:
            # Try to create the directory if it doesn't exist
            try:
                self._data_file_path.parent.mkdir(parents=True, exist_ok=True)
                write_json_file(self._data_file_path, data)
            except:
                raise OSError(f"Could not save tasks to file: {str(e)}")
        except Exception as e:
            raise OSError(f"Could not save tasks to file: {str(e)}")

    def add_task(self, task: Task) -> Task:
        """Add a new task to the repository."""
        if task.id in self._tasks:
            raise ValueError(f"Task with ID {task.id} already exists")
        self._tasks[task.id] = task
        try:
            self._save_to_file()
        except OSError as e:
            # Remove the task if saving fails
            del self._tasks[task.id]
            raise e
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
        old_task = self._tasks[task_id]
        self._tasks[task_id] = updated_task
        try:
            self._save_to_file()
        except OSError as e:
            # Restore the old task if saving fails
            self._tasks[task_id] = old_task
            raise e
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        deleted_task = self._tasks[task_id]  # Keep a reference in case save fails
        del self._tasks[task_id]
        try:
            self._save_to_file()
        except OSError as e:
            # Restore the task if saving fails
            self._tasks[task_id] = deleted_task
            raise e
        return True

    def get_next_id(self) -> int:
        """Get the next available ID."""
        # This method might not be needed since we're using the id_generator
        # but keeping it for compatibility with the interface
        next_id = self.id_generator.get_next_id()
        if next_id >= self._next_id:
            self._next_id = next_id + 1
        return next_id