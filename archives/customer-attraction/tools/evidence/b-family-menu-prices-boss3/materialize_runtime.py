"""Recreate the frozen dependency tree and overlay this package's originals.

No research entrypoint, network, repository-control command, or optimizer is run.
"""
from pathlib import Path
import sys,json,hashlib,subprocess
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
OLD_R2=Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2')

def source_and_target(rec):
    # The current source manifest records repository-relative local_original or
    # local_replay; earlier versions used a package-relative stored_path.
    if 'local_original' in rec:
        source=REPO/rec['local_original']
    elif 'local_replay' in rec:
        source=REPO/rec['local_replay']
    else:
        source=HERE/rec['stored_path']
    target=Path(rec['path']) if 'path' in rec else OLD_R2/rec['basename']
    if not source.resolve().is_relative_to(REPO.resolve()) or target.is_absolute() or '..' in target.parts:
        raise ValueError('manifest paths must stay in the repository/runtime')
    return source,target

def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py /absolute/new-runtime')
    dest=Path(sys.argv[1])
    if not dest.is_absolute() or dest.exists():raise SystemExit('supply a fresh absolute runtime directory')
    base=REPO/'archives/customer-attraction/tools/evidence/combined-branch-master-program/materialize_runtime.py'
    subprocess.run([sys.executable,'-B',str(base),str(dest)],check=True)
    manifest=json.loads((HERE/'source-manifest.json').read_text())
    for rec in manifest:
        source,relative=source_and_target(rec)
        data=source.read_bytes()
        assert len(data)==rec['size'] and hashlib.sha256(data).hexdigest()==rec['sha256'],rec['id']
        target=dest/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    # This original point is retained and used by the documented optional
    # maxroot audit, but was omitted from the current eight-record manifest.
    point=HERE/'original/research_2/maxroot_identity_exact.json'
    data=point.read_bytes()
    assert len(data)==1440157 and hashlib.sha256(data).hexdigest()=='d3c456a03806aef08378e96f89387b83d77161081a260b3764b8aa8f8097d43a'
    (dest/OLD_R2/point.name).write_bytes(data)
    print(json.dumps({'status':'materialized; no mathematical entrypoint executed','base_frozen_files':47,'manifest_sources':len(manifest),'supplemental_original_points':1,'overlaid_sources':len(manifest)+1,'root':str(dest)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
