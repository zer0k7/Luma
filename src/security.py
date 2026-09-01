"""Path sanitization and security validation utilities.

Ensures that all file paths opened by Luma are strictly validated against
directory traversal, symlink vulnerabilities, and permission issues.
"""

import os
from pathlib import Path
from typing import Optional, Sequence

from src.strings import ERROR_FILE_NOT_FOUND, ERROR_FILE_UNREADABLE, ERROR_PATH_TRAVERSAL
from src.viewers.base import FileNotFoundViewerError, PermissionViewerError, SecurityViewerError


def _check_allowed_directories(
    resolved_path: Path,
    raw_path: str,
    allowed_dirs: Sequence[Path],
) -> None:
    """Verify that a resolved path resides within at least one allowed directory.

    Args:
        resolved_path: The canonical Path to test.
        raw_path: The raw user-supplied path string for error reporting.
        allowed_dirs: Collection of canonical base directories.

    Raises:
        SecurityViewerError: If resolved_path does not belong to any allowed dir.
    """
    is_inside = any(resolved_path == base or base in resolved_path.parents for base in allowed_dirs)
    if not is_inside:
        error_msg = ERROR_PATH_TRAVERSAL.format(path=raw_path)
        raise SecurityViewerError(error_msg, path=raw_path)


def validate_file_path(
    raw_path: str,
    allowed_directories: Optional[Sequence[str]] = None,
) -> Path:
    """Validate and sanitize a file path before opening.

    Resolves symlinks and relative segments, verifies file existence,
    checks read permissions, and optionally enforces allowed base directories.

    Args:
        raw_path: Path string supplied by user or command line.
        allowed_directories: Optional list of directory roots to restrict access.

    Returns:
        The canonical, validated Path object.

    Raises:
        FileNotFoundViewerError: If the target file does not exist.
        PermissionViewerError: If the process does not have read access.
        SecurityViewerError: If path traversal outside allowed directories is detected.
    """
    path_obj = Path(raw_path)
    try:
        resolved = path_obj.resolve(strict=True)
    except (FileNotFoundError, RuntimeError):
        error_msg = ERROR_FILE_NOT_FOUND.format(path=raw_path)
        raise FileNotFoundViewerError(error_msg, path=raw_path)

    if not resolved.is_file():
        error_msg = ERROR_FILE_NOT_FOUND.format(path=raw_path)
        raise FileNotFoundViewerError(error_msg, path=raw_path)

    if allowed_directories is not None:
        canonical_allowed = [Path(d).resolve() for d in allowed_directories]
        _check_allowed_directories(resolved, raw_path, canonical_allowed)

    if not os.access(resolved, os.R_OK):
        error_msg = ERROR_FILE_UNREADABLE.format(path=raw_path)
        raise PermissionViewerError(error_msg, path=raw_path)

    return resolved
