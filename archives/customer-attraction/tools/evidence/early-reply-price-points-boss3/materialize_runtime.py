"""Restore the frozen dependency layout without invoking research or Git."""
from pathlib import Path
import sys,subprocess,json,hashlib
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py /absolute/new-runtime')
    dest=Path(sys.argv[1])
    if not dest.is_absolute() or dest.exists():raise SystemExit('supply a fresh absolute runtime directory')
    base=REPO/'archives/customer-attraction/tools/evidence/combined-branch-master-program/materialize_runtime.py'
    subprocess.run([sys.executable,'-B',str(base),str(dest)],check=True)
    manifest=json.loads((HERE/'source-manifest.json').read_text())
    for rec in manifest:
        source=(HERE if rec['storage_scope']=='package' else REPO)/rec['stored_path']
        data=source.read_bytes()
        assert len(data)==rec['size'] and hashlib.sha256(data).hexdigest()==rec['sha256'],rec['id']
        target=dest/rec['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print(json.dumps({'status':'materialized; no mathematical entrypoint or network invoked','base_frozen_sources':47,'overlay_primary_sources':4,'root':str(dest)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
