"""Unit tests for version reading and formatting."""

import re
from pathlib import Path

from src import VERSION_FILE_PATH, get_version


def test_version_file_exists() -> None:
    """Verify that VERSION file exists at the repository root."""
    assert VERSION_FILE_PATH.is_file()


def test_version_format() -> None:
    """Verify that the version string strictly adheres to semantic versioning."""
    version = get_version()
    assert version != ""
    pattern = r"^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$"
    assert re.match(pattern, version) is not None
