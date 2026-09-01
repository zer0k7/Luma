"""Raster and vector image viewer widget.

Displays image files (.png, .jpg, .jpeg, .webp, .svg) with scaling,
fit-to-window toggle, and centered viewport.
"""

from pathlib import Path
from typing import Any

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk  # type: ignore # noqa: E402

from src.strings import (  # noqa: E402
    ERROR_PARSING_FAILED,
    IMG_FIT_TOOLTIP,
    IMG_ZOOM_IN_TOOLTIP,
    IMG_ZOOM_OUT_TOOLTIP,
)
from src.viewers.base import FormatViewerError  # noqa: E402


class ImageViewer(Gtk.Box):
    """Image viewer container with scaling and viewport controls."""

    def __init__(self, file_path: str) -> None:
        """Initialize ImageViewer with given image file.

        Args:
            file_path: Absolute filesystem path to image file.

        Raises:
            FormatViewerError: If image loading fails.
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.file_path = file_path

        self._build_toolbar()
        self._build_image_area(file_path)

    def _build_toolbar(self) -> None:
        """Create toolbar with zoom controls."""
        self.toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.toolbar.set_margin_top(6)
        self.toolbar.set_margin_bottom(6)
        self.toolbar.set_margin_start(12)
        self.toolbar.set_margin_end(12)

        self.btn_fit = Gtk.ToggleButton()
        self.btn_fit.set_icon_name("zoom-fit-best-symbolic")
        self.btn_fit.set_tooltip_text(IMG_FIT_TOOLTIP)
        self.btn_fit.set_active(True)
        self.btn_fit.connect("toggled", self._on_fit_toggled)
        self.toolbar.append(self.btn_fit)

        self.btn_zoom_in = Gtk.Button.new_from_icon_name("zoom-in-symbolic")
        self.btn_zoom_in.set_tooltip_text(IMG_ZOOM_IN_TOOLTIP)
        self.btn_zoom_in.connect("clicked", self._on_zoom_in)
        self.toolbar.append(self.btn_zoom_in)

        self.btn_zoom_out = Gtk.Button.new_from_icon_name("zoom-out-symbolic")
        self.btn_zoom_out.set_tooltip_text(IMG_ZOOM_OUT_TOOLTIP)
        self.btn_zoom_out.connect("clicked", self._on_zoom_out)
        self.toolbar.append(self.btn_zoom_out)

        self.append(self.toolbar)

    def _build_image_area(self, file_path: str) -> None:
        """Create scrolled container with centered Gtk.Picture child.

        Args:
            file_path: Path to image file.

        Raises:
            FormatViewerError: If Gtk.Picture cannot load the file.
        """
        try:
            self.scrolled = Gtk.ScrolledWindow()
            self.scrolled.set_hexpand(True)
            self.scrolled.set_vexpand(True)

            gio_file = Gio.File.new_for_path(file_path)
            self.picture = Gtk.Picture.new_for_file(gio_file)
            self.picture.set_can_shrink(True)
            if hasattr(Gtk, "ContentFit"):
                self.picture.set_content_fit(Gtk.ContentFit.CONTAIN)

            self.scrolled.set_child(self.picture)
            self.append(self.scrolled)
        except Exception as exc:
            filename = Path(file_path).name
            error_msg = ERROR_PARSING_FAILED.format(
                path=filename,
                format_name="Image",
            )
            raise FormatViewerError(error_msg, path=file_path) from exc

    def _on_fit_toggled(self, button: Gtk.ToggleButton) -> None:
        """Toggle fit-to-window mode."""
        if hasattr(Gtk, "ContentFit"):
            fit_mode = Gtk.ContentFit.CONTAIN if button.get_active() else Gtk.ContentFit.SCALE_DOWN
            self.picture.set_content_fit(fit_mode)

    def _on_zoom_in(self, _button: Any) -> None:
        """Increase picture size."""
        current_width = self.picture.get_size_request()[0]
        if current_width < 0:
            current_width = 800
        new_width = int(current_width * 1.2)
        self.picture.set_size_request(new_width, -1)

    def _on_zoom_out(self, _button: Any) -> None:
        """Decrease picture size."""
        current_width = self.picture.get_size_request()[0]
        if current_width < 0:
            current_width = 800
        new_width = max(int(current_width * 0.8), 200)
        self.picture.set_size_request(new_width, -1)
