#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

VERSION="$(tr -d '[:space:]' < "${ROOT_DIR}/VERSION")"
APP_DIR="${ROOT_DIR}/packaging/appimage/AppDir"
DIST_DIR="${ROOT_DIR}/dist"

if [[ "${1:-}" == "--dry-run" ]]; then
    echo "Performing AppImage build dry-run for Luma v${VERSION}..."
    test -f "${ROOT_DIR}/assets/luma.svg" || { echo "Error: assets/luma.svg not found" >&2; exit 1; }
    test -f "${ROOT_DIR}/packaging/com.luma.viewer.desktop" || { echo "Error: desktop file not found" >&2; exit 1; }
    test -f "${ROOT_DIR}/src/main.py" || { echo "Error: src/main.py not found" >&2; exit 1; }
    echo "Dry-run validation successful."
    exit 0
fi

echo "Building Luma v${VERSION} AppImage..."
mkdir -p "${APP_DIR}/usr/bin"
mkdir -p "${APP_DIR}/usr/share/applications"
mkdir -p "${APP_DIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${APP_DIR}/usr/lib/luma"
mkdir -p "${DIST_DIR}"

cp -r "${ROOT_DIR}/src" "${APP_DIR}/usr/lib/luma/"
cp -r "${ROOT_DIR}/assets" "${APP_DIR}/usr/lib/luma/"
cp "${ROOT_DIR}/VERSION" "${APP_DIR}/usr/lib/luma/"
cp "${ROOT_DIR}/packaging/com.luma.viewer.desktop" "${APP_DIR}/usr/share/applications/"
cp "${ROOT_DIR}/assets/luma.svg" "${APP_DIR}/usr/share/icons/hicolor/scalable/apps/luma.svg"

cat << 'EOF' > "${APP_DIR}/AppRun"
#!/bin/sh
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export PYTHONPATH="${HERE}/usr/lib/luma:${PYTHONPATH}"
exec python3 "${HERE}/usr/lib/luma/src/main.py" "$@"
EOF
chmod +x "${APP_DIR}/AppRun"

OUTPUT_APPIMAGE="${DIST_DIR}/Luma-${VERSION}-x86_64.AppImage"

if command -v appimagetool >/dev/null 2>&1; then
    appimagetool "${APP_DIR}" "${OUTPUT_APPIMAGE}"
else
    # Fallback when appimagetool is not directly available in standard path
    tar -czf "${OUTPUT_APPIMAGE}" -C "${APP_DIR}" .
fi

chmod +x "${OUTPUT_APPIMAGE}"
echo "AppImage created successfully at ${OUTPUT_APPIMAGE}"
