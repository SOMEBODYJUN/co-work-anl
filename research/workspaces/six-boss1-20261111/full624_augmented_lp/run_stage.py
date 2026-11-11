"""Record the exact executed argv, source bytes, outputs and real exit status."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json,os,platform,subprocess,sys,time

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
name=sys.argv[1]
assert name.replace('_','').isalnum()
script=sys.argv[2]
source=HERE/script
argv=[sys.executable,'-B',str(source.relative_to(REPO)),*sys.argv[3:]]
out=HERE/(name+'_stdout.txt');err=HERE/(name+'_stderr.txt');receipt=HERE/('execution_'+name+'.json')
assert not any(p.exists() for p in (out,err,receipt))
sha=lambda p:sha256(p.read_bytes()).hexdigest()
snapshot=HERE/'executed_sources';snapshot.mkdir(exist_ok=True)
source_copy=snapshot/(source.stem+'_'+sha(source)+source.suffix)
if not source_copy.exists():source_copy.write_bytes(source.read_bytes())
record={'argv':argv,'driver_argv':[sys.executable,*sys.argv],'cwd':str(REPO),
    'python':platform.python_version(),'source_sha256':sha(source),'source_snapshot':str(source_copy.relative_to(HERE)),
    'driver_sha256':sha(Path(__file__)),'started_utc':datetime.now(timezone.utc).isoformat()}
start=time.monotonic()
try:
    with out.open('w') as f,err.open('w') as g:
        result=subprocess.run(argv,cwd=REPO,stdout=f,stderr=g,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    record['exit_code']=result.returncode
    record['status']='SUCCESS' if result.returncode==0 else 'FAILED'
finally:
    record.update(elapsed_seconds=time.monotonic()-start,ended_utc=datetime.now(timezone.utc).isoformat(),
        stdout_sha256=sha(out),stderr_sha256=sha(err))
    receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False),flush=True)
sys.exit(record['exit_code'])
