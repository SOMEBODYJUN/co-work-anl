#!/usr/bin/env python3
"""Exact directed-odd-ring certificates; no external solver or float decisions.

All mathematical comparisons use fractions.Fraction. Decimal values are display
only. Compressed enumeration accounts for every hub bit and every cohort count.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def approx(x: F) -> str:
    with localcontext() as c:
        c.prec = 18
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def make(d: int, alpha: F, denominator: int, k: int, n: int, m: int = 3):
    assert m >= 3 and m % 2 == 1 and 1 <= k <= d
    t = [F(1, denominator)] * m
    x = [t[0] ** (2*m-1)] + [1/t[0]] * (m-1)
    ns, ks = [n] + [1] * (m-1), [k] + [d] * (m-1)
    u = [F(1)]
    for i in range(m):
        u.append(u[-1] * x[i] / t[i])
    assert u[-1] == u[0]
    u.pop()
    v = [u[i] * x[i] for i in range(m)]
    N = [(1+x[i])**ks[i] - alpha*(ns[i]*x[i])**ks[i] for i in range(m)]
    M = [alpha*(1+ns[i]*x[i])**ks[i] - 1 for i in range(m)]
    P = [alpha*(1+t[i])**d - t[i]**d for i in range(m)]
    Q = [(1+t[i])**d - alpha for i in range(m)]
    assert all(z > 0 for z in N+M+P+Q)
    fs = [ns[i]*N[i]*Q[i]/(M[i]*P[i]) for i in range(m)]
    G = F(1)
    for f in fs:
        G *= f
    assert G > 1, (d, alpha, approx(G))
    K = [ns[i]*N[i]*Q[i]/(P[i]*M[(i+1)%m]) for i in range(m)]
    # A deterministic rational slack; halving must terminate because G>1.
    delta = F(2)
    while delta**(m-1) >= G:
        delta = 1 + (delta-1)/2
    q = [F(1)]
    for i in range(m-1):
        q.append(q[-1]*K[i]/delta)
    p = []
    for i in range(m):
        lower = q[(i+1)%m]*M[(i+1)%m]/(ns[i]*Q[i])
        upper = q[i]*N[i]/P[i]
        assert lower < upper
        p.append((lower+upper)/2)
    light_margins = [q[i]*N[i]-p[i]*P[i] for i in range(m)]
    hub_margins = [ns[i]*p[i]*Q[i]-q[(i+1)%m]*M[(i+1)%m] for i in range(m)]
    assert all(z > 0 for z in light_margins+hub_margins)
    a = [q[i]/u[i]**ks[i] for i in range(m)]
    b = [p[i]/u[(i+1)%m]**d for i in range(m)]
    return dict(d=d, alpha=alpha, denominator=denominator, m=m, x=x, t=t,
                ns=ns, ks=ks, u=u, v=v, q=q, p=p, a=a, b=b, N=N, M=M,
                P=P, Q=Q, F=fs, G=G, delta=delta,
                light_margins=light_margins, hub_margins=hub_margins)


def enumerate_compressed(g):
    """Literal load-derived costs, independent of N/M/P/Q endpoint bounds."""
    m, d, ns = g['m'], g['d'], g['ns']
    q, p, x, t, ks = (g[key] for key in ('q','p','x','t','ks'))
    # [i][hub-present][number of cohort users]
    main = [[[q[i]*(present+c*x[i])**ks[i] for c in range(ns[i]+1)]
             for present in (0,1)] for i in range(m)]
    side = [[p[i]*t[i]**d, p[i]*(1+t[i])**d] for i in range(m)]
    seen = bad = by_light = by_hub = 0
    for hubs in product((0,1), repeat=m):
        for zeros in product(*(range(n+1) for n in ns)):
            seen += 1
            counts = [(zeros[i],ns[i]-zeros[i]) for i in range(m)]
            witness = False
            # Test each nonempty cohort action type, using actual post-move loads.
            for i in range(m):
                for bit in (0,1):
                    if not counts[i][bit]:
                        continue
                    current = main[i][int(bit==hubs[i])][counts[i][bit]]
                    current += side[i][int(1-bit==hubs[(i+1)%m])]
                    dev = main[i][int(1-bit==hubs[i])][counts[i][1-bit]+1]
                    dev += side[i][int(bit==hubs[(i+1)%m])]
                    if current > g['alpha']*dev:
                        witness = True
                        by_light += 1
                        break
                if witness:
                    break
            if witness:
                continue
            for i in range(m):
                prev, bit = (i-1)%m, hubs[i]
                current = main[i][1][counts[i][bit]]
                current += counts[prev][1-bit]*side[prev][1] + counts[prev][bit]*p[prev]
                dev = main[i][1][counts[i][1-bit]]
                dev += counts[prev][bit]*side[prev][1] + counts[prev][1-bit]*p[prev]
                if current > g['alpha']*dev:
                    witness = True
                    by_hub += 1
                    break
            if not witness:
                bad += 1
                raise AssertionError(('uncovered state',hubs,zeros))
    expected = 2**m
    for n in ns:
        expected *= n+1
    assert seen == expected and not bad
    return dict(compressed_states=seen, uncovered_states=bad,
                first_witness_light=by_light, first_witness_hub=by_hub,
                represented_profiles_exponent=sum(ns)+m)


def report(g):
    r = dict(degree=g['d'], alpha=str(g['alpha']), hubs=g['m'],
             cohort_counts=g['ns'], main_degrees=g['ks'],
             t=f"1/{g['denominator']}", weights_hubs=list(map(str,g['u'])),
             weights_cohorts=list(map(str,g['v'])),
             exact_product_gt_one=(g['G'] > 1), product_display=approx(g['G']),
             rational_delta=str(g['delta']),
             all_exact_light_margins_positive=all(z>0 for z in g['light_margins']),
             all_exact_hub_margins_positive=all(z>0 for z in g['hub_margins']),
             coefficient_recipe='README.md, Coefficient consistency and exact rational realization',
             independent_literal_compressed_enumeration=None)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--enumerate', action='store_true', help='enumerate every compressed degree-10 state')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    instances = [
        make(10,F(2),6,2,1944),
        make(100,F(8),26,3,3*26**5//12),
        make(1000,F(40),176,4,3*176**5//16),
    ]
    rows = [report(g) for g in instances]
    if args.enumerate:
        rows[0]['independent_literal_compressed_enumeration'] = enumerate_compressed(instances[0])
    data = dict(claim='OC-INTERFACE-v1 / OC-AMPLIFIER-v1',
                arithmetic='Exact rational; decimal displays are not used for decisions',
                cases=rows)
    text = json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
