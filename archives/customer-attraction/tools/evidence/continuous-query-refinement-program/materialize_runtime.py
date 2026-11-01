"""Restore a new isolated input layout; do not run the original program."""
from pathlib import Path
from hashlib import sha256
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: materialize_runtime.py /absolute/new-runtime-directory')
    dest = Path(sys.argv[1])
    if not dest.is_absolute():
        raise SystemExit('destination must be absolute')
    dest.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    count = 0
    for rec in manifest['runtime_sources']:
        data = (REPO / rec['stored_path']).read_bytes()
        assert len(data) == rec['size'] and sha256(data).hexdigest() == rec['sha256'], rec['id']
        target = dest / rec['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        count += 1
    (dest / 'work.py').write_text('# ROOT-location marker only; never imported or executed.\n')
    print(json.dumps({'status': 'materialized; no historical program executed',
                      'frozen_files': count, 'root': str(dest)}, indent=2))


if __name__ == '__main__':
    main()
