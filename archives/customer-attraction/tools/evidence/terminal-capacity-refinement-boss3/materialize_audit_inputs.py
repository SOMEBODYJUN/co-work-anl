"""Copy the four hash-bound static audit inputs to a new external root.

Usage: python3 materialize_audit_inputs.py REPO NEW_EXTERNAL_ROOT
No mathematical entrypoint is invoked.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys

HERE=Path(__file__).resolve().parent


def main():
    repo,dest=map(lambda x:Path(x).resolve(),sys.argv[1:3])
    dest.mkdir(parents=True,exist_ok=False)
    inputs=json.loads((HERE/'independent-inputs-manifest.json').read_text())['inputs']
    for row in inputs:
        source=repo/row['relative_path'];target=dest/row['relative_path']
        assert source.stat().st_size==row['size']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        assert hashlib.sha256(target.read_bytes()).hexdigest()==row['sha256']
    print(json.dumps({'files':len(inputs),'root':str(dest),'mathematical_entries':0}))


if __name__=='__main__':
    main()
