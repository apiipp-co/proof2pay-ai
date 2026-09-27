#!/usr/bin/env bash
set -euo pipefail

LANGFLOW_BIN="${LANGFLOW_BIN:-$HOME/.langflow/.langflow-venv/bin/langflow}"
DATA_DIR="${PROOF2PAY_LANGFLOW_DATA_DIR:-$HOME/Library/Application Support/Proof2Pay Langflow}"

if [[ ! -x "$LANGFLOW_BIN" ]]; then
  printf 'Langflow belum ditemukan di %s\n' "$LANGFLOW_BIN" >&2
  printf 'Instal Langflow Desktop, atau set LANGFLOW_BIN ke executable Langflow.\n' >&2
  exit 1
fi

mkdir -p "$DATA_DIR"
if [[ ! -f "$DATA_DIR/database.db" ]]; then
  printf 'Database demo lokal belum ada: %s/database.db\n' "$DATA_DIR" >&2
  printf 'Import JSON dari langflow/exports/ ke project baru, lalu perbarui .bob/mcp.json.\n' >&2
  exit 1
fi

export LANGFLOW_CONFIG_DIR="$DATA_DIR/config"
export LANGFLOW_DATABASE_URL="sqlite:///$DATA_DIR/database.db"
export LANGFLOW_AUTO_LOGIN=true
export LANGFLOW_SKIP_AUTH_AUTO_LOGIN=true
export DO_NOT_TRACK=true

printf 'Langflow demo lokal: http://127.0.0.1:7862\n'
printf 'Hanya untuk mesin pribadi; auto-login aktif dan server dibatasi ke 127.0.0.1.\n'
exec "$LANGFLOW_BIN" run --host 127.0.0.1 --port 7862 --no-open-browser
