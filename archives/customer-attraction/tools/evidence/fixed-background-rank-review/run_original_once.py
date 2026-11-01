"""One untouched successor-review CLI, isolated from all frozen files."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import time

BASE = Path('/workspace/scratch/c0ab78c47566')
SOURCE = BASE/'r18-check-fixed-background-rank.py'
FROZEN = BASE/'r18-fixed-background-rank-review.json'
RUN = BASE/'r18-fixed-background-rank-review-run'
RUN.mkdir(exist_ok=False)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE) == 'b867a608f4b0805b3c13573d3fd9b73d51a7133328c8b3fdcbf6c42eb8382cee'
assert sha(FROZEN) == 'a32a40a239c64bb266568edd25fe403f869c208c5148464f830e2ea5538b006c'
target = RUN/'check_fixed_background_rank.py'
shutil.copyfile(SOURCE,target)
before = sha(target)
command = [sys.executable,'-I','-B',str(target)]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.perf_counter()
process = subprocess.run(command,cwd=RUN,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
elapsed = time.perf_counter()-t
(RUN/'stdout.txt').write_bytes(process.stdout)
(RUN/'stderr.txt').write_bytes(process.stderr)
out = RUN/'fixed_background_rank_review.json'
event = {
    'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'command':command,'cwd':str(RUN),'returncode':process.returncode,'wall_seconds':elapsed,
    'python':sys.version,'assertions_enabled_by_isolated_non_O_invocation':True,
    'source_sha256_before':before,'source_sha256_after':sha(target),
    'frozen_report_sha256':sha(FROZEN),
    'new_output_exists':out.exists(),
    'new_output_byte_identical_to_frozen':out.exists() and out.read_bytes()==FROZEN.read_bytes(),
    'files':{name:{'bytes':(RUN/name).stat().st_size,'sha256':sha(RUN/name)}
             for name in ['check_fixed_background_rank.py','stdout.txt','stderr.txt'] +
             (['fixed_background_rank_review.json'] if out.exists() else [])},
    'original_successor_main_calls':1,'author_main_calls':0,
    'additional_original_helper_calls':0,'new_independent_matrix_scans':0,
    'LP_calls':0,'SPE_solver_calls':0,
    'observation':'direct untouched original CLI; no runpy/profile/helper interception; no matrix capture',
    'rank_calls_from_static_loop_structure_not_dynamic_trace':672,
}
(RUN/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
assert process.returncode==0
assert event['new_output_byte_identical_to_frozen'] and before==sha(target)
print(json.dumps({'status':'pass','wall_seconds':elapsed,'returncode':process.returncode,
    'output_bytes':out.stat().st_size,'output_sha256':sha(out),
    'stdout_bytes':len(process.stdout),'stderr_bytes':len(process.stderr)},ensure_ascii=False))
