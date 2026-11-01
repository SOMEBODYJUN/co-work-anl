"""Materialize exact inputs in a fresh directory; never execute the old program."""
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
    checked = 0
    for rec in manifest['frozen_sources']:
        data = (REPO / rec['stored_path']).read_bytes()
        assert len(data) == rec['size'] and sha256(data).hexdigest() == rec['sha256'], rec['id']
        target = dest / rec['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        checked += 1
    (dest / 'work.py').write_text('# Root-location marker only; no executable behavior.\n')
    print(json.dumps({'status': 'materialized; no historical entrypoint invoked',
                      'frozen_files': checked, 'root': str(dest)}, indent=2))


if __name__ == '__main__':
    main()
