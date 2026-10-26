"""Verify packaged bytes and safe names; this is not a mathematics proof."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
for row in manifest['files']:
    name = PurePosixPath(row['path'])
    assert not name.is_absolute() and '..' not in name.parts
    file = root / name
    assert file.is_file() and not file.is_symlink(), str(name)
    data = file.read_bytes()
    assert len(data) == row['size_bytes'], str(name)
    assert hashlib.sha256(data).hexdigest() == row['sha256'], str(name)
print(json.dumps({'status': 'PASS', 'files': len(manifest['files']),
                  'source_commit': manifest['source_commit'],
                  'scope': 'byte identity, not mathematical validity'}))
