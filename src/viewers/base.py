"""Base viewer interfaces and typed exception classes for Luma.

Provides standard exceptions and base classes used across all file viewers.
"""

from typing import Optional


class LumaViewerError(Exception):
    """Base exception for all Luma viewer errors.

    Attributes:
        message: Actionable human-readable error description for the user.
        path: Path to the problematic file, if applicable.
    """

    def __init__(self, message: str, path: Optional[str] = None) -> None:
        """Initialize LumaViewerError.

        Args:
            message: Action-oriented error message explaining the issue and resolution.
            path: Target file path, if known.
        """
        super().__init__(message)
        self.message = message
        self.path = path


class FileNotFoundViewerError(LumaViewerError):
    """Raised when a requested document does not exist."""


class PermissionViewerError(LumaViewerError):
    """Raised when the process lacks permission to open or read the file."""


class SecurityViewerError(LumaViewerError):
    """Raised when a path traversal, symlink loop, or unsafe path is detected."""


class FormatViewerError(LumaViewerError):
    """Raised when a file cannot be parsed or decoded by the expected viewer."""
