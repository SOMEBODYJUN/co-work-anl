"""Preserve frozen primary bytes and run the self-contained compact audit once."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-direct-surplus-compact-wallet')
EV=STAGE/'archives/customer-attraction/tools/evidence/direct-surplus-compact-wallet-primary'
PRIMARY=['23058322be690f0f6cc0','5aa36b9a875a25bc107b','4f9bddd16812ef8b7605','c056b152c687bc4468ec','8ed477b1d30e8bca1bb1']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    replay=EV/'replay'
    replay.mkdir(parents=True,exist_ok=True)
    assert not (replay/'execution.json').exists(),'Original audit already executed'
    records=[]
    for sid in PRIMARY:
        row=inv[sid]
        first=None
        locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw
            locations.append(dict(loc,bytes_verified=True))
        dest=EV/'original'/row['path']
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary',saved_path=str(dest.relative_to(STAGE))))
    code=inv['4f9bddd16812ef8b7605']
    tree=EV/'replay-tree'
    entry=tree/code['path']
    entry.parent.mkdir(parents=True,exist_ok=True)
    entry.write_bytes((EV/'original'/code['path']).read_bytes())
    started=time.time()
    result=subprocess.run([sys.executable,str(entry)],cwd=tree,capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    elapsed=time.time()-started
    (replay/'stdout.txt').write_bytes(result.stdout)
    (replay/'stderr.txt').write_bytes(result.stderr)
    report=entry.parent/'compact_adjacent_counterexample_exact.json'
    generated=report.read_bytes() if report.exists() else b''
    frozen=(EV/'original'/inv['c056b152c687bc4468ec']['path']).read_bytes()
    (replay/'compact_adjacent_counterexample_exact.json').write_bytes(generated)
    execution=dict(command=[sys.executable,code['path']],working_directory=str(tree),python=sys.version,executions_of_original_entrypoint=1,exit_code=result.returncode,wall_seconds=elapsed,generated_report_bytes=len(generated),generated_report_sha256=sha(generated),frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=generated==frozen,original_code_bytes_unchanged=sha(entry.read_bytes())==code['sha256'],runtime_external_input_files=[],runtime_external_packages=[],input_scope='All ten unit customers, root/SECOND/LAST complete policy are literal constants in the original code; standard library only.',stdout_sha256=sha(result.stdout),stderr_sha256=sha(result.stderr),scope='21 full ordered histories,84 incl-self ICs,all64 ordered comparison tuples and every optimal multiset assignment; no equilibrium/instance search and no HALF counterexample.')
    (replay/'execution.json').write_text(json.dumps(execution,ensure_ascii=False,indent=2)+'\n')
    (EV/'runtime-input-manifest.json').write_text(json.dumps(dict(frozen_sources=records,external_runtime_dependency_count=0,embedded_inputs=dict(labels=['C','A','B','D'],players=3,unit_customer_types=[dict(topics=[0,1,2],multiplicity=6),dict(topics=[1],multiplicity=1),dict(topics=[2,3],multiplicity=1),dict(topics=[3],multiplicity=2)],SECOND=[0,1,2,1],LAST=[[3,2,1,1],[2,2,2,2],[1,1,1,1],[1,2,1,1]])),ensure_ascii=False,indent=2)+'\n')
    assert result.returncode==0 and generated==frozen and execution['original_code_bytes_unchanged']
    print(json.dumps({k:execution[k] for k in ['exit_code','wall_seconds','executions_of_original_entrypoint','generated_report_bytes','generated_report_byte_identical_to_frozen','original_code_bytes_unchanged']},ensure_ascii=False))
if __name__=='__main__':main()
