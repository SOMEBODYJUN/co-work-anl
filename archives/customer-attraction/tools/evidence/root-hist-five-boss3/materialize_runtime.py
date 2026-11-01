"""Copy the SHA-bound original layout to a NEW external directory, without running it."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--repo-root',required=True,type=Path)
ap.add_argument('--destination',required=True,type=Path)
args=ap.parse_args()
repo=args.repo_root.resolve();dest=args.destination.resolve()
if dest.exists():raise SystemExit('destination must not exist; original programs overwrite reports')
if dest==repo or repo in dest.parents:raise SystemExit('use a destination outside the repository')
manifest=json.loads(Path(__file__).with_name('dependency-manifest.json').read_text())
prepared=[]
for r in manifest['files']:
    source=(repo/r['preserved_at']).resolve();target=(dest/r['runtime_relative_path']).resolve()
    if repo not in source.parents or dest not in target.parents:raise SystemExit('nonrelative manifest path')
    data=source.read_bytes()
    if len(data)!=r['size']or hashlib.sha256(data).hexdigest()!=r['sha256']:
        raise SystemExit('source hash or size mismatch: '+r['preserved_at'])
    prepared.append((source,target))
for source,target in prepared:
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
print(json.dumps({'materialized_files':len(prepared),'destination':str(dest),'source_import_exec_or_solver_runs':0}))
