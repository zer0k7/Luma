"""Unit tests for path validation and security controls."""

from pathlib import Path
from unittest.mock import patch

import pytest

from src.security import validate_file_path
from src.viewers.base import (
    FileNotFoundViewerError,
    PermissionViewerError,
    SecurityViewerError,
)


def test_validate_existing_file(tmp_path: Path) -> None:
    """Verify valid file path resolves successfully."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello world", encoding="utf-8")

    resolved = validate_file_path(str(test_file))
    assert resolved.is_file()
    assert resolved == test_file.resolve()


def test_validate_nonexistent_file(tmp_path: Path) -> None:
    """Verify nonexistent file raises FileNotFoundViewerError."""
    fake_path = tmp_path / "does_not_exist.txt"
    with pytest.raises(FileNotFoundViewerError) as exc_info:
        validate_file_path(str(fake_path))

    assert "could not be found" in str(exc_info.value)


def test_validate_directory_path(tmp_path: Path) -> None:
    """Verify attempting to open a directory raises FileNotFoundViewerError."""
    with pytest.raises(FileNotFoundViewerError):
        validate_file_path(str(tmp_path))


def test_validate_path_traversal_restricted(tmp_path: Path) -> None:
    """Verify path outside allowed directories raises SecurityViewerError."""
    allowed_dir = tmp_path / "allowed"
    allowed_dir.mkdir()
    secret_dir = tmp_path / "secret"
    secret_dir.mkdir()

    secret_file = secret_dir / "confidential.txt"
    secret_file.write_text("classified", encoding="utf-8")

    with pytest.raises(SecurityViewerError) as exc_info:
        validate_file_path(str(secret_file), allowed_directories=[str(allowed_dir)])

    assert "Access denied" in str(exc_info.value)


def test_validate_permission_denied(tmp_path: Path) -> None:
    """Verify unreadable file raises PermissionViewerError."""
    test_file = tmp_path / "unreadable.txt"
    test_file.write_text("protected", encoding="utf-8")

    with patch("os.access", return_value=False):
        with pytest.raises(PermissionViewerError) as exc_info:
            validate_file_path(str(test_file))
        assert "does not have permission" in str(exc_info.value)
