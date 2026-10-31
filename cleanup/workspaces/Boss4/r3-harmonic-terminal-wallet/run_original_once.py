"""Run the frozen harmonic-wallet main once with all exact local dependencies."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-harmonic-terminal-wallet')
EV=STAGE/'archives/customer-attraction/tools/evidence/harmonic-terminal-wallet-primary'
PRIMARY=['f811c6617841fee2c723','70c3ea6d4f224667baf7','24605d29e47dc547a839','1deb05327659c64eae69','1a2500b24700429ddb8f']
DEPENDENCIES=['3beb17d5735520b90e84','a7579960b289fff40c97','ff1a437e39e730d230eb','be317a14860bf5650dfe']

def sha(raw): return hashlib.sha256(raw).hexdigest()
def main():
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    replay=EV/'replay'
    replay.mkdir(parents=True,exist_ok=True)
    assert not (replay/'execution.json').exists(),'Original main already executed'
    records=[]
    tree=EV/'replay-tree'
    for sid in PRIMARY+DEPENDENCIES:
        row=inv[sid]
        first=None
        locations=[]
        for loc in row['sources']:
            # Missing local objects fail here instead of initiating authentication.
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or raw==first
            first=raw
            locations.append(dict(loc,bytes_verified=True))
        dest=EV/'original'/row['path']
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(first)
        if sid=='70c3ea6d4f224667baf7' or sid in DEPENDENCIES:
            target=tree/row['path']
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary' if sid in PRIMARY else 'runtime-dependency-only-not-done',saved_path=str(dest.relative_to(STAGE))))
    entry=tree/inv['70c3ea6d4f224667baf7']['path']
    started=time.time()
    run=subprocess.run([sys.executable,str(entry)],cwd=tree,capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    elapsed=time.time()-started
    (replay/'stdout.txt').write_bytes(run.stdout)
    (replay/'stderr.txt').write_bytes(run.stderr)
    report=entry.parent/'harmonic_terminal_wallet_exact_audit.json'
    generated=report.read_bytes() if report.exists() else b''
    frozen=(EV/'original'/inv['24605d29e47dc547a839']['path']).read_bytes()
    (replay/'harmonic_terminal_wallet_exact_audit.json').write_bytes(generated)
    used=[r for r in records if r['id']=='70c3ea6d4f224667baf7' or r['id'] in DEPENDENCIES]
    unchanged=all(sha((tree/r['path']).read_bytes())==r['sha256'] for r in used)
    execution=dict(command=[sys.executable,str(entry.relative_to(tree))],working_directory=str(tree),python=sys.version,executions_of_original_entrypoint=1,exit_code=run.returncode,wall_seconds=elapsed,generated_report_bytes=len(generated),generated_report_sha256=sha(generated),frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=generated==frozen,input_and_code_bytes_unchanged=unchanged,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr),calls='HW main once; round8 old.audit(loader) once per case (two calls total); four loader calls total; round8 main not called.',scope='Two fixed complete policies, all incl-self ICs and previous terminal-wallet assertions, then COPY/CLIENT/HW/REFUND. m5 substitution is output metadata, not a five-player fixture. No weak-Q LP or peer program run.')
    (replay/'execution.json').write_text(json.dumps(execution,ensure_ascii=False,indent=2)+'\n')
    (EV/'runtime-input-manifest.json').write_text(json.dumps(dict(frozen_sources=records,replay_code_and_inputs=used),ensure_ascii=False,indent=2)+'\n')
    assert run.returncode==0 and generated==frozen and unchanged
    print(json.dumps({k:execution[k] for k in ['exit_code','wall_seconds','executions_of_original_entrypoint','generated_report_bytes','generated_report_byte_identical_to_frozen','input_and_code_bytes_unchanged']},ensure_ascii=False))

if __name__=='__main__': main()
