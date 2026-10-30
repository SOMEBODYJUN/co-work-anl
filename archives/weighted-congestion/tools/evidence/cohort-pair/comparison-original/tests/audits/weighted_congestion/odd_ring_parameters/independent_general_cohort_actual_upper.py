#!/usr/bin/env python3
"""Independent literal audit of the single-conflict cohort upper-bound proof.

Exact Fraction arithmetic; deterministic finite evidence, not a general proof.
No imports from the author's audit. Defaults to JSON on stdout.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import random

SEED = 95017
rng = random.Random(SEED)
stats = dict(games=0, literal_states=0, literal_deviations=0,
             stable_intervals=0, mixed_comparisons=0, centers=0,
             certified_upper_games=0, endpoint_boundaries=0,
             reverse_scalar_checks=0)


def value(p, x):
    return sum((a * x**j for j, a in enumerate(p)), Q(0))


def alpha_bound(d):
    # Expand numerator/denominator of f_d at R=1+y. Positive coefficients
    # give a rigorous rational upper bound for every R>=1.
    ratios = []
    for j in range(d + 2):
        t = comb(d, j)*2**(d-j) if j <= d else 0
        num = int(j == 0) + t
        if 1 <= j <= d+1:
            num += comb(d, j-1)*2**(d-j+1)
        den = t + comb(d+1, j)
        ratios.append(Q(num, den))
    return max(Q(2), *ratios)


class Game:
    def __init__(self, n, u, v, F, G):
        self.n, self.u, self.v, self.F, self.G = n, u, v, F, G
        self.m = len(n)
        self.w = list(u)
        self.actions = []
        self.fees = {}
        self.lights = []
        for i in range(self.m):
            for b in (0, 1):
                self.fees[('A', i, b)] = F[i]
                for j in range(n[i]):
                    self.fees[('B', i, j, b)] = G[i]
        for i in range(self.m):
            prev = (i-1) % self.m
            self.actions.append(tuple(
                frozenset([('A', i, b)] + [('B', prev, j, b)
                                          for j in range(n[prev])])
                for b in (0, 1)))
        for i in range(self.m):
            row = []
            for j in range(n[i]):
                row.append(len(self.w))
                self.w.append(v[i])
                self.actions.append(tuple(frozenset((('A', i, b),
                                                     ('B', i, j, 1-b)))
                                          for b in (0, 1)))
            self.lights.append(row)

    def state(self, z, k):
        assert sum(z) % 2 == 0
        h = [0]
        for i in range(self.m-1):
            h.append(h[-1] ^ z[i])
        assert h[-1] ^ h[0] == z[-1]
        s = h[:]
        for i in range(self.m):
            s.extend([h[i]]*k[i] + [1-h[i]]*(self.n[i]-k[i]))
        return tuple(s)

    def costs(self, s):
        loads = {e: Q(0) for e in self.fees}
        for i, b in enumerate(s):
            for e in self.actions[i][b]:
                loads[e] += self.w[i]
        return tuple(sum((value(self.fees[e], loads[e])
                          for e in self.actions[i][b]), Q(0))
                     for i, b in enumerate(s))

    def pair(self, s, i):
        t = list(s)
        t[i] ^= 1
        return self.costs(s)[i], self.costs(t)[i]

    def light_stable(self, i, z, k, a):
        n,u,v,F,G = self.n[i],self.u[i],self.v[i],self.F[i],self.G[i]
        q = value(G,v)
        V = value(G,v+self.u[(i+1)%self.m])
        A = lambda j: value(F,u+j*v)+(V if z else q)
        B = lambda j: value(F,(n-j+1)*v)+(q if z else V)
        return (k == 0 or A(k) <= a*B(k)) and (
            k == n or B(k+1) <= a*A(k+1))


def audit(game, d, full=False):
    g=game
    stats['games'] += 1
    upper=alpha_bound(d)
    # Cover both sides of alpha=2, a noninteger alpha and a
    # separately certified f_d upper endpoint.
    for alpha in sorted({Q(11,10),Q(3,2),Q(2),Q(5,2),upper}):
        I = [[ [k for k in range(g.n[i]+1)
                if g.light_stable(i,z,k,alpha)] for z in (0,1)]
             for i in range(g.m)]
        c=[]
        for i,(I0,I1) in enumerate(I):
            for ints in (I0,I1):
                assert ints and ints == list(range(ints[0],ints[-1]+1))
                stats['stable_intervals'] += 1
            c.append(I1[0])
            assert c[i] <= min(I0[0],g.n[i]//2)
            if 2*I0[0] > g.n[i]:
                assert c[i] <= g.n[i]-I0[0]
            lo,hi=I0[0],I0[-1]
            n,u,v,F,G=g.n[i],g.u[i],g.v[i],g.F[i],g.G[i]
            q=value(G,v);V=value(G,v+g.u[(i+1)%g.m])
            if hi<n:
                assert value(F,u+(hi+1)*v)+q > alpha*(value(F,(n-hi)*v)+V)
                stats['endpoint_boundaries']+=1
            if lo>0:
                assert value(F,(n-lo+1)*v)+V > alpha*(value(F,u+lo*v)+q)
                stats['endpoint_boundaries']+=1
            if alpha>=upper:
                for shift in (Q(0),v,2*v):
                    for x,y in ((u,v),(v,u),(u,n*v)):
                        P=lambda t:value(F,t+shift)
                        assert x*(P(x+y)-alpha*P(x)) <= y*(alpha*P(x+y)-P(y))
                        stats['reverse_scalar_checks']+=1
        candidates=[]
        labels=[]
        for i in range(g.m):
            z=[1]*g.m;z[i]=0
            lo,hi=I[i][0][0],I[i][0][-1]
            opts=[]
            if g.n[i]%2 == 0 and g.n[i]//2 in I[i][0]:
                k=c[:];k[i]=g.n[i]//2
                s=g.state(z,k)
                assert all(A <= alpha*B for j in range(len(s))
                           for A,B in [g.pair(s,j)])
                stats['centers']+=1
            flex=(g.n[i]%2 == 1 and g.n[i]//2 in I[i][0]
                  and g.n[i]//2+1 in I[i][0])
            if 2*hi < g.n[i] or flex:
                opts.append(('L',g.n[i]//2 if flex else hi))
            if 2*lo > g.n[i] or flex:
                opts.append(('R',g.n[i]//2+1 if flex else lo))
            labels.append(opts)
            bylabel={}
            for label,k0 in opts:
                k=c[:];k[i]=k0
                s=g.state(z,k)
                bad=[]
                for j in range(len(s)):
                    A,B=g.pair(s,j)
                    if A>alpha*B:bad.append(j)
                expected=(i+1)%g.m if label=='L' else i
                assert set(bad) <= {expected}
                bylabel[label]=(s,k0,expected,bad)
                candidates.append(not bad)
            labels[i]=bylabel
        for i in range(g.m):
            nxt=(i+1)%g.m
            if 'L' in labels[i] and 'R' in labels[nxt]:
                s=labels[i]['L'][0];t=labels[nxt]['R'][0]
                A,B=g.pair(s,nxt);C,D=g.pair(t,nxt)
                assert C<=B and A<=D
                assert not(A>alpha*B and C>alpha*D)
                stats['mixed_comparisons']+=1
        if alpha>=upper:
            assert any(candidates) or any(
                g.n[i]%2==0 and g.n[i]//2 in I[i][0] for i in range(g.m))
            stats['certified_upper_games']+=1
    # Recompute every deviation of every orbit representative directly from
    # resources on selected fixtures, rather than importing count costs.
    if full:
        for z in product((0,1),repeat=g.m):
            if sum(z)%2:continue
            for k in product(*(range(n+1) for n in g.n)):
                s=g.state(z,k);cc=g.costs(s)
                for i in range(g.m):
                    prev=(i-1)%g.m
                    r=z[prev]*k[prev]+(1-z[prev])*(g.n[prev]-k[prev])
                    W=value(g.G[prev],g.u[i])
                    V=value(g.G[prev],g.u[i]+g.v[prev])
                    assert cc[i] == value(g.F[i],g.u[i]+k[i]*g.v[i])+g.n[prev]*W+r*(V-W)
                for i,row in enumerate(g.lights):
                    for j in row:
                        aligned=s[j]==s[i]
                        main=g.u[i]+k[i]*g.v[i] if aligned else (g.n[i]-k[i])*g.v[i]
                        shared=(int(aligned)==z[i])
                        side=g.v[i]+(g.u[(i+1)%g.m] if shared else 0)
                        assert cc[j] == value(g.F[i],main)+value(g.G[i],side)
                for j in range(len(s)):
                    A,B=g.pair(s,j)
                    assert A>=0 and B>=0
                    stats['literal_deviations']+=1
                stats['literal_states']+=1


def main():
    inputs=[]
    for t in range(36):
        m=5 if t%12==0 else 3
        n=[rng.choice((1,1,2,3)) for _ in range(m)]
        d=[2,3,4,7,8,16][t%6]
        weights=[Q(1,8),Q(1,2),Q(1),Q(3),Q(8)]
        u=[rng.choice(weights) for _ in range(m)]
        v=[rng.choice(weights) for _ in range(m)]
        def poly():
            if rng.randrange(6)==0:return [Q(0)]*(d+1)
            p=[Q(0)]*(d+1)
            for j in {0,rng.randrange(d+1),d}:
                p[j]=Q(rng.randrange(4),rng.choice((1,2,5)))
            return p
        F=[poly() for _ in range(m)];G=[poly() for _ in range(m)]
        inputs.append(dict(n=n,u=list(map(str,u)),v=list(map(str,v)),
                           F=[list(map(str,p)) for p in F],
                           G=[list(map(str,p)) for p in G],d=d))
        audit(Game(n,u,v,F,G),d,full=t<8)
    # Degenerate all-zero resources force flexible singleton intervals.
    audit(Game([1]*3,[Q(1)]*3,[Q(1)]*3,[[Q(0)]]*3,[[Q(0)]]*3),2,True)
    # Verify an explicit threshold witness without numerical optimization.
    f7=Q(3*4**7+1,4**7+3**8)
    assert f7>2 and (f7.numerator==3781 and f7.denominator==1765)
    print(json.dumps(dict(status='PASS', arithmetic='fractions.Fraction',
        seed=SEED, python=platform.python_version(), stats=stats,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest(),
        command='python3 '+str(Path(__file__).resolve()),
        scope='Finite literal resources and single-conflict proof interfaces; no general or full-class proof.'),indent=2))


if __name__=='__main__':main()
