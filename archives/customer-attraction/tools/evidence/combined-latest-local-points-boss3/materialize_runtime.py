"""Restore the frozen 47-file dependency tree and overlay two primary points.

No repository-control command, mathematical builder, optimizer or network is run.
"""
from pathlib import Path
import sys,json,subprocess,hashlib
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py /absolute/new-runtime')
    dest=Path(sys.argv[1])
    if not dest.is_absolute() or dest.exists():raise SystemExit('supply a fresh absolute runtime directory')
    tool=REPO/'archives/customer-attraction/tools/evidence/combined-branch-master-program/materialize_runtime.py'
    subprocess.run([sys.executable,'-B',str(tool),str(dest)],check=True)
    for rec in json.loads((HERE/'source-manifest.json').read_text()):
        data=(HERE/rec['stored_path']).read_bytes()
        assert len(data)==rec['size'] and hashlib.sha256(data).hexdigest()==rec['sha256']
        target=dest/rec['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print(json.dumps({'status':'materialized; no research or Git entrypoint invoked','frozen_base_sources':47,'primary_point_overlays':2,'root':str(dest)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
