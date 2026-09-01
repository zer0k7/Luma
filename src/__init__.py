"""Luma document viewer package.

Provides a polished, minimal desktop document viewer for Linux desktops.
"""

from pathlib import Path

VERSION_FILE_PATH = Path(__file__).resolve().parent.parent / "VERSION"


def get_version() -> str:
    """Read the application version from the VERSION file.

    Returns:
        The stripped semantic version string.
    """
    if VERSION_FILE_PATH.is_file():
        with open(VERSION_FILE_PATH, "r", encoding="utf-8") as file_handle:
            return file_handle.read().strip()
    return "0.1.0"


__version__ = get_version()
__all__ = ["__version__", "get_version"]
