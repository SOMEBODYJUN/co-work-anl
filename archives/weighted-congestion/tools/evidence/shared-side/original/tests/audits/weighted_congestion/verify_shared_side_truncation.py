#!/usr/bin/env python3
"""Fraction audit for equal-hub shared-side truncated Rosenthal candidate.

All finite games are reconstructed as actual resource-subset strategies. No
quotients of zero costs are used. This is an implementation audit, not a proof.
"""
from fractions import Fraction as Q
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import random
import sys

SEED = 2026101503


def cost(poly, x):
    return sum((a*x**k for k, a in enumerate(poly)), Q(0))


def positive(x):
    return max(Q(0), x)


def admissible(d, a):
    # Equivalent to alpha >= A_d, using only rational arithmetic.
    return d*(Q(d)*(a-1)/(a*(d-1)))**(d-1) >= 1


def H(poly, w, u, a, m):
    return sum((positive(cost(poly, w+r*u)-a*cost(poly, r*u))
                for r in range(1, m+1)), Q(0))


def R(poly, u, m):
    return sum((cost(poly, r*u) for r in range(1, m+1)), Q(0))


def scalar_audit():
    checked = 0
    for d, a in [(2,Q(3,2)), (3,Q(2)), (4,Q(2)), (8,Q(3)),
                 (16,Q(5)), (32,Q(8))]:
        assert admissible(d, a)
        for u,w,m in product([Q(1,3),Q(1),Q(5)],
                             [Q(1,100),Q(1,3),Q(1),Q(7)], range(9)):
            for poly in ([Q(1)]+[Q(0)]*d, [Q(0)]*d+[Q(1)],
                         [Q(1,k+1) for k in range(d+1)]):
                lhs=H(poly,w,u,a,m)
                strong=a*(w/u)*(cost(poly,w+m*u)-cost(poly,w))
                rhs=(w/u)*(a*cost(poly,w+m*u)-cost(poly,w))
                assert 0 <= lhs <= strong <= rhs, (d,a,u,w,m,poly)
                checked += 1
    return checked


def build_game(d,a,nh,weights,source,sides,mainconst,strict):
    """Choose main monomial amplitudes from exact UF constraints."""
    u=Q(5)
    nl=len(weights)
    W=[sum((weights[l] for l in range(nl) if source[l]==v),Q(0))
       for v in range(nh)]
    F=[]
    for v in range(nh):
        needed=[]
        for l in range(nl):
            if source[l] != v:
                continue
            P=sum((a*cost(g,weights[l]+len(hs)*u)-cost(g,weights[l])
                   for ll,hs,g in sides if ll==l),Q(0))
            denom=(u+weights[l])**d-a*W[v]**d
            assert denom>0
            needed.append((P+(a-1)*mainconst[v])/denom)
        amp=max(needed,default=Q(0))+(Q(1) if strict else Q(0))
        F.append([mainconst[v]]+[Q(0)]*(d-1)+[amp])

    # Actual resource identities and strategies.
    resource={}
    strategies=[[set(),set()] for _ in range(nh+nl)]
    playerweights=[u]*nh+weights
    for v,f in enumerate(F):
        for b in range(2):
            key=('A',v,b); resource[key]=f
            strategies[v][b].add(key)
            for l in range(nl):
                if source[l]==v:
                    strategies[nh+l][b].add(key)
    for j,(l,hs,g) in enumerate(sides):
        for b in range(2):
            key=('B',j,b); resource[key]=g
            for v in hs:
                strategies[v][b].add(key)
            strategies[nh+l][1-b].add(key)

    def actual(s):
        loads={e:Q(0) for e in resource}
        for i,b in enumerate(s):
            for e in strategies[i][b]:
                loads[e]+=playerweights[i]
        return [sum((cost(resource[e],loads[e]) for e in strategies[i][b]),Q(0))
                for i,b in enumerate(s)]

    def energy(h,q=None):
        ans=Q(0)
        for l,hs,g in sides:
            n=[sum(h[v]==b for v in hs) for b in range(2)]
            lightbit=h[source[l]] if q is None else q[l]
            ans+=a*(R(g,u,n[0])+R(g,u,n[1]))+H(g,weights[l],u,a,n[lightbit])
        return ans

    # Check UF from its original formulas.
    equalities=0
    for l in range(nl):
        v=source[l];w=weights[l]
        lhs=cost(F[v],u+w)+sum((cost(g,w) for ll,hs,g in sides if ll==l),Q(0))
        rhs=a*(cost(F[v],W[v])+sum((cost(g,w+len(hs)*u)
                                  for ll,hs,g in sides if ll==l),Q(0)))
        assert lhs>=rhs
        if strict: assert lhs>rhs
        equalities += lhs==rhs
    budgets=[]
    for v in range(nh):
        M=a*cost(F[v],u+W[v])-cost(F[v],u)
        out=sum((H(g,weights[l],u,a,len(hs))
                 for l,hs,g in sides if source[l]==v),Q(0))
        assert out<=M
        budgets.append((out,M))

    localmins=[]
    hubstates=0
    direct_checks=0
    for h in product(range(2),repeat=nh):
        hubstates+=1
        s=tuple(h)+tuple(1-h[source[l]] for l in range(nl))
        c=actual(s)
        e=energy(h)
        ismin=True
        for v in range(nh):
            hh=list(h);hh[v]=1-hh[v];hh=tuple(hh)
            ss=list(s);ss[v]=1-ss[v]
            cc=actual(ss)
            M=a*cost(F[v],u+W[v])-cost(F[v],u)
            out=budgets[v][0]
            assert c[v]-a*cc[v] <= -M+e-energy(hh)+out
            # Independently compare frozen-light and reset-light energies.
            q=[h[source[l]] for l in range(nl)]
            frozen=energy(hh,q)
            assert energy(hh)-frozen<=out
            # Fixed external light exact alpha-cost/energy inequality.
            actualside=(c[v]-cost(F[v],u)) \
                       -a*(cc[v]-cost(F[v],u+W[v]))
            assert actualside<=e-frozen
            direct_checks+=3
            if e>energy(hh):
                ismin=False
        if ismin:
            localmins.append(h)
            for i in range(nh+nl):
                ss=list(s);ss[i]=1-ss[i]
                cc=actual(ss)
                assert c[i]<=a*cc[i], (d,a,h,i,c[i],cc[i])
                if i>=nh: assert a*c[i]<=cc[i]
    assert localmins
    allstates=0
    pne=0
    for s in product(range(2),repeat=nh+nl):
        allstates+=1;c=actual(s);ok=True
        for i in range(nh+nl):
            ss=list(s);ss[i]=1-ss[i]
            if c[i]>a*actual(ss)[i]:ok=False
        pne+=ok
    return {'d':d,'alpha':str(a),'u':str(u),'hub_count':nh,
            'light_weights':list(map(str,weights)),'sources':source,
            'main_polynomials':[[str(x) for x in f] for f in F],
            'sides':[{'light':l,'hubs':list(hs),'polynomial':list(map(str,g))}
                     for l,hs,g in sides],
            'strict_UF':strict,'UF_equalities':equalities,
            'hub_states':hubstates,'all_states':allstates,
            'PNE_count':pne,'local_minima':[list(h) for h in localmins],
            'direct_inequality_checks':direct_checks}


