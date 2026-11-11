"""Small finite probe of the analytically forced zero-fee 53-ray face.

This is a separate calculation, not a dependency of the frozen Actions job.
It uses only the already generated 271 b=0 types from the local loop. A beta
below 2 on this subset proves nothing about the full 35-ray face.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.optimize import linprog
from cone import HERE, NAMES, literal_vector


def main():
    source = HERE/'local_loop/checkpoint.json'
    state = json.loads(source.read_text())
    witnesses = [w for w in state['witnesses'] if w['background'] == 0]
    a, k = literal_vector(witnesses[0])
    ids = [j for j in range(53) if k[j] == 0]
    A, rhs = [], []
    for w in witnesses:
        a, kk = literal_vector(w)
        assert kk == k
        V = int(any(map(int, w['bits'][:5])))
        R = int(w['d'] > 0)
        A.append([float(a[j]) for j in ids]+[-V])
        rhs.append(-R)
    fit = linprog([0]*len(ids)+[1], A_ub=A, b_ub=rhs, bounds=(0, None), method='highs-ds')
    result = {'scope': 'Finite necessary probe only; not full separation or an exact bound',
              'input': str(source), 'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'finite_types': len(witnesses), 'ray_names': [NAMES[j] for j in ids],
              'lp_status': int(fit.status), 'numeric_min_beta': float(fit.fun) if fit.success else None,
              'positive_weights': int(np.count_nonzero(fit.x[:-1] > 1e-10)) if fit.success else None,
              'conclusion': 'The existing small type subset does not yet obstruct beta=2 on the 35-ray face.'}
    (HERE/'capacity_free_face_probe.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
