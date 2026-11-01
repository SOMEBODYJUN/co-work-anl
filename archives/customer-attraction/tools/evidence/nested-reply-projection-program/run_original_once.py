"""Replay the unmodified frozen main exactly once in an isolated output directory."""
from pathlib import Path
import hashlib,json,platform,shutil,subprocess,sys,time
import numpy,scipy
HERE=Path(__file__).resolve().parent
original=HERE/'original/nested_reply_projection.py'
point=HERE/'related/combined_branch_latest_exact.json'
replay=HERE/'replay';replay.mkdir(exist_ok=True)
script=replay/original.name
shutil.copy2(original,script)
assert hashlib.sha256(script.read_bytes()).hexdigest()=='19ef4b99b8a315d0f4a4f064eece25dd240601d28729f935d5960ce17d124b96'
assert hashlib.sha256(point.read_bytes()).hexdigest()=='50d51fadd1bd5cc6f2eb2230f1c35ac7001e21a5a75d11e91f4e259c1bf69224'
cmd=[sys.executable,str(script),'--point',str(point)]
started=time.time();tic=time.perf_counter()
p=subprocess.run(cmd,cwd=replay,capture_output=True)
elapsed=time.perf_counter()-tic
(replay/'stdout.txt').write_bytes(p.stdout);(replay/'stderr.txt').write_bytes(p.stderr)
record={'command':cmd,'cwd':str(replay),'started_unix':started,'wall_seconds':elapsed,'exit_code':p.returncode,
        'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
        'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(point.read_bytes()).hexdigest(),
        'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'original_main_calls':1,
        'linprog_calls_if_success':6,'scope':'original discovery on one specified necessary-point input; exact acceptance is in original code, no full-SPE validation'}
(replay/'execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
print(p.stdout.decode())
if p.returncode:print(p.stderr.decode())
raise SystemExit(p.returncode)
