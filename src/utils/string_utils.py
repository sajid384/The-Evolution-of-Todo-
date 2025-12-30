"""String utility functions for the todo application."""


def is_empty_or_whitespace(text: str) -> bool:
    """Check if a string is empty or contains only whitespace."""
    return not text or not text.strip()


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with an optional suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in a string, trimming and collapsing multiple spaces."""
    if not text:
        return text
    return ' '.join(text.split())