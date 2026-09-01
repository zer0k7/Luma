#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

VERSION="$(tr -d '[:space:]' < "${ROOT_DIR}/VERSION")"
BUILD_DIR="${ROOT_DIR}/packaging/deb/build/luma_${VERSION}_amd64"
DIST_DIR="${ROOT_DIR}/dist"

echo "Building Debian package for Luma v${VERSION}..."
mkdir -p "${BUILD_DIR}/DEBIAN"
mkdir -p "${BUILD_DIR}/usr/bin"
mkdir -p "${BUILD_DIR}/usr/lib/luma"
mkdir -p "${BUILD_DIR}/usr/share/applications"
mkdir -p "${BUILD_DIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${DIST_DIR}"

cat << EOF > "${BUILD_DIR}/DEBIAN/control"
Package: luma
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Luma Contributors <dev@luma.local>
Description: Desktop file viewer for Linux
 Luma is a minimal, polished document viewer for Linux desktops.
EOF

cp -r "${ROOT_DIR}/src" "${BUILD_DIR}/usr/lib/luma/"
cp -r "${ROOT_DIR}/assets" "${BUILD_DIR}/usr/lib/luma/"
cp "${ROOT_DIR}/VERSION" "${BUILD_DIR}/usr/lib/luma/"
cp "${ROOT_DIR}/packaging/com.luma.viewer.desktop" "${BUILD_DIR}/usr/share/applications/"
cp "${ROOT_DIR}/assets/luma.svg" "${BUILD_DIR}/usr/share/icons/hicolor/scalable/apps/luma.svg"

cat << 'EOF' > "${BUILD_DIR}/usr/bin/luma"
#!/bin/sh
export PYTHONPATH="/usr/lib/luma:${PYTHONPATH}"
exec python3 /usr/lib/luma/src/main.py "$@"
EOF
chmod +x "${BUILD_DIR}/usr/bin/luma"

dpkg-deb --build "${BUILD_DIR}" "${DIST_DIR}/luma_${VERSION}_amd64.deb"
echo "Debian package created at ${DIST_DIR}/luma_${VERSION}_amd64.deb"