def run():
    rng=random.Random(SEED)
    cases=[]
    # Empty light set, zero-cost sides absent, arbitrary zero/constant main.
    cases.append(build_game(2,Q(3,2),3,[],[],[],[Q(0),Q(1),Q(0)],False))
    # Final audit additions: exact A_2=4/3 endpoint and all-zero game.
    cases.append(build_game(2,Q(4,3),2,[Q(1,2)],[0],
                            [(0,(0,1),[Q(0),Q(0),Q(0)])],
                            [Q(0),Q(0)],False))
    cases.append(build_game(2,Q(4,3),3,[Q(1,3),Q(2,3),Q(1,2)],[0,0,1],
                            [(0,(0,1,2),[Q(0),Q(1,5),Q(1)]),
                             (1,(0,1),[Q(1),Q(0),Q(1,7)]),
                             (2,(),[Q(1)])],[Q(0),Q(0),Q(0)],False))
    # Every hub subset, including empty and source-containing; repeated side.
    for d,a in [(2,Q(3,2)),(3,Q(2)),(4,Q(2)),(8,Q(3)),(16,Q(5))]:
        sides=[]
        for mask in range(8):
            hs=tuple(v for v in range(3) if mask&(1<<v))
            g=[Q(1,7)]+[Q(0)]*(d-1)+[Q(mask,13)]
            sides.append((mask%2,hs,g))
        sides.append(sides[-1])
        sides.append((0,(0,1,2),[Q(0)]*(d+1)))
        cases.append(build_game(d,a,3,[Q(1,3),Q(2,3)],[0,1],
                                sides,[Q(0),Q(1,5),Q(0)],False))
    # Reproducible mixed-polynomial, multi-source/light topologies.
    for trial in range(18):
        d,a=[(2,Q(3,2)),(3,Q(2)),(4,Q(2))][trial%3]
        nl=rng.randint(1,4)
        weights=[Q(rng.randint(1,3),4) for _ in range(nl)]
        source=[rng.randrange(3) for _ in range(nl)]
        sides=[]
        for j in range(rng.randint(0,9)):
            l=rng.randrange(nl)
            hs=tuple(v for v in range(3) if rng.randrange(2))
            g=[Q(rng.randint(0,2),rng.randint(1,4)) for _ in range(d+1)]
            sides.append((l,hs,g))
        cases.append(build_game(d,a,3,weights,source,sides,
                                [Q(rng.randint(0,1),5) for _ in range(3)],
                                trial%2==0))
    return {'kind':'finite exact implementation audit; not general proof',
            'seed':SEED,'python_version':platform.python_version(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scalar_checks':scalar_audit(),'case_count':len(cases),
            'all_state_count':sum(c['all_states'] for c in cases),
            'hub_state_count':sum(c['hub_states'] for c in cases),
            'local_min_count':sum(len(c['local_minima']) for c in cases),
            'cases':cases}


if __name__=='__main__':
    result=run()
    data=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if len(sys.argv)==3 and sys.argv[1]=='--output':
        with open(sys.argv[2],'x',encoding='utf-8') as f:f.write(data)
        print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=False))
    else:
        print(data,end='')
