#!/usr/bin/env python3
"""Run four unchanged audits in separate copies; freeze original reports.

The robust audit is run through runpy with a call profiler that only records
actual threshold_extrema arguments; it does not replace any audit function.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = Path('research/workspaces/shared/R-4018d5657f5d492ba41aa074bf9a5bbd/application_drafts')
RUN = ROOT / 'replay'
RUN.mkdir(exist_ok=True)
CONFIG = [
 ('cycle_intervention', 'audit.py', 'audit.json', 'audit.json'),
 ('independent_value_attack', 'audit_sparse_gate.py', 'sparse_gate_audit.json', 'sparse_gate_audit.json'),
 ('root_feedback', 'feedback_cycle_audit.py', None, 'feedback_cycle_audit.json'),
 ('robust_dynamics', 'robust_calibration_audit.py', 'audit_result.json', 'audit_result_v2.json'),
]
WRAPPER = '''import json,runpy,sys
from pathlib import Path
calls=[]
def capture(frame,event,arg):
    if event=='call' and frame.f_code.co_name=='threshold_extrema':
        calls.append({k:[str(x) for x in frame.f_locals[k]] for k in ('num','den','lower','upper')})
sys.setprofile(capture)
try:
    runpy.run_path(sys.argv[1],run_name='__main__')
finally:
    sys.setprofile(None)
    Path('actual-threshold-inputs.json').write_text(json.dumps(calls,indent=2)+'\\n')
'''

def run(cfg):
    group, code, report, frozen_name = cfg
    source = ROOT / 'original' / BASE / group / code
    work = RUN / group
    work.mkdir(exist_ok=True)
    destination = work / code
    shutil.copyfile(source, destination)
    if report and (work / report).exists():
        raise RuntimeError('Use a new output directory rather than replacing a prior run: ' + str(work))
    command = [sys.executable, '-B', code]
    if group == 'robust_dynamics':
        (work / 'capture_inputs.py').write_text(WRAPPER)
        command = [sys.executable, '-B', 'capture_inputs.py', code]
    result = subprocess.run(command, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (work / 'stdout.txt').write_bytes(result.stdout)
    (work / 'stderr.txt').write_bytes(result.stderr)
    assert result.returncode == 0, (group, result.stderr.decode())
    actual_bytes = (work / report).read_bytes() if report else result.stdout
    old = ROOT / 'original' / BASE / group / frozen_name
    actual, frozen = json.loads(actual_bytes), json.loads(old.read_bytes())
    assert actual == frozen, (group, actual, frozen)
    row = {'group':group, 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
           'copy_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),
           'exit_code':result.returncode, 'frozen_report':str(BASE/group/frozen_name),
           'json_equal':True, 'report_byte_equal':actual_bytes==old.read_bytes(),
           'actual_result':actual, 'input_scope':'complete deterministic inputs in unchanged source'}
    if group == 'robust_dynamics':
        v1 = json.loads((ROOT/'original'/BASE/group/'audit_result.json').read_bytes())
        row['v1_difference'] = {k:{'old':v1.get(k),'new':actual.get(k)} for k in actual.keys()|v1.keys() if actual.get(k)!=v1.get(k)}
        row['actual_threshold_input_calls'] = len(json.loads((work/'actual-threshold-inputs.json').read_text()))
    return row

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, help='new directory; prior run reports are never replaced')
    args = parser.parse_args()
    if args.output_dir:
        RUN = args.output_dir.resolve()
        RUN.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(run, CONFIG))
    output = {'runs':rows, 'all_passed':True, 'frozen_originals_never_run_in_place':True}
    (RUN/'comparison.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{'group':r['group'],'json_equal':r['json_equal'],'report_byte_equal':r['report_byte_equal']} for r in rows]))
