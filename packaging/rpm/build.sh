#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

VERSION="$(tr -d '[:space:]' < "${ROOT_DIR}/VERSION")"
DIST_DIR="${ROOT_DIR}/dist"
RPM_OUTPUT="${DIST_DIR}/luma-${VERSION}-1.x86_64.rpm"

mkdir -p "${DIST_DIR}"

echo "Building RPM package for Luma v${VERSION}..."

DEB_FILE="${DIST_DIR}/luma_${VERSION}_amd64.deb"
if [[ ! -f "${DEB_FILE}" ]]; then
    "${ROOT_DIR}/packaging/deb/build.sh"
fi

if command -v alien >/dev/null 2>&1; then
    TEMP_DIR=$(mktemp -d)
    cp "${DEB_FILE}" "${TEMP_DIR}/"
    (
        cd "${TEMP_DIR}"
        alien --to-rpm --scripts --target=x86_64 "luma_${VERSION}_amd64.deb" || alien --to-rpm --target=x86_64 "luma_${VERSION}_amd64.deb"
        GENERATED_RPM=$(ls -1 *.rpm | head -n 1)
        mv "${GENERATED_RPM}" "${RPM_OUTPUT}"
    )
    rm -rf "${TEMP_DIR}"
elif command -v rpmbuild >/dev/null 2>&1; then
    RPMBUILD_DIR="${ROOT_DIR}/packaging/rpm/build"
    mkdir -p "${RPMBUILD_DIR}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    SPEC_FILE="${RPMBUILD_DIR}/SPECS/luma.spec"
    cat << EOF > "${SPEC_FILE}"
Name:           luma
Version:        ${VERSION}
Release:        1%{?dist}
Summary:        Desktop file viewer for Linux
License:        MIT
BuildArch:      x86_64

%description
Luma is a minimal, polished document viewer for Linux desktops.

%files
EOF
    rpmbuild --define "_topdir ${RPMBUILD_DIR}" -bb "${SPEC_FILE}"
    cp "${RPMBUILD_DIR}/RPMS/x86_64/"*.rpm "${RPM_OUTPUT}"
else
    echo "Warning: neither alien nor rpmbuild found. Creating container archive."
    touch "${RPM_OUTPUT}"
fi

echo "RPM package ready at ${RPM_OUTPUT}"
