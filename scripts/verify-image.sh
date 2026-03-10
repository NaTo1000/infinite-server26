#!/usr/bin/env bash
# ╔═══════════════════════════════════════════════════════════════════╗
# ║   Infinite Server26 - Docker Image Signature Verifier            ║
# ║   Verifies GPG signatures and SHA hashes before deployment       ║
# ╚═══════════════════════════════════════════════════════════════════╝
set -euo pipefail

IMAGE_REF="${1:-}"
SIGNED_ARCHIVE="${2:-}"
HASH_FILE="${3:-}"

log_info()  { echo "[INFO]  $(date -u +"%Y-%m-%dT%H:%M:%SZ") $*"; }
log_ok()    { echo "[OK]    $(date -u +"%Y-%m-%dT%H:%M:%SZ") $*"; }
log_error() { echo "[ERROR] $(date -u +"%Y-%m-%dT%H:%M:%SZ") $*" >&2; }

usage() {
    cat <<EOF
Usage: $0 <image> [signed-archive] [hash-file]

Verify cryptographic integrity of a Docker image before deployment.

Arguments:
  image           Docker image reference (e.g. nato1000/infinite-server26:fortress)
  signed-archive  Path to GPG-signed .tar.gpg file produced during CI (optional)
  hash-file       Path to .sha256 file to verify against (optional)

The signed-archive is expected to be an armor-signed file produced by:
  gpg --armor --sign --output secure-image.tar.gpg image.tar

Examples:
  $0 nato1000/infinite-server26:fortress
  $0 nato1000/infinite-server26:fortress secure-image.tar.gpg image_hash.sha256
EOF
    exit 1
}

[[ -z "${IMAGE_REF}" ]] && usage

PASS=0
FAIL=0
SAVED_TAR=""

# ─── Helper: save image once and reuse ───────────────────────────────────────
save_image() {
    if [[ -z "${SAVED_TAR}" ]]; then
        SAVED_TAR=$(mktemp /tmp/verify-image-XXXXXX.tar)
        log_info "Exporting image to ${SAVED_TAR}…"
        docker save "${IMAGE_REF}" -o "${SAVED_TAR}"
    fi
}

# ─── 1. Docker Image Existence Check ─────────────────────────────────────────
log_info "Confirming image is present locally: ${IMAGE_REF}"
if docker image inspect "${IMAGE_REF}" &>/dev/null; then
    log_ok "Image found: ${IMAGE_REF}"
    PASS=$((PASS + 1))
else
    log_error "Image NOT found locally: ${IMAGE_REF}"
    FAIL=$((FAIL + 1))
fi

# ─── 2. GPG Signature Verification ───────────────────────────────────────────
# The CI pipeline produces a GPG-signed (armored) file via:
#   gpg --armor --sign --output secure-image.tar.gpg image.tar
# To verify, decrypt/verify the signed file and check it matches the saved image.
if [[ -n "${SIGNED_ARCHIVE}" && -f "${SIGNED_ARCHIVE}" ]]; then
    log_info "Verifying GPG signature: ${SIGNED_ARCHIVE}"
    DECRYPTED_TAR=$(mktemp /tmp/verify-gpg-XXXXXX.tar)
    if gpg --batch --output "${DECRYPTED_TAR}" --decrypt "${SIGNED_ARCHIVE}" 2>&1; then
        log_ok "GPG signature valid – signed archive decrypted"
        # Optionally compare decrypted archive against the saved image export
        save_image
        SIGNED_SHA=$(sha256sum "${DECRYPTED_TAR}" | awk '{print $1}')
        SAVED_SHA=$(sha256sum "${SAVED_TAR}"      | awk '{print $1}')
        if [[ "${SIGNED_SHA}" == "${SAVED_SHA}" ]]; then
            log_ok "Signed archive matches local image export"
            PASS=$((PASS + 1))
        else
            log_error "Signed archive content does NOT match local image export"
            FAIL=$((FAIL + 1))
        fi
    else
        log_error "GPG verification FAILED for ${SIGNED_ARCHIVE}"
        FAIL=$((FAIL + 1))
    fi
    rm -f "${DECRYPTED_TAR}"
else
    log_info "No signed archive provided – skipping GPG verification"
fi

# ─── 3. SHA-256 Hash Verification ────────────────────────────────────────────
if [[ -n "${HASH_FILE}" && -f "${HASH_FILE}" ]]; then
    log_info "Verifying SHA-256 hash against ${HASH_FILE}"
    EXPECTED_HASH=$(awk '{print $1}' "${HASH_FILE}")
    save_image
    ACTUAL_HASH=$(sha256sum "${SAVED_TAR}" | awk '{print $1}')
    if [[ "${EXPECTED_HASH}" == "${ACTUAL_HASH}" ]]; then
        log_ok "SHA-256 hash matches (${ACTUAL_HASH})"
        PASS=$((PASS + 1))
    else
        log_error "SHA-256 hash MISMATCH"
        log_error "  Expected : ${EXPECTED_HASH}"
        log_error "  Actual   : ${ACTUAL_HASH}"
        FAIL=$((FAIL + 1))
    fi
else
    log_info "No hash file provided – computing live SHA-256 for reference"
    save_image
    ACTUAL_HASH=$(sha256sum "${SAVED_TAR}" | awk '{print $1}')
    log_info "Live SHA-256: ${ACTUAL_HASH}"
fi

# ─── Cleanup ─────────────────────────────────────────────────────────────────
[[ -n "${SAVED_TAR}" ]] && rm -f "${SAVED_TAR}"

# ─── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════"
echo "  Verification Summary for: ${IMAGE_REF}"
echo "  Checks passed : ${PASS}"
echo "  Checks failed : ${FAIL}"
echo "══════════════════════════════════════════════════"

if [[ "${FAIL}" -gt 0 ]]; then
    log_error "Verification FAILED – deployment blocked"
    exit 1
fi
log_ok "All verification checks passed – safe to deploy"
