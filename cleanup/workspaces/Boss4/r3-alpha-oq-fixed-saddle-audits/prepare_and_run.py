"""Freeze exact inputs first; --run invokes the original OQ main at most once."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
REPO=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-alpha-oq-fixed-saddle-audits')
EV=Path('archives/customer-attraction/tools/evidence/alpha-oq-fixed-saddle-primary')
PRIMARY=['9edffc6508386d059f3a','a33dd82cb4d23fab6163','8b9cf44d16a024398ef3','17bad95333c2be5f6402','34930f098ddd0db955e8']
RUNTIME=['847a210188334e25b4bd','8d74fd183eba467a811f']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(rel,obj):
    path=STAGE/rel;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def prepare():
    inv={r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    records=[]
    for sid in PRIMARY+RUNTIME:
        row=inv[sid];first=None;locations=[]
        for loc in row['sources']:
            raw=subprocess.check_output(['git','show',loc['commit']+':'+loc['path']],cwd=REPO,timeout=30,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'))
            assert len(raw)==row['size'] and sha(raw)==row['sha256']
            assert first is None or first==raw
            first=raw;locations.append(dict(loc,bytes_verified=True))
        rel=EV/'original'/row['path'];target=STAGE/rel
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(first)
        records.append(dict(id=sid,path=row['path'],blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,role='primary'if sid in PRIMARY else'runtime-dependency-only-not-done',saved_path=str(rel)))
    replay=STAGE/EV/'replay-tree'
    assert not replay.exists(),'Existing replay tree; no second prepare over an execution.'
    for sid in ['17bad95333c2be5f6402']+RUNTIME:
        row=inv[sid];dest=replay/row['path'];dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(STAGE/EV/'original'/row['path'],dest)
    dump(EV/'runtime-input-manifest.json',dict(claim_push='6976742b9e0d64b0fd6ea8cbd7dd34e3acac5bd2',sources=records,primary_count=5,primary_bytes=sum(inv[s]['size']for s in PRIMARY),runtime_dependency_count=2,runtime_dependency_bytes=sum(inv[s]['size']for s in RUNTIME),original_main='17bad95333c2be5f6402',original_helper_main_executed=False,helper_calls=['load(all)','query_lp'],alpha_one_executed_this_batch=False))
    print(json.dumps(dict(prepared=True,primary_count=5,primary_bytes=sum(inv[s]['size']for s in PRIMARY),runtime_dependencies=2),ensure_ascii=False))
def run():
    execution=STAGE/EV/'replay/execution.json'
    assert not execution.exists(),'Already attempted: do not rerun the original entrypoint.'
    data=json.loads((STAGE/EV/'runtime-input-manifest.json').read_text());rows={r['id']:r for r in data['sources']}
    code=rows['17bad95333c2be5f6402']['path'];report=rows['34930f098ddd0db955e8']['path'];tree=STAGE/EV/'replay-tree'
    assert not (tree/report).exists(),'Original output must start absent.'
    import numpy,scipy
    command=[sys.executable,code]
    dump(EV/'replay/execution.json',dict(status='original-main-started',executions_of_original_entrypoint=1,command=command,working_directory=str(tree),python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__))
    start=time.time()
    try:
        proc=subprocess.run(command,cwd=tree,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),capture_output=True,timeout=120)
        stdout,stderr,exitcode=proc.stdout,proc.stderr,proc.returncode
        error=None
    except subprocess.TimeoutExpired as exc:
        stdout,stderr,exitcode=exc.stdout or b'',exc.stderr or b'',None
        error='Original entrypoint timeout after 120 seconds; process terminated, no retry.'
    (STAGE/EV/'replay/stdout.txt').write_bytes(stdout)
    (STAGE/EV/'replay/stderr.txt').write_bytes(stderr)
    raw=(tree/report).read_bytes()if(tree/report).exists()else None
    if raw is not None:(STAGE/EV/'replay/optimal_query_fixed_cone_attack.json').write_bytes(raw)
    unchanged=all(sha((tree/rows[s]['path']).read_bytes())==rows[s]['sha256']for s in ['17bad95333c2be5f6402']+RUNTIME)
    dump(EV/'replay/execution.json',dict(status='finished'if error is None else'timeout',executions_of_original_entrypoint=1,command=command,working_directory=str(tree),python=sys.version,numpy=numpy.__version__,scipy=scipy.__version__,wall_seconds=time.time()-start,exit_code=exitcode,error=error,stdout_sha256=sha(stdout),stderr_sha256=sha(stderr),generated_report_bytes=len(raw)if raw is not None else None,generated_report_sha256=sha(raw)if raw is not None else None,frozen_report_sha256=rows['34930f098ddd0db955e8']['sha256'],generated_report_byte_identical_to_frozen=raw==(STAGE/EV/'original'/report).read_bytes()if raw is not None else False,code_and_inputs_unchanged=unchanged,scope='One original fixed-automaton/fixed-original-saddle OQ main; includes its three LP calls. Helper alternating-search main and old13 scalar main not executed. Floating optimum and rational recovered-point checks remain distinct.'))
    print(json.dumps(json.loads(execution.read_text()),ensure_ascii=False))
if __name__=='__main__':
    if '--run'in sys.argv:run()
    else:prepare()
