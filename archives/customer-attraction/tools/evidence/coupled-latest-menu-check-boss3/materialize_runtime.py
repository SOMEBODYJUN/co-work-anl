"""Copy frozen dependencies and four current primary files; run no mathematics."""
from pathlib import Path
from hashlib import sha256
import json,sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]


def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py NEW_ABSOLUTE_RUNTIME')
    dest=Path(sys.argv[1]);assert dest.is_absolute();dest.mkdir(parents=True,exist_ok=False)
    base=json.loads((REPO/'archives/customer-attraction/tools/evidence/combined-branch-master-program/source-manifest.json').read_text())['frozen_sources']
    older=json.loads((REPO/'archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/source-manifest.json').read_text())['sources']
    newer=json.loads((HERE/'source-manifest.json').read_text())['sources']
    for rec in base+older+newer:
        stored=rec.get('stored_path',rec.get('preserved_at'));data=(REPO/stored).read_bytes()
        assert len(data)==rec['size'] and sha256(data).hexdigest()==rec['sha256'],rec['id']
        target=dest/rec['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    (dest/'work.py').write_text('# Directory marker only; not executable research code.\n')
    print(json.dumps({'status':'materialized frozen inputs; no historical entrypoint invoked','files':len(base+older+newer),'root':str(dest)},indent=2))


if __name__=='__main__':main()
