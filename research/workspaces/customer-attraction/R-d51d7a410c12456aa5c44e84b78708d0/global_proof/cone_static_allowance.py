"""Exact-coefficient policy-cone exploration of the static deviation allowance."""
import json
import math
import random
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate


def matrix(cert, k, m):
    masks = list(range(1, 1 << k))
    member = np.array([[(mask >> a) & 1 for mask in masks] for a in range(k)], dtype=int)
    scale = math.lcm(*range(1, m+1))
    rows = []

    def f(a, q):
        loads = np.array(q) @ member
        return member[a] * (scale // np.maximum(loads, 1))

    def walk(h):
        if len(h) == m:
            return tuple(h.count(a) for a in range(k))
        branches = [walk(h+(a,)) for a in range(k)]
        a = cert.actions[h]
        q = branches[a]
        for b in range(k):
            if b != a:
                rows.append(f(a, q)-f(b, branches[b]))
        return q

    q = walk(())
    cover = ((np.array(q) @ member) > 0).astype(int)
    ds = []
    for a in range(k):
        d = np.zeros(len(masks), dtype=int)
        for b, count in enumerate(q):
            if count:
                qq = list(q)
                qq[b] -= 1
                qq[a] += 1
                d += count*f(a, qq)
        ds.append(d)
    return np.array(rows), cover, ds, scale


def main():
    rng = random.Random(202610212)
    best = 0
    for m, k, runs in [(2, 5, 30), (3, 5, 60), (4, 6, 60), (5, 7, 30)]:
        for trial in range(runs):
            cs = [CustomerType(frozenset(a for a in range(k) if mask >> a & 1), rng.randrange(1, 11))
                  for mask in range(1, 1 << k) if rng.random() < .4]
            ins = Instance(tuple(map(str, range(k))), tuple(cs), m)
            solver = ExactSPESolver(ins)
            cert = solver.certificate(target_counts=min(solver.outcomes(), key=ins.welfare))
            G, cover, ds, scale = matrix(cert, k, m)
            for a, d in enumerate(ds):
                result = linprog(-d, A_ub=-G, b_ub=np.zeros(len(G)),
                                 A_eq=cover[None, :], b_eq=[1], bounds=(0, None), method='highs')
                if not result.success:
                    raise RuntimeError(result.message)
                ratio = -result.fun/scale
                if ratio > best+1e-8:
                    best = ratio
                    print(json.dumps({'m': m, 'k': k, 'trial': trial, 'a': a,
                                      'ratio': ratio}), flush=True)
                if ratio > (m+1)/m + 1e-7:
                    rr = [Fraction(float(x)).limit_denominator(100000) for x in result.x]
                    denom = math.lcm(*(x.denominator for x in rr))
                    integers = [int(x*denom) for x in rr]
                    exact_ins = Instance(tuple(map(str, range(k))), tuple(
                        CustomerType(frozenset(b for b in range(k) if mask >> b & 1), v)
                        for mask, v in enumerate(integers, start=1) if v), m)
                    check = verify_certificate(exact_ins, cert)
                    if not check.valid:
                        print('RATIONAL_RECONSTRUCTION_FAILED', flush=True)
                        continue
                    dd = Fraction(sum(int(x)*int(v) for x, v in zip(d, integers)), scale)
                    ww = sum(int(x)*int(v) for x, v in zip(cover, integers))
                    if dd <= Fraction(m+1, m)*ww:
                        continue
                    out = Path(__file__).with_name('static_allowance_cone_failure.json')
                    out.write_text(json.dumps({'instance': exact_ins.to_dict(), 'certificate': cert.to_dict(),
                                               'a': a, 'D': str(dd), 'W': ww,
                                               'D_over_W': str(dd/ww)}, indent=2)+'\n')
                    print('EXACT_FAILURE', out, flush=True)
                    return
    print('COMPLETE', best, flush=True)


if __name__ == '__main__':
    main()
