#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root="$here/source-root"
sec="$root/research/workspaces/customer-attraction/R-2f6cae284faf43fea7a09c0a4fe7c679/security"
python3 "$sec/check_local_slope.py" > "$here/replay.stdout.jsonl" 2> "$here/replay.stderr.txt"
cp "$sec/local_slope_check.json" "$here/replay-generated-local_slope_check.json"
