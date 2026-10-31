"""Capture exact sources/three inputs and run only the named-packet audit once."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-security-named-attack-history')
EV=STAGE/'archives/customer-attraction/tools/evidence/security-named-attack-history-primary'
PRIMARY=['2c2fdb99195aa0a9e3ad','1d305bb3f9999d836b5b','c19b4a93560ff473adf5','6aca9b93763f751a2cb7','6b81f6445e9914b0b550']
DEPS=['a7579960b289fff40c97','ff1a437e39e730d230eb','be317a14860bf5650dfe']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    replay=EV/'replay';replay.mkdir(parents=True,exist_ok=True)
    assert not (replay/'execution.json').exists(),'Original named audit already executed'
    records=[];tree=EV/'replay-tree'
    for sid in PRIMARY+DEPS:
        row=inv[sid];first=None;locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw;locations.append(dict(loc,bytes_verified=True))
        dest=EV/'original'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(first)
        if sid in DEPS or sid=='1d305bb3f9999d836b5b':
            target=tree/row['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(first)
        records.append(dict(id=sid,path=row['path'],size=row['size'],blob=row['blob'],sha256=row['sha256'],sources=locations,role='primary' if sid in PRIMARY else 'runtime-dependency-only-not-done',saved_path=str(dest.relative_to(STAGE))))
    code=inv['1d305bb3f9999d836b5b'];entry=tree/code['path'];started=time.time()
    run=subprocess.run([sys.executable,str(entry)],cwd=tree,capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    elapsed=time.time()-started
    (replay/'stdout.txt').write_bytes(run.stdout);(replay/'stderr.txt').write_bytes(run.stderr)
    output=entry.parent/'adjacent_wallet_named_packets.json';generated=output.read_bytes() if output.exists() else b''
    frozen=(EV/'original'/inv['c19b4a93560ff473adf5']['path']).read_bytes()
    (replay/'adjacent_wallet_named_packets.json').write_bytes(generated)
    used=[r for r in records if r['id'] in DEPS or r['id']=='1d305bb3f9999d836b5b']
    unchanged=all(sha((tree/r['path']).read_bytes())==r['sha256'] for r in used)
    execution=dict(command=[sys.executable,code['path']],working_directory=str(tree),python=sys.version,executions_of_original_entrypoint=1,exit_code=run.returncode,wall_seconds=elapsed,generated_report_bytes=len(generated),generated_report_sha256=sha(generated),frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=generated==frozen,code_and_input_bytes_unchanged=unchanged,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr),scope='Exactly the named old52 and old1953 full policies: 302 ordered decision histories,1812 incl-self ICs,1512 ordered comparison tuples; no new model/policy search, no old13 or optimal-query LP run.')
    (replay/'execution.json').write_text(json.dumps(execution,ensure_ascii=False,indent=2)+'\n')
    (EV/'runtime-input-manifest.json').write_text(json.dumps(dict(frozen_sources=records,replay_code_and_inputs=used,runtime_dependency_count=3,imports_no_previous_audit_module=True),ensure_ascii=False,indent=2)+'\n')
    assert run.returncode==0 and generated==frozen and unchanged
    print(json.dumps({k:execution[k] for k in ['exit_code','wall_seconds','executions_of_original_entrypoint','generated_report_bytes','generated_report_byte_identical_to_frozen','code_and_input_bytes_unchanged']},ensure_ascii=False))
if __name__=='__main__':main()
