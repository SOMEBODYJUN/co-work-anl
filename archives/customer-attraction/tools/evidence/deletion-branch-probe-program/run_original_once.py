"""Isolate the unmodified top-level entry; preserve its self-overwrite behavior."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import numpy
import scipy

BASE=Path('/workspace/scratch/c0ab78c47566')
SHARED=BASE/'round15-deletion-runtime'
OUT=BASE/'round15-deletion36-original-event'
RUNTIME=OUT/'runtime'
SOURCE=BASE/'deletion-36-source.py'
TAX=SHARED/'research/workspaces/customer-attraction/R-5e9dedd2606746ff8afbbb73bf816e7a/security/static/tax_probe.py'

def fp(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}

assert not OUT.exists(), 'This runner is single-use; retain the existing event.'
assert fp(SOURCE)=={'bytes':2574,'sha256':'b1c904461bf89c16ecee9d9e363aebd545d9a7117b5a7de4cf4ae2ff45ed0aef'}
assert fp(TAX)=={'bytes':1887,'sha256':'8f72ad4dc8464ef17883bce8f273faefe55152dd31b35aeee136c8bcf3579e21'}
(RUNTIME/'customer_attraction').mkdir(parents=True)
inputs=[]
for name in ['__init__.py','model.py','exact.py','certificate.py']:
    src=SHARED/'customer_attraction'/name;dst=RUNTIME/'customer_attraction'/name
    shutil.copyfile(src,dst);inputs.append({'runtime_path':str(dst.relative_to(RUNTIME)),'source_path':str(src),'before':fp(dst)})
ENTRY=RUNTIME/'deletion_36.py';shutil.copyfile(SOURCE,ENTRY);shutil.copyfile(TAX,RUNTIME/'tax_probe.py')
inputs += [{'runtime_path':'deletion_36.py','source_path':str(SOURCE),'before':fp(ENTRY)}, {'runtime_path':'tax_probe.py','source_path':str(TAX),'before':fp(RUNTIME/'tax_probe.py')}]
cmd=[sys.executable,'-B',str(ENTRY)]
start=datetime.now(timezone.utc).isoformat();tick=time.perf_counter()
completed=subprocess.run(cmd,cwd=RUNTIME,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
duration=time.perf_counter()-tick;end=datetime.now(timezone.utc).isoformat()
(OUT/'stdout.txt').write_bytes(completed.stdout);(OUT/'stderr.txt').write_bytes(completed.stderr)
for record in inputs:record['after']=fp(RUNTIME/record['runtime_path'])
changed=fp(ENTRY)!=fp(SOURCE)
if changed:shutil.copyfile(ENTRY,OUT/'post-entry-file.json')
event={'scope':'Unmodified deletion_36.py top-level execution once; isolated original output-path behavior retained; no entry renaming and no optimizer monkeypatch',
 'command':cmd,'cwd':str(RUNTIME),'started_utc':start,'finished_utc':end,'wall_seconds':duration,'exit_code':completed.returncode,
 'versions':{'python':sys.version.split()[0],'numpy':numpy.__version__,'scipy':scipy.__version__},'timeout_seconds':120,
 'original_top_level_executions':1,'deletion_probe_executions':0,'tax_probe_main_executions':0,'ExactSPESolver_calls':0,
 'LP_invocations_if_normal_completion':22,'LP_count_basis':'One iteration with all 6 pure, 15 uniform-pair and one uniform-all queries; source has no inner early exit. Not an instrumented solver trace.',
 'input_files':inputs,'entry_was_overwritten_by_original_output':changed,'candidate_expected_path':str(ENTRY),
 'preserved_post_entry_file':'post-entry-file.json' if changed else None,'stdout':fp(OUT/'stdout.txt'),'stderr':fp(OUT/'stderr.txt'),
 'immutable_primary_source_before_and_after':fp(SOURCE)}
(OUT/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exit_code':completed.returncode,'wall_seconds':duration,'entry_overwritten':changed,'stdout_bytes':len(completed.stdout),'stderr_bytes':len(completed.stderr)},indent=2))
