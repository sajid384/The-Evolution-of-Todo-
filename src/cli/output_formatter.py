"""Output formatter for displaying tasks and messages."""
from typing import List
from core.task import Task


class OutputFormatter:
    """Formatter for displaying tasks and messages in a readable format."""

    @staticmethod
    def format_task_list(tasks: List[Task]) -> str:
        """Format a list of tasks in a tabular format."""
        if not tasks:
            return "No tasks found."

        # Create header
        header = f"{'ID':<4} | {'Title':<20} | {'Description':<30} | {'Status':<15}"
        separator = "-" * len(header)

        # Format each task
        task_lines = []
        for task in tasks:
            description = task.description or ""
            # Truncate long titles and descriptions for display
            title = (task.title[:17] + "...") if len(task.title) > 20 else task.title
            desc = (description[:27] + "...") if len(description) > 30 else description
            line = f"{task.id:<4} | {title:<20} | {desc:<30} | {task.status_display:<15}"
            task_lines.append(line)

        return "\n".join([header, separator] + task_lines)

    @staticmethod
    def format_task_added(task: Task) -> str:
        """Format a success message for a newly added task."""
        return f"Task added successfully with ID {task.id}: {task.title}"

    @staticmethod
    def format_task_updated(task_id: int, title: str) -> str:
        """Format a success message for an updated task."""
        return f"Task {task_id} updated successfully: {title}"

    @staticmethod
    def format_task_deleted(task_id: int) -> str:
        """Format a success message for a deleted task."""
        return f"Task {task_id} deleted successfully"

    @staticmethod
    def format_task_status_changed(task: Task) -> str:
        """Format a success message for a task status change."""
        status = "completed" if task.completed else "marked incomplete"
        return f"Task {task.id} {status}: {task.title}"

    @staticmethod
    def format_error(message: str) -> str:
        """Format an error message."""
        return f"Error: {message}"

    @staticmethod
    def format_help() -> str:
        """Format help information."""
        help_text = """
Todo CLI Application

Usage: todo [command] [arguments]

Commands:
  add, a [title] [description]     Add a new task
  list, l, ls                     List all tasks
  update, u [id] [title] [desc]   Update a task
  delete, d [id]                  Delete a task
  complete, c [id]                Mark task as complete
  incomplete, i [id]              Mark task as incomplete
  toggle, t [id]                  Toggle task completion status
  help, -h, --help               Show this help message

Examples:
  todo add "Buy groceries" "Milk, bread, eggs"
  todo list
  todo update 1 "Updated title" "Updated description"
  todo complete 1
  todo delete 2
        """
        return help_text.strip()