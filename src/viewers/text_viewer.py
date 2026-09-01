"""Plain text and code document viewer widget.

Renders text-based formats (.txt, .md, .rst, .log, .csv) with monospace
typography and un-wrapped horizontal scrolling.
"""

from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore # noqa: E402

from src.strings import ERROR_PARSING_FAILED  # noqa: E402
from src.viewers.base import FormatViewerError  # noqa: E402


class PlainTextViewer(Gtk.ScrolledWindow):
    """Scrolled viewer displaying text in monospace font without line wrapping."""

    def __init__(self, file_path: str) -> None:
        """Initialize PlainTextViewer with file contents.

        Args:
            file_path: Absolute filesystem path to text file.

        Raises:
            FormatViewerError: If file cannot be read or decoded.
        """
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        self.text_view.set_monospace(True)
        self.text_view.set_wrap_mode(Gtk.WrapMode.NONE)
        self.text_view.set_left_margin(16)
        self.text_view.set_right_margin(16)
        self.text_view.set_top_margin(12)
        self.text_view.set_bottom_margin(12)

        self._load_file(file_path)
        self.set_child(self.text_view)

    def _load_file(self, file_path: str) -> None:
        """Read text from filesystem and populate the text view buffer.

        Args:
            file_path: Target text file path.

        Raises:
            FormatViewerError: If reading fails.
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as file_handle:
                content = file_handle.read()
            buffer = self.text_view.get_buffer()
            buffer.set_text(content)
        except Exception as exc:
            filename = Path(file_path).name
            error_msg = ERROR_PARSING_FAILED.format(
                path=filename,
                format_name="Text Document",
            )
            raise FormatViewerError(error_msg, path=file_path) from exc
