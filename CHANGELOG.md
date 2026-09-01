# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-01

### Added
- Initial release of Luma desktop document viewer for Linux.
- Support for PDF viewing with page navigation, zoom, search, and printing via WebKitGTK.
- Support for Word documents (`.docx`), presentations (`.pptx`), and spreadsheets (`.xlsx`).
- Support for plain text, Markdown, and tabular text files (`.txt`, `.md`, `.rst`, `.log`, `.csv`).
- Support for raster and vector images (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`).
- Support for archive inspection (`.zip`, `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz`).
- Fallback hex preview for unsupported formats.
- Native GNOME integration using GTK4 and libadwaita.
- Packaging scripts for AppImage, Debian (.deb), and RPM (.rpm).
