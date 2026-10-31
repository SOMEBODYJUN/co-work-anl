#!/usr/bin/env bash
# Reuse this clone's checkpoint authentication for the equal-peer public board.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/board_entry.py" "$@"
