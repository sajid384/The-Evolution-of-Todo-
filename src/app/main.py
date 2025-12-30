"""Main application entry point for the todo CLI application."""
import sys
from typing import List, Optional
from core.task import Task
from core.exceptions import TaskNotFoundError, InvalidTaskError
from data.repository_factory import RepositoryFactory
from data.config import Config
from data.id_generator import SequentialIDGenerator
from services.task_service import TaskService
from services.validation_service import ValidationService
from services.config_service import ConfigService
from cli.command_parser import CommandParser
from cli.output_formatter import OutputFormatter
from cli.help_system import HelpSystem


class TodoApp:
    """Main application class that orchestrates the todo CLI application."""

    def __init__(self, data_file: Optional[str] = None):
        # Initialize configuration
        self.config_service = ConfigService(data_file)
        self.config = self.config_service.config

        # Initialize data layer with file repository by default
        self.id_generator = SequentialIDGenerator()
        self.repository = RepositoryFactory.create_repository("file", self.config, self.id_generator)

        # Initialize services
        self.task_service = TaskService(self.repository, self.id_generator)
        self.validation_service = ValidationService()

        # Initialize CLI components
        self.command_parser = CommandParser()
        self.output_formatter = OutputFormatter()
        self.help_system = HelpSystem()

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the application with the given arguments."""
        try:
            if args is None:
                args = sys.argv[1:]

            # Parse the command
            parsed_args = self.command_parser.parse(args)

            # Execute the command
            result = self.execute_command(parsed_args)

            # Print the result if there is one
            if result:
                print(result)

            return 0

        except TaskNotFoundError as e:
            print(self.output_formatter.format_error(str(e)), file=sys.stderr)
            return 1
        except InvalidTaskError as e:
            print(self.output_formatter.format_error(str(e)), file=sys.stderr)
            return 1
        except ValueError as e:
            print(self.output_formatter.format_error(str(e)), file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.", file=sys.stderr)
            return 1
        except Exception as e:
            print(self.output_formatter.format_error(f"An unexpected error occurred: {str(e)}"), file=sys.stderr)
            return 1

    def execute_command(self, args) -> Optional[str]:
        """Execute the parsed command."""
        command = args.command

        if command == 'add':
            return self.handle_add(args)
        elif command == 'list':
            return self.handle_list()
        elif command == 'update':
            return self.handle_update(args)
        elif command == 'delete':
            return self.handle_delete(args)
        elif command in ['complete', 'c']:
            return self.handle_complete(args)
        elif command in ['incomplete', 'i']:
            return self.handle_incomplete(args)
        elif command in ['toggle', 't']:
            return self.handle_toggle(args)
        elif command == 'help':
            return self.help_system.get_help_text()
        elif command in ['shell', 'sh']:
            from shell.shell_manager import ShellManager
            shell = ShellManager(self.task_service, self.validation_service, self.output_formatter, self.help_system)
            shell.cmdloop()
            # Return a special indicator that the shell was run
            # This will be handled in the run method to exit properly
            sys.exit(0)
        else:
            return self.output_formatter.format_error(f"Unknown command: {command}. Use 'todo help' for available commands.")

    def handle_add(self, args) -> str:
        """Handle the add command."""
        task = self.task_service.add_task(args.title, args.description)
        return self.output_formatter.format_task_added(task)

    def handle_list(self) -> str:
        """Handle the list command."""
        tasks = self.task_service.get_all_tasks()
        return self.output_formatter.format_task_list(tasks)

    def handle_update(self, args) -> str:
        """Handle the update command."""
        # Validate task ID
        self.validation_service.validate_task_id(args.id)

        # Update the task
        updated_task = self.task_service.update_task(args.id, args.title, args.description)
        return self.output_formatter.format_task_updated(args.id, updated_task.title)

    def handle_delete(self, args) -> str:
        """Handle the delete command."""
        # Validate task ID
        self.validation_service.validate_task_id(args.id)

        # Delete the task
        self.task_service.delete_task(args.id)
        return self.output_formatter.format_task_deleted(args.id)

    def handle_complete(self, args) -> str:
        """Handle the complete command."""
        # Validate task ID
        self.validation_service.validate_task_id(args.id)

        # Mark task as complete
        task = self.task_service.mark_task_complete(args.id)
        return self.output_formatter.format_task_status_changed(task)

    def handle_incomplete(self, args) -> str:
        """Handle the incomplete command."""
        # Validate task ID
        self.validation_service.validate_task_id(args.id)

        # Mark task as incomplete
        task = self.task_service.mark_task_incomplete(args.id)
        return self.output_formatter.format_task_status_changed(task)

    def handle_toggle(self, args) -> str:
        """Handle the toggle command."""
        # Validate task ID
        self.validation_service.validate_task_id(args.id)

        # Toggle task status
        task = self.task_service.toggle_task_status(args.id)
        return self.output_formatter.format_task_status_changed(task)


def main():
    """Main entry point for the application."""
    import sys

    # Check if --data-file is in the command line arguments
    data_file = None
    args_to_pass = []

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--data-file' and i + 1 < len(sys.argv):
            data_file = sys.argv[i + 1]
            i += 2  # Skip both --data-file and its value
        else:
            args_to_pass.append(sys.argv[i])
            i += 1

    # Create app with custom data file if specified
    app = TodoApp(data_file=data_file)
    exit_code = app.run(args_to_pass)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()