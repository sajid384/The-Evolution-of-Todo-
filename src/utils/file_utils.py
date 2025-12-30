"""File utilities for JSON operations and file management."""
import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional
from core.task import Task


class FileLock:
    """Simple file locking mechanism to prevent concurrent access issues."""

    def __init__(self):
        self._locks = {}
        self._global_lock = threading.Lock()

    def acquire(self, file_path: Path) -> bool:
        """Acquire a lock for the specified file."""
        with self._global_lock:
            if file_path not in self._locks:
                self._locks[file_path] = threading.Lock()
            return self._locks[file_path].acquire(blocking=False)

    def release(self, file_path: Path) -> None:
        """Release the lock for the specified file."""
        with self._global_lock:
            if file_path in self._locks:
                self._locks[file_path].release()


# Global file lock instance
_file_lock = FileLock()


def read_json_file(file_path: Path) -> Optional[List[Dict[str, Any]]]:
    """
    Safely read JSON data from a file.

    Args:
        file_path: Path to the JSON file

    Returns:
        List of task dictionaries or None if file doesn't exist
    """
    # Acquire file lock
    if not _file_lock.acquire(file_path):
        raise OSError(f"Could not acquire lock for file: {file_path}")

    try:
        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {file_path}: {str(e)}")
    except Exception as e:
        raise OSError(f"Error reading file {file_path}: {str(e)}")
    finally:
        _file_lock.release(file_path)


def write_json_file(file_path: Path, data: List[Dict[str, Any]]) -> None:
    """
    Safely write JSON data to a file.

    Args:
        file_path: Path to the JSON file
        data: List of task dictionaries to write
    """
    # Acquire file lock
    if not _file_lock.acquire(file_path):
        raise OSError(f"Could not acquire lock for file: {file_path}")

    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to a temporary file first, then rename to avoid corruption
        temp_file = file_path.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        # Atomic rename to prevent corruption
        temp_file.replace(file_path)

        # Set appropriate file permissions (read/write for owner only)
        os.chmod(file_path, 0o600)

        # Also set secure permissions on the parent directory
        os.chmod(file_path.parent, 0o700)
    except PermissionError:
        raise OSError(f"Permission denied when writing to file: {file_path}")
    except Exception as e:
        raise OSError(f"Error writing to file {file_path}: {str(e)}")
    finally:
        # Release the lock even if temp file rename failed
        try:
            _file_lock.release(file_path)
        except:
            pass  # Lock might not be held


def validate_file_permissions(file_path: Path) -> bool:
    """
    Validate that the file has appropriate permissions (owner-only access).

    Args:
        file_path: Path to validate

    Returns:
        True if permissions are appropriate, False otherwise
    """
    if not file_path.exists():
        return True  # File doesn't exist, permissions will be set on creation

    stat = file_path.stat()
    # Check if file permissions are 600 (owner read/write only)
    return (stat.st_mode & 0o777) == 0o600


def backup_file(file_path: Path) -> Optional[Path]:
    """
    Create a backup of the specified file.

    Args:
        file_path: Path to the file to backup

    Returns:
        Path to the backup file or None if backup failed
    """
    if not file_path.exists():
        return None

    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception:
        return None