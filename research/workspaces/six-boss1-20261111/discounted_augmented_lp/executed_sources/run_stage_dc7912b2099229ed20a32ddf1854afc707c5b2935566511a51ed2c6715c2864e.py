"""Record the exact executed source, command, output and exit code per stage."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
STAGES={"solve":"solve_full.py","recover":"recover_full.py","verify":"verify_certificates.py"}
stage=sys.argv[1]
assert stage in STAGES
script=HERE/STAGES[stage]
snapshots=HERE/"executed_sources"
snapshots.mkdir(exist_ok=True)
source_records=[]
for name in ("run_stage.py","solve_full.py","recover_full.py","verify_certificates.py"):
    path=HERE/name
    digest=sha256(path.read_bytes()).hexdigest()
    snapshot=snapshots/(path.stem+"_"+digest+".py")
    if snapshot.exists():
        assert snapshot.read_bytes()==path.read_bytes()
    else:
        snapshot.write_bytes(path.read_bytes())
    source_records.append({"source":name,"sha256":digest,"snapshot":str(snapshot.relative_to(HERE))})
start=time.time()
record={"stage":stage,"started_utc":datetime.now(timezone.utc).isoformat(),
        "command":[sys.executable,"-B",str(script)],"cwd":str(HERE),"sources":source_records,
        "stdout":stage+"_stdout.txt","stderr":stage+"_stderr.txt"}
env=dict(os.environ)
env["PYTHONDONTWRITEBYTECODE"]="1"
with (HERE/record["stdout"]).open("w") as out,(HERE/record["stderr"]).open("w") as err:
    process=subprocess.run(record["command"],cwd=HERE,env=env,stdout=out,stderr=err)
record.update({"returncode":process.returncode,"seconds":time.time()-start,
               "finished_utc":datetime.now(timezone.utc).isoformat(),
               "stdout_sha256":sha256((HERE/record["stdout"]).read_bytes()).hexdigest(),
               "stderr_sha256":sha256((HERE/record["stderr"]).read_bytes()).hexdigest()})
path=HERE/"execution_records.json"
records=json.loads(path.read_text()) if path.exists() else []
records.append(record)
path.write_text(json.dumps(records,indent=2)+"\n")
print(json.dumps(record,indent=2))
raise SystemExit(process.returncode)
