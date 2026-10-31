"""Save full frozen sources; run each of the two original mains at most once."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-root-stationary-weak-history')
EV=Path('archives/customer-attraction/tools/evidence/root-stationary-weak-primary')
PRIMARY=['d9373374b8958e716d53','a5b0c3a6776a1e022678','6808f2beec1bb6b2941b','8b152f1b38c788bfe6c2','e1d7eeedac139253663e']
RUNTIME=['8d74fd183eba467a811f','74e42e785c0da1cb0ee5']
COMPARE=['ceaf1282ad9019816dd7','8fb492268f7ad2fd3e37','cc31f0e547a5bce7512e','deb74d312cf9a35b4985']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def prepare():
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    records=[];retrieval=[]
    for sid in PRIMARY+RUNTIME+COMPARE:
        row=inv[sid];target=STAGE/EV/'original'/row['path'];first=None;locations=[]
        for loc in row['sources']:
            result=subprocess.run(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'),capture_output=True,timeout=30)
            if result.returncode:
                error=result.stderr.decode()
                if 'bad object'not in error:raise RuntimeError(error)
                # One normal read-only clean show obtains a missing promised blob.
                res=subprocess.run([sys.executable,'work.py','clean','show',sid,'--out',str(target)],cwd=REPO,capture_output=True,timeout=55)
                retrieval.append(dict(id=sid,initial_local_error=error.strip(),normal_clean_show_exit=res.returncode,credential_retry=False))
                if res.returncode:raise RuntimeError(res.stderr.decode())
                raw=target.read_bytes()
            else:raw=result.stdout
            assert len(raw)==row['size']and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw;locations.append(dict(loc,bytes_verified=True))
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(first)
        records.append(dict(id=sid,path=row['path'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary'if sid in PRIMARY else'runtime-dependency-only-not-done'if sid in RUNTIME else'comparison-only-not-done',saved_path=str(target.relative_to(STAGE))))
    tree=STAGE/EV/'replay-tree';assert not tree.exists(),'Do not prepare over an existing execution tree.'
    for sid in ['a5b0c3a6776a1e022678','8b152f1b38c788bfe6c2']+RUNTIME:
        row=inv[sid];dest=tree/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(STAGE/EV/'original'/row['path'],dest)
    dump(EV/'source-manifest.json',dict(claim_push='2c9523cd6d3412e71de5ac705007b0c57e5d8f66',primary_count=5,primary_bytes=sum(inv[s]['size']for s in PRIMARY),runtime_dependency_count=2,runtime_dependency_bytes=sum(inv[s]['size']for s in RUNTIME),comparison_count=4,sources=records,normal_read_only_clean_show_for_missing_local_blobs=retrieval,independent_root_review_executed_this_batch=False))
    print(json.dumps(dict(prepared=True,primary_count=5,primary_bytes=sum(inv[s]['size']for s in PRIMARY),runtime_dependencies=2,comparisons=4),ensure_ascii=False),flush=True)
def run(kind):
    data=json.loads((STAGE/EV/'source-manifest.json').read_text());rows={r['id']:r for r in data['sources']}
    if kind=='audit':sid,rid='a5b0c3a6776a1e022678','6808f2beec1bb6b2941b';deps=RUNTIME[:1]
    else:sid,rid='8b152f1b38c788bfe6c2','e1d7eeedac139253663e';deps=RUNTIME[1:]
    folder=EV/('replay-'+kind);ex=STAGE/folder/'execution.json';assert not ex.exists(),'Original main already attempted; no retry.'
    tree=STAGE/EV/'replay-tree';code=rows[sid]['path'];report=rows[rid]['path'];assert not(tree/report).exists()
    versions={}
    if kind=='probe':
        import numpy,scipy
        versions=dict(numpy=numpy.__version__,scipy=scipy.__version__)
    dump(folder/'execution.json',dict(status='started',original_entrypoint_executions=1,command=[sys.executable,code],cwd=str(tree)))
    start=time.time()
    proc=subprocess.run([sys.executable,code],cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=120)
    (STAGE/folder/'stdout.txt').write_bytes(proc.stdout);(STAGE/folder/'stderr.txt').write_bytes(proc.stderr)
    raw=(tree/report).read_bytes()if(tree/report).exists()else None
    if raw is not None:(STAGE/folder/Path(report).name).write_bytes(raw)
    result=dict(status='finished',kind=kind,original_entrypoint_executions=1,command=[sys.executable,code],cwd=str(tree),python=sys.version,versions=versions,wall_seconds=time.time()-start,exit_code=proc.returncode,code_and_inputs_unchanged=all(sha((tree/rows[s]['path']).read_bytes())==rows[s]['sha256']for s in [sid]+deps),generated_report_bytes=len(raw)if raw is not None else None,generated_report_sha256=sha(raw)if raw is not None else None,frozen_report_sha256=rows[rid]['sha256'],generated_report_byte_identical_to_frozen=raw==(STAGE/rows[rid]['saved_path']).read_bytes()if raw is not None else False,stdout_sha256=sha(proc.stdout),stderr_sha256=sha(proc.stderr),scope='One standard-library definition-level audit of the old13 automaton.'if kind=='audit'else'One original six-LP fixed-three-player-policy stationary-weak probe; no extension or new input search.')
    dump(folder/'execution.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':
    if '--run-audit'in sys.argv:run('audit')
    elif '--run-probe'in sys.argv:run('probe')
    else:prepare()
