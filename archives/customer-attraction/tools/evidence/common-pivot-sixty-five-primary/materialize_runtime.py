"""Verify/copy only the ten-file original reopt runtime; execute nothing."""
from pathlib import Path
import argparse,json,hashlib,shutil
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
pkg=Path(__file__).resolve().parent;repo=a.repo.resolve();out=a.output.resolve()
assert not out.exists(), 'destination must be new'
assert out!=repo and repo not in out.parents, 'runtime must be outside repository'
records=json.loads((pkg/'dependency-manifest.json').read_text())
for d in records:
 src=pkg/d['package_saved_path'] if 'package_saved_path' in d else repo/d['repo_saved_path']
 data=src.read_bytes();assert len(data)==d['size'] and hashlib.sha256(data).hexdigest()==d['sha256']
for d in records:
 src=pkg/d['package_saved_path'] if 'package_saved_path' in d else repo/d['repo_saved_path']
 dest=out/d['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
print(json.dumps({'files_copied':len(records),'runtime':str(out),'original_entries_executed':0},indent=2))
