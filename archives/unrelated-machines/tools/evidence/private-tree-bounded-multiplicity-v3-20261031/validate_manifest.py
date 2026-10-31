#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parent
m=json.loads((base/'manifest.json').read_text())
for s in m['sources']:
    p=base/s['evidence_path'].split('private-tree-bounded-multiplicity-v3-20261031/',1)[-1]
    data=p.read_bytes()
    assert len(data)==s['size'],(s['id'],len(data),s['size'])
    assert hashlib.sha256(data).hexdigest()==s['source_sha256'],s['id']
print('PASS',len(m['sources']))
