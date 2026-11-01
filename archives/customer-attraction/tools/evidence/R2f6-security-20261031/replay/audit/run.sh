#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$here/source/audit_flat_security_increment.py" > "$here/replay.stdout.json" 2> "$here/replay.stderr.txt"
cp "$here/source/flat_security_increment_certificate.json" "$here/replay-generated-flat_security_increment_certificate.json"
