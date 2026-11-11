"""Exactly one local small phase-I LP; original point remains entirely fixed."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack

HERE = Path(__file__).resolve().parent
POINT = HERE.parent/'union_augmented_lp/augmented_lp_exact.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data = json.loads((HERE/'symbolic_lift.json').read_bytes())
    assert sha(POINT) == data['point_sha256']
    weights = [F(c['weight']) for c in json.loads(POINT.read_bytes())['columns']]
    old, n = data['fixed_old_columns'],len(data['new_columns'])
    ri,ci,vs = [],[],[]
    rhs = []
    for r,desc in enumerate(data['rows']):
        fixed = F()
        for j,v in desc['row']:
            q = F(v)
            if j<old:
                fixed += q*weights[j]
            else:
                ri.append(r);ci.append(j-old);vs.append(-float(q))
        rhs.append(fixed)
    m = len(rhs)
    A = coo_matrix((vs,(ri,ci)),shape=(m,n)).tocsr()
    # a X + b z + delta >= 0; minimize nonnegative shared delta.
    A = hstack([A,-np.ones((m,1))],format='csr')
    c = np.zeros(n+1); c[-1] = 1
    start = time.perf_counter()
    sol = linprog(c,A_ub=A,b_ub=np.array([float(x) for x in rhs]),bounds=(0,None),
                  method='highs', options={'time_limit':45.0,'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    elapsed = time.perf_counter()-start
    result = {
        'scope':'Discovery only; floating feasibility/infeasibility is not an exact certificate.',
        'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json'),'point_sha256':sha(POINT),
        'script_sha256':sha(Path(__file__)), 'scipy_version':scipy.__version__,
        'shape':[m,n+1], 'time_limit_seconds':45,'elapsed_seconds':elapsed,
        'status':int(sol.status),'message':str(sol.message),'success':bool(sol.success),
        'iterations':int(sol.nit), 'phase_I':None if sol.fun is None else float(sol.fun),
        'x':None if sol.x is None else sol.x.tolist(),
        'row_slack':None if sol.ineqlin.residual is None else sol.ineqlin.residual.tolist(),
        'dual_lambda':None if sol.ineqlin.marginals is None else (-sol.ineqlin.marginals).tolist(),
        'lower_marginals':None if sol.lower.marginals is None else sol.lower.marginals.tolist(),
        'fixed_old_row_values':[str(x) for x in rhs],
        'actual_calls_to_linprog':1,
    }
    (HERE/'phase_I_discovery.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('x','row_slack','dual_lambda','lower_marginals','fixed_old_row_values')},ensure_ascii=False))
    if not sol.success:
        raise SystemExit(2)


if __name__=='__main__':
    main()
