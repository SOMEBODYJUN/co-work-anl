"""Copy the hash-bound original input closure into a fresh destination; run nothing.

This restores the original relative import paths for optional future studies.
The original LP probe writes results.json beside its source, so the preserved
archive should never be used as a discovery run's working copy.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import shutil


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repository',type=Path,required=True)
    ap.add_argument('--destination',type=Path,required=True)
    args=ap.parse_args()
    evidence=Path(__file__).resolve().parent
    repository=args.repository.resolve()
    destination=args.destination.resolve()
    if destination.exists():
        raise FileExistsError(destination)
    rows=[]
    for name in ('source-manifest.json','dependency-manifest.json'):
        rows.extend(json.loads((evidence/name).read_text()))
    verified=[]
    for row in rows:
        source=repository/row['preserved_path']
        data=source.read_bytes()
        if len(data)!=row['size'] or sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('Frozen input fingerprint mismatch: '+row['path'])
        target=destination/row['path']
        if not target.is_relative_to(destination):
            raise ValueError('Unsafe source path')
        verified.append((source,target,row))
    destination.mkdir(parents=True,exist_ok=False)
    for source,target,row in verified:
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
    print(json.dumps({'status':'materialized-only; no program executed',
                      'destination':str(destination),'files':len(verified)},ensure_ascii=False))


if __name__=='__main__':
    main()
