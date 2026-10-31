"""Run the actual root/weak and multiset default mains once, unmodified."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-security-closure-and-uniform-root-primary')
EV=Path('archives/customer-attraction/tools/evidence/security-closure-uniform-root-primary')
WS=Path('cleanup/workspaces/Boss4/r3-security-closure-and-uniform-root-primary')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    p=STAGE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def prepare():
    pm=json.loads((STAGE/EV/'primary-manifest.json').read_text())
    rm=json.loads((STAGE/EV/'runtime-manifest.json').read_text())
    claim=json.loads((STAGE/WS/'claim-observation.json').read_text())
    assert claim['status']=='pushed'and claim['actor']=='Boss4'and set(claim['claimed_primary_ids'])=={r['id']for r in pm['sources']}
    sources=pm['sources']+rm['sources'];rows={r['id']:r for r in sources}
    tree=STAGE/EV/'replay-tree';assert not tree.exists()
    for sid in [r['id']for r in rm['sources']]+['ed3eaf5a278ffefe256c']:
        dest=tree/rows[sid]['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(STAGE/rows[sid]['saved_path'],dest)
    dump(EV/'source-manifest.json',dict(claim_push=claim['remote_tip'],claim_capture=claim['capture'],claim_capture_sha256=claim['capture_sha256'],primary_count=5,primary_bytes=pm['primary_bytes'],runtime_dependency_count=rm['runtime_dependency_count'],runtime_dependency_bytes=rm['runtime_dependency_bytes'],sources=sources,only_actual_claim_intersection_disposed=True))
    print('prepared actual dependency tree',flush=True)
def run(kind):
    sm=json.loads((STAGE/EV/'source-manifest.json').read_text());rows={r['id']:r for r in sm['sources']}
    if kind=='root-weak':
        cid,rid='847a210188334e25b4bd','9e72daa5a0b2a448316c';args=['--mode','root','--weak'];deps=[cid,'8d74fd183eba467a811f']
    else:
        cid,rid='ed3eaf5a278ffefe256c','f4a36f001a7aed051f24';args=[]
        deps=[cid]+[sid for sid in rows if rows[sid]['role']=='runtime-dependency-only-not-done'and sid not in ['847a210188334e25b4bd','8d74fd183eba467a811f']]
    folder=EV/('replay-'+kind);eventpath=STAGE/folder/'execution.json';assert not eventpath.exists(),'Original main already attempted; no retry.'
    tree=STAGE/EV/'replay-tree';report=tree/rows[rid]['path'];assert not report.exists()
    import numpy,scipy
    cmd=[sys.executable,rows[cid]['path']]+args
    dump(folder/'execution.json',dict(status='started',original_main_executions=1,command=cmd,cwd=str(tree)))
    start=time.time()
    try:
        p=subprocess.run(cmd,cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=120)
        stdout,stderr,rc,error=p.stdout,p.stderr,p.returncode,None
    except subprocess.TimeoutExpired as exc:
        stdout,stderr,rc,error=exc.stdout or b'',exc.stderr or b'',None,'Original main timed out after120s; no retry.'
    (STAGE/folder/'stdout.txt').write_bytes(stdout);(STAGE/folder/'stderr.txt').write_bytes(stderr)
    raw=report.read_bytes()if report.exists()else None
    if raw is not None:(STAGE/folder/report.name).write_bytes(raw)
    frozen=(STAGE/rows[rid]['saved_path']).read_bytes()
    result=dict(status='finished'if error is None else'timeout',kind=kind,original_main_executions=1,command=cmd,cwd=str(tree),python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,wall_seconds=time.time()-start,exit_code=rc,error=error,code_and_input_bytes_unchanged=all(sha((tree/rows[sid]['path']).read_bytes())==rows[sid]['sha256']for sid in deps),actual_dependency_ids=deps,generated_report_bytes=len(raw)if raw is not None else None,generated_report_sha256=sha(raw)if raw is not None else None,frozen_report_sha256=sha(frozen),generated_report_byte_identical_to_frozen=raw==frozen if raw is not None else False,generated_report_semantically_equal_to_frozen=json.loads(raw)==json.loads(frozen)if raw is not None else False,stdout_sha256=sha(stdout),stderr_sha256=sha(stderr))
    if raw is not None:
        d=json.loads(raw)
        if kind=='root-weak':result.update(mode='root',factor=12.5,trace_rows=len(d['trace']),starts=len({r['start']for r in d['trace']}),LP_calls_from_completed_control_flow=1+2*len(d['trace']),scope='Only free root-menu restricted backgrounds with weak factor; not stationary-weighted Q or true unrestricted security.')
        else:result.update(certificate_records=len(d),LP_calls=sum(r['LPs']for r in d),positive_candidate_exported=any('candidate'in r for r in d),scope='Four certificate reads but three different complete action maps; all comparison multiplicity vertices, floating negative branch only, no helper solver/main/exact upper dual invoked.')
    dump(folder/'execution.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':
    if '--run-root-weak'in sys.argv:run('root-weak')
    elif '--run-uniform'in sys.argv:run('uniform')
    else:prepare()
