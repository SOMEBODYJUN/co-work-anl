"""Preserve the five frozen primaries and run the exact count-prefix audit once."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-adjacent-wallet-general-family')
EV=STAGE/'archives/customer-attraction/tools/evidence/adjacent-wallet-general-family-primary'
PRIMARY=['81bc4b8504d7a37b9805','3a4479719e981f9bc43d','2e83f00a05168c0aa558','d6ada5ea6dd4defa20fe','662bb9acaf7487aaf7e7']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    replay=EV/'replay';replay.mkdir(parents=True,exist_ok=True)
    assert not (replay/'execution.json').exists(),'Original audit already executed'
    records=[]
    for sid in PRIMARY:
        row=inv[sid];first=None;locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw;locations.append(dict(loc,bytes_verified=True))
        dest=EV/'original'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary',saved_path=str(dest.relative_to(STAGE))))
    code=inv['3a4479719e981f9bc43d'];tree=EV/'replay-tree';entry=tree/code['path']
    entry.parent.mkdir(parents=True,exist_ok=True);entry.write_bytes((EV/'original'/code['path']).read_bytes())
    output=entry.parent/'optimal_adjacent_family_exact_audit.json';assert not output.exists()
    started=time.time()
    result=subprocess.run([sys.executable,str(entry)],cwd=tree,capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    elapsed=time.time()-started
    (replay/'stdout.txt').write_bytes(result.stdout);(replay/'stderr.txt').write_bytes(result.stderr)
    generated=output.read_bytes() if output.exists() else b''
    frozen=(EV/'original'/inv['2e83f00a05168c0aa558']['path']).read_bytes()
    (replay/'optimal_adjacent_family_exact_audit.json').write_bytes(generated)
    execution=dict(command=[sys.executable,code['path']],working_directory=str(tree),python=sys.version,executions_of_original_entrypoint=1,exit_code=result.returncode,wall_seconds=elapsed,generated_report_bytes=len(generated),generated_report_sha256=sha(generated),frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=generated==frozen,original_code_bytes_unchanged=sha(entry.read_bytes())==code['sha256'],runtime_external_input_files=[],runtime_external_packages=[],stdout_sha256=sha(result.stdout),stderr_sha256=sha(result.stderr),scope='Exact count-prefix IC QA only for the one explicit count-dependent policy at m=2,3,5,7; 5361 count states and 47480 incl-self comparisons represent 600708 ordered histories, not literal ordered-tree iteration. Analytic proof carries all m; not a HALF counterexample or equilibrium search.')
    (replay/'execution.json').write_text(json.dumps(execution,ensure_ascii=False,indent=2)+'\n')
    (EV/'runtime-input-manifest.json').write_text(json.dumps(dict(frozen_sources=records,external_runtime_dependency_count=0,embedded_input_family='k=m-1; core k(k+1), k private singleton A_i, one b shared B/D, k E-only-D; explicit count policy in source; audit m=(2,3,5,7)',output_open_mode='exclusive x; isolated output absent before the sole run'),ensure_ascii=False,indent=2)+'\n')
    assert result.returncode==0 and generated==frozen and execution['original_code_bytes_unchanged']
    print(json.dumps({k:execution[k] for k in ['exit_code','wall_seconds','executions_of_original_entrypoint','generated_report_bytes','generated_report_byte_identical_to_frozen','original_code_bytes_unchanged']},ensure_ascii=False))
if __name__=='__main__':main()
