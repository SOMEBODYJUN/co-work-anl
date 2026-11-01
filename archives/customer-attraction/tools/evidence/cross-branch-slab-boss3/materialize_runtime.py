"""Restore original paths from existing frozen manifests; never run the old code."""
from pathlib import Path
from hashlib import sha256
import json,sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]


def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py NEW_ABSOLUTE_RUNTIME')
    dest=Path(sys.argv[1]);assert dest.is_absolute();dest.mkdir(parents=True,exist_ok=False)
    packs=[('archives/customer-attraction/tools/evidence/combined-branch-master-program/source-manifest.json','frozen_sources'),('archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/source-manifest.json','sources'),('archives/customer-attraction/tools/evidence/coupled-latest-menu-check-boss3/source-manifest.json','sources')]
    records=[r for path,key in packs for r in json.loads((REPO/path).read_text())[key]]+json.loads((HERE/'source-manifest.json').read_text())['sources']
    for rec in records:
        saved=rec.get('stored_path',rec.get('preserved_at'));data=(REPO/saved).read_bytes()
        assert len(data)==rec['size'] and sha256(data).hexdigest()==rec['sha256'],rec['id']
        target=dest/rec['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    (dest/'work.py').write_text('# Directory marker only; not imported or executed.\n')
    print(json.dumps({'status':'restored exact source inputs only; no historical entrypoint or solver run','files':len(records),'root':str(dest)},indent=2))


if __name__=='__main__':main()
