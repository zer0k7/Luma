"""PDF document viewer widget powered by WebKitGTK.

Renders PDF files with page navigation, zoom controls, in-document search,
and printing support.
"""

from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
try:
    gi.require_version("WebKit", "6.0")
except (ValueError, AttributeError):
    pass

from gi.repository import Gdk, Gtk  # type: ignore # noqa: E402

try:
    from gi.repository import WebKit  # type: ignore # noqa: E402
except (ImportError, AttributeError):
    WebKit = None

from src.strings import (  # noqa: E402
    PDF_FIT_WIDTH_TOOLTIP,
    PDF_NEXT_PAGE_TOOLTIP,
    PDF_PAGE_STATUS_TEMPLATE,
    PDF_PREV_PAGE_TOOLTIP,
    PDF_PRINT_TOOLTIP,
    PDF_SEARCH_PLACEHOLDER,
    PDF_SEARCH_TOOLTIP,
    PDF_ZOOM_IN_TOOLTIP,
    PDF_ZOOM_OUT_TOOLTIP,
    PDF_ZOOM_STATUS_TEMPLATE,
)

STRINGS = {
    "page_status": PDF_PAGE_STATUS_TEMPLATE,
    "zoom_status": PDF_ZOOM_STATUS_TEMPLATE,
    "prev_page": PDF_PREV_PAGE_TOOLTIP,
    "next_page": PDF_NEXT_PAGE_TOOLTIP,
    "zoom_out": PDF_ZOOM_OUT_TOOLTIP,
    "zoom_in": PDF_ZOOM_IN_TOOLTIP,
    "fit_width": PDF_FIT_WIDTH_TOOLTIP,
    "search": PDF_SEARCH_TOOLTIP,
    "print": PDF_PRINT_TOOLTIP,
    "search_placeholder": PDF_SEARCH_PLACEHOLDER,
}


