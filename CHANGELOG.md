# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-01

### Added
- Initial release of Luma desktop document viewer for Linux.
- **PDF Viewer** with full-featured page navigation, zoom controls, in-document text search, fit-to-width toggle, and native print support powered by WebKitGTK.
- **Word Document Viewer** (`.docx`) preserving heading hierarchy, bold, and italic text formatting via python-docx.
- **Presentation Viewer** (`.pptx`) with slide-by-slide navigation, shape content extraction, and thumbnail layout via python-pptx.
- **Spreadsheet Viewer** (`.xlsx`) rendering multi-sheet workbooks in tabbed grid layouts with column headers via openpyxl.
- **Plain Text Viewer** for `.txt`, `.md`, `.rst`, `.log`, and `.csv` files with monospace rendering and horizontal scroll.
- **Image Viewer** for `.png`, `.jpg`, `.jpeg`, `.webp`, and `.svg` with zoom in/out, fit-to-window, and centered viewport.
- **Archive Inspector** for `.zip`, `.tar`, `.tar.gz`, `.tar.bz2`, and `.tar.xz` with tabular file listing showing name, size, compressed size, and modification date.
- **Unsupported Format Fallback** displaying file metadata (name, MIME type, size) and a formatted hexadecimal preview.
- Native GNOME desktop integration using GTK4 and libadwaita with adaptive header bar and dark mode support.
- Path traversal protection and strict file validation via the security module.
- MIME type detection using both `python-magic` (libmagic) and `mimetypes` fallback.
- Command-line interface with `--open` and `--version` flags.
- Comprehensive unit test suite (26 tests) covering security validation, viewer dispatch, and format rendering.
- CI/CD pipeline with `verify.yml` (lint, type-check, unit tests, build dry-run, dependency audit) and `release.yml` (automated packaging and GitHub Releases).
- Packaging scripts for AppImage, Debian (`.deb`), and RPM (`.rpm`) formats.
- Professional documentation: README, CONTRIBUTING, SECURITY, and CHANGELOG.
- Zero telemetry, zero network access, fully offline operation.

[0.1.0]: https://github.com/zer0k7/Luma/releases/tag/v0.1.0
