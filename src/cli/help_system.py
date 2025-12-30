"""Help system for the todo CLI application."""
from typing import Dict


class HelpSystem:
    """System for providing help information about commands."""

    def __init__(self):
        self._help_texts = self._initialize_help_texts()

    def _initialize_help_texts(self) -> Dict[str, str]:
        """Initialize help texts for all commands."""
        return {
            'add': """Add Command Help:
Usage: todo add <title> [description]
       todo a <title> [description]

Add a new task with the given title and optional description.

Examples:
  todo add "Buy groceries" "Milk, bread, eggs"
  todo a "Complete project" """,
            'list': """List Command Help:
Usage: todo list
       todo l
       todo ls

Display all tasks with their ID, title, description, and status.

Example:
  todo list""",
            'update': """Update Command Help:
Usage: todo update <id> [title] [description]
       todo u <id> [title] [description]

Update an existing task with new title and/or description.

Examples:
  todo update 1 "New title"
  todo u 2 "New title" "New description"
  todo update 2 "" "New description"  # Empty string keeps title unchanged""",
            'delete': """Delete Command Help:
Usage: todo delete <id>
       todo d <id>

Delete a task by its ID.

Example:
  todo delete 1""",
            'complete': """Complete Command Help:
Usage: todo complete <id>
       todo c <id>

Mark a task as complete.

Example:
  todo complete 1""",
            'incomplete': """Incomplete Command Help:
Usage: todo incomplete <id>
       todo i <id>

Mark a task as incomplete.

Example:
  todo incomplete 1""",
            'toggle': """Toggle Command Help:
Usage: todo toggle <id>
       todo t <id>

Toggle the completion status of a task.

Example:
  todo toggle 1""",
            'shell': """Shell Command Help:
Usage: todo shell

Start an interactive shell mode for continuous task management.
In shell mode, you can run commands without the 'todo' prefix.
Available shell commands include: add, list, update, delete,
complete, incomplete, toggle, status, stats, clear, help, exit, quit.

Examples:
  todo shell
  > add "Buy groceries" "Milk, bread, eggs"
  > list
  > complete 1
  > exit""",
            'general': """Todo CLI Application Help

Usage: todo [command] [arguments]

Commands:
  add, a [title] [description]     Add a new task
  list, l, ls                     List all tasks
  update, u [id] [title] [desc]   Update a task
  delete, d [id]                  Delete a task
  complete, c [id]                Mark task as complete
  incomplete, i [id]              Mark task as incomplete
  toggle, t [id]                  Toggle task completion status
  shell                           Start interactive shell mode
  help, -h, --help               Show this help message

Examples:
  todo add "Buy groceries" "Milk, bread, eggs"
  todo list
  todo shell
  todo complete 1
  todo delete 2"""
        }

    def get_help_text(self, command: str = None) -> str:
        """Get help text for a specific command or general help."""
        if command and command in self._help_texts:
            return self._help_texts[command]
        return self._help_texts['general']