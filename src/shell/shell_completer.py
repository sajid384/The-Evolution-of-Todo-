"""Tab completion for the interactive shell."""
from typing import List


class ShellCompleter:
    """Tab completion handler for the shell."""

    def __init__(self):
        self.commands = [
            'add', 'list', 'update', 'delete', 'complete', 'incomplete', 'toggle',
            'status', 'stats', 'clear', 'help', 'exit', 'quit'
        ]

    def complete(self, text: str, state: int) -> str:
        """Complete text based on available commands."""
        import readline

        # Get all possible completions
        options = [cmd for cmd in self.commands if cmd.startswith(text)]

        if state < len(options):
            return options[state]
        else:
            return None

    def setup_completion(self):
        """Setup readline completion."""
        try:
            import readline
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")
        except ImportError:
            # readline is not available on all platforms
            pass