"""Run the unchanged author's finite CLI once in a new isolated directory."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
RUNTIME=HERE/'runtime'
RUNTIME.mkdir(exist_ok=False)
def digest(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
names=['cartesian_finite.py','cartesian_convexification_k4.json']
for name in names:shutil.copyfile(HERE/name,RUNTIME/name)
inputs=[digest(RUNTIME/name) for name in names]
expected=digest(HERE/'cartesian_two_copy_exact.json')
argv=[sys.executable,'-I','-B',str(RUNTIME/'cartesian_finite.py')]
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
start=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
result=subprocess.run(argv,cwd=RUNTIME,env=env,capture_output=True,check=False)
elapsed=time.perf_counter()-clock
(HERE/'stdout.txt').write_bytes(result.stdout)
(HERE/'stderr.txt').write_bytes(result.stderr)
output=RUNTIME/'cartesian_two_copy_exact.json'
event=dict(started_utc=start,finished_utc=datetime.now(timezone.utc).isoformat(),argv=argv,cwd=str(RUNTIME),
    python=platform.python_version(),returncode=result.returncode,wall_seconds=elapsed,
    stdout_bytes=len(result.stdout),stderr_bytes=len(result.stderr),
    inputs_before=inputs,inputs_after=[digest(RUNTIME/name) for name in names],
    frozen_expected_report=expected,generated_report=digest(output) if output.exists() else None,
    generated_equal_frozen=output.read_bytes()==(HERE/'cartesian_two_copy_exact.json').read_bytes() if output.exists() else False,
    original_CLI_invocations=1,profile_or_trace=False,functions_replaced=0,additional_original_calls=0,
    independent_SPE_audits=0,LP_calls=0,assertions_enabled=True,removed_PYTHONOPTIMIZE=True,
    script_digest=digest(Path(__file__)),scope='One unchanged original finite CLI; no independent 4368-comparison repeat, no asymptotic analyze or solver call')
(HERE/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(event,ensure_ascii=False))
raise SystemExit(result.returncode)
