<p align="center">
  <img src="assets/luma.svg" alt="Luma Logo" width="128" height="128" />
</p>

<h1 align="center">Luma</h1>

<p align="center">
  <strong>A minimal, polished document viewer for Linux desktops.</strong>
</p>

<p align="center">
  <a href="#build-status"><img src="https://img.shields.io/badge/CI-Passing-2ea44f?style=flat-square&logo=githubactions&logoColor=white" alt="CI Status" /></a>
  <a href="VERSION"><img src="https://img.shields.io/badge/version-0.1.0-blue?style=flat-square" alt="Version" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational?style=flat-square" alt="License" /></a>
  <a href="#dependencies"><img src="https://img.shields.io/badge/python-3.11+-yellow?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+" /></a>
  <a href="#dependencies"><img src="https://img.shields.io/badge/GTK-4.0%20%2B%20Adwaita-purple?style=flat-square&logo=gnome&logoColor=white" alt="GTK4 & Libadwaita" /></a>
  <a href="SECURITY.md"><img src="https://img.shields.io/badge/telemetry-zero-success?style=flat-square" alt="Zero Telemetry" /></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#supported-formats">Supported Formats</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage--shortcuts">Shortcuts</a> •
  <a href="#architecture">Architecture</a> •
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

## Overview

**Luma** is a fast, purposeful desktop file viewer designed specifically for the modern Linux desktop. Instead of launching heavy office suites or separate standalone utilities just to inspect a document, Luma opens PDFs, Word documents, PowerPoint presentations, Excel spreadsheets, vector and raster images, plain text, and compressed archives within a unified, beautifully crafted interface.

Built with **GTK4** and **libadwaita**, Luma adheres to GNOME Human Interface Guidelines (HIG) and brings the refined presentation standard of macOS software to Linux without compromising desktop independence.

---

## Features

- **macOS-Grade Polish, Native GNOME Integration**  
  Uses standard libadwaita styling, native system fonts, dynamic dark and light mode adaptation, and standard Adwaita iconography.
- **Built-in WebKit PDF Engine**  
  Smooth vector zooming, continuous page navigation, in-document text search, and native print dialog support.
- **Office Document Inspection**  
  Read `.docx`, `.pptx`, and `.xlsx` files without running LibreOffice or Microsoft Office. Formats headings, styles, slide cards, and spreadsheet grids automatically.
- **Archive Cataloging**  
  Inspect the contents and compressed/uncompressed sizes of `.zip`, `.tar`, `.tar.gz`, `.tar.bz2`, and `.tar.xz` archives without extraction.
- **Strict Privacy & Offline Guarantee**  
  Zero analytics, zero telemetry, no tracking, and no outbound network connections. Your documents never leave your machine.
- **Secure File Handling**  
  Strict path validation, canonical link resolution, directory traversal guards, and safe exception containment.

---

## Supported Formats

| Category | File Formats | Supported Capabilities |
|:---|:---|:---|
| **PDF Documents** | `.pdf` | Multi-page scrolling, page counter, zoom in/out, fit-to-width, search (`Ctrl+F`), print (`Ctrl+P`) |
| **Word Documents** | `.docx` | Paragraph styling, headings preservation, bold and italic text formatting |
| **Presentations** | `.pptx` | Slide-by-slide navigation, slide title & bullet point rendering |
| **Spreadsheets** | `.xlsx` | Multi-sheet tab switching, structured row/column cell grids, header rows |
| **Plain Text & Code** | `.txt`, `.md`, `.rst`, `.log`, `.csv` | Monospace typography, horizontal scrolling, clean un-wrapped viewing |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg` | Vector and raster rendering, fit-to-window scaling, manual zoom |
| **Archives** | `.zip`, `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz` | Structured file listing, file size breakdowns, timestamp inspection |
| **Unsupported Types** | `*` | Graceful fallback showing file size, detected MIME type, and structured hex preview |

---

## Installation

Pre-built packages are automatically verified and compiled on Linux runners by GitHub Actions for every tagged release.

### AppImage (Universal Linux)

Works on Debian, Ubuntu, Fedora, Arch, openSUSE, and any distribution with FUSE support:

```sh
chmod +x Luma-*.AppImage
./Luma-*.AppImage
```

### Debian / Ubuntu (`.deb`)

```sh
sudo dpkg -i luma_*_amd64.deb
sudo apt-get install -f
```

### Fedora / RHEL / openSUSE (`.rpm`)

```sh
sudo rpm -i luma-*-1.x86_64.rpm
```

### Building From Source

For development or packaging maintainers:

```sh
# System dependencies (Debian/Ubuntu example)
sudo apt-get install -y python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 libmagic1

# Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Launch Luma
python3 src/main.py
```

---

## Usage & Shortcuts

Open any file from the command line:

```sh
luma --open /path/to/document.pdf
luma --version
```

### Keyboard Shortcuts

| Shortcut | Action | Scope |
|:---|:---|:---|
| <kbd>Ctrl</kbd> + <kbd>O</kbd> | Open file chooser dialog | Global |
| <kbd>Ctrl</kbd> + <kbd>F</kbd> | Toggle document search bar | PDF Viewer |
| <kbd>Ctrl</kbd> + <kbd>P</kbd> | Open system print dialog | PDF Viewer |
| <kbd>Ctrl</kbd> + <kbd>+</kbd> | Zoom in | PDF & Image Viewers |
| <kbd>Ctrl</kbd> + <kbd>-</kbd> | Zoom out | PDF & Image Viewers |
| <kbd>Left</kbd> | Previous page / slide | PDF & Presentation Viewers |
| <kbd>Right</kbd> | Next page / slide | PDF & Presentation Viewers |

---

## Architecture

Luma is architected with clear boundaries, modular components, and pure dispatching logic:

```
src/
├── main.py              # Adw.Application entry point & CLI option parser
├── window.py            # MainWindow container with libadwaita HeaderBar
├── viewer_dispatch.py   # Pure MIME inspection and viewer instantiation
├── security.py          # Strict path traversal guards & file validation
├── strings.py           # Centralized constants for all user-facing strings
└── viewers/             # Specialized view implementations
    ├── base.py          # Typed exception hierarchy (LumaViewerError)
    ├── pdf_viewer.py    # WebKitGTK embedded PDF viewer
    ├── docx_viewer.py   # OpenXML Word document parser
    ├── pptx_viewer.py   # OpenXML Presentation slide navigator
    ├── xlsx_viewer.py   # OpenXML Spreadsheet tabbed grid
    ├── text_viewer.py   # Monospace text scrolled viewer
    ├── image_viewer.py  # Scaled vector & raster image canvas
    ├── archive_viewer.py# Compressed archive member catalog
    └── unsupported_viewer.py # Metadata & hex inspection fallback
```

---

## Quality & Security

- **Zero Inline Strings:** All user-facing strings and error messages are centralized in `src/strings.py`.
- **Pure Functions & Modularity:** No function exceeds 60 lines. Single-responsibility design throughout.
- **Automated CI Validation:** Every pull request runs `flake8`, `black --check`, `isort`, `mypy --strict`, `pytest`, `packaging/appimage/build.sh --dry-run`, and dependency security auditing via `pip-audit`.
- **Security Policy:** Review our vulnerability disclosure policy and hardening principles in [SECURITY.md](SECURITY.md).

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before submitting pull requests.

---

## License

Luma is open-source software licensed under the **[MIT License](LICENSE)**.
