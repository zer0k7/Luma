"""Archive file viewer widget.

Inspects archive contents (.zip, .tar, .tar.gz, .tar.bz2, .tar.xz)
and renders a file catalog with names and sizes.
"""

import tarfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore # noqa: E402

from src.strings import (  # noqa: E402
    ARCHIVE_COL_COMPRESSED,
    ARCHIVE_COL_DATE,
    ARCHIVE_COL_FILENAME,
    ARCHIVE_COL_SIZE,
    ARCHIVE_EMPTY,
    ERROR_PARSING_FAILED,
)
from src.viewers.base import FormatViewerError  # noqa: E402


class ArchiveViewer(Gtk.ScrolledWindow):
    """Scrolled table viewer displaying the contents of compressed archives."""

    def __init__(self, file_path: str) -> None:
        """Initialize ArchiveViewer with archive entry rows.

        Args:
            file_path: Absolute filesystem path to archive file.

        Raises:
            FormatViewerError: If archive cannot be read or is corrupted.
        """
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.entries: List[Tuple[str, str, str, str]] = []
        self._load_archive(file_path)
        self._build_ui()

    def _load_archive(self, file_path: str) -> None:
        """Inspect archive and extract member metadata.

        Args:
            file_path: Path to archive.

        Raises:
            FormatViewerError: If format is invalid or corrupted.
        """
        try:
            if zipfile.is_zipfile(file_path):
                self._read_zip(file_path)
            elif tarfile.is_tarfile(file_path):
                self._read_tar(file_path)
            else:
                self._read_zip(file_path)
        except Exception as exc:
            filename = Path(file_path).name
            error_msg = ERROR_PARSING_FAILED.format(
                path=filename,
                format_name="Archive",
            )
            raise FormatViewerError(error_msg, path=file_path) from exc

    def _read_zip(self, file_path: str) -> None:
        """Read members from a zip archive."""
        with zipfile.ZipFile(file_path, "r") as zf:
            for info in zf.infolist():
                date_str = "%04d-%02d-%02d %02d:%02d" % info.date_time[:5]
                self.entries.append(
                    (
                        info.filename,
                        f"{info.file_size:,} bytes",
                        f"{info.compress_size:,} bytes",
                        date_str,
                    )
                )

    def _read_tar(self, file_path: str) -> None:
        """Read members from a tar archive."""
        with tarfile.open(file_path, "r:*") as tf:
            for member in tf.getmembers():
                dt = datetime.fromtimestamp(member.mtime).strftime("%Y-%m-%d %H:%M")
                self.entries.append(
                    (
                        member.name,
                        f"{member.size:,} bytes",
                        "-",
                        dt,
                    )
                )

    def _build_ui(self) -> None:
        """Build the grid table displaying archive entries."""
        if not self.entries:
            empty_lbl = Gtk.Label(label=ARCHIVE_EMPTY)
            self.set_child(empty_lbl)
            return

        grid = Gtk.Grid()
        grid.set_row_spacing(6)
        grid.set_column_spacing(24)
        grid.set_margin_top(16)
        grid.set_margin_bottom(16)
        grid.set_margin_start(20)
        grid.set_margin_end(20)

        headers = [
            ARCHIVE_COL_FILENAME,
            ARCHIVE_COL_SIZE,
            ARCHIVE_COL_COMPRESSED,
            ARCHIVE_COL_DATE,
        ]
        for col_idx, text in enumerate(headers):
            lbl = Gtk.Label(label=text)
            lbl.set_xalign(0.0)
            lbl.add_css_class("heading")
            grid.attach(lbl, col_idx, 0, 1, 1)

        for row_idx, row_data in enumerate(self.entries, start=1):
            if row_idx > 1000:
                break
            for col_idx, cell_value in enumerate(row_data):
                lbl = Gtk.Label(label=cell_value)
                lbl.set_xalign(0.0)
                grid.attach(lbl, col_idx, row_idx, 1, 1)

        self.set_child(grid)
