"""Command parser for the todo CLI application."""
import argparse
import sys
from typing import List, Optional, Tuple, Union


class CommandParser:
    """Parser for CLI commands and arguments."""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser."""
        parser = argparse.ArgumentParser(
            prog='todo',
            description='In-memory todo console application',
            add_help=False
        )

        # Add help argument
        parser.add_argument(
            '-h', '--help',
            action='help',
            help='Show this help message and exit'
        )

        # Create subparsers for commands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        add_parser = subparsers.add_parser('add', aliases=['a'], help='Add a new task')
        add_parser.add_argument('title', help='Task title')
        add_parser.add_argument('description', nargs='?', default=None, help='Task description')

        # List command
        list_parser = subparsers.add_parser('list', aliases=['l', 'ls'], help='List all tasks')

        # Update command
        update_parser = subparsers.add_parser('update', aliases=['u'], help='Update a task')
        update_parser.add_argument('id', type=int, help='Task ID')
        update_parser.add_argument('title', nargs='?', default=None, help='New task title')
        update_parser.add_argument('description', nargs='?', default=None, help='New task description')

        # Delete command
        delete_parser = subparsers.add_parser('delete', aliases=['d'], help='Delete a task')
        delete_parser.add_argument('id', type=int, help='Task ID')

        # Complete command
        complete_parser = subparsers.add_parser('complete', aliases=['c'], help='Mark task as complete')
        complete_parser.add_argument('id', type=int, help='Task ID')

        # Incomplete command
        incomplete_parser = subparsers.add_parser('incomplete', aliases=['i'], help='Mark task as incomplete')
        incomplete_parser.add_argument('id', type=int, help='Task ID')

        # Toggle command
        toggle_parser = subparsers.add_parser('toggle', aliases=['t'], help='Toggle task completion status')
        toggle_parser.add_argument('id', type=int, help='Task ID')

        # Help command
        subparsers.add_parser('help', help='Show help information')

        # Shell command
        shell_parser = subparsers.add_parser('shell', aliases=['sh'], help='Start interactive shell mode')

        return parser

    def parse(self, args: List[str]) -> argparse.Namespace:
        """Parse command line arguments."""
        if not args:
            self.parser.print_help()
            sys.exit(2)

        # Handle the 'help' command specially
        if len(args) >= 1 and args[0] in ['help', '--help', '-h']:
            self.parser.print_help()
            sys.exit(0)

        # Handle aliases by expanding them
        if len(args) >= 1:
            command_map = {
                'a': 'add',
                'l': 'list',
                'ls': 'list',
                'u': 'update',
                'd': 'delete',
                'c': 'complete',
                'i': 'incomplete',
                't': 'toggle'
            }
            if args[0] in command_map:
                args = [command_map[args[0]]] + args[1:]

        try:
            return self.parser.parse_args(args)
        except SystemExit:
            # argparse calls sys.exit on error, we want to handle it gracefully
            raise ValueError("Invalid command or arguments")