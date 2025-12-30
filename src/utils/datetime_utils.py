"""DateTime utility functions for the todo application."""
from datetime import datetime


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as a string."""
    return dt.strftime(format_str)


def format_iso_datetime(dt: datetime) -> str:
    """Format a datetime object as ISO format string."""
    return dt.isoformat()


def get_current_datetime() -> datetime:
    """Get the current datetime."""
    return datetime.now()