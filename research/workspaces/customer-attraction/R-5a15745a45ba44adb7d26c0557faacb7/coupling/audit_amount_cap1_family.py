"""Definition-level audit of the explicit AMOUNT-CAP1 counterfamily.

No solver imports. The default n=3 replay is implementation evidence for the
analytic all-n counterfamily, never evidence against HALF.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--n', type=int, default=3)
args = parser.parse_args()
n = args.n
assert n >= 3
m, k = n + 1, 2 * n + 1
# Labels A_j=0..n-1, D=n, T_j=n+1..2n.
likes = [frozenset((j, n)) for j in range(n) for _ in range(2)]
likes += [frozenset((j, n + 1 + j))
          for j in range(n) for _ in range(2 * (n - 1))]
sigma, completed = {}, {}

def pay(z, j):
    return sum((Q(1, sum(a in x for a in z))
                for x in likes if z[j] in x), Q())

def build(h):
    if len(h) == m:
        return h
    children = {a: build(h + (a,)) for a in range(k)}
    i = len(h)
    vals = {a: pay(z, i) for a, z in children.items()}
    fresh = all(a < n for a in h) and len(set(h)) == len(h)
    if fresh and i < n:
        a = min(set(range(n)) - set(h))
    elif fresh and i == n:
        a = n
    else:
        a = max(range(k), key=lambda a: (vals[a], -a))
    assert vals[a] == max(vals.values()), (h, a, vals)
    sigma[h] = a
    completed[h] = children[a]
    return children[a]

P = build(())
assert P == tuple(range(n)) + (n,)
comparisons = 0
for i in range(m):
    for h in product(range(k), repeat=i):
        z = completed[h]
        for a in range(k):
            w = h + (a,) if i == m - 1 else completed[h + (a,)]
            assert pay(z, i) >= pay(w, i)
            comparisons += 1

cp = [sum(a in x for a in P) for x in likes]
column = Q()
rows = []
for j in range(n):
    W = tuple(range(n)) + (n + 1 + j,)
    cw = [sum(a in x for a in W) for x in likes]
    q = sum((Q(1, cp[t] * cw[t]) for t, x in enumerate(likes)
             if P[j] in x and P[-1] in x and W[-1] not in x), Q())
    v, w = pay(P, j), pay(W, j)
    lam = v / w
    assert (v, w, q) == (2 * n - 1, n + 1, 1)
    assert lam * w == v
    column += lam * q
    rows.append({'sender': j + 1, 'cut': m, 'forced_topic': n + 1 + j,
                 'parent_payoff': str(v), 'child_payoff': str(w),
                 'claim_coefficient': str(lam), 'positive_price': str(q)})
target = pay(P, m - 1)
assert target == n and column > target
assert column / target == Q(2 * n - 1, n + 1)
welfare = len({t for t, x in enumerate(likes) if any(a in x for a in P)})
assert welfare == len(likes) == 2 * n * n
out = {'claim': 'AMOUNT-CAP1 false; no HALF counterexample', 'n': n,
       'players': m, 'topics': k, 'unit_customers': len(likes),
       'ordered_nodes': len(sigma), 'IC_including_self': comparisons,
       'actual_path': P, 'welfare': welfare, 'optimum': welfare,
       'recipient': m, 'recipient_payoff': str(target),
       'combined_positive_price': str(column),
       'column_coefficient': str(column / target), 'requests': rows,
       'actions': [{'history': h, 'action': a}
                   for h, a in sorted(sigma.items(), key=lambda z: (len(z[0]), z[0]))]}
dest = Path(__file__).with_name(f'amount_cap1_family_n{n}.json')
dest.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({key: value for key, value in out.items() if key != 'actions'}, indent=2))
