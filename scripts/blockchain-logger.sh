#!/usr/bin/env bash
# ╔═══════════════════════════════════════════════════════════════════╗
# ║   Infinite Server26 - Blockchain Audit Logger                    ║
# ║   Pushes build/deployment logs to the Hyperledger Fabric ledger  ║
# ║                                                                   ║
# ║   Prerequisites:                                                  ║
# ║   • A running Hyperledger Fabric network with an orderer service  ║
# ║   • A created and joined channel (default: mychannel)             ║
# ║   • Chaincode deployed that implements PutLog(key,value,ts,hash) ║
# ║   • The 'peer' CLI binary on PATH                                 ║
# ║   • Fabric MSP environment vars set (CORE_PEER_*, FABRIC_CFG_PATH)║
# ╚═══════════════════════════════════════════════════════════════════╝
set -euo pipefail

PEER_HOST="${BLOCKCHAIN_PEER_HOST:-localhost}"
ORDERER_HOST="${BLOCKCHAIN_ORDERER_HOST:-${PEER_HOST}}"
ORDERER_PORT="${BLOCKCHAIN_ORDERER_PORT:-7050}"
CHANNEL_NAME="${BLOCKCHAIN_CHANNEL:-mychannel}"
CHAINCODE_NAME="${CHAINCODE_NAME:-mychaincode}"
LOG_KEY="${1:-}"
LOG_VALUE="${2:-}"

usage() {
    cat <<EOF
Usage: $0 <key> <value>

Log an immutable entry to the Hyperledger Fabric blockchain ledger.

Arguments:
  key    Unique identifier for this log entry (e.g. "image_hash", "build_id")
  value  Value to record (e.g. sha256 hash string or JSON blob)

Environment variables:
  BLOCKCHAIN_PEER_HOST     Fabric peer hostname        (default: localhost)
  BLOCKCHAIN_ORDERER_HOST  Fabric orderer hostname     (default: PEER_HOST)
  BLOCKCHAIN_ORDERER_PORT  Fabric orderer port         (default: 7050)
  BLOCKCHAIN_CHANNEL       Fabric channel name         (default: mychannel)
  CHAINCODE_NAME           Chaincode to invoke         (default: mychaincode)
  BLOCKCHAIN_AUDIT_LOG     Local fallback log file     (default: /var/log/blockchain-audit.log)

Examples:
  $0 image_hash "\$(cat image_hash.sha256)"
  $0 build_id   "run-42-commit-abc1234"
EOF
    exit 1
}

if [[ -z "${LOG_KEY}" || -z "${LOG_VALUE}" ]]; then
    usage
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ENTRY_HASH=$(printf '%s:%s:%s' "${LOG_KEY}" "${LOG_VALUE}" "${TIMESTAMP}" | sha256sum | awk '{print $1}')

log_info()  { echo "[INFO]  $(date -u +"%Y-%m-%dT%H:%M:%SZ") $*"; }
log_error() { echo "[ERROR] $(date -u +"%Y-%m-%dT%H:%M:%SZ") $*" >&2; }

log_info "Preparing blockchain log entry"
log_info "  Key       : ${LOG_KEY}"
log_info "  Timestamp : ${TIMESTAMP}"
log_info "  Entry hash: ${ENTRY_HASH}"

# ─── Attempt peer CLI invocation ─────────────────────────────────────────────
if command -v peer &>/dev/null; then
    # Build the JSON arguments safely using jq to prevent injection
    if command -v jq &>/dev/null; then
        CHAINCODE_ARGS=$(jq -nc \
            --arg fn  "PutLog" \
            --arg key "${LOG_KEY}" \
            --arg val "${LOG_VALUE}" \
            --arg ts  "${TIMESTAMP}" \
            --arg hsh "${ENTRY_HASH}" \
            '{"function":$fn,"Args":[$key,$val,$ts,$hsh]}')
    else
        # jq not available – manually escape double-quotes and backslashes only
        SAFE_KEY=$(printf '%s' "${LOG_KEY}"   | sed 's/\\/\\\\/g; s/"/\\"/g')
        SAFE_VAL=$(printf '%s' "${LOG_VALUE}" | sed 's/\\/\\\\/g; s/"/\\"/g')
        CHAINCODE_ARGS="{\"function\":\"PutLog\",\"Args\":[\"${SAFE_KEY}\",\"${SAFE_VAL}\",\"${TIMESTAMP}\",\"${ENTRY_HASH}\"]}"
    fi

    log_info "Invoking chaincode on ${PEER_HOST}:7051 via orderer ${ORDERER_HOST}:${ORDERER_PORT}"
    peer chaincode invoke \
        -o "${ORDERER_HOST}:${ORDERER_PORT}" \
        -C "${CHANNEL_NAME}" \
        -n "${CHAINCODE_NAME}" \
        -c "${CHAINCODE_ARGS}" \
        --peerAddresses "${PEER_HOST}:7051" 2>&1 \
        && log_info "Log committed to ledger (key=${LOG_KEY} hash=${ENTRY_HASH})" \
        || log_error "peer chaincode invoke failed – falling back to local log"
else
    log_info "peer CLI not available – writing to local audit log instead"
fi

# ─── Always write a local append-only audit log as fallback ──────────────────
AUDIT_LOG="${BLOCKCHAIN_AUDIT_LOG:-/var/log/blockchain-audit.log}"
mkdir -p "$(dirname "${AUDIT_LOG}")"
printf '%s\t%s\t%s\t%s\n' "${TIMESTAMP}" "${LOG_KEY}" "${ENTRY_HASH}" "${LOG_VALUE}" \
    >> "${AUDIT_LOG}"
log_info "Audit entry appended to ${AUDIT_LOG}"
