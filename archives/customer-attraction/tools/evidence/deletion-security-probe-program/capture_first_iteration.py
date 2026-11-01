"""Run unmodified deletion_probe.py through one iteration; stop before iteration 2.

The trace only observes module-line locals and raises at the next outer-loop
header. It does not replace an optimizer, change source or alter first-loop data.
"""
import argparse
import contextlib
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import runpy
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runtime', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
root = args.runtime.resolve()
source = root / 'research/workspaces/customer-attraction/R-5e9dedd2606746ff8afbbb73bf816e7a/security/static/deletion_probe.py'
out = args.out.resolve()
out.mkdir(parents=True, exist_ok=True)
if (out / 'execution.json').exists():
    raise RuntimeError('Unique first-iteration event already exists')
before = hashlib.sha256(source.read_bytes()).hexdigest()
os.chdir(root)
stream, errors = io.StringIO(), io.StringIO()
records, snapshot = [], {}

class FirstIterationComplete(Exception):
    pass

def take_snapshot(g):
    snapshot.update(n=g['n'], k=g['k'], it=g['it'], masks=g['masks'],
                    seed_weights=g['ww'],
                    sigma=[dict(history=list(h), action=a) for h, a in g['sig'].items()],
                    root=g['z0'], gamma=[[str(x) for x in row] for row in g['gam']],
                    coverage=[str(x) for x in g['c']],
                    queries=[{str(a): str(v) for a, v in p.items()} for p in g['pp']],
                    best_score=g['best'][0])

def observe(frame, event, arg):
    if frame.f_code.co_filename != str(source) or frame.f_code.co_name != '<module>':
        return None
    if event == 'line':
        g = frame.f_globals
        if frame.f_lineno == 33:
            result = g['res']
            records.append(dict(query={str(a): str(v) for a, v in g['p'].items()},
                                success=bool(result.success), status=int(result.status),
                                message=str(result.message),
                                objective=float(result.fun) if result.fun is not None else None,
                                solution=result.x.tolist() if result.x is not None else None,
                                deletion_rows=[[str(x) for x in row] for row in g['ub'][-g['n']:]]))
        elif frame.f_lineno == 34:
            take_snapshot(g)
        elif frame.f_lineno == 13 and g.get('it') == 0:
            raise FirstIterationComplete()
    return observe

start = datetime.datetime.now(datetime.timezone.utc).isoformat()
clock = time.monotonic()
mode = None
with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(errors):
    sys.settrace(observe)
    try:
        runpy.run_path(str(source), run_name='__main__')
        mode = 'original_natural_exit_after_first_positive_candidate'
    except FirstIterationComplete:
        mode = 'controlled_stop_at_outer_header_before_second_iteration'
    finally:
        sys.settrace(None)
elapsed = time.monotonic() - clock
import numpy
import scipy
assert len(records) == 22 and snapshot['it'] == 0
snapshot['LP_results'] = records
(out / 'first-iteration.json').write_text(json.dumps(snapshot, indent=2) + '\n')
(out / 'stdout.txt').write_text(stream.getvalue())
(out / 'stderr.txt').write_text(errors.getvalue())
candidate = source.with_name('deletion_candidate.json')
if candidate.exists():
    (out / 'candidate.json').write_bytes(candidate.read_bytes())
event = dict(start_utc=start, end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             wall_seconds=elapsed, execution_mode=mode, source=str(source), cwd=str(root),
             python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__,
             source_sha256_before=before, source_sha256_after=hashlib.sha256(source.read_bytes()).hexdigest(),
             source_top_level_entries=1, completed_outer_iterations=1, declared_outer_limit=100,
             LP_calls=22, original_makepolicy_calls=1, historical_scan_reproduced=False,
             candidate_written=candidate.exists(), trace_changed_source=False,
             trace_scope='Observe original module lines33/34; stop on second visit to line13 only. Optimizer and functions untouched.',
             captured_files={name: hashlib.sha256((out/name).read_bytes()).hexdigest()
                             for name in ('first-iteration.json','stdout.txt','stderr.txt')})
(out / 'execution.json').write_text(json.dumps(event, indent=2) + '\n')
print(stream.getvalue(), end='')
print(json.dumps(event, indent=2))
