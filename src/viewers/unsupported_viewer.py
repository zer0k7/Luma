"""Fallback viewer widget for unsupported file types.

Displays metadata (file name, MIME type, size) and a raw hexadecimal preview
of the file contents.
"""

from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore # noqa: E402

from src.strings import (  # noqa: E402
    UNSUPPORTED_INSTRUCTIONS,
    UNSUPPORTED_MIME_LABEL,
    UNSUPPORTED_SIZE_LABEL,
    UNSUPPORTED_TITLE,
)


class UnsupportedViewer(Gtk.ScrolledWindow):
    """Viewer displaying file details and formatted hex preview for unsupported formats."""

    def __init__(self, file_path: str, mime_type: str) -> None:
        """Initialize UnsupportedViewer with file information and hex preview.

        Args:
            file_path: Absolute filesystem path to file.
            mime_type: Detected MIME type of file.
        """
        super().__init__()
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.file_path = file_path
        self.mime_type = mime_type

        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        container.set_margin_top(24)
        container.set_margin_bottom(24)
        container.set_margin_start(28)
        container.set_margin_end(28)

        self._build_header(container)
        self._build_hex_dump(container)

        self.set_child(container)

    def _build_header(self, container: Gtk.Box) -> None:
        """Add title, info labels, and explanation text.

        Args:
            container: Destination box container.
        """
        title = Gtk.Label(label=UNSUPPORTED_TITLE)
        title.add_css_class("title-2")
        title.set_xalign(0.0)
        container.append(title)

        file_size = Path(self.file_path).stat().st_size
        meta_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        mime_lbl = Gtk.Label(label=UNSUPPORTED_MIME_LABEL.format(mime_type=self.mime_type))
        mime_lbl.set_xalign(0.0)
        meta_box.append(mime_lbl)

        size_lbl = Gtk.Label(label=UNSUPPORTED_SIZE_LABEL.format(size_bytes=f"{file_size:,}"))
        size_lbl.set_xalign(0.0)
        meta_box.append(size_lbl)

        container.append(meta_box)

        desc = Gtk.Label(label=UNSUPPORTED_INSTRUCTIONS)
        desc.set_wrap(True)
        desc.set_xalign(0.0)
        container.append(desc)

    def _build_hex_dump(self, container: Gtk.Box) -> None:
        """Generate and attach hex dump text view.

        Args:
            container: Destination box container.
        """
        hex_text = self._generate_hex_dump()
        tv = Gtk.TextView()
        tv.set_editable(False)
        tv.set_cursor_visible(False)
        tv.set_monospace(True)
        tv.get_buffer().set_text(hex_text)
        tv.add_css_class("card")
        container.append(tv)

    def _generate_hex_dump(self, max_bytes: int = 512) -> str:
        """Create a formatted hex dump string for the first bytes of the file.

        Args:
            max_bytes: Maximum number of bytes to preview.

        Returns:
            Formatted hex dump string.
        """
        lines = []
        try:
            with open(self.file_path, "rb") as fh:
                data = fh.read(max_bytes)

            for offset in range(0, len(data), 16):
                chunk = data[offset : offset + 16]
                hex_part = " ".join(f"{b:02x}" for b in chunk)
                ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
                lines.append(f"{offset:08x}  {hex_part:<48}  |{ascii_part}|")
        except OSError:
            lines.append("Unable to read file content for hex preview.")

        return "\n".join(lines)
