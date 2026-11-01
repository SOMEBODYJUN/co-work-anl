"""Copy the frozen cascade sources/dependencies to a new tree; execute nothing."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    evidence = Path(__file__).resolve().parent
    sources = json.loads((evidence / 'source-manifest.json').read_text())
    dependencies = json.loads((evidence / 'dependency-manifest.json').read_text())
    copies = []
    for entry in sources:
        source = evidence / 'original' / entry['id'] / Path(entry['path']).name
        copies.append((source, Path(entry['path']), entry))
    for entry in dependencies:
        copies.append((evidence / entry['evidence_path'], Path(entry['runtime_path']), entry))
    for source, relative, entry in copies:
        assert not relative.is_absolute() and '..' not in relative.parts
        data = source.read_bytes()
        assert len(data) == entry['size']
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
    args.destination.mkdir(parents=True, exist_ok=False)
    for source, relative, _ in copies:
        target = args.destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(source.read_bytes())
    print(json.dumps({'restored_files': len(copies), 'destination': str(args.destination),
                      'program_imports_or_execution': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
