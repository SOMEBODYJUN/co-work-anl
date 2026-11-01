"""Restore frozen dependencies and both fixed/source compact points.

No mathematical build, original main, solver or repository-control tool is run.
"""
from pathlib import Path
import json,hashlib,subprocess,sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py /absolute/new-runtime')
    dest=Path(sys.argv[1])
    if not dest.is_absolute() or dest.exists():raise SystemExit('supply a fresh absolute runtime directory')
    prior=REPO/'archives/customer-attraction/tools/evidence/pair-threshold-closure-program/materialize_runtime.py'
    subprocess.run([sys.executable,'-B',str(prior),str(dest)],check=True)
    for rec in json.loads((HERE/'related-manifest.json').read_text()):
        data=(REPO/rec['stored_path']).read_bytes()
        assert len(data)==rec['size'] and hashlib.sha256(data).hexdigest()==rec['sha256']
        target=dest/rec['path'];target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert target.read_bytes()==data
        else:target.write_bytes(data)
    for rec in json.loads((HERE/'source-manifest.json').read_text()):
        data=(HERE/rec['stored_path']).read_bytes()
        assert len(data)==rec['size'] and hashlib.sha256(data).hexdigest()==rec['sha256']
        target=dest/rec['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print(json.dumps({'status':'materialized only; no research or Git entrypoint invoked','base_available_frozen_files':50,'new_fixed_inputs':2,'primary_point_overlays':2,'root':str(dest)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
