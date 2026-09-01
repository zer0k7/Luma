"""Unit tests for application entry point and command-line handling."""

import io
from unittest.mock import patch

from src import get_version
from src.main import LumaApplication, create_app


def test_app_instantiation() -> None:
    """Verify LumaApplication instantiates with correct application ID."""
    app = create_app()
    assert isinstance(app, LumaApplication)


def test_cli_version_flag() -> None:
    """Verify do_handle_local_options prints version when version flag is passed."""
    app = create_app()

    class MockOptions:
        def contains(self, key: str) -> bool:
            return key == "version"

        def lookup_value(self, _key: str):
            return None

    captured_out = io.StringIO()
    with patch("sys.stdout", captured_out):
        ret = app.do_handle_local_options(MockOptions())

    assert ret == 0
    assert get_version() in captured_out.getvalue()


def test_cli_open_flag() -> None:
    """Verify do_handle_local_options stores path when open flag is passed."""
    app = create_app()

    class MockVal:
        def get_string(self) -> str:
            return "/path/to/document.pdf"

    class MockOptions:
        def contains(self, key: str) -> bool:
            return key == "open"

        def lookup_value(self, key: str):
            if key == "open":
                return MockVal()
            return None

    ret = app.do_handle_local_options(MockOptions())
    assert ret == -1
    assert app.pending_open_path == "/path/to/document.pdf"
