#!/usr/bin/env python3
"""Independent finite checks of the equal-path graphic correlation-gap candidate.

Enumerates edge subsets and computes ranks with union-find, without using the
path-completion formula. Exact Fraction witnesses and rank inequalities are
separate from floating-point LP checks. Not a proof or novelty certificate.
Prints JSON; redirect to a fresh output file, never silently overwrite evidence.
"""
from fractions import Fraction as F
from itertools import product
import json
import platform
import random
import sys
import numpy as np
import scipy
from scipy.optimize import linprog


def graph(k, length):
    if k < 1 or length < 2:
        raise ValueError('require k>=1 and length>=2')
    edges, nxt = [], 2
    for _ in range(k):
        vertices = [0] + list(range(nxt, nxt + length - 1)) + [1]
        nxt += length - 1
        edges.extend(zip(vertices, vertices[1:]))
    return nxt, edges


def ranks(n, edges):
    out = []
    for mask in range(1 << len(edges)):
        parent = list(range(n))
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        rank = 0
        for j, (u, v) in enumerate(edges):
            if mask >> j & 1:
                u, v = find(u), find(v)
                if u != v:
                    parent[u] = v
                    rank += 1
        out.append(rank)
    return out


def expected_rank(xs, rs):
    ans = F(0)
    for mask, rank in enumerate(rs):
        probability = F(1)
        for j, x in enumerate(xs):
            probability *= x if mask >> j & 1 else 1 - x
        ans += rank * probability
    return ans


def candidate(k, length):
    best = (F(1), 1, 1)
    for s in range(2, k + 1):
        for q in range(1, s + 1):
            pa = ((F(length-1) + F(1, q))/length)**length
            p0 = F(length-1, length)**length
            loss = q*pa + (s-q)*p0 - 1 + (1-pa)**q*(1-p0)**(s-q)
            ratio = 1 - loss/F(s*(length-1)+1)
            best = min(best, (ratio, s, q))
    return best


def run_case(k, length, rng):
    n, edges = graph(k, length)
    m = len(edges)
    rs = ranks(n, edges)
    ratio, s, q = candidate(k, length)
    xs = [((F(length-1)+F(1,q))/length if i < q else
           F(length-1,length) if i < s else F(0))
          for i in range(k) for _ in range(length)]
    mass = sum(xs, F(0))
    for mask, rank in enumerate(rs):
        assert sum((x for j,x in enumerate(xs) if mask >> j & 1), F(0)) <= rank
    exact_ratio = expected_rank(xs, rs)/mass
    assert exact_ratio == ratio
    assert exact_ratio*mass == expected_rank(xs, rs)
    # Full concave extension as an LP over all subsets: a genuinely different
    # denominator computation, including samples outside the independent polytope.
    incidence = np.array([[1.0]*len(rs)] +
        [[float(mask >> j & 1) for mask in range(len(rs))] for j in range(m)])
    samples = [[F(0)]*m, [F(1)]*m, [F(1,2)]*m, xs]
    samples += [[F(rng.randrange(5),4) for _ in range(m)] for _ in range(24)]
    min_margin = float('inf')
    max_residual = 0.0
    for x in samples:
        rhs = np.array([1.0] + [float(z) for z in x])
        lp = linprog(-np.array(rs,dtype=float), A_eq=incidence, b_eq=rhs,
                     bounds=(0,None), method='highs')
        assert lp.success, lp.message
        residual = float(np.max(np.abs(incidence@lp.x-rhs)))
        max_residual = max(max_residual,residual)
        assert residual < 1e-8
        denom = -lp.fun
        observed = float(expected_rank(x,rs))/denom if denom > 1e-12 else 1.0
        margin = observed-float(ratio)
        min_margin = min(min_margin,margin)
        assert margin > -1e-8, (k,length,x,observed,float(ratio))
    return {'k':k,'length':length,'subsets':len(rs),'candidate_ratio':str(ratio),
            'attaining_support_paths':s,'attaining_active_t':q,
            'exact_witness_mass':str(mass),'exact_witness_ratio':str(exact_ratio),
            'lp_samples':len(samples),'min_numeric_margin':min_margin,
            'max_lp_equality_residual':max_residual}


def main():
    rng = random.Random(20261020)
    cases = [(1,2),(2,2),(3,2),(4,2),(2,3),(3,3)]
    rows = [run_case(k,l,rng) for k,l in cases]
    for bad in [(0,2),(2,1),(-1,3)]:
        try:
            graph(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid graph accepted')
    print(json.dumps({'method':'union-find subset ranks + exact Fraction expectation + full concave-envelope LP',
        'seed':20261020,'python':platform.python_version(),'numpy':np.__version__,
        'scipy':scipy.__version__,'cases':rows,
        'scope':'finite cross-checks only; analytic proof and literature novelty remain separate'},indent=2))

if __name__ == '__main__':
    main()
