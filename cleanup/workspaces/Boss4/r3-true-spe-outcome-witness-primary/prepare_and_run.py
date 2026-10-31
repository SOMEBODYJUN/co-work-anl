"""Run the original default DAG audit and the needed old exact counterexample audit once."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-true-spe-outcome-witness-primary')
E=Path('archives/customer-attraction/tools/evidence/true-spe-outcome-witness-primary')
W=Path('cleanup/workspaces/Boss4/r3-true-spe-outcome-witness-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def prepare():
    pm=json.loads((S/E/'primary-manifest.json').read_text());rm=json.loads((S/E/'runtime-manifest.json').read_text());im=json.loads((S/E/'input-manifest.json').read_text());cm=json.loads((S/E/'exploration-comparison-manifest.json').read_text());cl=json.loads((S/W/'claim-observation.json').read_text());assert cl['status']=='pushed'and cl['actor']=='Boss4'and set(cl['claimed_primary_ids'])=={r['id']for r in pm['sources']}
    sources=pm['sources']+rm['sources']+im['sources']+cm['sources'];byid={r['id']:r for r in sources};tree=S/E/'replay-tree';other=S/E/'replay-markov-tree';assert not tree.exists()and not other.exists()
    ids=['ba24829ca8aa642f892c','962b57c6915dcb2636ca']+[r['id']for r in rm['sources']]+[r['id']for r in im['sources']if r['role']=='runtime-input-not-primary']
    for sid in ids:
        r=byid[sid];t=tree/r['path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/r['saved_path'],t)
    r=byid['6543d29d729f96c9276b'];t=other/r['path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/r['saved_path'],t)
    (S/E/'source-manifest.json').write_text(json.dumps(dict(claim_push=cl['remote_tip'],claim_capture=cl['capture'],claim_capture_sha256=cl['capture_sha256'],primary_count=5,primary_bytes=pm['primary_bytes'],runtime_code_dependencies=5,runtime_code_bytes=rm['runtime_dependency_bytes'],runtime_inputs=3,runtime_input_bytes=sum(r['size']for r in im['sources']if r['role']=='runtime-input-not-primary'),comparison_only_sources=4,sources=sources,only_actual_claim_intersection_disposed=True),ensure_ascii=False,indent=2)+'\n')
def run(kind):
    byid={r['id']:r for r in json.loads((S/E/'source-manifest.json').read_text())['sources']}
    cid,rid=('962b57c6915dcb2636ca','7e9c940cf8071349841b')if kind=='audit'else('6543d29d729f96c9276b','1c15c43ca580c43498d7')
    tree=S/E/('replay-tree'if kind=='audit'else'replay-markov-tree');out=S/E/f'replay-{kind}';out.mkdir(exist_ok=True);event=out/'execution.json';assert not event.exists();target=tree/byid[rid]['path'];assert not target.exists()
    args=[sys.executable,byid[cid]['path']];e=dict(status='started',kind=kind,original_main_executions=1,command=args,cwd=str(tree),python=sys.version,large_baseline_branch_executed=False)
    if kind=='audit':
        import numpy,scipy
        e.update(numpy=numpy.__version__,scipy=scipy.__version__)
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');start=time.time()
    try:
        p=subprocess.run(args,cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=120);code=p.returncode;stdout=p.stdout;stderr=p.stderr;error=None
    except subprocess.TimeoutExpired as ex:
        code=None;stdout=ex.stdout or b'';stderr=ex.stderr or b'';error='timeout120s; stopped without rerun'
    (out/'stdout.txt').write_bytes(stdout);(out/'stderr.txt').write_bytes(stderr)
    dependencies=[byid[cid]] if kind=='markov'else[byid[x]for x in ['ba24829ca8aa642f892c','962b57c6915dcb2636ca','51b578ac60c377c6f060','e34d11916a2c223f010d','999293c4e866618a72f6','14e0922138e43b337600','52369ae591b07d52c7df','1c15c43ca580c43498d7','c0d7c7c0952b288ed370','dbbb96f5098589f83146']]
    e.update(status='finished',wall_seconds=time.time()-start,exit_code=code,error=error,code_and_input_bytes_unchanged=all(sha((tree/r['path']).read_bytes())==r['sha256']for r in dependencies))
    if target.exists():
        raw=target.read_bytes();old=(S/byid[rid]['saved_path']).read_bytes();(out/target.name).write_bytes(raw);d=json.loads(raw)
        e.update(report_bytes=len(raw),report_sha256=sha(raw),frozen_report_sha256=sha(old),report_byte_identical_to_frozen=raw==old,report_semantically_equal_to_frozen=d==json.loads(old))
        if kind=='audit':e.update(completed_milp_calls=60,completed_exact_fixed_cone_LPs=2,fixed_input_target_checks=d['fixed_input_positive_welfare_target_checks'],successful_oracle_target_witnesses=d['successful_full_history_exact_checks'],fixed_m4_duals_replayed=d['exact_fixed_m4_cone_new_budget_optimal_duals'])
        else:e.update(solver_calls=0,complete_SPE_comparisons=d['complete_SPE_comparisons'],Markov_last_maps_exhausted=d['Markov_last_maps_exhausted'],Markov_second_maps_exhausted=d['Markov_second_maps_exhausted'],full_min_welfare=d['full_min_welfare'],Markov_min_welfare=d['Markov_min_welfare'])
    event.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');print(json.dumps(e,ensure_ascii=False,indent=2))
if __name__=='__main__':
    if '--prepare'in sys.argv:prepare()
    else:run(sys.argv[1])
