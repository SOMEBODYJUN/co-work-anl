"""Probe the explicit all-p, uniform-position full-terminal menu budget.

This is only a finite candidate test. It imports no equilibrium solver.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
CASES = [
    ('root_tax_failure', 'root_tax_failure'),
    ('global_decorrelation_failure', 'global_decorrelation_failure'),
    ('aggregate_theta_failure', 'onpath_budget_failure'),
    ('individual_security_failure', 'individual_security_failure'),
    ('local_security_increment', 'local_security_increment'),
]

def probe(game_name, cert_name):
    game = json.loads((ROOT / f'examples/customer_attraction/{game_name}.json').read_text())
    cert = json.loads((ROOT / f'evidence/certificates/customer_attraction/{cert_name}.json').read_text())
    n, k = game['players'], len(game['topics'])
    types = [(frozenset(row['topics']), row['multiplicity']) for row in game['customers']]
    policy = {tuple(row['history']): row['action'] for row in cert['strategy']['actions']}

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == n else terminal(h + (policy[h],))

    def query(a, z):
        return sum((F(w, 1 + sum(b in likes for b in z))
                    for likes, w in types if a in likes), F(0))

    z = terminal(())
    W = sum(w for likes, w in types if any(a in likes for a in z))
    matrices = [[[query(t, terminal(z[:i] + (a,))) for t in range(k)]
                 for a in range(k)] for i in range(n)]
    constraints = []
    for i, matrix in enumerate(matrices):
        for row in matrix:
            constraints.append([-float(x) for x in row] + [int(j == i) for j in range(n)])
    objective = [0] * k + [-1] * n
    lp = linprog(objective, A_ub=constraints, b_ub=[0] * len(constraints),
                 A_eq=[[1] * k + [0] * n], b_eq=[1], bounds=[(0, None)] * (k+n),
                 method='highs')
    if not lp.success:
        raise RuntimeError(lp.message)
    p = [F(float(v)).limit_denominator(10**7) for v in lp.x[:k]]
    if sum(p) != 1:
        p = [v / sum(p) for v in p]
    R = [min(sum((p[t] * row[t] for t in range(k)), F(0)) for row in matrix)
         for matrix in matrices]
    return {'game':game_name, 'outcome':z, 'W':W, 'p':list(map(str,p)),
            'R':list(map(str,R)), 'sum_R_minus_W':str(sum(R)-W),
            'lp_optimum_minus_W':-lp.fun-W}

if __name__ == '__main__':
    for game_name, cert_name in CASES:
        print(json.dumps(probe(game_name, cert_name), ensure_ascii=False))
