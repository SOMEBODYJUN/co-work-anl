"""Copy only the frozen writer and its two exact dependencies into a new folder."""
from pathlib import Path
from hashlib import sha256
import json,sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]


def main():
    if len(sys.argv)!=2:raise SystemExit('usage: materialize_runtime.py NEW_ABSOLUTE_DIRECTORY')
    dest=Path(sys.argv[1]);assert dest.is_absolute();dest.mkdir(parents=True,exist_ok=False)
    code=(HERE/'original/materialize_diagonal_seeds.py').read_bytes()
    assert sha256(code).hexdigest()=='e43a5b4187dd184c46b31e6483d1e3f8b458399eeb2d7c6fe7f65187301aff83'
    (dest/'materialize_diagonal_seeds.py').write_bytes(code)
    for rec in json.loads((HERE/'input-manifest.json').read_text())['files']:
        data=(REPO/rec['path']).read_bytes();assert len(data)==rec['size'] and sha256(data).hexdigest()==rec['sha256']
        (dest/rec['runtime_name']).write_bytes(data)
    print(json.dumps({'status':'restored three frozen files only; no writer or game solver run','root':str(dest)},indent=2))


if __name__=='__main__':main()
