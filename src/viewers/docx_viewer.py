"""Word document (.docx) viewer widget.

Parses OpenXML WordprocessingML documents using python-docx and presents
formatted text preserving headings, bold, and italic runs.
"""

from pathlib import Path
from typing import Any

import docx  # type: ignore
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Pango  # type: ignore

from src.strings import ERROR_PARSING_FAILED
from src.viewers.base import FormatViewerError


class DocxViewer(Gtk.ScrolledWindow):
    """Scrolled viewer for Word (.docx) documents preserving text styling."""

    def __init__(self, file_path: str) -> None:
        """Initialize DocxViewer with parsed document content.

        Args:
            file_path: Absolute filesystem path to .docx document.

        Raises:
            FormatViewerError: If docx parsing fails or file is corrupted.
        """
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_left_margin(24)
        self.text_view.set_right_margin(24)
        self.text_view.set_top_margin(20)
        self.text_view.set_bottom_margin(20)

        self.buffer = self.text_view.get_buffer()
        self._setup_tags()
        self._load_document(file_path)

        self.set_child(self.text_view)

    def _setup_tags(self) -> None:
        """Create text tags for headings, bold, and italic styling."""
        tag_table = self.buffer.get_tag_table()

        heading1 = Gtk.TextTag.new("heading1")
        heading1.set_property("scale", 1.8)
        heading1.set_property("weight", Pango.Weight.BOLD)
        tag_table.add(heading1)

        heading2 = Gtk.TextTag.new("heading2")
        heading2.set_property("scale", 1.4)
        heading2.set_property("weight", Pango.Weight.BOLD)
        tag_table.add(heading2)

        bold_tag = Gtk.TextTag.new("bold")
        bold_tag.set_property("weight", Pango.Weight.BOLD)
        tag_table.add(bold_tag)

        italic_tag = Gtk.TextTag.new("italic")
        italic_tag.set_property("style", Pango.Style.ITALIC)
        tag_table.add(italic_tag)

    def _load_document(self, file_path: str) -> None:
        """Parse the DOCX document and populate the text buffer.

        Args:
            file_path: Absolute path to docx file.

        Raises:
            FormatViewerError: If docx parsing fails.
        """
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                self._insert_paragraph(para)
        except Exception as exc:
            filename = Path(file_path).name
            error_msg = ERROR_PARSING_FAILED.format(
                path=filename,
                format_name="Word Document (.docx)",
            )
            raise FormatViewerError(error_msg, path=file_path) from exc

    def _insert_paragraph(self, para: Any) -> None:
        """Render a single paragraph run by run with applied styles.

        Args:
            para: python-docx Paragraph object.
        """
        iter_end = self.buffer.get_end_iter()
        is_heading1 = para.style.name.startswith("Heading 1")
        is_heading2 = para.style.name.startswith("Heading 2")

        for run in para.runs:
            tags = []
            if is_heading1:
                tags.append("heading1")
            elif is_heading2:
                tags.append("heading2")
            if run.bold:
                tags.append("bold")
            if run.italic:
                tags.append("italic")

            if tags:
                self.buffer.insert_with_tags_by_name(iter_end, run.text, *tags)
            else:
                self.buffer.insert(iter_end, run.text)

        self.buffer.insert(iter_end, "\n\n")
