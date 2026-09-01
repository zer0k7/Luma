"""Unit tests for individual viewer components."""

from pathlib import Path
import tarfile
import zipfile

import pytest

from src.viewers.archive_viewer import ArchiveViewer
from src.viewers.base import FormatViewerError
from src.viewers.docx_viewer import DocxViewer
from src.viewers.pdf_viewer import PdfViewer
from src.viewers.text_viewer import PlainTextViewer
from src.viewers.unsupported_viewer import UnsupportedViewer
from src.viewers.xlsx_viewer import XlsxViewer


def test_plain_text_viewer(tmp_path: Path) -> None:
    """Verify PlainTextViewer correctly loads text into buffer."""
    test_file = tmp_path / "hello.txt"
    test_file.write_text("Line 1\nLine 2", encoding="utf-8")

    viewer = PlainTextViewer(str(test_file))
    assert viewer.text_view is not None


def test_archive_viewer_zip(tmp_path: Path) -> None:
    """Verify ArchiveViewer reads member entries from a zip archive."""
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("test1.txt", "content 1")
        zf.writestr("test2.txt", "longer content 2")

    viewer = ArchiveViewer(str(zip_path))
    assert len(viewer.entries) == 2
    assert viewer.entries[0][0] == "test1.txt"


def test_archive_viewer_tar(tmp_path: Path) -> None:
    """Verify ArchiveViewer reads member entries from a tar archive."""
    tar_path = tmp_path / "test.tar"
    file_to_tar = tmp_path / "member.txt"
    file_to_tar.write_text("tarred content", encoding="utf-8")

    with tarfile.open(tar_path, "w") as tf:
        tf.add(file_to_tar, arcname="member.txt")

    viewer = ArchiveViewer(str(tar_path))
    assert len(viewer.entries) == 1
    assert viewer.entries[0][0] == "member.txt"


def test_unsupported_viewer_hex_dump(tmp_path: Path) -> None:
    """Verify UnsupportedViewer generates structured hex dump."""
    bin_file = tmp_path / "raw.dat"
    bin_file.write_bytes(b"LUMA_BINARY_HEADER\x00\x01\x02\x03")

    viewer = UnsupportedViewer(str(bin_file), "application/octet-stream")
    hex_output = viewer._generate_hex_dump(max_bytes=32)
    assert "00000000" in hex_output
    assert "LUMA" in hex_output


def test_pdf_viewer_controls(tmp_path: Path) -> None:
    """Verify PdfViewer zoom and page navigation state transitions."""
    pdf_file = tmp_path / "doc.pdf"
    pdf_file.write_bytes(b"%PDF-1.4")

    viewer = PdfViewer(str(pdf_file))
    initial_zoom = viewer.zoom_level

    viewer.on_zoom_in_clicked(viewer.btn_zoom_in)
    assert viewer.zoom_level > initial_zoom

    viewer.on_zoom_out_clicked(viewer.btn_zoom_out)
    assert viewer.zoom_level == pytest.approx(initial_zoom)

    viewer.on_next_page_clicked(viewer.btn_next)
    assert viewer.current_page == 2

    viewer.on_prev_page_clicked(viewer.btn_prev)
    assert viewer.current_page == 1


def test_docx_viewer_corrupted_raises(tmp_path: Path) -> None:
    """Verify DocxViewer raises FormatViewerError for corrupted files."""
    bad_docx = tmp_path / "corrupt.docx"
    bad_docx.write_bytes(b"not a valid zip or docx")

    with pytest.raises(FormatViewerError):
        DocxViewer(str(bad_docx))


def test_xlsx_viewer_corrupted_raises(tmp_path: Path) -> None:
    """Verify XlsxViewer raises FormatViewerError for corrupted files."""
    bad_xlsx = tmp_path / "corrupt.xlsx"
    bad_xlsx.write_bytes(b"not a valid xlsx")

    with pytest.raises(FormatViewerError):
        XlsxViewer(str(bad_xlsx))
