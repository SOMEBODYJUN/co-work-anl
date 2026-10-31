"""Two unmodified original mains, once each, with no mathematical input files."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-global-menu-prefix-primary')
EV=Path('archives/customer-attraction/tools/evidence/global-menu-prefix-primary')
WS=Path('cleanup/workspaces/Boss4/r3-global-menu-prefix-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):(STAGE/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepare():
    pm=json.loads((STAGE/EV/'primary-manifest.json').read_text());cm=json.loads((STAGE/EV/'comparison-manifest.json').read_text());cl=json.loads((STAGE/WS/'claim-observation.json').read_text())
    assert cl['status']=='pushed'and cl['actor']=='Boss4'and set(cl['claimed_primary_ids'])=={r['id']for r in pm['sources']}
    tree=STAGE/EV/'replay-tree';assert not tree.exists()
    for row in pm['sources']:
        if not row['path'].endswith('.py'):continue
        t=tree/row['path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(STAGE/row['saved_path'],t)
    dump(EV/'source-manifest.json',dict(claim_push=cl['remote_tip'],claim_capture=cl['capture'],claim_capture_sha256=cl['capture_sha256'],primary_count=5,primary_bytes=pm['primary_bytes'],runtime_input_files=0,runtime_local_import_files=0,external_packages=['numpy','scipy.optimize.linprog'],comparison_only_count=1,sources=pm['sources']+cm['sources'],only_actual_claim_intersection_disposed=True))
def run(kind):
    import numpy,scipy
    sm=json.loads((STAGE/EV/'source-manifest.json').read_text());byid={r['id']:r for r in sm['sources']};tree=STAGE/EV/'replay-tree'
    cid,rid=('b1068437e0a3ccccf70e','63b07199c23072ad96d9')if kind=='v1'else('1f14d618a7256ce9fdd4','2306bc61d5e35b40eabd')
    outdir=STAGE/EV/f'replay-{kind}';outdir.mkdir(exist_ok=True);event=outdir/'execution.json';assert not event.exists()
    report=outdir/Path(byid[rid]['path']).name
    tree_report=tree/byid[rid]['path'];assert not tree_report.exists()
    args=[sys.executable,byid[cid]['path']]+(['--output',str(tree_report)]if kind=='v1'else[])
    e=dict(status='started',kind=kind,original_main_executions=1,command=args,cwd=str(tree),python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,original_input_files=0,local_import_files=0,report_channel='original --output file'if kind=='v1'else'original stdout captured byte-for-byte; source does not write a report file')
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');begin=time.time()
    try:
        p=subprocess.run(args,cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=120)
        code=p.returncode;stdout=p.stdout;stderr=p.stderr;error=None
    except subprocess.TimeoutExpired as ex:
        code=None;stdout=ex.stdout or b'';stderr=ex.stderr or b'';error='timeout after 120 seconds; no rerun'
    (outdir/'stdout.txt').write_bytes(stdout);(outdir/'stderr.txt').write_bytes(stderr)
    generated=tree_report.read_bytes()if kind=='v1'and tree_report.exists()else stdout if kind=='v2'and code==0 else None
    frozen=(STAGE/byid[rid]['saved_path']).read_bytes()
    e.update(status='finished',wall_seconds=time.time()-begin,exit_code=code,error=error,code_bytes_unchanged=sha((tree/byid[cid]['path']).read_bytes())==byid[cid]['sha256'],frozen_report_sha256=sha(frozen),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr))
    if generated is not None:
        report.write_bytes(generated);parsed=json.loads(generated)
        e.update(report_bytes=len(generated),report_sha256=sha(generated),report_byte_identical_to_frozen=generated==frozen,report_semantically_equal_to_frozen=parsed==json.loads(frozen),players=[r['m']for r in parsed],success=[r['success']for r in parsed],LP_calls_from_completed_control_flow=len(parsed)+sum(not r['success']for r in parsed)if kind=='v1'else len(parsed))
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');print(json.dumps(e,ensure_ascii=False,indent=2))
if __name__=='__main__':
    if '--prepare'in sys.argv:prepare()
    elif '--run-v1'in sys.argv:run('v1')
    elif '--run-v2'in sys.argv:run('v2')
    else:raise SystemExit('explicit prepare or one original main selector required')
