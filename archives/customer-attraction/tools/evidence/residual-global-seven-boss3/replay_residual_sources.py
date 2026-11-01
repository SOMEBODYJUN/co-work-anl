#!/usr/bin/env python3
"""The two finite original CLIs once each, plus one top-level partial LP run.
No import of either random test and no additional response-map search.
"""
from pathlib import Path
from fractions import Fraction as F
from contextlib import redirect_stdout, redirect_stderr
from itertools import product, combinations_with_replacement
import hashlib
import io
import json
import platform
import runpy
import subprocess
import sys
import time

P=Path(__file__).resolve().parent
R=Path('/workspace/scratch/9559bf893d22/boss3_residual_global_runtime')
assert not R.exists(), 'fresh runtime required'
R.mkdir()
events=[]
for entry,output in [('audit_residual_obstruction.py','audit_residual_obstruction.json'),
                     ('residual_two_full.py','residual_two_full.json')]:
    folder=R/entry.removesuffix('.py');folder.mkdir()
    code=(P/'original'/entry).read_bytes();source=folder/entry;source.write_bytes(code)
    command=[sys.executable,str(source)]
    start=time.perf_counter();result=subprocess.run(command,cwd=folder,capture_output=True)
    elapsed=time.perf_counter()-start
    (P/(entry+'.stdout')).write_bytes(result.stdout)
    (P/(entry+'.stderr')).write_bytes(result.stderr)
    assert result.returncode==0,(entry,result.stderr.decode())
    data=(folder/output).read_bytes();(P/('replayed_'+output)).write_bytes(data)
    expected=(P/'original'/output).read_bytes()
    assert json.loads(data)==json.loads(expected),(entry,'structured mismatch')
    events.append({'entry':entry,'mode':'one original CLI','command':command,'cwd':str(folder),
                   'returncode':result.returncode,'wall_seconds':elapsed,
                   'source_sha256':hashlib.sha256(code).hexdigest(),'structured_match':True,
                   'byte_exact':data==expected,'output_sha256':hashlib.sha256(data).hexdigest()})
    print(json.dumps(events[-1]),flush=True)

# The original partial LP is executed only here, allowing exact inspection of
# the same result object. run_path does not invoke its source a second time.
entry='residual_two_lp.py';folder=R/'partial';folder.mkdir()
source=folder/entry;source.write_bytes((P/'original'/entry).read_bytes())
stdout=io.StringIO();stderr=io.StringIO();start=time.perf_counter()
with redirect_stdout(stdout),redirect_stderr(stderr):
    ns=runpy.run_path(str(source),run_name='__main__')
elapsed=time.perf_counter()-start
(P/'residual_two_lp.py.stdout').write_text(stdout.getvalue())
(P/'residual_two_lp.py.stderr').write_text(stderr.getvalue())
lp=ns['lp'];bits=ns['bits'];names=ns['names']
assert lp.success
weights=tuple(F(float(v)).limit_denominator(10000) for v in lp.x)
columns=[ns['column'](z)[1] for z in bits]
G=list(zip(*columns))
W=tuple(F(int(v)) for v in ns['W']);O=tuple(F(int(v)) for v in ns['O'])
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
slacks=[dot(row,weights) for row in G]
nu=F(float(lp.eqlin.marginals[0])).limit_denominator(10000)
lam=tuple(F(float(-v)).limit_denominator(10000) for v in lp.ineqlin.marginals)
residual=[W[j]-nu*O[j]-sum((mu*row[j] for mu,row in zip(lam,G)),F(0))
          for j in range(len(bits))]
primal_ok=all(v>=0 for v in weights) and min(slacks)>=0 and dot(O,weights)==1
dual_ok=all(v>=0 for v in lam) and min(residual)>=0
value=dot(W,weights)
point={'partial_float_objective':float(lp.fun),'rational_recovery_primal_ok':primal_ok,
       'rational_recovery_dual_ok':dual_ok,'recovered_W':str(value),'recovered_residual_TS':str(dot(O,weights)),
       'recovered_dual_value':str(nu),'exact_partial_optimality':primal_ok and dual_ok and value==nu,
       'primal_slacks':[{'row':name,'slack':str(v)} for name,v in zip(names,slacks)],
       'dual_support':[{'row':name,'multiplier':str(v)} for name,v in zip(names,lam) if v],
       'dual_coordinate_residuals':list(map(str,residual)),
       'support':[{'bits':list(z),'weight':str(v)} for z,v in zip(bits,weights) if v]}

def utility(a,b):
    return sum((v*F(z[a],1+z[b]) for z,v in zip(bits,weights) if z[a]),F(0))
u1=utility(0,1);last=[]
for a in range(6):
    values=[utility(b,a) for b in range(6)];mx=max(values)
    br=[b for b,v in enumerate(values) if v==mx]
    root_min=min(utility(a,b) for b in br)
    last.append({'first':a,'last_payoffs':list(map(str,values)),'BR':br,
                 'minimum_root_payoff_over_BR':str(root_min),
                 'root_gain_over_prescribed_A':str(root_min-u1)})
point['root_u1']=str(u1);point['all_complete_last_reply_options']=last
point['nonextendable_first_actions']=[r['first'] for r in last if F(r['minimum_root_payoff_over_BR'])>u1]

# Compare the complete-program point with the exact audit's literal customer
# table and complete response map. This does not solve any further LP.
full=json.loads((P/'original/residual_two_full.json').read_text())
audit_ns=runpy.run_path  # deliberately not executed: the original exact CLI ran above
block_table=[('A',4),('AQR',2),('B',5),('BQR',2),('T',3),('TQ',2),('TR',2),('S',3),('SQ',2),('SR',2)]
labels='ABTSQR'
expected_types={tuple(int(a in likes) for a in labels):F(n,14) for likes,n in block_table}
full_types={tuple(z):F(v) for z,v in full[1]['types']}
assert full_types==expected_types
assert full[1]['replies']==[1,4,4,5,5,4]
point['full_report_exact_customer_table_divisor']=14
point['full_report_matches_audit_27_customer_types_and_reply']=True
(P/'partial-lp-exact-postcheck.json').write_text(json.dumps(point,indent=2)+'\n')
events.append({'entry':entry,'mode':'one original top-level execution under runpy plus exact postcheck of same LP',
               'path':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
               'source_execution_wall_seconds':elapsed,'original_LP_calls':1,
               'exact_recovery_success':point['exact_partial_optimality']})
import numpy,scipy
report={'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
        'events':events,'original_CLI_runs':2,'original_partial_top_level_runs':1,
        'full_program_configured_response_maps':216,'full_program_LP_calls':216,
        'partial_program_LP_calls':1,'random_test_imports_or_runs':0}
(P/'replay-events.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'partial':{k:v for k,v in point.items() if k not in ('primal_slacks','dual_coordinate_residuals','all_complete_last_reply_options','support')},'events_complete':True}),flush=True)
