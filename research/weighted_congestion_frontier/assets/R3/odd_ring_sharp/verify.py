#!/usr/bin/env python3
"""Exact scalar identities, constructive certificates and an actual small game.

No random seed, no floating-point optimization. Every tested inequality is
evaluated with Fraction. Huge families are checked through proved local tests;
only the explicitly reported small game is enumerated in full.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform


def f(d, r):
    return (r * (1 + r)**d + 1) / ((1 + r)**d + r**(d + 1))


def terms(d, alpha, x, t, n, k):
    return ((1+x)**k-alpha*(n*x)**k,
            alpha*(1+n*x)**k-1,
            alpha*(1+t)**d-t**d,
            (1+t)**d-alpha)


def certificates():
    rows = []
    for d, r, alpha in [(2,F(4),F(9,8)), (3,F(4),F(13,10)),
                        (4,F(4),F(3,2)), (10,F(4),F(5,2)),
                        (32,F(8),F(6))]:
        assert 1 < alpha < f(d, r)
        e = (1+1/r)**d
        q = (e-alpha)/(alpha*e-r**(-d))
        assert 0 < q < 1 < r*q
        b = (4*alpha*d).__ceil__()
        m = 3
        while (r*q)**(2*m-1) <= 12*b*alpha:
            m += 2
        ell = 2*m-1
        n = (r**ell/b).__floor__()
        x = r**(-ell)
        nn, mm, pp, qq = terms(d,alpha,x,1/r,n,d)
        ordinary = terms(d,alpha,r,1/r,1,d)
        assert all(t>0 for t in (nn,mm,pp,qq,*ordinary))
        assert ordinary[0]/ordinary[1] == qq/pp == q
        gain = n*nn/mm*q**ell
        assert gain > 1
        assert n >= r**ell/(2*b)
        assert nn >= F(3,4)
        assert r**ell*x == 1  # reverse-check load and multiplicity inputs
        rows.append({'d':d,'R':str(r),'alpha':str(alpha),
                     'scalar_f':str(f(d,r)),'m':m,'B':b,
                     'n0_bit_length':n.bit_length(),
                     'gain_floor':gain.__floor__(),
                     'scope':'exact scalar construction, not full-state enumeration'})
    return rows


def identities():
    count = 0
    for d, k, n, x, t, alpha in product(
            range(1,7),range(1,7),range(1,5),
            [F(1,20),F(1,2),F(1),F(2),F(5)],
            [F(1,20),F(1,2),F(1),F(2),F(5)],
            [F(11,10),F(3,2),F(2),F(4)]):
        if k>d:
            continue
        nn,mm,pp,qq=terms(d,alpha,x,t,n,k)
        y=n*x
        fk=y*((1+y)**k-alpha*y**k)/(alpha*(1+y)**k-1)
        assert x*n*nn/mm <= fk
        z=1/t
        fd=z*((1+z)**d-alpha*z**d)/(alpha*(1+z)**d-1)
        assert qq/(t*pp)==fd
        assert (fk>1)==(alpha<f(k,y))
        if y<=1:
            assert f(k,y)<=1
        else:
            assert f(k,y)<=f(d,y)
        if nn>0 and qq>0:
            assert n*nn*qq/(mm*pp)<(1+1/x)/(alpha-1)**2
        count+=1
    assert all(f(1,F(r))==1 for r in range(1,12))
    return count


def coefficients(d,alpha,u,v,n,k):
    m=len(u)
    tm=[terms(d,alpha,v[i]/u[i],v[i]/u[(i+1)%m],n[i],k[i])
        for i in range(m)]
    assert all(z>0 for row in tm for z in row)
    rs=[n[i-1]*tm[i-1][3]*tm[i][0]/(tm[i][1]*tm[i][2])
        for i in range(m)]
    gain=F(1)
    for r in rs:
        gain*=r
    assert gain>1
    delta=(gain-1)/(2*m*gain)
    bs=[F(1)]
    for i in range(1,m):
        bs.append((1-delta)*rs[i]*bs[i-1])
    aa=[]
    for i in range(m):
        low=bs[i]*tm[i][2]/tm[i][0]
        high=n[i-1]*bs[i-1]*tm[i-1][3]/tm[i][1]
        assert low<high
        aa.append((low+high)/2)
    # Reverse-check both original (unscaled) local inequalities.
    a=[aa[i]/u[i]**k[i] for i in range(m)]
    b=[bs[i]/u[(i+1)%m]**d for i in range(m)]
    for i in range(m):
        assert a[i]*u[i]**k[i]*tm[i][0] > b[i]*u[(i+1)%m]**d*tm[i][2]
        assert n[i-1]*b[i-1]*u[i]**d*tm[i-1][3] > a[i]*u[i]**k[i]*tm[i][1]
    return a,b


def literal():
    d=10; alpha=F(11,10)
    u=[F(32),F(2),F(8)]; v=[F(1),F(4),F(16)]
    n=[3,1,1]; k=[2,10,10]; m=3
    a,b=coefficients(d,alpha,u,v,n,k)
    resources={}
    for i in range(m):
        for side in (0,1):
            resources[('A',i,side)]=(a[i],k[i])
            for j in range(n[i]):
                resources[('B',i,j,side)]=(b[i],d)
    weights=list(u); strategies=[]
    for i in range(m):
        strategies.append([{('A',i,h)}|{('B',(i-1)%m,j,h) for j in range(n[i-1])}
                           for h in (0,1)])
    light_ids=[]
    for i in range(m):
        for j in range(n[i]):
            light_ids.append((i,j))
            weights.append(v[i])
            strategies.append([{('A',i,l),('B',i,j,1-l)} for l in (0,1)])
    def costs(state):
        loads={r:F(0) for r in resources}
        for p,h in enumerate(state):
            for r in strategies[p][h]:
                loads[r]+=weights[p]
        fees={r:c*loads[r]**power for r,(c,power) in resources.items()}
        return [sum((fees[r] for r in strategies[p][h]),F(0))
                for p,h in enumerate(state)]
    states=deviations=aligned_checks=hub_checks=0
    worst=None
    for state in product((0,1),repeat=len(weights)):
        old=costs(state); ratios=[]
        has_aligned=False
        for p in range(len(weights)):
            changed=list(state);changed[p]^=1
            new=costs(changed)[p]
            assert new>0
            ratios.append(old[p]/new)
            deviations+=1
            if p>=m:
                i,_=light_ids[p-m]
                if state[p]==state[i]:
                    has_aligned=True;aligned_checks+=1
                    assert old[p]>alpha*new
        if not has_aligned:
            equal=[i for i in range(m) if state[(i-1)%m]==state[i]]
            assert equal
            for i in equal:
                assert ratios[i]>alpha
                hub_checks+=1
        assert max(ratios)>alpha
        worst=max(ratios) if worst is None else min(worst,max(ratios))
        states+=1
    return {'d':d,'alpha':str(alpha),'players':len(weights),'resources':len(resources),
            'states':states,'deviations':deviations,'aligned_checks':aligned_checks,
            'equal_edge_hub_checks':hub_checks,'minimum_best_improvement':str(worst),
            'alpha_PNE_count':0,'scope':'all states/all unilateral deviations of this actual game'}


def main():
    result={'schema_version':1,'python_version':platform.python_version(),
            'arithmetic':'fractions.Fraction, no random seed or floating assertions',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'replay_command':'python3 research/weighted_congestion_frontier/assets/R3/odd_ring_sharp/verify.py',
            'local_identity_cases':identities(),'constructed_scalar_cases':certificates(),
            'literal_game':literal(),
            'limitations':'Finite arithmetic and actual small-game evidence only; general all-d claims depend on PROOF.md.'}
    target=Path(__file__).with_name('verification.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
