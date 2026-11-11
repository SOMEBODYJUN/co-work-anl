"""Materialize byte-exact archived frozen sources, without overwriting edits."""
from pathlib import Path
from hashlib import sha256
import gzip
import json

W=Path(__file__).resolve().parent
manifests=sorted(W.glob('portable_frozen_text*/manifest.json'))
assert manifests, 'No exact frozen-text manifests are available.'
items=[item for path in manifests for item in json.loads(path.read_text())['files']]
assert len({item['target'] for item in items})==len(items), 'Duplicate restoration targets.'
for item in items:
    payload=gzip.decompress((W/item['archive']).read_bytes())
    assert sha256(payload).hexdigest()==item['sha256']
    target=W/item['target']
    if target.exists():
        assert target.read_bytes()==payload, 'Preserve a later edit instead of overwriting: '+str(target)
        status='already byte-exact'
    else:
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as out:
            out.write(payload)
        status='restored byte-exact'
    print(item['target']+': '+status)
