"""Exact quadratic fresh-game to frequency-two unit-CAG compiler and audit.

This is a representation tool, not a proof of Q-CAG-HALF. Run from repo root:
python research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/new_representation/quadratic_graph_compiler.py
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
from math import ceil, lcm
from pathlib import Path
from random import Random
import json
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'customer_attraction' / 'exact.py').exists())
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate


def compile_game(alpha, beta, m):
    alpha = tuple(map(F, alpha)); p = len(alpha)
    beta = tuple(tuple(map(F, row)) for row in beta)
    if not 1 <= m <= p or len(beta) != p or any(len(row) != p for row in beta):
        raise ValueError('require 1 <= m <= p and a square beta matrix')
    if any(beta[a][a] or beta[a][b] != beta[b][a] for a in range(p) for b in range(p)):
        raise ValueError('beta must be symmetric with zero diagonal')
    A = max(map(abs, alpha), default=F(0))
    L = max((abs(beta[a][b]) for a, b in combinations(range(p), 2)), default=F(0))
    K = 1 + ceil(6 * A + 6 * L * (m - 1) + 2 * L)
    edges = {(a, b): K - 2 * beta[a][b] for a, b in combinations(range(p), 2)}
    degree = tuple(sum((w for (a,b), w in edges.items() if v in (a,b)), F(0)) for v in range(p))
    delta = tuple(alpha[a] - degree[a] for a in range(p))
    E = max(map(abs, delta), default=F(0)); D = max(degree, default=F(0))
    C = 1 + ceil(3 * E + 2 * D)
    singletons = tuple(C + d for d in delta)
    scale = lcm(*(r.denominator for r in singletons), *(w.denominator for w in edges.values()))
    customers = tuple(CustomerType(frozenset({a}), int(scale * r)) for a, r in enumerate(singletons))
    customers += tuple(CustomerType(frozenset({a,b}), int(scale * w)) for (a,b), w in edges.items() if w)
    ins = Instance(tuple(f'T{a}' for a in range(p)), customers, m)
    return ins, {'A': A, 'L': L, 'K': F(K), 'E': E, 'D': D, 'C': F(C),
                 'B': F(C) - F((m-1)*K, 2), 'scale': scale}


class FreshSolver:
    def __init__(self, alpha, beta, m):
        self.alpha=tuple(map(F,alpha)); self.beta=tuple(tuple(map(F,row)) for row in beta)
        self.m=m;self.p=len(alpha)
    def u(self,S,a):return self.alpha[a]+sum((self.beta[a][b] for b in S if b!=a),F(0))
    @lru_cache(None)
    def outcomes(self,S=()):
        if len(S)==self.m:return frozenset([S])
        children={a:self.outcomes(tuple(sorted(S+(a,)))) for a in range(self.p) if a not in S}
        M=max(min(self.u(q,a) for q in child) for a,child in children.items())
        return frozenset(q for a,child in children.items() for q in child if self.u(q,a)>=M)
    def paths(self):
        def walk(h,S,target):
            if len(h)==self.m:
                yield h;return
            children={a:self.outcomes(tuple(sorted(S+(a,)))) for a in range(self.p) if a not in S}
            M=max(min(self.u(q,a) for q in child) for a,child in children.items())
            for a,child in children.items():
                if target in child and self.u(target,a)>=M:
                    yield from walk(h+(a,),tuple(sorted(S+(a,))),target)
        return {h for target in self.outcomes() for h in walk((),(),target)}
    def theta(self):
        return min(max(self.u(S+(a,),a) for a in range(self.p) if a not in S)
                   for S in combinations(range(self.p),self.m-1))


def audit_case(alpha,beta,m,counters):
    ins,c=compile_game(alpha,beta,m);p=len(alpha);s=c['scale'];B=c['B']
    fresh=FreshSolver(alpha,beta,m);cg=ExactSPESolver(ins)
    actual=set(cg.ordered_outcomes());expected=fresh.paths()
    assert actual==expected
    for path in actual:
        assert len(set(path))==m
        values=ins.player_payoffs(path)
        assert values==tuple(s*(B+fresh.u(path,a)) for a in path)
        assert ins.welfare(ins.counts(path))==s*(m*B+sum((fresh.u(path,a) for a in path),F(0)))
        counters['ordered_paths']+=1
    theta=None
    for h in combinations_with_replacement(range(p),m-1):
        q=ins.counts(h)
        br=max(ins.topic_payoff(a,q[:a]+(q[a]+1,)+q[a+1:]) for a in range(p))
        theta=br if theta is None else min(theta,br)
        if len(set(h))<len(h):assert br>s*(B+fresh.theta())
        counters['last_prefix_counts']+=1
    assert theta==s*(B+fresh.theta())
    # Verify every state has only fresh current actions in every attainable SPE path.
    for t in range(m):
        for h in combinations_with_replacement(range(p),t):
            counts=ins.counts(h); floor=cg.threshold(counts)
            for a in set(h):
                child=counts[:a]+(counts[a]+1,)+counts[a+1:]
                assert all(ins.topic_payoff(a,q)<floor for q in cg.outcomes(child))
            counters['subgames']+=1
    # At least one full ordered-history certificate per case is independently verified.
    chosen=min(actual);cert=cg.certificate(on_path=chosen);v=verify_certificate(ins,cert)
    assert v.valid
    counters['certificate_histories']+=v.checked_histories
    counters['cases']+=1


def main():
    counters={k:0 for k in ['cases','ordered_paths','last_prefix_counts','subgames','certificate_histories']}
    # Exhaust all integer coefficients from {-1,0,1} for p=3, for each legal m.
    for values in product([-1,0,1],repeat=6):
        alpha=values[:3];beta=[[0]*3 for _ in range(3)]
        for (a,b),v in zip(combinations(range(3),2),values[3:]):beta[a][b]=beta[b][a]=v
        for m in range(1,4):audit_case(alpha,beta,m,counters)
    rng=Random(128112)
    for p,m,n in [(1,1,1),(2,2,20),(4,2,20),(4,3,20),(4,4,20),(5,3,10),(5,5,10)]:
        for _ in range(n):
            alpha=[F(rng.randrange(-5,6),rng.randrange(1,4)) for _ in range(p)]
            beta=[[F(0)]*p for _ in range(p)]
            for a,b in combinations(range(p),2):beta[a][b]=beta[b][a]=F(rng.randrange(-5,6),rng.randrange(1,4))
            audit_case(alpha,beta,m,counters)
    result={'status':'passed','scope':'finite exact compiler regression, not a general welfare theorem',
            'seed':128112,'python':sys.version.split()[0],**counters}
    output=Path(__file__).with_name('quadratic_graph_audit.json')
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
