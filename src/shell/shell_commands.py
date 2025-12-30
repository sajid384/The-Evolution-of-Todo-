"""Shell-specific commands for the interactive shell."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.task_service import TaskService
    from services.validation_service import ValidationService
    from cli.output_formatter import OutputFormatter
    from cli.help_system import HelpSystem


class ShellCommands:
    """Handler for shell-specific commands."""

    def __init__(self, task_service: 'TaskService', validation_service: 'ValidationService',
                 output_formatter: 'OutputFormatter', help_system: 'HelpSystem'):
        self.task_service = task_service
        self.validation_service = validation_service
        self.output_formatter = output_formatter
        self.help_system = help_system

    def handle_status(self) -> str:
        """Handle the status command."""
        try:
            tasks = self.task_service.get_all_tasks()
            total = len(tasks)
            completed = sum(1 for task in tasks if task.completed)
            pending = total - completed

            return f"Total tasks: {total}\nCompleted: {completed}\nPending: {pending}"
        except Exception as e:
            return self.output_formatter.format_error(str(e))

    def handle_stats(self) -> str:
        """Handle the stats command."""
        try:
            tasks = self.task_service.get_all_tasks()
            total = len(tasks)
            completed = sum(1 for task in tasks if task.completed)
            pending = total - completed

            result = "Detailed Statistics:\n"
            result += f"  Total tasks: {total}\n"
            result += f"  Completed: {completed}\n"
            result += f"  Pending: {pending}\n"
            if total > 0:
                completion_rate = (completed / total) * 100
                result += f"  Completion rate: {completion_rate:.1f}%\n"
            return result
        except Exception as e:
            return self.output_formatter.format_error(str(e))