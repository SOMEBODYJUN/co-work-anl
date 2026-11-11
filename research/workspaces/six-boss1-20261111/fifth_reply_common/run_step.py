"""Record actual local mathematical commands, output, exit status, and source bytes."""
from pathlib import Path
from hashlib import sha256
import datetime, json, subprocess, sys, time
HERE=Path(__file__).resolve().parent
name=sys.argv[1];script=HERE/(name+'.py');sha=sha256(script.read_bytes()).hexdigest()
manifest=HERE/'execution_manifest.json';old=json.loads(manifest.read_text()) if manifest.exists() else []
tag=f'{len(old)+1:02d}-'+name
saved=HERE/'executed_sources';saved.mkdir(exist_ok=True)
snapshot=saved/(name+'-'+sha+'.py');snapshot.write_bytes(script.read_bytes())
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
cmd=[sys.executable,str(script),*sys.argv[2:]]
p=subprocess.run(cmd,text=True,capture_output=True,cwd=HERE.parents[3])
(HERE/(tag+'.stdout.txt')).write_text(p.stdout);(HERE/(tag+'.stderr.txt')).write_text(p.stderr)
record=dict(name=name,command=cmd,start_utc=start,elapsed_seconds=time.monotonic()-t,exit_code=p.returncode,
            script_sha256=sha,source_snapshot=str(snapshot.relative_to(HERE)),stdout=tag+'.stdout.txt',stderr=tag+'.stderr.txt')
old.append(record);manifest.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False));print(p.stdout,end='');print(p.stderr,end='',file=sys.stderr)
sys.exit(p.returncode)
