"""Record one unchanged original floor-main verification and immutable inputs."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys
import time
import numpy
import scipy

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent/'combined-branch-runtime'
OUT = HERE/'rerun'
SOURCE = RUNTIME/'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/all_reply_actual_floors.py'
POINT = SOURCE.parent/'all_reply_floors_exact.json'
SHA = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    assert not (OUT/'execution.json').exists(), 'Do not overwrite or repeat the recorded original execution'
    manifest = json.loads((RUNTIME/'current-frozen-files-manifest.json').read_text())
    before = []
    for entry in manifest:
        p = RUNTIME/entry['path']
        assert p.is_file() and SHA(p) == entry['sha256'] and p.stat().st_size == entry['size'], entry['path']
        before.append({'path':entry['path'],'id':entry['id'],'bytes':entry['size'],'sha256':entry['sha256']})
    assert SHA(POINT) == 'f6f4d5c28857e8e6350bdc8528daa6109122bce8a6fb00e8ac5c3150ffc42314'
    assert SHA(SOURCE) == '24302c9a3e2b29d373d7d92d28df661e9f65c39f222365d12932e87574d8bdef'
    capture = HERE/'capture_floor_main.py'
    cmd=[sys.executable,'-B',str(capture),str(RUNTIME),str(OUT)]
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    t=time.monotonic()
    result=subprocess.run(cmd,cwd=RUNTIME,capture_output=True)
    (OUT/'stdout.txt').write_bytes(result.stdout)
    (OUT/'stderr.txt').write_bytes(result.stderr)
    unchanged=all(SHA(RUNTIME/e['path'])==e['sha256'] for e in before)
    event={'scope':'first verification of the floor4963 frozen weight point by unchanged original all_reply_actual_floors main, with read-only return-local observer; no 9900 discovery or LP',
           'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'wall_seconds':time.monotonic()-t,'command':cmd,'original_argv':[str(SOURCE),'--priced','--optimum','--verify'],
           'cwd':str(RUNTIME),'python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,
           'assertions_enabled':not sys.flags.optimize,'exit_code':result.returncode,
           'source_sha256':SHA(SOURCE),'point_sha256':SHA(POINT),'capture_wrapper_sha256':SHA(capture),
           'stdout_sha256':SHA(OUT/'stdout.txt'),'stderr_bytes':len(result.stderr),
           'prechecked_frozen_files':before,'all_prechecked_frozen_bytes_unchanged':unchanged,
           'original_main_invocations':1,'entry_mechanism':'runpy.run_path(original, run_name=__main__), original argv; profile observes main return without modifying locals',
           'not_claimed':['literal direct-script process invocation','independent full 4963-row derivation','exact optimum','complete SPE']}
    if (OUT/'original-row-slacks.json').exists():event['row_report_sha256']=SHA(OUT/'original-row-slacks.json')
    (OUT/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
    print(result.stdout.decode(),end='')
    if result.stderr:print(result.stderr.decode(),file=sys.stderr,end='')
    assert result.returncode == 0 and unchanged
