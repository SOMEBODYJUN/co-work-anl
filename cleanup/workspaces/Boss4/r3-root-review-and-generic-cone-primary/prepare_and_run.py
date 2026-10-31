"""Freeze exact dependency/comparisons; run each claimed original once."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-root-review-and-generic-cone-primary')
EV=Path('archives/customer-attraction/tools/evidence/root-review-and-generic-cone-primary')
DEP='8d74fd183eba467a811f'
COMPARE=['d9373374b8958e716d53','a5b0c3a6776a1e022678','6808f2beec1bb6b2941b','ceaf1282ad9019816dd7','17bad95333c2be5f6402']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def prepare():
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    primary=json.loads((STAGE/EV/'primary-manifest.json').read_text());records=primary['sources']
    for sid in [DEP]+COMPARE:
        row=inv[sid];first=None;locations=[];target=STAGE/EV/'original'/row['path']
        for loc in row['sources']:
            p=subprocess.run(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'),capture_output=True,timeout=30)
            if p.returncode:
                if b'bad object'not in p.stderr:raise RuntimeError(p.stderr.decode())
                fetched=subprocess.run([sys.executable,'work.py','clean','show',sid,'--out',str(target)],cwd=REPO,capture_output=True,timeout=55)
                if fetched.returncode:raise RuntimeError(fetched.stderr.decode())
                raw=target.read_bytes()
            else:raw=p.stdout
            assert len(raw)==row['size']and sha(raw)==row['sha256'];assert first is None or first==raw
            first=raw;locations.append(dict(loc,bytes_verified=True))
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(first)
        records.append(dict(id=sid,path=row['path'],size=row['size'],sha256=row['sha256'],sources=locations,role='runtime-dependency-only-not-done'if sid==DEP else'comparison-only-not-done',saved_path=str(target.relative_to(STAGE))))
    tree=STAGE/EV/'replay-tree';assert not tree.exists()
    rows={r['id']:r for r in records}
    for sid in ['8fb492268f7ad2fd3e37','847a210188334e25b4bd',DEP]:
        dest=tree/rows[sid]['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(STAGE/rows[sid]['saved_path'],dest)
    dump(EV/'source-manifest.json',dict(primary_count=5,primary_bytes=25179,claim_push='4062d709a9b0b600597ed94cf4dbd33dfc647b41',runtime_dependency_count=1,runtime_dependency_bytes=372216,comparison_count=len(COMPARE),comparison_bytes=sum(inv[s]['size']for s in COMPARE),sources=records,canonical_source_read_only_clean_show_allowed=True))
    print('prepared full dependency and comparison tree',flush=True)
def run(kind):
    sm=json.loads((STAGE/EV/'source-manifest.json').read_text());rows={r['id']:r for r in sm['sources']}
    if kind=='review':
        cid,rid='8fb492268f7ad2fd3e37','cc31f0e547a5bce7512e';output=rows[rid]['path']
    else:
        cid,rid='847a210188334e25b4bd','d0790545c28af71b92b1'
        output=str(Path(rows[cid]['path']).with_name('cone_security_probe_all_13.json'))
    folder=EV/('replay-'+kind);eventpath=STAGE/folder/'execution.json';assert not eventpath.exists()
    tree=STAGE/EV/'replay-tree';assert not(tree/output).exists()
    versions={}
    if kind=='cone':
        import numpy,scipy
        versions=dict(numpy=numpy.__version__,scipy=scipy.__version__)
    cmd=[sys.executable,rows[cid]['path']]
    dump(folder/'execution.json',dict(status='started',original_main_executions=1,command=cmd,cwd=str(tree),arguments='no optional arguments; cone default all/strong factor13'if kind=='cone'else'no optional arguments'))
    start=time.time()
    try:
        p=subprocess.run(cmd,cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=120)
        stdout,stderr,rc,error=p.stdout,p.stderr,p.returncode,None
    except subprocess.TimeoutExpired as exc:
        stdout,stderr,rc,error=exc.stdout or b'',exc.stderr or b'',None,'original main timed out after120s; no retry'
    (STAGE/folder/'stdout.txt').write_bytes(stdout);(STAGE/folder/'stderr.txt').write_bytes(stderr)
    raw=(tree/output).read_bytes()if(tree/output).exists()else None
    if raw is not None:(STAGE/folder/Path(output).name).write_bytes(raw)
    frozen=(STAGE/rows[rid]['saved_path']).read_bytes()
    result=dict(status='finished'if error is None else'timeout',kind=kind,original_main_executions=1,command=cmd,cwd=str(tree),python=sys.version,versions=versions,wall_seconds=time.time()-start,exit_code=rc,error=error,code_and_input_bytes_unchanged=all(sha((tree/rows[s]['path']).read_bytes())==rows[s]['sha256']for s in [cid,DEP]),actual_generated_relative_path=output,frozen_report_relative_path=rows[rid]['path'],generated_report_bytes=len(raw)if raw is not None else None,generated_report_sha256=sha(raw)if raw is not None else None,frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=raw==frozen if raw is not None else False,generated_report_semantically_equal_to_frozen=json.loads(raw)==json.loads(frozen)if raw is not None else False,stdout_sha256=sha(stdout),stderr_sha256=sha(stderr))
    if kind=='cone'and raw is not None:
        report=json.loads(raw);result.update(executed_mode='all',executed_factor=13,generated_trace_rows=len(report['trace']),start_count=len({r['start']for r in report['trace']}),internal_LP_calls_from_completed_control_flow=1+2*len(report['trace']),scope='One default all-background strong-factor alternating numerical search; no root/onpath/weak runs or exact cone upper certification.')
    dump(folder/'execution.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':
    if '--run-review'in sys.argv:run('review')
    elif '--run-cone'in sys.argv:run('cone')
    else:prepare()
