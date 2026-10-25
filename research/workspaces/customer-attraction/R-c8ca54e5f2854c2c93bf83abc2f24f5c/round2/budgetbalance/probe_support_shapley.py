"""One directed test of a precise extension, not a CAG search.

Candidate: SUMmin-full for a common-action Shapley game whose welfare is a
monotone submodular function of the support.  We first freeze the already
available finite-DR counterexample's full policy and optimize the support
welfare on four labels.  A nonpositive optimum is no general evidence.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parent
K, M = 4, 3
NF = 1 << K
NVAR = NF + M


@lru_cache(None)
def potential(q):
    out = [Q(0) for _ in range(NF)]
    n = sum(q)
    if n:
        mask = sum(1 << a for a in range(K) if q[a])
        out[mask] += Q(1, n)
        for a in range(K):
            if q[a]:
                child = list(q)
                child[a] -= 1
                for j, c in enumerate(potential(tuple(child))):
                    out[j] += Q(q[a], n) * c
    return tuple(out)


def counts(z):
    return tuple(z.count(a) for a in range(K))


def subtract(a, b):
    return tuple(x-y for x, y in zip(a, b))


def utility(z, i):
    return subtract(potential(counts(z)), potential(counts(z[:i] + z[i+1:])))


def full_query(z):
    out = [Q(0) for _ in range(NF)]
    base = potential(counts(z))
    for a in range(K):
        diff = subtract(potential(counts(z + (a,))), base)
        for j in range(NF):
            out[j] += diff[j] / K
    return tuple(out)


def main():
    old = json.loads((BASE.parent / 'fullslots' / 'dr_counterexample_exact.json').read_text())
    print('keys', sorted(old))
    policy_raw = old.get('policy', old.get('sigma'))
    if isinstance(policy_raw, list):
        sigma = {tuple(row['history']): row.get('action', row.get('chosen')) for row in policy_raw}
    elif isinstance(policy_raw, dict):
        sigma = {tuple(map(int, key.split(','))) if key else (): val for key, val in policy_raw.items()}
    else:
        raise ValueError('unknown policy representation')
    def finish(h):
        while len(h) < M:
            h += (sigma[h],)
        return h
    actual = finish(())
    rows, rhs = [], []
    def row(coeff, value=0):
        rows.append(np.asarray(coeff, dtype=float))
        rhs.append(value)
    def pad(v):
        return list(v) + [0] * M
    for mask in range(NF):
        for a in range(K):
            if not mask >> a & 1:
                r = [0] * NVAR
                r[mask], r[mask | 1 << a] = 1, -1
                row(r)
                for b in range(a+1, K):
                    if not mask >> b & 1:
                        r = [0] * NVAR
                        r[mask] += 1
                        r[mask | 1 << a] -= 1
                        r[mask | 1 << b] -= 1
                        r[mask | 1 << a | 1 << b] += 1
                        row(r)
    for i in range(M):
        for h in product(range(K), repeat=i):
            chosen = utility(finish(h), i)
            for a in range(K):
                row(pad(subtract(utility(finish(h + (a,)), i), chosen)))
        for a in range(K):
            r = pad(tuple(-x for x in full_query(finish(actual[:i] + (a,)))))
            r[NF+i] = 1
            row(r)
    obj = np.zeros(NVAR)
    obj[sum(1 << a for a in set(actual))] = 1
    obj[NF:] = -1
    bounds = [(0, 1)] * NF + [(0, 1)] * M
    bounds[0] = (0, 0)
    bounds[NF-1] = (1, 1)
    res = linprog(obj, A_ub=np.asarray(rows), b_ub=np.asarray(rhs), bounds=bounds, method='highs')
    output = dict(candidate='SUMmin-full for monotone-submodular support-Shapley games',
                  scope='one fixed policy and uniform query on four actions',
                  status=res.message, success=bool(res.success),
                  actual=list(actual))
    if res.success:
        output.update(gap=float(-res.fun), vector=[float(x) for x in res.x],
                      fractions=[str(Q(float(x)).limit_denominator(100000)) for x in res.x])
    (BASE / 'support_shapley_fixed_policy_float.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
