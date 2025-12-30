from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a todo task with title, description, and completion status."""

    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

    @property
    def status_display(self) -> str:
        """Return a display string for the task status."""
        return "✅ Complete" if self.completed else "❌ Incomplete"

    @property
    def status_emoji(self) -> str:
        """Return an emoji for the task status."""
        return "✅" if self.completed else "❌"