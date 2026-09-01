"""File viewer dispatcher for Luma.

Inspects document paths and MIME types to instantiate and return the
appropriate viewer widget.
"""

import mimetypes
from pathlib import Path
from typing import Optional

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore # noqa: E402

try:
    import magic  # type: ignore # noqa: E402
except (ImportError, AttributeError):
    magic = None  # type: ignore[assignment]

from src.security import validate_file_path  # noqa: E402
from src.viewers.archive_viewer import ArchiveViewer  # noqa: E402
from src.viewers.docx_viewer import DocxViewer  # noqa: E402
from src.viewers.image_viewer import ImageViewer  # noqa: E402
from src.viewers.pdf_viewer import PdfViewer  # noqa: E402
from src.viewers.pptx_viewer import PptxViewer  # noqa: E402
from src.viewers.text_viewer import PlainTextViewer  # noqa: E402
from src.viewers.unsupported_viewer import UnsupportedViewer  # noqa: E402
from src.viewers.xlsx_viewer import XlsxViewer  # noqa: E402

# Ensure standard office and web mimetypes are registered
mimetypes.add_type(
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".docx",
)
mimetypes.add_type(
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".pptx",
)
mimetypes.add_type(
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xlsx",
)
mimetypes.add_type("text/markdown", ".md")
mimetypes.add_type("text/x-rst", ".rst")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("image/webp", ".webp")

ARCHIVE_MIME_TYPES = {
    "application/zip",
    "application/x-zip-compressed",
    "application/x-tar",
    "application/tar",
    "application/gzip",
    "application/x-gzip",
    "application/x-bzip2",
    "application/x-xz",
}


def _detect_mime_type(file_path: Path) -> str:
    """Detect MIME type using file extension and libmagic inspection.

    Args:
        file_path: Validated Path to file.

    Returns:
        MIME type string (e.g. 'application/pdf').
    """
    guessed_type, _ = mimetypes.guess_type(str(file_path))

    magic_type: Optional[str] = None
    if magic is not None and hasattr(magic, "from_file"):
        try:
            magic_type = magic.from_file(str(file_path), mime=True)
        except Exception:
            magic_type = None

    # Prefer specific OpenXML MIME types over generic application/zip from magic
    if guessed_type and "openxmlformats" in guessed_type:
        return guessed_type

    if magic_type and magic_type != "application/octet-stream":
        return magic_type

    return guessed_type or magic_type or "application/octet-stream"


def _select_widget(resolved_path: Path, mime_type: str) -> Gtk.Widget:
    """Select the viewer widget matching the detected MIME type.

    Args:
        resolved_path: Canonical path to target file.
        mime_type: Detected MIME type.

    Returns:
        Instantiated Gtk.Widget.
    """
    path_str = str(resolved_path)

    if mime_type == "application/pdf":
        return PdfViewer(path_str)

    docx_mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    if mime_type == docx_mime or resolved_path.suffix.lower() == ".docx":
        return DocxViewer(path_str)

    pptx_mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    if mime_type == pptx_mime or resolved_path.suffix.lower() == ".pptx":
        return PptxViewer(path_str)

    xlsx_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if mime_type == xlsx_mime or resolved_path.suffix.lower() == ".xlsx":
        return XlsxViewer(path_str)

    if mime_type.startswith("text/") or resolved_path.suffix.lower() in {
        ".txt",
        ".md",
        ".rst",
        ".log",
        ".csv",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".ini",
        ".conf",
    }:
        return PlainTextViewer(path_str)

    if mime_type.startswith("image/"):
        return ImageViewer(path_str)

    if mime_type in ARCHIVE_MIME_TYPES or resolved_path.suffix.lower() in {
        ".zip",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".tgz",
    }:
        return ArchiveViewer(path_str)

    return UnsupportedViewer(path_str, mime_type)


def open_file(path: str) -> Gtk.Widget:
    """Validate a document path, identify its format, and instantiate the viewer widget.

    Args:
        path: Path to target file.

    Returns:
        A Gtk.Widget tailored to viewing the file.

    Raises:
        LumaViewerError: If the file is missing, unreadable, or cannot be accessed safely.
    """
    resolved_path = validate_file_path(path)
    mime_type = _detect_mime_type(resolved_path)
    return _select_widget(resolved_path, mime_type)
