from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time

STAGE = Path(__file__).resolve().parents[4]
REPO = Path('/workspace/scratch/37f0f9248cfc/boss4-research')
PRIOR = STAGE.parent / 'r3-true-spe-outcome-witness-primary'
EV = STAGE / 'archives/customer-attraction/tools/evidence/true-spe-outcome-evidence-primary'
PE = PRIOR / 'archives/customer-attraction/tools/evidence/true-spe-outcome-witness-primary'
SUB = Path('research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search')
COMMITS = ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

if (EV/'replay-large-baseline/execution.json').exists():
    raise SystemExit('Execution already recorded; do not run twice')
sources = json.loads((PE/'runtime-manifest.json').read_text())['sources']
sources += [x for x in json.loads((PE/'primary-manifest.json').read_text())['sources']
            if x['path'].endswith(('/audit_outcome_dag.py','/outcome_dag_milp.py'))]
assert len(sources) == 7
records=[]
tree=EV/'replay-tree'
for old in sources:
    p=old['path']; data=(PRIOR/old['saved_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == old['sha256']
    for commit in COMMITS:
        actual=subprocess.run(['git','show',f'{commit}:{p}'],cwd=REPO,
                              env={**os.environ,'GIT_NO_LAZY_FETCH':'1'},capture_output=True,check=True).stdout
        assert actual == data, (commit,p)
    target=EV/'original'/p; target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    runtime=tree/p;runtime.parent.mkdir(parents=True,exist_ok=True);runtime.write_bytes(data)
    record=dict(old);record.update(role='runtime-code-not-primary',saved_path=str(target.relative_to(STAGE)),
                                  runtime_path=str(runtime.relative_to(STAGE)),
                                  read_identity='same-SHA full prior read; actual optional branch re-read this batch')
    records.append(record)
dump(EV/'runtime-manifest.json',{'code_files':len(records),'code_bytes':sum(x['size'] for x in records),
 'input_data_files':0,'input_note':'large_baseline constructs all 127 multiplicities in source; default audit JSON inputs are not used',
 'sources':records})
out=EV/'replay-large-baseline';out.mkdir(parents=True,exist_ok=True)
cmd=[sys.executable,str(tree/SUB/'audit_outcome_dag.py'),'--large-baseline']
started=time.time(); wall=time.monotonic()
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
result=subprocess.run(cmd,cwd=tree,env=env,capture_output=True,timeout=90)
elapsed=time.monotonic()-wall
(out/'stdout.txt').write_bytes(result.stdout);(out/'stderr.txt').write_bytes(result.stderr)
produced=tree/SUB/'dag_baseline_fixed_m5p7.json'
new=produced.read_bytes() if produced.exists() else None
old=(EV/'original'/SUB/'dag_baseline_fixed_m5p7.json').read_bytes()
if new is not None: (out/'dag_baseline_fixed_m5p7.json').write_bytes(new)
changes=[]
def compare(a,b,at=''):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(a.keys()|b.keys()):compare(a.get(k),b.get(k),at+'/'+k)
    elif a != b: changes.append({'pointer':at,'frozen':a,'new':b})
if new is not None: compare(json.loads(old),json.loads(new))
dump(out/'execution.json',{'command':cmd,'cwd':str(tree),'original_entry_runs_this_batch':1,
 'branch':'--large-baseline only; not default audit and not generic CLI','started_unix':started,
 'wall_seconds':elapsed,'returncode':result.returncode,'stdout_bytes':len(result.stdout),
 'stderr_bytes':len(result.stderr),'original_milp_calls':1,'exact_fixed_cone_lp_calls':0,
 'all_other_original_entry_runs_this_batch':0,'frozen_report_sha256':hashlib.sha256(old).hexdigest(),
 'new_report_sha256':hashlib.sha256(new).hexdigest() if new else None,
 'new_report_bytes':len(new) if new else 0,'byte_identical':new==old,'json_differences':changes,
 'strategy_table_persisted_by_original_branch':False,
 'environment_overrides':{k:env[k] for k in ['PYTHONDONTWRITEBYTECODE','PYTHONHASHSEED','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']}})
print(json.dumps({'returncode':result.returncode,'wall_seconds':elapsed,'differences':changes},ensure_ascii=False))
if result.returncode: raise SystemExit(result.returncode)
