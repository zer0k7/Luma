"""Luma document viewers package.

Provides specialized viewer widgets for various document, spreadsheet,
presentation, image, text, and archive formats.
"""

from src.viewers.archive_viewer import ArchiveViewer
from src.viewers.base import (
    FileNotFoundViewerError,
    FormatViewerError,
    LumaViewerError,
    PermissionViewerError,
    SecurityViewerError,
)
from src.viewers.docx_viewer import DocxViewer
from src.viewers.image_viewer import ImageViewer
from src.viewers.pdf_viewer import PdfViewer
from src.viewers.pptx_viewer import PptxViewer
from src.viewers.text_viewer import PlainTextViewer
from src.viewers.unsupported_viewer import UnsupportedViewer
from src.viewers.xlsx_viewer import XlsxViewer

__all__ = [
    "LumaViewerError",
    "FileNotFoundViewerError",
    "PermissionViewerError",
    "SecurityViewerError",
    "FormatViewerError",
    "PdfViewer",
    "DocxViewer",
    "PptxViewer",
    "XlsxViewer",
    "PlainTextViewer",
    "ImageViewer",
    "ArchiveViewer",
    "UnsupportedViewer",
]
