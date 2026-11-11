"""One small phase-I call after the complete symbolic and literal preflight."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import time
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'


def sha(p):return sha256(p.read_bytes()).hexdigest()


def main():
    output=HERE/'phase_I_discovery.json'
    assert not output.exists(),'The authorized single discovery was already saved; do not repeat it.'
    data=json.loads((HERE/'symbolic_lift.json').read_bytes())
    audit=json.loads((HERE/'preflight_literal_audit.json').read_bytes())
    assert audit['symbolic_lift_sha256']==sha(HERE/'symbolic_lift.json')
    assert audit['point_sha256']==sha(POINT)==data['point_sha256']
    w=[F(c['weight']) for c in json.loads(POINT.read_bytes())['columns'][:4849]]
    ri=[];ci=[];av=[];rhs=[]
    for i,row in enumerate(data['rows']):
        fixed=F()
        for j,t in row['row']:
            v=F(t)
            if j<4849:fixed+=v*w[j]
            else:ri.append(i);ci.append(j-4849);av.append(-float(v))
        rhs.append(fixed)
    n=len(data['new_columns']);m=len(rhs)
    A=coo_matrix((av,(ri,ci)),shape=(m,n)).tocsr()
    A=hstack([A,-np.ones((m,1))],format='csr')
    c=np.zeros(n+1);c[-1]=1
    start=time.perf_counter()
    result=linprog(c,A_ub=A,b_ub=np.array([float(x) for x in rhs]),bounds=(0,None),method='highs',
                   options={'time_limit':45.0,'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    report={'scope':'Floating discovery only; no exact feasibility or separation conclusion.',
            'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json'),
            'preflight_sha256':sha(HERE/'preflight_literal_audit.json'),'source_sha256':sha(Path(__file__)),
            'scipy_version':scipy.__version__,'shape':[m,n+1],
            'time_limit_seconds':45,'elapsed_seconds':time.perf_counter()-start,'linprog_calls':1,
            'success':bool(result.success),'status':int(result.status),'message':str(result.message),
            'iterations':int(result.nit),'phase_I':None if result.fun is None else float(result.fun),
            'x':None if result.x is None else result.x.tolist(),
            'row_slack':None if result.ineqlin.residual is None else result.ineqlin.residual.tolist(),
            'lambda':None if result.ineqlin.marginals is None else (-result.ineqlin.marginals).tolist(),
            'lower_marginals':None if result.lower.marginals is None else result.lower.marginals.tolist(),
            'fixed_old_row_values':[str(v) for v in rhs]}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('x','row_slack','lambda','lower_marginals','fixed_old_row_values')},ensure_ascii=False))
    assert result.success


if __name__=='__main__':main()
