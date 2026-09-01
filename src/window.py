"""Main application window for Luma.

Integrates libadwaita header bar, file opening interactions, error reporting,
and the document display container.
"""

from pathlib import Path
from typing import Optional

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, Gtk  # type: ignore

from src.strings import (
    APP_NAME,
    BTN_OPEN_FILE,
    BTN_OPEN_FILE_TOOLTIP,
    HEADER_SUBTITLE_NO_FILE,
    HEADER_TITLE_DEFAULT,
)
from src.viewer_dispatch import open_file
from src.viewers.base import LumaViewerError


class MainWindow(Adw.ApplicationWindow):
    """Main window embedding the header bar, open action, and content container."""

    def __init__(self, application: Adw.Application) -> None:
        """Initialize MainWindow.

        Args:
            application: Parent Adw.Application instance.
        """
        super().__init__(application=application)
        self.set_title(APP_NAME)
        self.set_default_size(1050, 750)

        self.current_viewer: Optional[Gtk.Widget] = None
        self._build_ui()
        self._setup_actions()

    def _build_ui(self) -> None:
        """Construct window layout including header bar and content viewport."""
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        self._build_header_bar()
        self._build_content_area()

        self.set_content(self.main_box)

    def _build_header_bar(self) -> None:
        """Construct the libadwaita header bar with title and action buttons."""
        self.header_bar = Adw.HeaderBar()

        self.title_widget = Adw.WindowTitle()
        self.title_widget.set_title(HEADER_TITLE_DEFAULT)
        self.title_widget.set_subtitle(HEADER_SUBTITLE_NO_FILE)
        self.header_bar.set_title_widget(self.title_widget)

        self.btn_open = Gtk.Button()
        self.btn_open.set_icon_name("document-open-symbolic")
        self.btn_open.set_tooltip_text(BTN_OPEN_FILE_TOOLTIP)
        self.btn_open.connect("clicked", self._on_open_clicked)
        self.header_bar.pack_start(self.btn_open)

        self.main_box.append(self.header_bar)

    def _build_content_area(self) -> None:
        """Construct the container area for documents."""
        self.content_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.content_container.set_vexpand(True)
        self.content_container.set_hexpand(True)

        self.status_page = Adw.StatusPage()
        self.status_page.set_title(HEADER_TITLE_DEFAULT)
        self.status_page.set_description(BTN_OPEN_FILE_TOOLTIP)
        self.status_page.set_icon_name("document-open-symbolic")

        self.content_container.append(self.status_page)
        self.main_box.append(self.content_container)

    def _setup_actions(self) -> None:
        """Register window action for opening files via keyboard shortcut."""
        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", lambda _a, _p: self._on_open_clicked(None))
        self.add_action(open_action)

    def _on_open_clicked(self, _button: Optional[Gtk.Button]) -> None:
        """Present file chooser dialog to select a document."""
        file_dialog = Gtk.FileDialog()
        file_dialog.set_title(BTN_OPEN_FILE)
        file_dialog.open(self, None, self._on_file_dialog_complete)

    def _on_file_dialog_complete(
        self, dialog: Gtk.FileDialog, result: Gio.AsyncResult
    ) -> None:
        """Callback invoked when user selects a file in file dialog."""
        try:
            selected_file = dialog.open_finish(result)
            if selected_file:
                path = selected_file.get_path()
                if path:
                    self.load_document(path)
        except GLib.Error as err:
            GLib.log_structured(
                "Luma",
                GLib.LogLevelFlags.LEVEL_WARNING,
                {"MESSAGE": f"File selection canceled or failed: {err.message}"},
            )

    def load_document(self, path: str) -> None:
        """Load and display a document by path.

        Args:
            path: Absolute filesystem path to document.
        """
        try:
            viewer_widget = open_file(path)
            self._set_viewer(viewer_widget, path)
        except LumaViewerError as exc:
            self._show_error_dialog(exc.message)
            GLib.log_structured(
                "Luma",
                GLib.LogLevelFlags.LEVEL_WARNING,
                {"MESSAGE": f"Viewer error for {path}: {exc.message}"},
            )

    def _set_viewer(self, viewer_widget: Gtk.Widget, path: str) -> None:
        """Replace current content view with the newly instantiated viewer.

        Args:
            viewer_widget: Newly created viewer widget.
            path: Document file path.
        """
        while child := self.content_container.get_first_child():
            self.content_container.remove(child)

        self.current_viewer = viewer_widget
        self.content_container.append(viewer_widget)

        file_name = Path(path).name
        parent_dir = str(Path(path).parent)
        self.title_widget.set_title(file_name)
        self.title_widget.set_subtitle(parent_dir)

    def _show_error_dialog(self, message: str) -> None:
        """Present an alert dialog to the user describing an error and remedy.

        Args:
            message: User-facing actionable error message.
        """
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="Cannot Open File",
            body=message,
        )
        dialog.add_response("ok", "OK")
        dialog.present()
