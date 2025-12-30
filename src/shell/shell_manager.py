"""Interactive shell for the todo CLI application."""
import cmd
import sys
from typing import Optional
from services.task_service import TaskService
from services.validation_service import ValidationService
from cli.output_formatter import OutputFormatter
from cli.help_system import HelpSystem
from shell.shell_completer import ShellCompleter
from shell.shell_history import ShellHistory


class ShellManager(cmd.Cmd):
    """Interactive shell manager for the todo application."""

    intro = 'Welcome to the Todo CLI shell. Type help or ? to list commands.\n'
    prompt = 'todo> '

    def __init__(self, task_service: TaskService, validation_service: ValidationService,
                 output_formatter: OutputFormatter, help_system: HelpSystem):
        super().__init__()
        self.task_service = task_service
        self.validation_service = validation_service
        self.output_formatter = output_formatter
        self.help_system = help_system
        self.completer = ShellCompleter()
        self.history = ShellHistory()

        # Setup completion and history
        self.completer.setup_completion()
        self.history.setup_history()

    def preloop(self) -> None:
        """Execute before the command loop starts."""
        # Show a summary of current tasks
        try:
            tasks = self.task_service.get_all_tasks()
            if tasks:
                print(f"Current tasks: {len(tasks)} total")
                print(self.output_formatter.format_task_list(tasks))
            else:
                print("No tasks yet. Use 'add \"task title\"' to create your first task.")
        except Exception as e:
            print(f"Error loading tasks: {e}")

    def do_add(self, arg: str) -> bool:
        """Add a new task. Usage: add \"task title\" [description]"""
        try:
            args = self._parse_args(arg)
            if not args:
                print("Error: Please provide a task title. Usage: add \"task title\" [description]")
                return False

            title = args[0]
            description = args[1] if len(args) > 1 else None

            task = self.task_service.add_task(title, description)
            print(self.output_formatter.format_task_added(task))
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"add {arg}")
        return False

    def help_add(self) -> None:
        """Help for add command."""
        print("Usage: add \"task title\" [description]")
        print("Add a new task with the given title and optional description")

    def do_list(self, arg: str) -> bool:
        """List all tasks. Usage: list"""
        try:
            tasks = self.task_service.get_all_tasks()
            print(self.output_formatter.format_task_list(tasks))
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"list {arg}".strip())
        return False

    def help_list(self) -> None:
        """Help for list command."""
        print("Usage: list")
        print("List all tasks")

    def do_update(self, arg: str) -> bool:
        """Update a task. Usage: update id [title] [description]"""
        try:
            args = self._parse_args(arg)
            if len(args) < 2:
                print("Error: Please provide task ID and at least one field to update. Usage: update id [title] [description]")
                return False

            task_id = int(args[0])
            title = args[1] if len(args) > 1 and args[1] != 'None' else None
            description = args[2] if len(args) > 2 and args[2] != 'None' else None

            self.validation_service.validate_task_id(task_id)
            updated_task = self.task_service.update_task(task_id, title, description)
            print(self.output_formatter.format_task_updated(task_id, updated_task.title))
        except ValueError:
            print(self.output_formatter.format_error("Invalid task ID. Please provide a valid number."))
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"update {arg}")
        return False

    def help_update(self) -> None:
        """Help for update command."""
        print("Usage: update id [title] [description]")
        print("Update an existing task with new title and/or description")

    def do_delete(self, arg: str) -> bool:
        """Delete a task. Usage: delete id"""
        try:
            args = self._parse_args(arg)
            if not args:
                print("Error: Please provide a task ID. Usage: delete id")
                return False

            task_id = int(args[0])
            self.validation_service.validate_task_id(task_id)
            self.task_service.delete_task(task_id)
            print(self.output_formatter.format_task_deleted(task_id))
        except ValueError:
            print(self.output_formatter.format_error("Invalid task ID. Please provide a valid number."))
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"delete {arg}")
        return False

    def help_delete(self) -> None:
        """Help for delete command."""
        print("Usage: delete id")
        print("Delete a task by its ID")

    def do_complete(self, arg: str) -> bool:
        """Mark a task as complete. Usage: complete id"""
        try:
            args = self._parse_args(arg)
            if not args:
                print("Error: Please provide a task ID. Usage: complete id")
                return False

            task_id = int(args[0])
            self.validation_service.validate_task_id(task_id)
            task = self.task_service.mark_task_complete(task_id)
            print(self.output_formatter.format_task_status_changed(task))
        except ValueError:
            print(self.output_formatter.format_error("Invalid task ID. Please provide a valid number."))
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"complete {arg}")
        return False

    def help_complete(self) -> None:
        """Help for complete command."""
        print("Usage: complete id")
        print("Mark a task as complete")

    def do_incomplete(self, arg: str) -> bool:
        """Mark a task as incomplete. Usage: incomplete id"""
        try:
            args = self._parse_args(arg)
            if not args:
                print("Error: Please provide a task ID. Usage: incomplete id")
                return False

            task_id = int(args[0])
            self.validation_service.validate_task_id(task_id)
            task = self.task_service.mark_task_incomplete(task_id)
            print(self.output_formatter.format_task_status_changed(task))
        except ValueError:
            print(self.output_formatter.format_error("Invalid task ID. Please provide a valid number."))
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"incomplete {arg}")
        return False

    def help_incomplete(self) -> None:
        """Help for incomplete command."""
        print("Usage: incomplete id")
        print("Mark a task as incomplete")

    def do_toggle(self, arg: str) -> bool:
        """Toggle task completion status. Usage: toggle id"""
        try:
            args = self._parse_args(arg)
            if not args:
                print("Error: Please provide a task ID. Usage: toggle id")
                return False

            task_id = int(args[0])
            self.validation_service.validate_task_id(task_id)
            task = self.task_service.toggle_task_status(task_id)
            print(self.output_formatter.format_task_status_changed(task))
        except ValueError:
            print(self.output_formatter.format_error("Invalid task ID. Please provide a valid number."))
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"toggle {arg}")
        return False

    def help_toggle(self) -> None:
        """Help for toggle command."""
        print("Usage: toggle id")
        print("Toggle the completion status of a task")

    def do_status(self, arg: str) -> bool:
        """Show current status summary. Usage: status"""
        try:
            tasks = self.task_service.get_all_tasks()
            total = len(tasks)
            completed = sum(1 for task in tasks if task.completed)
            pending = total - completed

            print(f"Total tasks: {total}")
            print(f"Completed: {completed}")
            print(f"Pending: {pending}")
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"status {arg}".strip())
        return False

    def help_status(self) -> None:
        """Help for status command."""
        print("Usage: status")
        print("Show current status summary")

    def do_stats(self, arg: str) -> bool:
        """Show detailed statistics. Usage: stats"""
        try:
            tasks = self.task_service.get_all_tasks()
            total = len(tasks)
            completed = sum(1 for task in tasks if task.completed)
            pending = total - completed

            print(f"Detailed Statistics:")
            print(f"  Total tasks: {total}")
            print(f"  Completed: {completed}")
            print(f"  Pending: {pending}")
            if total > 0:
                completion_rate = (completed / total) * 100
                print(f"  Completion rate: {completion_rate:.1f}%")
        except Exception as e:
            print(self.output_formatter.format_error(str(e)))
        finally:
            self.history.add_command(f"stats {arg}".strip())
        return False

    def help_stats(self) -> None:
        """Help for stats command."""
        print("Usage: stats")
        print("Show detailed statistics about tasks")

    def do_clear(self, arg: str) -> bool:
        """Clear the screen. Usage: clear"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self.history.add_command(f"clear {arg}".strip())
        return False

    def help_clear(self) -> None:
        """Help for clear command."""
        print("Usage: clear")
        print("Clear the screen")

    def do_exit(self, arg: str) -> bool:
        """Exit the shell. Usage: exit"""
        print("Goodbye!")
        self.history.add_command(f"exit {arg}".strip())
        return True

    def help_exit(self) -> None:
        """Help for exit command."""
        print("Usage: exit")
        print("Exit the shell")

    def do_quit(self, arg: str) -> bool:
        """Exit the shell. Usage: quit"""
        print("Goodbye!")
        self.history.add_command(f"quit {arg}".strip())
        return True

    def help_quit(self) -> None:
        """Help for quit command."""
        print("Usage: quit")
        print("Exit the shell")

    def do_EOF(self, arg: str) -> bool:
        """Handle Ctrl+D (EOF) to exit the shell."""
        print("\nGoodbye!")
        self.history.add_command(f"EOF {arg}".strip())
        return True

    def help_EOF(self) -> None:
        """Help for EOF (Ctrl+D) command."""
        print("Press Ctrl+D to exit the shell")

    def _parse_args(self, arg: str) -> list:
        """Parse arguments, handling quoted strings."""
        import shlex
        try:
            return shlex.split(arg)
        except ValueError:
            # If shlex fails, fall back to simple splitting
            return arg.split()

    def emptyline(self) -> bool:
        """Handle empty lines."""
        # Don't repeat the last command on empty line
        return False

    def postcmd(self, stop: bool, line: str) -> bool:
        """Hook called after a command is executed."""
        # Save history after each command
        try:
            self.history.save_history(self.load_history_from_readline())
        except:
            pass  # If saving history fails, continue
        return stop

    def load_history_from_readline(self):
        """Load history from readline."""
        try:
            import readline
            history = []
            for i in range(1, readline.get_current_history_length() + 1):
                history.append(readline.get_history_item(i))
            return [cmd for cmd in history if cmd]  # Remove empty strings
        except ImportError:
            return []