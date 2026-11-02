"""Copy frozen source/input bytes to an explicit external root; never run them."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('target',type=Path)
    a=p.parse_args()
    here=Path(__file__).resolve().parent
    repo=here.parents[4]
    target=a.target.expanduser().resolve()
    if target==repo or repo in target.parents:
        raise ValueError('target must be outside the source repository')
    if target.exists() and any(target.iterdir()):
        raise FileExistsError('target must be absent or empty')
    todo=[]
    src=json.loads((here/'source-manifest.json').read_text())
    for r in src['sources']:
        todo.append((repo/r['preserved_path'],target/r['path'],r['sha256']))
    for entry in json.loads((here/'input-routing.json').read_text())['inputs']:
        for r in entry['input_pair']:
            todo.append((repo/r['preserved_path'],target/r['path'],r['sha256']))
    for source,dest,expected in todo:
        data=source.read_bytes()
        if hashlib.sha256(data).hexdigest()!=expected:
            raise ValueError(f'input hash mismatch: {source}')
    for source,dest,expected in todo:
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,dest)
    print(json.dumps({'copied_files':len(todo),'target':str(target),'executed_original_entries':0}))

if __name__=='__main__':
    main()
