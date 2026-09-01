# Security Policy

The Luma project takes software security and user privacy seriously. This document outlines our supported versions, security architecture principles, and the process for responsibly reporting security vulnerabilities.

---

## Supported Versions

Only the latest active release branch receives security updates.

| Version | Supported | Notes |
|:---|:---:|:---|
| `0.1.x` | Yes | Current development release |
| `< 0.1.0` | No | Pre-release snapshots |

---

## Security Architecture & Design Principles

Luma is engineered with proactive defense-in-depth principles:

### 1. Offline & Zero Telemetry Guarantee
Luma is designed to operate completely offline.
- No analytics, metrics, or telemetry are collected or transmitted.
- No network requests are made during runtime or document inspection.
- All document rendering occurs exclusively in memory and on local disks.

### 2. Path Sanitization & Traversal Prevention
Any file opened by the user (via CLI flag `--open` or file picker) is sanitized through `validate_file_path()` in `src/security.py`:
- Relative segments (`../`) and symbolic links are strictly resolved.
- Strict boundary checks prevent access outside authorized directories.
- File existence and OS read permissions are verified before opening.

### 3. Safe Subprocess Spawning
When external system tools or build helpers are invoked:
- Commands are executed strictly using argument lists (never shell string interpolation).
- User input is never passed unescaped to shell interpreters.

### 4. File Descriptor & Resource Management
To prevent resource exhaustion and descriptor leaks:
- All file operations use deterministic context managers (`with open(...)`).
- Archive inspections close file archives immediately upon reading catalog metadata.

### 5. Automated Dependency Auditing
- All dependencies in `requirements.txt` and `requirements-dev.txt` are pinned to exact versions.
- Continuous Integration runs `pip-audit` on every push and pull request to verify that no high- or critical-severity CVEs exist in dependencies.

---

## Reporting a Vulnerability

If you discover a potential security vulnerability in Luma, please report it responsibly:

1. **Do not create a public issue.** Please report the issue privately using [GitHub Security Advisories](https://github.com/<your-org>/luma/security/advisories/new) or via email to `security@luma.local`.
2. **Include detailed information:**
   - A description of the vulnerability and its potential impact.
   - Exact steps or minimal proof-of-concept file to reproduce the issue.
   - Operating system and version of Luma tested.
3. **Response Timeline:**
   - **Initial Acknowledgment:** Within 48 hours.
   - **Assessment & Triage:** Within 5 business days.
   - **Patch & Advisory:** Coordinated release and CVE disclosure once verified.
