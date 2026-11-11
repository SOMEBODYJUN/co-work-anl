"""Record exact-recovery subprocesses without touching frozen input files."""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json,os,platform,subprocess,sys,time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parents[3]
stage=sys.argv[1]
assert stage in ('sameW','freeW','dual','verify')
source=ROOT/('verify_certificates.py' if stage=='verify' else 'actions_stage.py')
argv=[sys.executable,'-B',str(source.relative_to(REPO))]
if stage=='verify':argv.append(str(HERE))
else:argv.extend([stage,str(HERE)])
out=HERE/(stage+'_stdout.txt');err=HERE/(stage+'_stderr.txt')
receipt=HERE/('execution_'+stage+'.json')
assert not any(p.exists() for p in (out,err,receipt))
sha=lambda p:sha256(p.read_bytes()).hexdigest()
snapshotdir=HERE/'executed_sources';snapshotdir.mkdir(exist_ok=True)
snapshot=snapshotdir/(source.stem+'_'+sha(source)+source.suffix)
if not snapshot.exists():snapshot.write_bytes(source.read_bytes())
dependencies={name:sha(ROOT/name) for name in ('assemble_solve.py','recover.py','verify_certificates.py')}
record={'argv':argv,'driver_argv':[sys.executable,*sys.argv],'cwd':str(REPO),
    'python':platform.python_version(),'source_sha256':sha(source),'source_snapshot':str(snapshot.relative_to(HERE)),
    'dependency_sha256':dependencies,'driver_sha256':sha(Path(__file__)),
    'started_utc':datetime.now(timezone.utc).isoformat(),'optimizer_calls':0,
    'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','FULL624_EXACT_TIME_LIMIT':'170'}}
started=time.monotonic()
with out.open('w') as f,err.open('w') as g:
    result=subprocess.run(argv,cwd=REPO,stdout=f,stderr=g,
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','FULL624_EXACT_TIME_LIMIT':'170'})
record.update(exit_code=result.returncode,status='SUCCESS' if result.returncode==0 else 'FAILED',
    elapsed_seconds=time.monotonic()-started,ended_utc=datetime.now(timezone.utc).isoformat(),
    stdout_sha256=sha(out),stderr_sha256=sha(err))
receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False),flush=True)
sys.exit(result.returncode)
