"""Restore the eight frozen sources and three specified inputs; run no program."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--destination', type=Path, required=True)
    args = ap.parse_args()
    evidence = Path(__file__).resolve().parent
    sources = json.loads((evidence / 'source-manifest.json').read_text())
    related = json.loads((evidence / 'related-input-manifest.json').read_text())
    copies = [(evidence / 'original' / row['id'] / Path(row['path']).name, row) for row in sources]
    copies += [(evidence / row['evidence_path'], row) for row in related]
    for source, row in copies:
        relative = Path(row['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        data = source.read_bytes()
        assert len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256']
    args.destination.mkdir(parents=True, exist_ok=False)
    for source, row in copies:
        target = args.destination / row['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(source.read_bytes())
    print(json.dumps({'restored_files': len(copies), 'destination': str(args.destination),
                      'program_imports_or_execution': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
