"""Command history for the interactive shell."""
import os
from pathlib import Path
from typing import List


class ShellHistory:
    """Command history handler for the shell."""

    def __init__(self, history_file: str = None):
        if history_file:
            self.history_file = Path(history_file).expanduser()
        else:
            # Default to ~/.todo/history
            home_dir = Path.home()
            todo_dir = home_dir / '.todo'
            todo_dir.mkdir(exist_ok=True)
            self.history_file = todo_dir / 'history'

    def load_history(self) -> List[str]:
        """Load command history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip()]
        except Exception:
            pass  # If there's an error loading, return empty history
        return []

    def save_history(self, history: List[str]):
        """Save command history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for command in history:
                    f.write(command + '\n')
        except Exception:
            pass  # If there's an error saving, just continue

    def add_command(self, command: str):
        """Add a command to history."""
        try:
            import readline
            # Add to readline history
            readline.add_history(command)

            # Also save to our file
            history = self.load_history()
            history.append(command)
            # Keep only the last 1000 commands
            history = history[-1000:]
            self.save_history(history)
        except Exception:
            pass  # If there's an error, just continue

    def setup_history(self):
        """Setup command history."""
        try:
            import readline
            # Load existing history
            history = self.load_history()
            for command in history:
                readline.add_history(command)
        except ImportError:
            # readline is not available on all platforms
            pass