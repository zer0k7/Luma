# Contributing to Luma

Thank you for your interest in contributing to Luma! We welcome contributions from the community that align with our focus on quality, polish, and privacy.

Please read this guide before contributing to ensure smooth collaboration.

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Treat all contributors and users with respect and constructive feedback.

---

## Development Environment Setup

### Prerequisites

Luma is developed for modern Linux desktops. Ensure you have the required development headers installed:

**Debian / Ubuntu:**
```sh
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  python3-dev \
  python3-gi \
  gir1.2-gtk-4.0 \
  gir1.2-adw-1 \
  libwebkitgtk-6.0-dev \
  libmagic1
```

**Fedora / RHEL:**
```sh
sudo dnf install -y \
  python3-devel \
  python3-gobject \
  gtk4-devel \
  libadwaita-devel \
  webkitgtk6.0-devel \
  file-devel
```

### Local Virtual Environment

```sh
# Clone your fork
git clone https://github.com/<your-username>/luma.git
cd luma

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install runtime and development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the app locally
python3 src/main.py
```

---

## Code Quality Standards

All contributions must adhere to the engineering standards enforced in `AGENTS.md`:

1. **No Inline User Strings**  
   Every user-facing label, button title, tooltip, and error message must be defined as a constant in `src/strings.py`. Never hardcode user strings inside widget logic.
2. **Function Length & Single Responsibility**  
   Each function must do exactly one thing. If a function exceeds **60 lines**, split it into cohesive helper methods.
3. **No Debug Prints**  
   Do not commit `print()` or `console.log()` statements. Use `GLib.log_structured` with `G_LOG_DOMAIN = "Luma"`.
4. **No Dead or Commented Code**  
   Do not leave commented-out code, `TODO`, or `FIXME` comments in submitted files.
5. **No Emojis in the User Interface**  
   The application interface must remain clean and purposeful. Use standard Adwaita symbolic icons or SVG assets from `assets/`.
6. **Strict Typing & Documentation**  
   All functions must have complete type annotations that pass `mypy --strict` and docstrings describing parameters, return values, and side effects.
7. **Safe File Operations**  
   Always validate paths using `validate_file_path()` in `src/security.py` to prevent directory traversal and symlink attacks. Use context managers (`with open(...)`) to release file descriptors immediately.

---

## Commit Guidelines

Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): short description
```

### Allowed Types
- `feat`: A new user-facing feature or viewer capability.
- `fix`: A bug fix or error handling improvement.
- `refactor`: Code change that neither fixes a bug nor adds a feature.
- `docs`: Documentation changes (`README.md`, `CONTRIBUTING.md`, etc.).
- `test`: Adding or correcting tests.
- `chore`: Maintenance tasks, dependency bumps, or tool configurations.
- `ci`: Changes to GitHub Actions workflows.
- `perf`: Performance optimization.

### Example
```
feat(pdf): add fit-to-width toolbar toggle
fix(dispatch): handle case-insensitive file extensions
docs(readme): update format support matrix
```

---

## Verification & Testing

Before opening a pull request, run the test suite and quality checks locally:

```sh
# 1. Format and lint checks
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203

# 2. Type checking
mypy src/ --strict --ignore-missing-imports

# 3. Unit tests and coverage
pytest tests/ -v --tb=short

# 4. AppImage build dry-run
packaging/appimage/build.sh --dry-run
```

Every new feature must be accompanied by at least one unit test in `tests/` mirroring the `src/` hierarchy. Every bug fix must include a regression test.

---

## Pull Request Workflow

1. Fork the repository and create a descriptive branch: `git checkout -b feat/your-feature-name`.
2. Commit your changes following the Conventional Commits format.
3. Push to your fork and submit a Pull Request targeting `main`.
4. Ensure all GitHub Actions CI checks (`Verify`) pass.
5. Address code review feedback promptly.
