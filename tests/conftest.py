"""Pytest configuration and test fixtures.

Provides test fixtures and mock GTK/Adwaita/WebKit bindings when running in environments
where native C-libraries are not available.
"""

from pathlib import Path
import sys
from unittest.mock import MagicMock

# If PyGObject (gi) is not installed in the local test environment,
# register mock modules in sys.modules so unit tests run seamlessly.
if "gi" not in sys.modules:
    try:
        import gi
    except ImportError:
        gi_mock = MagicMock()
        gi_repository_mock = MagicMock()

        class MockWidget:
            """Generic mock widget for GTK and Adwaita components."""

            def __init__(self, *args, **kwargs):
                self._children = []
                self._visible = True
                self._text = ""
                self._zoom = 1.0
                self._size = (800, 600)

            @classmethod
            def new(cls, *args, **kwargs):
                return cls(*args, **kwargs)

            @classmethod
            def new_from_icon_name(cls, *args, **kwargs):
                return cls(*args, **kwargs)

            @classmethod
            def new_for_file(cls, *args, **kwargs):
                return cls(*args, **kwargs)

            @classmethod
            def new_for_path(cls, *args, **kwargs):
                return cls(*args, **kwargs)

            def __getattr__(self, name):
                return MagicMock()

            def append(self, child):
                self._children.append(child)

            def get_first_child(self):
                return self._children[0] if self._children else None

            def remove(self, child):
                if child in self._children:
                    self._children.remove(child)

            def set_child(self, child):
                self.child = child

            def set_visible(self, val):
                self._visible = val

            def get_visible(self):
                return self._visible

            def connect(self, signal, handler, *args):
                pass

            def set_label(self, label):
                self._text = label

            def get_label(self):
                return self._text

            def get_buffer(self):
                buf = MagicMock()
                buf.get_tag_table.return_value = MagicMock()
                return buf

            def set_content(self, content):
                pass

            def pack_start(self, child):
                self._children.append(child)

            def add_controller(self, controller):
                pass

            def add_action(self, action):
                pass

            def get_size_request(self):
                return self._size

            def set_size_request(self, width, height):
                self._size = (width, height)

            def set_zoom_level(self, zoom):
                self._zoom = zoom

            def add_css_class(self, css_class):
                pass

        gi_repository_mock.Gtk.Widget = MockWidget
        gi_repository_mock.Gtk.Box = MockWidget
        gi_repository_mock.Gtk.ScrolledWindow = MockWidget
        gi_repository_mock.Gtk.Grid = MockWidget
        gi_repository_mock.Gtk.Notebook = MockWidget
        gi_repository_mock.Gtk.Button = MockWidget
        gi_repository_mock.Gtk.ToggleButton = MockWidget
        gi_repository_mock.Gtk.Label = MockWidget
        gi_repository_mock.Gtk.Separator = MockWidget
        gi_repository_mock.Gtk.SearchEntry = MockWidget
        gi_repository_mock.Gtk.TextView = MockWidget
        gi_repository_mock.Gtk.Picture = MockWidget
        gi_repository_mock.Gtk.FileDialog = MockWidget

        gi_repository_mock.Adw.Application = MockWidget
        gi_repository_mock.Adw.ApplicationWindow = MockWidget
        gi_repository_mock.Adw.HeaderBar = MockWidget
        gi_repository_mock.Adw.WindowTitle = MockWidget
        gi_repository_mock.Adw.StatusPage = MockWidget
        gi_repository_mock.Adw.MessageDialog = MockWidget

        sys.modules["gi"] = gi_mock
        sys.modules["gi.repository"] = gi_repository_mock
        sys.modules["gi.repository.Gtk"] = gi_repository_mock.Gtk
        sys.modules["gi.repository.Adw"] = gi_repository_mock.Adw
        sys.modules["gi.repository.GLib"] = gi_repository_mock.GLib
        sys.modules["gi.repository.Gio"] = gi_repository_mock.Gio
        sys.modules["gi.repository.Pango"] = gi_repository_mock.Pango
        sys.modules["gi.repository.WebKit"] = gi_repository_mock.WebKit

# Mock document parsing packages if not installed in local development environment
for pkg_name in ["docx", "pptx", "openpyxl", "magic"]:
    if pkg_name not in sys.modules:
        try:
            __import__(pkg_name)
        except ImportError:
            mock_pkg = MagicMock()
            if pkg_name == "docx":
                def mock_document(path):
                    if "corrupt" in str(path):
                        raise ValueError("Corrupted docx")
                    doc = MagicMock()
                    para = MagicMock()
                    para.style.name = "Normal"
                    run = MagicMock()
                    run.text = "Sample text"
                    run.bold = False
                    run.italic = False
                    para.runs = [run]
                    doc.paragraphs = [para]
                    return doc
                mock_pkg.Document = mock_document
            elif pkg_name == "openpyxl":
                def mock_load_workbook(path, **kwargs):
                    if "corrupt" in str(path):
                        raise ValueError("Corrupted xlsx")
                    wb = MagicMock()
                    wb.sheetnames = ["Sheet1"]
                    sheet = MagicMock()
                    sheet.iter_rows.return_value = [("Header 1", "Header 2"), ("Val 1", "Val 2")]
                    wb.__getitem__.return_value = sheet
                    return wb
                mock_pkg.load_workbook = mock_load_workbook
            elif pkg_name == "pptx":
                def mock_presentation(path):
                    if "corrupt" in str(path):
                        raise ValueError("Corrupted pptx")
                    prs = MagicMock()
                    slide = MagicMock()
                    shape = MagicMock()
                    shape.has_text_frame = True
                    p = MagicMock()
                    p.text = "Slide Title"
                    shape.text_frame.paragraphs = [p]
                    slide.shapes = [shape]
                    prs.slides = [slide]
                    return prs
                mock_pkg.Presentation = mock_presentation
            elif pkg_name == "magic":
                mock_pkg.from_file.return_value = None

            sys.modules[pkg_name] = mock_pkg
