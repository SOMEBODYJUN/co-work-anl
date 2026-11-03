"""Copy the declared original files to a fresh tree; no mathematical execution."""
from pathlib import Path
import argparse,hashlib,json,shutil

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    repo=a.repo.resolve();out=a.out.resolve();base=Path(__file__).resolve().parent
    if out.exists():raise SystemExit('Output must be a new directory')
    records=[]
    for s in json.loads((base/'source-manifest.json').read_text()):records.append((s['saved_path'],s['path'],s['size'],s['sha256']))
    for s in json.loads((base/'dependency-manifest.json').read_text()):
        if 'materialize_to' in s:records.append((s['path'],s['materialize_to'],s['size'],s['sha256']))
    checked=[]
    for src,dst,size,digest in records:
        source=(repo/src).resolve();target=(out/dst).resolve()
        if not source.is_relative_to(repo) or not target.is_relative_to(out):raise SystemExit('Unsafe relative path')
        data=source.read_bytes()
        if len(data)!=size or hashlib.sha256(data).hexdigest()!=digest:raise SystemExit('Source bytes differ: '+src)
        checked.append((source,target))
    out.mkdir(parents=True)
    for source,target in checked:target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    print(json.dumps({'files_copied':len(checked),'mathematical_programs_run':0,'out':str(out)}))
if __name__=='__main__':main()
