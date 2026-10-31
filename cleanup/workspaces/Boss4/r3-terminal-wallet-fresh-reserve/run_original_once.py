"""Run the exact frozen terminal-wallet audit once in an isolated original-path tree."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

REPO = Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE = Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-terminal-wallet-fresh-reserve')
EVIDENCE = STAGE / 'archives/customer-attraction/tools/evidence/terminal-wallet-fresh-reserve-primary'
PRIMARY = ['30449824f9a39ec251e2','3beb17d5735520b90e84','53c66ec7d069d0a166ab','86f3b77f8de039cb76be','9da7c5510bd045b3d059']
DEPENDENCIES = ['a7579960b289fff40c97','ff1a437e39e730d230eb','be317a14860bf5650dfe']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    rows = {r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    original_records = []
    for sid in PRIMARY + DEPENDENCIES:
        row = rows[sid]
        raw = None
        locations = []
        for loc in row['sources']:
            data = subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30)
            assert len(data)==row['size'] and sha(data)==row['sha256']
            if raw is not None:
                assert raw==data
            raw=data
            locations.append(dict(loc,bytes_verified=True))
        target=EVIDENCE/'original'/row['path']
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(raw)
        original_records.append(dict(id=sid,role='primary' if sid in PRIMARY else 'runtime-dependency-only',blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,saved_path=str(target.relative_to(STAGE))))
    tree=EVIDENCE/'replay-tree'
    copied=[]
    for sid in ['3beb17d5735520b90e84']+DEPENDENCIES:
        row=rows[sid]
        target=tree/row['path']
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((EVIDENCE/'original'/row['path']).read_bytes())
        copied.append(dict(path=row['path'],sha256=sha(target.read_bytes())))
    entry=tree/rows['3beb17d5735520b90e84']['path']
    started=time.time()
    result=subprocess.run([sys.executable,str(entry)],cwd=tree,capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    elapsed=time.time()-started
    (EVIDENCE/'replay/stdout.txt').write_bytes(result.stdout)
    (EVIDENCE/'replay/stderr.txt').write_bytes(result.stderr)
    output=entry.parent/'terminal_wallet_exact_audit.json'
    frozen=(EVIDENCE/'original'/rows['53c66ec7d069d0a166ab']['path']).read_bytes()
    generated=output.read_bytes() if output.exists() else b''
    (EVIDENCE/'replay/terminal_wallet_exact_audit.json').write_bytes(generated)
    unchanged=all(sha((tree/r['path']).read_bytes())==r['sha256'] for r in copied)
    execution=dict(command=[sys.executable,str(entry.relative_to(tree))],working_directory=str(tree),python=sys.version,exit_code=result.returncode,wall_seconds=elapsed,executions_of_original_entrypoint=1,generated_report_sha256=sha(generated),frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=generated==frozen,input_and_code_bytes_unchanged=unchanged,stdout_sha256=sha(result.stdout),stderr_sha256=sha(result.stderr),scope='Full ordered-history ICs on two fixed certificates and all six terminal queries in each; this is the terminal program main(), distinct from the earlier cross-role import-only loader use. No general welfare proof follows from finite execution.')
    (EVIDENCE/'replay/execution.json').write_text(json.dumps(execution,ensure_ascii=False,indent=2)+'\n')
    (EVIDENCE/'runtime-input-manifest.json').write_text(json.dumps(dict(frozen_sources=original_records,replay_files=copied),ensure_ascii=False,indent=2)+'\n')
    assert result.returncode==0 and generated==frozen and unchanged
    print(json.dumps({k:execution[k] for k in ['exit_code','wall_seconds','executions_of_original_entrypoint','generated_report_byte_identical_to_frozen','input_and_code_bytes_unchanged']},ensure_ascii=False))

if __name__=='__main__':
    main()
