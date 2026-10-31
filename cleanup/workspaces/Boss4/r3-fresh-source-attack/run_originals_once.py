"""Capture the complete frozen scan directories and run each original main once."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time
import numpy
import scipy

REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-fresh-source-attack')
EV=STAGE/'archives/customer-attraction/tools/evidence/optimal-fresh-source-attack-primary'
PRIMARY=['e34ee6479d87bca78052','c320561014ad69bbebf0','2abfdaad5623537eeb3a','7cfd730044a42f607965','4ff936ca40b885e9237f']
CODE_IDS=['e34ee6479d87bca78052','2abfdaad5623537eeb3a']
OUTPUT_IDS=['c320561014ad69bbebf0','7cfd730044a42f607965']
PREFIXES=['evidence/certificates/customer_attraction/','examples/customer_attraction/']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
    records=[json.loads(l) for l in (REPO/'cleanup/inventory.jsonl').read_text().splitlines()]
    inv={r['id']:r for r in records}
    scanned=[r for r in records if any(r['path'].startswith(p) and r['path'][len(p):].endswith('.json') and '/' not in r['path'][len(p):] for p in PREFIXES)]
    tree=EV/'replay-tree'
    replay=EV/'replay'
    replay.mkdir(parents=True,exist_ok=True)
    assert not (replay/'execution.json').exists(),'Do not execute original mains twice'
    frozen=[]
    for row in [inv[sid] for sid in PRIMARY]+scanned:
        first=None
        locations=[]
        for source in row['sources']:
            raw=subprocess.check_output(['git','show',source['commit']+':'+source['path']],cwd=REPO,timeout=30)
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or raw==first
            first=raw
            locations.append(dict(source,bytes_verified=True))
        original=EV/'original'/row['path']
        original.parent.mkdir(parents=True,exist_ok=True)
        original.write_bytes(first)
        if row['id'] in CODE_IDS or row in scanned:
            target=tree/row['path']
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(first)
        frozen.append(dict(id=row['id'],path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary' if row['id'] in PRIMARY else 'frozen-scan-directory-input',saved_path=str(original.relative_to(STAGE))))
    code_inputs=[r for r in frozen if r['id'] in CODE_IDS or r['role']=='frozen-scan-directory-input']
    run_records=[]
    for sid,outid,label in zip(CODE_IDS,OUTPUT_IDS,['exact-fresh','float-policy-cones']):
        entry=tree/inv[sid]['path']
        start=time.time()
        result=subprocess.run([sys.executable,str(entry)],cwd=tree,capture_output=True,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        elapsed=time.time()-start
        (replay/(label+'.stdout.txt')).write_bytes(result.stdout)
        (replay/(label+'.stderr.txt')).write_bytes(result.stderr)
        output=tree/inv[outid]['path']
        raw=output.read_bytes() if output.exists() else b''
        (replay/Path(inv[outid]['path']).name).write_bytes(raw)
        frozen_raw=(EV/'original'/inv[outid]['path']).read_bytes()
        unchanged=all(sha((tree/r['path']).read_bytes())==r['sha256'] for r in code_inputs)
        run=dict(label=label,entrypoint_id=sid,command=[sys.executable,inv[sid]['path']],working_directory=str(tree),exit_code=result.returncode,wall_seconds=elapsed,executions_of_original_entrypoint=1,output_bytes=len(raw),generated_report_sha256=sha(raw),frozen_report_sha256=sha(frozen_raw),generated_report_byte_identical_to_frozen=raw==frozen_raw,input_and_code_bytes_unchanged=unchanged,stdout_sha256=sha(result.stdout),stderr_sha256=sha(result.stderr))
        run_records.append(run)
        write_json(replay/'execution.json',dict(python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,runs=run_records,scope='Each unmodified original main once; exact audit only checks stored terminal counts, floating attack varies four fixed policies. No general proof, exact dual or new SPE/half certificate follows.'))
        assert result.returncode==0 and unchanged
        print(json.dumps(run,ensure_ascii=False),flush=True)
    write_json(EV/'runtime-input-manifest.json',dict(primary_count=5,directory_json_files=len(scanned),frozen_sources=frozen,scan_prefixes=PREFIXES,scan_is_nonrecursive=True,comparison_sources_not_done=True))

if __name__=='__main__':
    main()
