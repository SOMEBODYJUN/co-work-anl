"""Execute one local research step; retain command, output and executed bytes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, time

HERE=Path(__file__).resolve().parent
name=sys.argv[1]
script=HERE/name
digest=hashlib.sha256(script.read_bytes()).hexdigest()
snap=HERE/'executed_sources'
snap.mkdir(exist_ok=True)
(snap/(script.stem+'-'+digest+'.py')).write_bytes(script.read_bytes())
command=[sys.executable,'-B',str(script),*sys.argv[2:]]
start=time.monotonic()
stamp=datetime.now(timezone.utc).isoformat()
run=subprocess.run(command,cwd=HERE.parents[3],capture_output=True,text=True)
log=HERE/'execution_manifest.json'
records=json.loads(log.read_text()) if log.exists() else []
step=len(records)+1
out=f'{step:02d}-{script.stem}.stdout.txt';err=f'{step:02d}-{script.stem}.stderr.txt'
(HERE/out).write_text(run.stdout);(HERE/err).write_text(run.stderr)
records.append(dict(step=step,argv=command,started_utc=stamp,script_sha256=digest,exit_code=run.returncode,
                    elapsed_seconds=time.monotonic()-start,stdout=out,stderr=err))
log.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(run.stdout,end='');print(run.stderr,end='',file=sys.stderr)
sys.exit(run.returncode)
