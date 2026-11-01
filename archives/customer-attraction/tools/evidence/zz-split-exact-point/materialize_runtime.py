"""Recreate the frozen split verification tree; copy/hash only, no original run."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import json


def main():
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--dest',type=Path,required=True);a=p.parse_args()
    here=Path(__file__).resolve().parent
    records=json.loads((here/'rerun/runtime-manifest.json').read_text())
    assert not a.dest.exists()
    prepared=[]
    for r in records:
        rel=Path(r['original_path']);assert not rel.is_absolute() and '..' not in rel.parts
        raw=(a.repo/r['stored_path']).read_bytes()
        assert len(raw)==r['bytes'] and sha256(raw).hexdigest()==r['sha256']
        prepared.append((rel,raw))
    a.dest.mkdir(parents=True);(a.dest/'work.py').write_text('# Inert root marker; never execute.\n')
    for rel,raw in prepared:
        target=a.dest/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        assert target.read_bytes()==raw
    print(json.dumps({'status':'MATERIALIZED_ONLY','frozen_files':len(records),'original_main_calls':0,'LP_calls':0,'destination':str(a.dest.resolve())},indent=2))


if __name__=='__main__':main()
