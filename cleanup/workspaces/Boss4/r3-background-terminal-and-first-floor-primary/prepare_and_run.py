"""Unmodified original mains once: exact terminal audit, cross probe, 5/7 walk."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-background-terminal-and-first-floor-primary')
E=Path('archives/customer-attraction/tools/evidence/background-terminal-first-floor-primary')
W=Path('cleanup/workspaces/Boss4/r3-background-terminal-and-first-floor-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def prepare():
    p=json.loads((S/E/'primary-manifest.json').read_text());c=json.loads((S/W/'claim-observation.json').read_text());assert c['status']=='pushed'and c['actor']=='Boss4'and set(c['claimed_primary_ids'])=={r['id']for r in p['sources']}
    tree=S/E/'replay-tree';assert not tree.exists()
    for r in p['sources']:
        if r['path'].endswith('.py'):
            t=tree/r['path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/r['saved_path'],t)
    (S/E/'source-manifest.json').write_text(json.dumps(dict(claim_push=c['remote_tip'],claim_capture=c['capture'],claim_capture_sha256=c['capture_sha256'],primary_count=5,primary_bytes=p['primary_bytes'],runtime_input_files=0,runtime_local_import_files=0,sources=p['sources'],only_actual_claim_intersection_disposed=True),ensure_ascii=False,indent=2)+'\n')
def run(kind):
    rows=json.loads((S/E/'primary-manifest.json').read_text())['sources'];byid={r['id']:r for r in rows};tree=S/E/'replay-tree'
    cid={'terminal':'791c11050bd539113e7b','probe':'9c939c75abe0238b894f','walk':'f44e0b68b125e6689ed2'}[kind]
    rid={'terminal':'62965fc71b6de6e370d6','walk':'54a842cb6b974fca2c33'}.get(kind)
    out=S/E/f'replay-{kind}';out.mkdir(exist_ok=True);event=out/'execution.json';assert not event.exists()
    report=tree/byid[rid]['path']if rid else None
    if report:assert not report.exists()
    args=[sys.executable,byid[cid]['path']]+(['5','7']if kind=='walk'else[])
    versions={}
    if kind!='terminal':
        import numpy,scipy
        versions=dict(numpy=numpy.__version__,scipy=scipy.__version__)
    e=dict(status='started',kind=kind,original_main_executions=1,command=args,cwd=str(tree),python=sys.version,original_input_files=0,local_import_files=0,**versions)
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');begin=time.time()
    try:
        p=subprocess.run(args,cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=180)
        code=p.returncode;stdout=p.stdout;stderr=p.stderr;error=None
    except subprocess.TimeoutExpired as ex:
        code=None;stdout=ex.stdout or b'';stderr=ex.stderr or b'';error='timeout at 180 seconds; stopped without rerun'
    (out/'stdout.txt').write_bytes(stdout);(out/'stderr.txt').write_bytes(stderr)
    e.update(status='finished',wall_seconds=time.time()-begin,exit_code=code,error=error,code_bytes_unchanged=sha((tree/byid[cid]['path']).read_bytes())==byid[cid]['sha256'])
    if report and report.exists():
        raw=report.read_bytes();frozen=(S/byid[rid]['saved_path']).read_bytes();(out/report.name).write_bytes(raw)
        e.update(report_bytes=len(raw),report_sha256=sha(raw),frozen_report_sha256=sha(frozen),report_byte_identical_to_frozen=raw==frozen,report_semantically_equal_to_frozen=json.loads(raw)==json.loads(frozen))
    if kind=='probe':e.update(scope='one original default cross policy, m3 k6, floating discovery; stdout only; no frozen stdout primary')
    if kind=='walk':e.update(scope='new explicit m5 k7 default n100/seed143; frozen historical n/iteration unknown, not backfilled',LP_calls_if_default_loop_completed=100 if code==0 and b'DONE 5 7'in stdout else None)
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');print(json.dumps(e,ensure_ascii=False,indent=2))
if __name__=='__main__':
    if '--prepare'in sys.argv:prepare()
    else:run(sys.argv[1])
