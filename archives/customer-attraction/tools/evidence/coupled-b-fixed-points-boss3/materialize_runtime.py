"""Restore frozen rows and witnesses in a new isolated directory; do not run them."""
from pathlib import Path
from hashlib import sha256
import json,sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]


def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py NEW_ABSOLUTE_RUNTIME')
    dest=Path(sys.argv[1]);assert dest.is_absolute();dest.mkdir(parents=True,exist_ok=False)
    base=REPO/'archives/customer-attraction/tools/evidence/combined-branch-master-program/source-manifest.json'
    inherited=json.loads(base.read_text())['frozen_sources'];primary=json.loads((HERE/'source-manifest.json').read_text())['sources']
    checked=[]
    for source in inherited+primary:
        saved=source.get('stored_path',source.get('preserved_at'));data=(REPO/saved).read_bytes()
        assert len(data)==source['size'] and sha256(data).hexdigest()==source['sha256'],source['id']
        target=dest/source['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);checked.append(source['id'])
    (dest/'work.py').write_text('# Directory marker only; never imported or executed.\n')
    print(json.dumps({'status':'restored frozen inputs only; no row builder or mathematical entrypoint executed','files_checked_and_copied':len(checked),'root':str(dest)},indent=2))


if __name__=='__main__':main()
