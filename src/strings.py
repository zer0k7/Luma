"""User-facing strings and message constants for Luma.

All user-facing text displayed in the user interface, dialogs, status bars,
and error messages is declared in this module to prevent inline string duplication
and ensure consistent messaging across the application.
"""

# Application Metadata
APP_NAME = "Luma"
APP_SUBTITLE = "Document Viewer for Linux"
APP_DESCRIPTION = "A minimal, polished document viewer for Linux desktops."

# Window & Header Bar Actions
BTN_OPEN_FILE = "Open File"
BTN_OPEN_FILE_TOOLTIP = "Open a document, spreadsheet, presentation, or archive (Ctrl+O)"
BTN_MENU = "Main Menu"
BTN_MENU_TOOLTIP = "Application options and keyboard shortcuts"
HEADER_TITLE_DEFAULT = "Luma"
HEADER_SUBTITLE_NO_FILE = "No file opened"

# PDF Viewer Toolbar
PDF_PAGE_STATUS_TEMPLATE = "Page {current} of {total}"
PDF_ZOOM_STATUS_TEMPLATE = "{percent}%"
PDF_PREV_PAGE_TOOLTIP = "Go to previous page (Left Arrow)"
PDF_NEXT_PAGE_TOOLTIP = "Go to next page (Right Arrow)"
PDF_ZOOM_OUT_TOOLTIP = "Zoom out (Ctrl+-)"
PDF_ZOOM_IN_TOOLTIP = "Zoom in (Ctrl++)"
PDF_FIT_WIDTH_TOOLTIP = "Fit to width"
PDF_SEARCH_TOOLTIP = "Search text in document (Ctrl+F)"
PDF_PRINT_TOOLTIP = "Print document (Ctrl+P)"
PDF_SEARCH_PLACEHOLDER = "Search document..."
PDF_NO_RESULTS = "No matches found"

# Presentation Viewer Toolbar
PPTX_PREV_SLIDE_TOOLTIP = "Previous slide (Left Arrow)"
PPTX_NEXT_SLIDE_TOOLTIP = "Next slide (Right Arrow)"
PPTX_SLIDE_STATUS_TEMPLATE = "Slide {current} of {total}"

# Spreadsheet Viewer
XLSX_EMPTY_SHEET = "This sheet does not contain any readable data."
XLSX_TAB_DEFAULT_TITLE = "Sheet {index}"

# Archive Viewer
ARCHIVE_COL_FILENAME = "Name"
ARCHIVE_COL_SIZE = "Uncompressed Size"
ARCHIVE_COL_COMPRESSED = "Compressed Size"
ARCHIVE_COL_DATE = "Date Modified"
ARCHIVE_EMPTY = "This archive is empty."

# Image Viewer
IMG_FIT_TOOLTIP = "Fit image to window"
IMG_ZOOM_IN_TOOLTIP = "Zoom image in"
IMG_ZOOM_OUT_TOOLTIP = "Zoom image out"

# Unsupported / Fallback Viewer
UNSUPPORTED_TITLE = "Unsupported File Format"
UNSUPPORTED_INSTRUCTIONS = (
    "Luma does not have a native renderer for this format. "
    "A raw byte inspection is displayed below. "
    "To view this file properly, please open it with its designated application."
)
UNSUPPORTED_MIME_LABEL = "Detected MIME type: {mime_type}"
UNSUPPORTED_SIZE_LABEL = "File size: {size_bytes} bytes"

# Error Messages (action-oriented as required by AGENTS.md)
ERROR_FILE_NOT_FOUND = (
    "The requested file '{path}' could not be found. "
    "Please check that the file path is correct and try again."
)
ERROR_FILE_UNREADABLE = (
    "Luma does not have permission to read '{path}'. "
    "Please verify file permissions or select another file."
)
ERROR_PATH_TRAVERSAL = (
    "Access denied to file '{path}'. "
    "The path resolves outside authorized boundaries or contains unsafe links."
)
ERROR_PARSING_FAILED = (
    "Unable to parse '{path}' as {format_name}. "
    "The file may be corrupted or encrypted. Please check the file and try again."
)
ERROR_PRINT_FAILED = (
    "Unable to complete the print operation. "
    "Please verify that your printer is configured and connected."
)

# CLI Help and Descriptions
CLI_OPEN_HELP = "Path to the file to open on launch"
CLI_VERSION_HELP = "Print version information and exit"
