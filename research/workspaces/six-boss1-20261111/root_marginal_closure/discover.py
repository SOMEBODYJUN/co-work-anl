"""One small local phase-I LP over the saved full symbolic lift.

Floating results only discover a face.  They are not mathematical evidence.
No old 32-column root-incidence model is optimized here.
"""
from pathlib import Path
import hashlib
import json
import platform
import sys
import time
from fractions import Fraction as F

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    path = HERE/'symbolic_coefficients_exact.json'
    raw = json.loads(path.read_text())
    weights = [F(c['weight']) for c in raw['original_columns']]
    nm, na = raw['mu_column_count'], raw['aux_column_count']
    nv, mainrows = nm+na+1, raw['principal_row_count']
    phase = nv-1

    def matrix(records, equality=False):
        rr, cc, vv, rhs = [], [], [], []
        for i, r in enumerate(records):
            sign = 1 if equality else -1
            for k, value in r['mu']:
                rr.append(i); cc.append(k); vv.append(sign*float(F(value)))
            for k, value in r['aux']:
                rr.append(i); cc.append(nm+k); vv.append(sign*float(F(value)))
            constant = sum((weights[k]*F(value) for k, value in r['old']), F())
            rhs.append(float(-constant if equality else constant))
            if not equality and i < mainrows:
                rr.append(i); cc.append(phase); vv.append(-1.)
        return coo_matrix((vv, (rr, cc)), shape=(len(records), nv)).tocsr(), np.array(rhs)

    A, b = matrix(raw['rows'])
    E, f = matrix(raw['equalities'], True)
    c = np.zeros(nv); c[-1] = 1.
    start = time.perf_counter()
    result = linprog(c, A_ub=A, b_ub=b, A_eq=E, b_eq=f,
                     bounds=(0, None), method='highs-ds',
                     options={'primal_feasibility_tolerance': 1e-9,
                              'dual_feasibility_tolerance': 1e-9,
                              'time_limit': 45.})
    elapsed = time.perf_counter()-start
    out = dict(scope='Floating phase-I discovery only; exact recovery/independent Fraction audit are required.',
               point_sha256=raw['point_sha256'], symbolic_sha256=digest(path),
               script_sha256=digest(__file__), argv=[sys.executable, *sys.argv],
               status=int(result.status), success=bool(result.success), message=result.message,
               elapsed_seconds=elapsed, method='highs-ds', variables=nv, rows=A.shape[0],
               equalities=E.shape[0], mu_columns=nm, min_auxiliaries=na,
               python=platform.python_version(), scipy=scipy.__version__, numpy=np.__version__)
    if result.x is not None:
        out.update(phase=float(result.x[-1]), mu=[float(v) for v in result.x[:nm]],
                   aux=[float(v) for v in result.x[nm:-1]],
                   row_slacks=[float(v) for v in result.ineqlin.residual],
                   row_dual=[float(v) for v in result.ineqlin.marginals],
                   equality_dual=[float(v) for v in result.eqlin.marginals],
                   positive_mu=int(np.sum(result.x[:nm] > 1e-9)))
    (HERE/'phase1_discovery.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('mu', 'aux', 'row_slacks', 'row_dual', 'equality_dual')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
