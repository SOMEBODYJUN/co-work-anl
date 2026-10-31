"""One original weak-DAG main on one declared representative parameter set."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-credible-weak-dag-attack-primary')
E=Path('archives/customer-attraction/tools/evidence/credible-weak-dag-attack-primary')
W=Path('cleanup/workspaces/Boss4/r3-credible-weak-dag-attack-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def prepare():
    pm=json.loads((S/E/'primary-manifest.json').read_text());rm=json.loads((S/E/'runtime-manifest.json').read_text());cl=json.loads((S/W/'claim-observation.json').read_text());assert cl['status']=='pushed'and cl['actor']=='Boss4'and set(cl['claimed_primary_ids'])=={r['id']for r in pm['sources']}
    sources=pm['sources']+rm['sources'];tree=S/E/'replay-tree';assert not tree.exists()
    for r in sources:
        if r['path'].endswith('.py'):
            p=tree/r['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/r['saved_path'],p)
    (S/E/'source-manifest.json').write_text(json.dumps(dict(claim_push=cl['remote_tip'],claim_capture=cl['capture'],claim_capture_sha256=cl['capture_sha256'],primary_count=5,primary_bytes=pm['primary_bytes'],runtime_dependency_count=6,runtime_dependency_bytes=rm['runtime_dependency_bytes'],runtime_input_files=0,sources=sources,only_actual_claim_intersection_disposed=True),ensure_ascii=False,indent=2)+'\n')
def run():
    import numpy,scipy
    sm=json.loads((S/E/'source-manifest.json').read_text());byid={r['id']:r for r in sm['sources']};tree=S/E/'replay-tree';out=S/E/'replay';out.mkdir(exist_ok=True);event=out/'execution.json';assert not event.exists()
    driver=byid['5253dce62f3159c5d985'];frozen=byid['82b0bd94aff958b218a8'];dest=tree/frozen['path'];assert not dest.exists()
    args=[sys.executable,driver['path'],'--root','1,1,1,0,0','--topic','0','--portfolio','2,3,4','--seconds','30','--output',str(dest)]
    e=dict(status='started',original_main_executions=1,command=args,cwd=str(tree),python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,new_time_limit_seconds=30,historical_time_limit_not_recorded=True,selected_case_primary_id=frozen['id'],unrerun_other_frozen_cases=3)
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');start=time.time()
    try:
        p=subprocess.run(args,cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=90);code=p.returncode;stdout=p.stdout;stderr=p.stderr;err=None
    except subprocess.TimeoutExpired as ex:
        code=None;stdout=ex.stdout or b'';stderr=ex.stderr or b'';err='timeout at 90s; no rerun'
    (out/'stdout.txt').write_bytes(stdout);(out/'stderr.txt').write_bytes(stderr)
    e.update(status='finished',wall_seconds=time.time()-start,exit_code=code,error=err,source_bytes_unchanged=all(sha((tree/r['path']).read_bytes())==r['sha256']for r in sm['sources']if r['path'].endswith('.py')))
    if dest.exists():
        raw=dest.read_bytes();old=(S/frozen['saved_path']).read_bytes();(out/dest.name).write_bytes(raw);d=json.loads(raw);before=json.loads(old);left=json.loads(raw);right=json.loads(old);left['milp'].pop('seconds',None);right['milp'].pop('seconds',None)
        e.update(report_bytes=len(raw),report_sha256=sha(raw),frozen_report_sha256=sha(old),report_byte_identical_to_frozen=raw==old,report_equal_except_measured_milp_seconds=left==right,milp_status=d['milp']['status'],milp_seconds=d['milp']['seconds'],milp_calls=1,exact_optimize_called=d['exact_candidate']is not None,exact_candidate_present=d['exact_candidate']is not None,scope='One fixed p5/m3/q11100/a0/J234 with W-normalized gap floor1e-6; negative MILP status not an exact mathematical upper certificate.')
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');print(json.dumps(e,ensure_ascii=False,indent=2))
if __name__=='__main__':
    if '--prepare'in sys.argv:prepare()
    elif '--run'in sys.argv:run()
    else:raise SystemExit('explicit selector required')
