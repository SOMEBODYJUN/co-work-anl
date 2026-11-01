"""Copy checked frozen inputs into a fresh root; execute no old entrypoint."""
from pathlib import Path
from hashlib import sha256
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: materialize_runtime.py /absolute/new-runtime-root')
    dest = Path(sys.argv[1])
    assert dest.is_absolute()
    dest.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    base = json.loads((REPO / manifest['base_frozen_manifest']).read_text())
    records = base['frozen_sources'] + manifest['supplemental_frozen_sources']
    seen = set()
    for rec in records:
        data = (REPO / rec['stored_path']).read_bytes()
        assert len(data) == rec['size'] and sha256(data).hexdigest() == rec['sha256']
        target = dest / rec['path']
        assert target not in seen
        seen.add(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (dest / 'work.py').write_text('# Root-location marker only; no executable behavior.\n')
    print(json.dumps({'status': 'materialized only; no original entrypoint executed', 'files': len(records), 'root': str(dest)}, indent=2))


if __name__ == '__main__':
    main()
