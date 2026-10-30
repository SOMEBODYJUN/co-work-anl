"""Independent exact audit of anchored complementary-triple clocks.
Not read from or derived from any candidate implementation.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from random import Random
import hashlib, platform, sys
from pathlib import Path
import json

rng = Random(20261015)


def ev(coeff, x):
    return sum((a * x**k for k, a in enumerate(coeff)), Q(0))


def cost(w, clocks, s, player):
    total = Q(0)
    for (i, j), coeff in clocks.items():
        ids = (0, i, j)
        pattern = (0, 1, 0)
        if player not in ids:
            continue
        used = {h: int(s[h] != bit) for h, bit in zip(ids, pattern)}
        own_resource = used[player]
        load = sum((w[h] for h in ids if used[h] == own_resource), Q(0))
        total += ev(coeff, load)
    return total


def margin(w, clocks, s, i, alpha):
    t = list(s)
    t[i] ^= 1
    return cost(w, clocks, s, i) - alpha * cost(w, clocks, t, i)


def symbolic_g_delta(w, clocks, alpha):
    g = [Q(0)] * len(w)
    delta = {}
    S = Q(0)
    for (i,j), coeff in clocks.items():
        a,b,c = w[0],w[i],w[j]
        ab,bc,ac = (ev(coeff,x) for x in (a+b,b+c,a+c))
        g[0] += ac - alpha*ab
        g[i] += ab - alpha*bc
        g[j] += bc - alpha*ac
        delta[i,j] = ev(coeff,a+b+c) - ab + alpha*(bc-ev(coeff,b))
        S += ab + bc + ac
    return g, delta, S

trials = 0
state_checks = 0
ring_edge_checks = 0
for n in range(3, 8):
    for trial in range(12):
        w = [Q(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(n)]
        alpha = Q(rng.randint(1, 12), rng.randint(1, 4))
        alpha = max(Q(1), alpha)
        degree = rng.randint(0, 5)
        clocks = {(i,j): [Q(rng.randint(0,4),rng.randint(1,5)) for _ in range(degree+1)]
                  for i,j in combinations(range(1,n),2)}
        # Include the all-zero polynomial, mixed degree, and rational-weight cases.
        if trial == 0:
            clocks = {ij: [Q(0)] for ij in clocks}
        g,delta,S = symbolic_g_delta(w,clocks,alpha)
        assert all(x >= 0 for x in delta.values())
        assert sum(g) == -(alpha-1)*S
        legal = set()
        for half in (0,1):
            s = [half]*n
            for i in range(n):
                legal.add(tuple(s))
                assert margin(w,clocks,s,i,alpha) == g[i]
                ring_edge_checks += 1
                s[i] ^= 1
        assert len(legal) == 2*n
        for s in product((0,1), repeat=n):
            opposite = [i for i in range(1,n) if s[i] != s[0]]
            first = min(opposite) if opposite else None
            same_after = [] if first is None else [j for j in range(first+1,n) if s[j] == s[0]]
            assert (s not in legal) == bool(same_after)
            if same_after:
                rhs = g[first] + sum((delta[first,j] for j in same_after), Q(0))
                assert margin(w,clocks,s,first,alpha) == rhs
            state_checks += 1
        trials += 1

# The proposed degree-q shortcut fails already at q=2.
a,b,c,alpha = Q(1,2),Q(1,10),Q(1,10),Q(10)
r = []
for k in range(3):
    num = (a+b+c)**k - (a+b)**k + alpha*((b+c)**k-b**k)
    den = (a+b)**k + (b+c)**k + (a+c)**k
    r.append(num/den)
assert r == [Q(0),Q(11,14),Q(43,76)] and r[1] > r[2]

# Mixture ratio is a denominator-weighted convex average of monomial ratios.
for _ in range(200):
    w = [Q(rng.randint(1,9),rng.randint(1,7)) for _ in range(3)]
    alpha = Q(rng.randint(1,12))
    coeff = [Q(rng.randint(0,7),rng.randint(1,7)) for _ in range(7)]
    if not any(coeff):
        coeff[0] = Q(1)
    a,b,c = w
    num = ev(coeff,a+b+c)-ev(coeff,a+b) + alpha*(ev(coeff,b+c)-ev(coeff,b))
    den = sum((ev(coeff,x) for x in (a+b,b+c,a+c)),Q(0))
    monomials = [((a+b+c)**k-(a+b)**k+alpha*((b+c)**k-b**k)) /
                 ((a+b)**k+(b+c)**k+(a+c)**k) for k in range(7)]
    assert min(monomials) <= num/den <= max(monomials)

print(json.dumps({'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python_version':platform.python_version(),'command':' '.join(sys.argv),'arithmetic':'fractions.Fraction exact','seed':20261015,'trials':trials,'state_checks':state_checks,
                  'ring_edge_checks':ring_edge_checks,'mixture_checks':200,
                  'highest_degree_counterexample':list(map(str,r)),
                  'result':'PASS; finite exact evidence, not a proof'}, ensure_ascii=False))
