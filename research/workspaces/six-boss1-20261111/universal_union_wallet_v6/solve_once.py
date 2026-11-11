"""The one explicitly authorized v6 discovery LP. Refuses any retry."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from datetime import datetime,timezone
import json

HERE=Path(__file__).resolve().parent
sha=lambda p:sha256(p.read_bytes()).hexdigest()
data=json.loads((HERE/'exact_input.json').read_text())
pre=json.loads((HERE/'source_check.json').read_text())
release=json.loads((HERE/'main_release.json').read_text())
scale_data=json.loads((HERE/'numerical_scaling.json').read_text())
assert pre['status']=='PASS' and pre['input_sha256']==sha(HERE/'exact_input.json')
assert release['authorized_by']=='/root' and release['optimizer_calls_authorized']==1
assert release['status']=='MAIN_EXPLICIT_867_ROW_RELEASE'
assert len(data['raw_rows'])==867 and data['variables']==257
assert not (HERE/'single_lp_started.txt').exists() and not (HERE/'discovery_output.json').exists(), 'No optimizer retry permitted'
rows=data['unique_rows']
scales=[F(scale_data['scales'][r['name']]) for r in rows]
assert all(s>0 for s in scales)
import numpy as np
import scipy
from scipy.optimize import linprog
A=np.array([[-float(F(r['a'].get(str(j),'0'))/s) for j in range(257)] for r,s in zip(rows,scales)])
b=np.array([-float(F(r['rhs'])/s) for r,s in zip(rows,scales)])
cost=np.array([float(F(data['objective'].get(str(j),'0'))) for j in range(257)])
eq=np.array([[float(F(data['equality']['a'].get(str(j),'0'))) for j in range(257)]])
record={'authorized_by':'/root','scope':'Exactly one867-row/257-column v6 LP after full source preflight',
    'input_sha256':sha(HERE/'exact_input.json'),'release_sha256':sha(HERE/'main_release.json'),
    'source_check_sha256':sha(HERE/'source_check.json'),'source_review_sha256':sha(HERE/'source_review.md'),
    'scaling_sha256':sha(HERE/'numerical_scaling.json'),'start_utc':datetime.now(timezone.utc).isoformat()}
with (HERE/'single_lp_started.txt').open('x') as f:f.write(json.dumps(record,indent=2)+'\n')
try:
    result=linprog(cost,A_ub=A,b_ub=b,A_eq=eq,b_eq=[1.],bounds=(0,None),method='highs')
except Exception as error:
    failure=dict(record,optimizer_calls=1,success=False,status='EXCEPTION',exception_type=type(error).__name__,message=str(error))
    (HERE/'discovery_output.json').write_text(json.dumps(failure,indent=2)+'\n')
    raise
out=dict(record,solver='scipy.optimize.linprog/highs',scipy_version=scipy.__version__,optimizer_calls=1,
    success=bool(result.success),status=int(result.status),message=result.message,iterations=int(result.nit),
    variables=257,raw_rows=867,unique_rows=len(rows),row_scales=[str(s) for s in scales],
    objective=None if result.fun is None else float(result.fun),x=None if result.x is None else result.x.tolist(),
    inequality_residual_scaled=None if result.ineqlin.residual is None else result.ineqlin.residual.tolist(),
    inequality_marginals_scaled=None if result.ineqlin.marginals is None else result.ineqlin.marginals.tolist(),
    equality_marginals=None if result.eqlin.marginals is None else result.eqlin.marginals.tolist(),
    lower_marginals=None if result.lower.marginals is None else result.lower.marginals.tolist(),
    finish_utc=datetime.now(timezone.utc).isoformat())
(HERE/'discovery_output.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['success','status','objective','iterations','variables','raw_rows','unique_rows']},indent=2))
if result.x is not None:print('positive_columns',[(j,float(v)) for j,v in enumerate(result.x) if v>1e-9])
