#!/usr/bin/env sh
set -euo pipefail

# Modes: http | socket | worker
MODE="${MODE:-http}"

echo "[entrypoint] Running DB migrations..."
zebras db upgrade || {
  echo "[entrypoint] Migration failed" >&2
  exit 1
}

case "$MODE" in
  http)
    PORT_RUNTIME="${PORT:-${ZEBRAS_HTTP_PORT:-43117}}"
    echo "[entrypoint] Starting HTTP server on ${ZEBRAS_HTTP_HOST:-0.0.0.0}:${PORT_RUNTIME}"
    exec zebras http --host "${ZEBRAS_HTTP_HOST:-0.0.0.0}" --port "${PORT_RUNTIME}"
    ;;
  socket)
    echo "[entrypoint] Starting Socket Mode app"
    exec zebras socket
    ;;
  worker)
    echo "[entrypoint] Starting RQ worker"
    exec zebras worker
    ;;
  *)
    echo "[entrypoint] Unknown MODE: $MODE" >&2
    exit 2
    ;;
esac
