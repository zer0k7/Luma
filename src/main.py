"""Luma application entry point.

Initializes GTK4/libadwaita application instance, configures GLib structured logging,
processes command line arguments, and launches the main window.
"""

from pathlib import Path
import sys
from typing import List, Optional

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib  # type: ignore

from src import get_version
from src.security import validate_file_path
from src.strings import CLI_OPEN_HELP, CLI_VERSION_HELP
from src.viewers.base import LumaViewerError
from src.window import MainWindow

LOG_DOMAIN = "Luma"


class LumaApplication(Adw.Application):
    """Luma GTK4 / libadwaita Application manager."""

    def __init__(self) -> None:
        """Initialize LumaApplication with com.luma.viewer ID and option flags."""
        super().__init__(
            application_id="com.luma.viewer",
            flags=Gio.ApplicationFlags.HANDLES_OPEN | Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.main_window: Optional[MainWindow] = None
        self.pending_open_path: Optional[str] = None

        self._setup_logging()
        self._setup_options()

    def _setup_logging(self) -> None:
        """Configure GLib structured logging domain."""
        GLib.set_prgname("luma")
        GLib.set_application_name("Luma")

    def _setup_options(self) -> None:
        """Register command line option entries for --version and --open."""
        self.add_main_option(
            "open",
            ord("o"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.FILENAME,
            CLI_OPEN_HELP,
            "FILE",
        )
        self.add_main_option(
            "version",
            ord("v"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            CLI_VERSION_HELP,
            None,
        )

    def do_handle_local_options(self, options: GLib.VariantDict) -> int:
        """Handle command line flags locally before IPC.

        Args:
            options: Parsed options dictionary.

        Returns:
            Exit code integer (0 for clean exit, -1 to continue startup).
        """
        if options.contains("version"):
            version = get_version()
            sys.stdout.write(f"{version}\n")
            sys.stdout.flush()
            return 0

        if options.contains("open"):
            val = options.lookup_value("open")
            if val is not None:
                # String value unpack
                self.pending_open_path = val.get_string()

        return -1

    def do_startup(self) -> None:
        """Perform one-time application initialization and shortcut registrations."""
        Adw.Application.do_startup(self)
        self.set_accels_for_action("win.open", ["<Control>o"])

        GLib.log_structured(
            LOG_DOMAIN,
            GLib.LogLevelFlags.LEVEL_INFO,
            {"MESSAGE": f"Luma v{get_version()} started successfully."},
        )

    def do_activate(self) -> None:
        """Present main window and load document if requested on launch."""
        if not self.main_window:
            self.main_window = MainWindow(application=self)

        self.main_window.present()

        if self.pending_open_path:
            self._open_cli_file(self.pending_open_path)
            self.pending_open_path = None

    def do_open(self, files: List[Gio.File], _hint: str) -> None:
        """Handle opening files passed via file manager activation or IPC.

        Args:
            files: List of Gio.File objects to open.
            _hint: Activation hint string.
        """
        self.do_activate()
        if files and self.main_window:
            file_path = files[0].get_path()
            if file_path:
                self._open_cli_file(file_path)

    def _open_cli_file(self, raw_path: str) -> None:
        """Validate and open a file supplied via CLI or file manager.

        Args:
            raw_path: User-provided path string.
        """
        if not self.main_window:
            return

        try:
            validated = validate_file_path(raw_path)
            self.main_window.load_document(str(validated))
        except LumaViewerError as exc:
            GLib.log_structured(
                LOG_DOMAIN,
                GLib.LogLevelFlags.LEVEL_WARNING,
                {"MESSAGE": f"Failed to open '{raw_path}': {exc.message}"},
            )
            self.main_window.load_document(raw_path)


def create_app() -> LumaApplication:
    """Instantiate the Luma application.

    Returns:
        Configured LumaApplication instance.
    """
    return LumaApplication()


if __name__ == "__main__":
    app = create_app()
    sys.exit(app.run(sys.argv))
