"""Unit tests for viewer dispatch logic and widget selection."""

import zipfile
from pathlib import Path

from src.viewer_dispatch import _detect_mime_type, open_file
from src.viewers.archive_viewer import ArchiveViewer
from src.viewers.docx_viewer import DocxViewer
from src.viewers.image_viewer import ImageViewer
from src.viewers.pdf_viewer import PdfViewer
from src.viewers.pptx_viewer import PptxViewer
from src.viewers.text_viewer import PlainTextViewer
from src.viewers.unsupported_viewer import UnsupportedViewer
from src.viewers.xlsx_viewer import XlsxViewer


def test_detect_mime_type(tmp_path: Path) -> None:
    """Verify MIME detection for known document extensions."""
    pdf_file = tmp_path / "doc.pdf"
    pdf_file.write_bytes(b"%PDF-1.4\n")
    assert _detect_mime_type(pdf_file) == "application/pdf"

    txt_file = tmp_path / "notes.txt"
    txt_file.write_text("plain text", encoding="utf-8")
    assert "text" in _detect_mime_type(txt_file)


def test_dispatch_pdf(tmp_path: Path) -> None:
    """Verify PDF file instantiates PdfViewer."""
    file = tmp_path / "sample.pdf"
    file.write_bytes(b"%PDF-1.4\n%EOF")
    widget = open_file(str(file))
    assert isinstance(widget, PdfViewer)


def test_dispatch_text(tmp_path: Path) -> None:
    """Verify text file instantiates PlainTextViewer."""
    file = tmp_path / "document.txt"
    file.write_text("Hello Luma", encoding="utf-8")
    widget = open_file(str(file))
    assert isinstance(widget, PlainTextViewer)


def test_dispatch_image(tmp_path: Path) -> None:
    """Verify PNG image file instantiates ImageViewer."""
    file = tmp_path / "photo.png"
    file.write_bytes(b"\x89PNG\r\n\x1a\n")
    widget = open_file(str(file))
    assert isinstance(widget, ImageViewer)


def test_dispatch_archive(tmp_path: Path) -> None:
    """Verify ZIP file instantiates ArchiveViewer."""
    file = tmp_path / "archive.zip"
    with zipfile.ZipFile(file, "w") as zf:
        zf.writestr("test.txt", "data")
    widget = open_file(str(file))
    assert isinstance(widget, ArchiveViewer)


def test_dispatch_docx(tmp_path: Path) -> None:
    """Verify DOCX extension is detected as the correct Office MIME type."""
    file = tmp_path / "document.docx"
    file.write_bytes(b"dummy docx")
    mime = _detect_mime_type(file)
    assert "officedocument.wordprocessingml" in mime or "msword" in mime


def test_dispatch_pptx(tmp_path: Path) -> None:
    """Verify PPTX extension is detected as the correct Office MIME type."""
    file = tmp_path / "slides.pptx"
    file.write_bytes(b"dummy pptx")
    mime = _detect_mime_type(file)
    assert "officedocument.presentationml" in mime or "powerpoint" in mime


def test_dispatch_xlsx(tmp_path: Path) -> None:
    """Verify XLSX extension is detected as the correct Office MIME type."""
    file = tmp_path / "sheet.xlsx"
    file.write_bytes(b"dummy xlsx")
    mime = _detect_mime_type(file)
    assert "officedocument.spreadsheetml" in mime or "excel" in mime


def test_dispatch_unsupported(tmp_path: Path) -> None:
    """Verify unknown binary file instantiates UnsupportedViewer."""
    file = tmp_path / "mystery.bin"
    file.write_bytes(b"\x00\x01\x02\x03\xff\xfe")
    widget = open_file(str(file))
    assert isinstance(widget, UnsupportedViewer)
