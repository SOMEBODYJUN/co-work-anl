"""Copy the eight frozen files into a caller-selected new empty source root.

This helper does not execute any original program and never overwrites an
existing nonempty directory. Original reports remain separately preserved.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    destination = args.destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit('destination must be new or empty')
    files = []
    for name, subdir in [('source-manifest.json', 'original'), ('related-input-manifest.json', 'related-inputs')]:
        for row in json.loads((HERE / name).read_text()):
            source = HERE / subdir / row['id'] / Path(row['path']).name
            raw = source.read_bytes()
            assert len(raw) == row['size']
            assert hashlib.sha256(raw).hexdigest() == row['sha256']
            target = destination / row['path']
            assert target.resolve().is_relative_to(destination)
            files.append((source, target))
    for source, target in files:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(json.dumps({'copied_files': len(files), 'destination': str(destination), 'original_programs_executed': 0}))


if __name__ == '__main__':
    main()
