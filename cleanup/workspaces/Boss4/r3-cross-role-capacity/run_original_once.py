"""Run the exact frozen cross-role audit once in an isolated original-path tree."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

REPO = Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE = Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-cross-role-capacity')
EVIDENCE = STAGE / 'archives/customer-attraction/tools/evidence/cross-role-capacity-primary'
PRIMARY = ['5324af15497c072261ab','7a47283b90da9d8af1bc','3ea81eb3459228c16b83','94f62b8bf6ed8c17630c','c458d6c7595f02da5781']
DEPENDENCIES = ['3beb17d5735520b90e84','a7579960b289fff40c97','ff1a437e39e730d230eb','be317a14860bf5650dfe']

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
    for sid in ['7a47283b90da9d8af1bc']+DEPENDENCIES:
        row=rows[sid]
        target=tree/row['path']
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((EVIDENCE/'original'/row['path']).read_bytes())
        copied.append(dict(path=row['path'],sha256=sha(target.read_bytes())))
    entry=tree/rows['7a47283b90da9d8af1bc']['path']
    started=time.time()
    result=subprocess.run([sys.executable,str(entry)],cwd=tree,capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    elapsed=time.time()-started
    (EVIDENCE/'replay/stdout.txt').write_bytes(result.stdout)
    (EVIDENCE/'replay/stderr.txt').write_bytes(result.stderr)
    output=entry.parent/'cross_role_exchange_audit.json'
    frozen=(EVIDENCE/'original'/rows['3ea81eb3459228c16b83']['path']).read_bytes()
    generated=output.read_bytes() if output.exists() else b''
    (EVIDENCE/'replay/cross_role_exchange_audit.json').write_bytes(generated)
    unchanged=all(sha((tree/r['path']).read_bytes())==r['sha256'] for r in copied)
    execution=dict(command=[sys.executable,str(entry.relative_to(tree))],working_directory=str(tree),python=sys.version,exit_code=result.returncode,wall_seconds=elapsed,executions_of_original_entrypoint=1,generated_report_sha256=sha(generated),frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=generated==frozen,input_and_code_bytes_unchanged=unchanged,stdout_sha256=sha(result.stdout),stderr_sha256=sha(result.stderr),scope='COPY/GATE formulas and joint optimal selection on two fixed certificates; imported loader audit()/main() are not called, so this run does not reverify complete SPE ICs.')
    (EVIDENCE/'replay/execution.json').write_text(json.dumps(execution,ensure_ascii=False,indent=2)+'\n')
    (EVIDENCE/'runtime-input-manifest.json').write_text(json.dumps(dict(frozen_sources=original_records,replay_files=copied),ensure_ascii=False,indent=2)+'\n')
    assert result.returncode==0 and generated==frozen and unchanged
    print(json.dumps({k:execution[k] for k in ['exit_code','wall_seconds','executions_of_original_entrypoint','generated_report_byte_identical_to_frozen','input_and_code_bytes_unchanged']},ensure_ascii=False))

if __name__=='__main__':
    main()
