"""Does sharp customer dilution hold for every decreasing marginal g?

Finite orbit search only. A negative result is not yet a submodular-game
counterexample; a decreasing g would still need a common submodular extension.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parent


def subs(mask):
    r = mask
    while True:
        yield r
        if not r:
            return
        r = (r-1) & mask


def counts(total, p):
    if p == 1:
        yield (total,)
    else:
        for v in range(total+1):
            for r in counts(total-v, p-1):
                yield (v,)+r


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


@lru_cache(None)
def beta(q):
    p = len(q)
    others = sum(1 << (b-1) for b in range(1, p) if q[b])
    out = [F(0)]*(1 << (p-1))
    for r in subs(others):
        power = q[0]-1+sum(q[b] for b in range(1, p) if (others & ~r) >> (b-1) & 1)
        out[r] = sum((F((-1)**s.bit_count(), power+1+sum(q[b] for b in range(1, p) if s >> (b-1) & 1)) for s in subs(r)), F(0))
    return tuple(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=5)
    parser.add_argument('--topics', type=int, default=7)
    parser.add_argument('--output', default='dilution_marginal_probe.json')
    args = parser.parse_args()
    n, p = args.players, args.topics
    qs = [q for q in counts(n, p) if q[0]]
    representatives = {}
    for q in qs:
        for r in qs:
            pairs = tuple(sorted((q[b], r[b]) for b in range(1, p) if q[b] or r[b]))
            signature = q[0], r[0], pairs
            representatives.setdefault(signature, ((q[0],)+tuple(x[0] for x in pairs),
                                                    (r[0],)+tuple(x[1] for x in pairs)))
    tested = []
    witness = None
    for q, r in representatives.values():
        l = len(q)-1
        kappa = max(F(r[0]+sum(r[b+1] for b in range(l) if s >> b & 1),
                      q[0]+sum(q[b+1] for b in range(l) if s >> b & 1)) for s in range(1 << l))
        delta = tuple(x-kappa*y for x, y in zip(beta(q), beta(r)))
        if all(x <= 0 for x in delta):
            tested.append('coordinate_domination')
            continue
        rows = []
        for s in range(1 << l):
            for b in range(l):
                if not s >> b & 1:
                    row = [0]*(1 << l)
                    row[s | (1 << b)], row[s] = 1, -1
                    rows.append(row)
        res = linprog(-np.array(delta, dtype=float), A_ub=np.array(rows, dtype=float),
                      b_ub=np.zeros(len(rows)), bounds=[(1, 1)]+[(0, 1)]*((1 << l)-1), method='highs')
        assert res.success
        g = tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
        assert g[0] == 1 and all(0 <= x <= 1 for x in g)
        assert all(dot(row, g) <= 0 for row in rows)
        value = dot(delta, g)
        tested.append(str(value))
        if value > 0:
            witness = {'q': q, 'r': r, 'kappa': str(kappa), 'exact_gap': str(value),
                       'g': {str(s): str(g[s]) for s in range(1 << l) if g[s]}}
            print(json.dumps(witness), flush=True)
            break
    out = {'players': n, 'topics': p, 'pair_orbits': len(representatives), 'tested': len(tested),
           'finite_scope_only': True, 'positive_witness': witness,
           'largest_returned_exact_gap': str(max((F(x) for x in tested if x != 'coordinate_domination'), default=F(0)))}
    (BASE/args.output).write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out), flush=True)


if __name__ == '__main__':
    main()