class PdfViewer(Gtk.Box):
    """Vertical box container embedding a WebKit viewer and PDF toolbar."""

    def __init__(self, file_path: str) -> None:
        """Initialize PDF viewer widget with document toolbar and webview.

        Args:
            file_path: Absolute canonical filesystem path to PDF document.
        """
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.file_path = file_path
        self.current_page = 1
        self.total_pages = 1
        self.zoom_level = 1.0

        self._build_toolbar()
        self._build_search_bar()
        self._build_webview()
        self._setup_shortcuts()

    def _build_toolbar(self) -> None:
        """Create the top toolbar containing page, zoom, search, and print buttons."""
        self.toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.toolbar.set_margin_top(6)
        self.toolbar.set_margin_bottom(6)
        self.toolbar.set_margin_start(12)
        self.toolbar.set_margin_end(12)

        self._add_navigation_controls()
        self._add_zoom_controls()
        self._add_action_controls()

        self.append(self.toolbar)

    def _add_navigation_controls(self) -> None:
        """Add previous/next page navigation buttons and page counter label."""
        self.btn_prev = Gtk.Button.new_from_icon_name("go-previous-symbolic")
        self.btn_prev.set_tooltip_text(STRINGS["prev_page"])
        self.btn_prev.connect("clicked", self.on_prev_page_clicked)
        self.toolbar.append(self.btn_prev)

        self.btn_next = Gtk.Button.new_from_icon_name("go-next-symbolic")
        self.btn_next.set_tooltip_text(STRINGS["next_page"])
        self.btn_next.connect("clicked", self.on_next_page_clicked)
        self.toolbar.append(self.btn_next)

        self.lbl_page = Gtk.Label(
            label=STRINGS["page_status"].format(
                current=self.current_page,
                total=self.total_pages,
            )
        )
        self.toolbar.append(self.lbl_page)

    def _add_zoom_controls(self) -> None:
        """Add zoom in, zoom out, fit to width, and zoom label."""
        sep1 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.toolbar.append(sep1)

        self.btn_zoom_out = Gtk.Button.new_from_icon_name("zoom-out-symbolic")
        self.btn_zoom_out.set_tooltip_text(STRINGS["zoom_out"])
        self.btn_zoom_out.connect("clicked", self.on_zoom_out_clicked)
        self.toolbar.append(self.btn_zoom_out)

        self.btn_zoom_in = Gtk.Button.new_from_icon_name("zoom-in-symbolic")
        self.btn_zoom_in.set_tooltip_text(STRINGS["zoom_in"])
        self.btn_zoom_in.connect("clicked", self.on_zoom_in_clicked)
        self.toolbar.append(self.btn_zoom_in)

        percent = int(self.zoom_level * 100)
        self.lbl_zoom = Gtk.Label(label=STRINGS["zoom_status"].format(percent=percent))
        self.toolbar.append(self.lbl_zoom)

        self.btn_fit_width = Gtk.ToggleButton()
        self.btn_fit_width.set_icon_name("zoom-fit-best-symbolic")
        self.btn_fit_width.set_tooltip_text(STRINGS["fit_width"])
        self.btn_fit_width.connect("toggled", self.on_fit_width_toggled)
        self.toolbar.append(self.btn_fit_width)

    def _add_action_controls(self) -> None:
        """Add document search and print trigger buttons."""
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.toolbar.append(sep2)

        self.btn_search = Gtk.Button.new_from_icon_name("edit-find-symbolic")
        self.btn_search.set_tooltip_text(STRINGS["search"])
        self.btn_search.connect("clicked", self.on_search_clicked)
        self.toolbar.append(self.btn_search)

        self.btn_print = Gtk.Button.new_from_icon_name("printer-symbolic")
        self.btn_print.set_tooltip_text(STRINGS["print"])
        self.btn_print.connect("clicked", self.on_print_clicked)
        self.toolbar.append(self.btn_print)

    def _build_search_bar(self) -> None:
        """Construct the collapsible search entry box below the toolbar."""
        self.search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.search_box.set_margin_start(12)
        self.search_box.set_margin_end(12)
        self.search_box.set_margin_bottom(6)
        self.search_box.set_visible(False)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(STRINGS["search_placeholder"])
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self.on_search_query_changed)
        self.search_box.append(self.search_entry)

        self.append(self.search_box)

    def _build_webview(self) -> None:
        """Embed the WebKit.WebView pointing to the PDF file:// URI."""
        if WebKit is not None:
            self.webview = WebKit.WebView()
            file_uri = Path(self.file_path).as_uri()
            self.webview.load_uri(file_uri)
            self.webview.set_vexpand(True)
            self.webview.set_hexpand(True)
            self.append(self.webview)
        else:
            fallback_label = Gtk.Label(label=Path(self.file_path).name)
            fallback_label.set_vexpand(True)
            self.append(fallback_label)
            self.webview = None

    def _setup_shortcuts(self) -> None:
        """Register keyboard shortcut event controller."""
        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

    def on_prev_page_clicked(self, _button: Gtk.Button) -> None:
        """Navigate to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_page_label()
            self._run_javascript("window.scrollBy(0, -window.innerHeight);")

    def on_next_page_clicked(self, _button: Gtk.Button) -> None:
        """Navigate to the next page."""
        self.current_page += 1
        self._update_page_label()
        self._run_javascript("window.scrollBy(0, window.innerHeight);")

    def on_zoom_in_clicked(self, _button: Gtk.Button) -> None:
        """Zoom in by 10%."""
        self.zoom_level = min(self.zoom_level + 0.1, 3.0)
        self._update_zoom()

    def on_zoom_out_clicked(self, _button: Gtk.Button) -> None:
        """Zoom out by 10%."""
        self.zoom_level = max(self.zoom_level - 0.1, 0.3)
        self._update_zoom()

    def on_fit_width_toggled(self, button: Gtk.ToggleButton) -> None:
        """Toggle fit-to-width mode."""
        if button.get_active():
            self.zoom_level = 1.0
            self._update_zoom()

    def on_search_clicked(self, _button: Gtk.Button) -> None:
        """Toggle the visibility of the search bar."""
        is_visible = self.search_box.get_visible()
        self.search_box.set_visible(not is_visible)
        if not is_visible:
            self.search_entry.grab_focus()

    def on_search_query_changed(self, entry: Gtk.SearchEntry) -> None:
        """Trigger in-page search via WebKit find controller."""
        if self.webview and hasattr(self.webview, "get_find_controller"):
            controller = self.webview.get_find_controller()
            query = entry.get_text()
            if query:
                controller.search(query, 0, 100)
            else:
                controller.search_finish()

    def on_print_clicked(self, _button: Gtk.Button) -> None:
        """Trigger the GTK PrintOperation."""
        if self.webview and hasattr(WebKit, "PrintOperation"):
            print_op = WebKit.PrintOperation.new(self.webview)
            print_op.run_dialog(None)
        else:
            gtk_print = Gtk.PrintOperation()
            gtk_print.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)

    def on_key_pressed(
        self,
        _controller: Gtk.EventControllerKey,
        keyval: int,
        _keycode: int,
        state: Gdk.ModifierType,
    ) -> bool:
        """Handle keyboard navigation and zoom shortcuts."""
        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)
        if ctrl and keyval in (Gdk.KEY_plus, Gdk.KEY_equal, Gdk.KEY_KP_Add):
            self.on_zoom_in_clicked(self.btn_zoom_in)
            return True
        if ctrl and keyval in (Gdk.KEY_minus, Gdk.KEY_KP_Subtract):
            self.on_zoom_out_clicked(self.btn_zoom_out)
            return True
        if ctrl and keyval in (Gdk.KEY_f, Gdk.KEY_F):
            self.on_search_clicked(self.btn_search)
            return True
        if ctrl and keyval in (Gdk.KEY_p, Gdk.KEY_P):
            self.on_print_clicked(self.btn_print)
            return True
        if keyval == Gdk.KEY_Left:
            self.on_prev_page_clicked(self.btn_prev)
            return True
        if keyval == Gdk.KEY_Right:
            self.on_next_page_clicked(self.btn_next)
            return True
        return False

    def _update_page_label(self) -> None:
        """Update page indicator text."""
        self.lbl_page.set_label(
            STRINGS["page_status"].format(
                current=self.current_page,
                total=self.total_pages,
            )
        )

    def _update_zoom(self) -> None:
        """Update webview zoom level and display label."""
        if self.webview and hasattr(self.webview, "set_zoom_level"):
            self.webview.set_zoom_level(self.zoom_level)
        percent = int(self.zoom_level * 100)
        self.lbl_zoom.set_label(STRINGS["zoom_status"].format(percent=percent))

    def _run_javascript(self, script: str) -> None:
        """Execute a JavaScript snippet within the webview."""
        if self.webview and hasattr(self.webview, "evaluate_javascript"):
            self.webview.evaluate_javascript(script, -1, None, None, None, None, None)
