#!/usr/bin/env python3
"""One original default __main__ entry, transparently recording its two solves.
No additional graph solve, anonymous sample, potential sample, or 84-point audit.
"""
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import importlib.util
import io
import json
import platform
import runpy
import sys
import time

P=Path(__file__).resolve().parent
R=Path('/workspace/scratch/9559bf893d22/boss3_anonymous_potential_runtime')
assert not R.exists(), 'fresh isolated runtime required'
R.mkdir()
for name in ('payoff_state_flow.py','cyclic_nonpotential_obstruction.py'):
    (R/name).write_bytes((P/'original'/name).read_bytes())
spec=importlib.util.spec_from_file_location('payoff_state_flow',R/'payoff_state_flow.py')
flow=importlib.util.module_from_spec(spec);sys.modules[spec.name]=flow;spec.loader.exec_module(flow)
original=flow.PayoffGraph.solve
calls=[]
def record(self,query,potential=False):
    start=time.perf_counter();result=original(self,query,potential)
    calls.append({'potential':potential,'query':list(map(str,query)),
                  'vertices':len(self.vertices),'arcs':len(self.edges),'backgrounds':len(self.backgrounds),
                  'wall_seconds':time.perf_counter()-start,'result':result})
    return result
flow.PayoffGraph.solve=record
stdout=io.StringIO();stderr=io.StringIO();start=time.perf_counter()
with redirect_stdout(stdout),redirect_stderr(stderr):
    runpy.run_path(str(R/'cyclic_nonpotential_obstruction.py'),run_name='__main__')
elapsed=time.perf_counter()-start
flow.PayoffGraph.solve=original
assert len(calls)==2 and not calls[0]['potential'] and calls[1]['potential']
assert not calls[0]['result']['success']
assert calls[1]['result']['success'] and calls[1]['result']['exact_ok']
(P/'cyclic-original-main.stdout').write_text(stdout.getvalue())
(P/'cyclic-original-main.stderr').write_text(stderr.getvalue())
(P/'cyclic-current-report.json').write_text(json.dumps(json.loads(stdout.getvalue()),indent=2)+'\n')
(P/'cyclic-two-solve-results.json').write_text(json.dumps(calls,indent=2)+'\n')
import numpy,scipy
event={'kind':'one original default __main__ executed under transparent solve-result recorder',
       'command':'python replay_cyclic_entry.py > replay-wrapper.stdout 2> replay-wrapper.stderr',
       'cwd':str(P),'runtime':str(R),'returncode':0,'original_main_runs':1,
       'original_solve_calls':2,'original_LP_calls':2,'additional_graph_solve_calls':0,
       'random_samples_generated':0,'potential_84_point_rechecks':0,
       'main_internal_wall_seconds':elapsed,'python':platform.python_version(),
       'numpy':numpy.__version__,'scipy':scipy.__version__,
       'assertions_enabled':__debug__,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'input_files':[{'file':name,'sha256':hashlib.sha256((R/name).read_bytes()).hexdigest()}
                      for name in ('payoff_state_flow.py','cyclic_nonpotential_obstruction.py')]}
(P/'cyclic-replay-event.json').write_text(json.dumps(event,indent=2)+'\n')
print(json.dumps(event),flush=True)
print(json.dumps({'original_report':json.loads(stdout.getvalue()),'ordinary':calls[0]['result'],
                  'potential_exact_ok':calls[1]['result']['exact_ok'],
                  'potential_arc_support':calls[1]['result']['arc_support']}),flush=True)
