#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[ -f .env ] && { set -a; . .env; set +a; }
PY="${PYTHON_BIN:-python}"

case "${1:-}" in
  train) shift; exec "$PY" -m {{PACKAGE_NAME}}.train "$@" ;;
  infer) shift; exec "$PY" -m {{PACKAGE_NAME}}.infer "$@" ;;
  eval)  shift; exec "$PY" -m {{PACKAGE_NAME}}.eval "$@" ;;
  *)
    echo "usage: bash scripts/run.sh <train|infer|eval> [args...]" >&2
    exit 2
    ;;
esac
