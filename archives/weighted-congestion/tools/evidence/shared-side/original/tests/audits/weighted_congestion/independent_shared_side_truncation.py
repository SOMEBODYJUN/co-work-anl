#!/usr/bin/env python3
"""Independent exact audit of common-hub shared-side all-anti theorem.
Uses actual resource sets and recomputed unilateral loads; no author imports.
Finite checks support implementation, not the general real-parameter proof.
"""
from fractions import Fraction as Q
from itertools import product
import random, json, hashlib, platform, sys
from pathlib import Path

SEED=20261015
rng=random.Random(SEED)
counts={k:0 for k in ['instances','all_profiles','allanti_profiles','localmin_profiles','hub_checks','light_checks','fixed_q_side_checks','reset_checks','budget_checks','scalar_checks']}

def poly(coeff,x):
    return sum((a*x**k for k,a in enumerate(coeff)),Q(0))

def alpha_for(d):
    if d==2:return Q(4,3)
    # Exact equivalent alpha >= A_d; avoid rounding its irrational value.
    for numerator in range(21,20*d+1):
        a=Q(numerator,20)
        if (a*(d-1)/(a-1))**(d-1)<=d**d:return a
    raise AssertionError('alpha search')

def threshold_ok(d,a):
    return (a*(d-1)/(a-1))**(d-1)<=d**d

def run_case(d,nh,origins,weights,side_specs,u=Q(1),zero=False):
    a=alpha_for(d)
    assert threshold_ok(d,a)
    nl=len(weights)
    W=[sum((weights[l] for l in range(nl) if origins[l]==v),Q(0)) for v in range(nh)]
    sides=[]
    for l,H,coeff in side_specs:
        assert len(set(H))==len(H)
        sides.append((l,frozenset(H),tuple(coeff)))
    # Make UF true by selecting only a main-resource amplitude, when needed.
    F=[]
    for v in range(nh):
        if zero:
            coeff=[Q(0)]*(d+1)
        elif not any(o==v for o in origins):
            coeff=[Q(rng.randrange(3)) for _ in range(d+1)]
        else:
            amp=Q(1)
            for l,o in enumerate(origins):
                if o!=v:continue
                denom=(u+weights[l])**d-a*W[v]**d
                assert denom>0,(d,u,weights,W)
                outgoing=sum((a*poly(g,weights[l]+len(H)*u)-poly(g,weights[l]) for ll,H,g in sides if ll==l),Q(0))
                amp=max(amp,outgoing/denom+1)
            coeff=[Q(0)]*d+[amp]
        F.append(tuple(coeff))
    if zero:
        assert all(not any(g) for _,_,g in sides)
    for l,v in enumerate(origins):
        lhs=poly(F[v],u+weights[l])+sum((poly(g,weights[l]) for ll,H,g in sides if ll==l),Q(0))
        rhs=a*(poly(F[v],W[v])+sum((poly(g,weights[l]+len(H)*u) for ll,H,g in sides if ll==l),Q(0)))
        assert lhs>=rhs
    # Build the actual finite congestion game from resource identities/actions.
    fees={}
    strategies=[]
    allweights=[u]*nh+list(weights)
    for v in range(nh):
        for b in [0,1]:fees[('A',v,b)]=F[v]
    for j,(_,_,g) in enumerate(sides):
        for b in [0,1]:fees[('B',j,b)]=g
    for v in range(nh):
        strategies.append(tuple(frozenset([('A',v,b)]+[('B',j,b) for j,(_,H,_) in enumerate(sides) if v in H]) for b in [0,1]))
    for l,v in enumerate(origins):
        strategies.append(tuple(frozenset([('A',v,b)]+[('B',j,1-b) for j,(ll,_,_) in enumerate(sides) if ll==l]) for b in [0,1]))
    def costs(profile):
        loads={e:Q(0) for e in fees}
        for i,b in enumerate(profile):
            for e in strategies[i][b]:loads[e]+=allweights[i]
        return tuple(sum((poly(fees[e],loads[e]) for e in strategies[i][b]),Q(0)) for i,b in enumerate(profile))
    # Every profile is checked by independent load recomputation.
    for p in product([0,1],repeat=nh+nl):
        c=costs(p)
        assert all(x>=0 for x in c)
        counts['all_profiles']+=1
    def Hfun(j,k):
        l,H,g=sides[j]
        return sum((max(poly(g,weights[l]+r*u)-a*poly(g,r*u),Q(0)) for r in range(1,k+1)),Q(0))
    def side_energy(j,h,q):
        l,H,g=sides[j]
        n=[sum(h[v]==b for v in H) for b in [0,1]]
        baseline=a*sum((poly(g,r*u) for b in [0,1] for r in range(1,n[b]+1)),Q(0))
        return baseline+Hfun(j,n[q])
    def energy(h):
        return sum((side_energy(j,h,h[origins[l]]) for j,(l,H,g) in enumerate(sides)),Q(0))
    M=[a*poly(F[v],u+W[v])-poly(F[v],u) for v in range(nh)]
    for v in range(nh):
        outgoing=sum((Hfun(j,len(H)) for j,(l,H,g) in enumerate(sides) if origins[l]==v),Q(0))
        assert outgoing<=M[v]
        counts['budget_checks']+=1
    localcount=0
    for h in product([0,1],repeat=nh):
        e=energy(h)
        full=h+tuple(1-h[v] for v in origins)
        c=costs(full)
        counts['allanti_profiles']+=1
        local=True
        for v in range(nh):
            hv=list(h);hv[v]=1-hv[v];hv=tuple(hv)
            if energy(hv)<e:local=False
            # Fixed-light side inequalities, each resource contribution directly.
            for j,(l,H,g) in enumerate(sides):
                for q in [0,1]:
                    n=[sum(h[x]==b for x in H) for b in [0,1]]
                    nn=[sum(hv[x]==b for x in H) for b in [0,1]]
                    old=poly(g,n[h[v]]*u+(weights[l] if h[v]==q else 0)) if v in H else Q(0)
                    new=poly(g,nn[hv[v]]*u+(weights[l] if hv[v]==q else 0)) if v in H else Q(0)
                    assert old-a*new<=side_energy(j,h,q)-side_energy(j,hv,q)
                    counts['fixed_q_side_checks']+=1
                if origins[l]==v:
                    oldq=h[v]
                    reset=side_energy(j,hv,hv[v])-side_energy(j,hv,oldq)
                    assert reset<=Hfun(j,len(H))
                    counts['reset_checks']+=1
        # Strong light inequality on every all-anti profile, not only minima.
        for l in range(nl):
            pp=list(full);i=nh+l;pp[i]=1-pp[i]
            assert a*c[i]<=costs(tuple(pp))[i]
            counts['light_checks']+=1
        if local:
            localcount+=1
            for i in range(nh+nl):
                pp=list(full);pp[i]=1-pp[i]
                assert c[i]<=a*costs(tuple(pp))[i]
                if i<nh:counts['hub_checks']+=1
            counts['localmin_profiles']+=1
    assert localcount>0
    counts['instances']+=1

# Scalar checks include constant/zero terms and positive-part cancellation.
for d in [2,3,4,8,16]:
    a=alpha_for(d)
    for u in [Q(1,3),Q(1),Q(5)]:
        for w in [Q(1,1000),Q(1,7),Q(1),Q(9)]:
            for m in [0,1,2,7]:
                for g in [[Q(0)]*(d+1),[Q(1)]*(d+1),[Q(0)]*d+[Q(1)]]:
                    h=sum((max(poly(g,w+r*u)-a*poly(g,r*u),Q(0)) for r in range(1,m+1)),Q(0))
                    assert h<=a*w/u*(poly(g,w+m*u)-poly(g,w))
                    assert h<=w/u*(a*poly(g,w+m*u)-poly(g,w))
                    counts['scalar_checks']+=1

# Curated cases: no lights; zero fees; empty H; self-source in H; all hubs in H;
# repeated side endpoints; constants; heavy single lights; heterogeneous lights.
for d in [2,3,4,8]:
    run_case(d,1,[],[],[])
    run_case(d,2,[0],[Q(1,4)],[(0,[],[Q(0)]*(d+1)),(0,[0,1],[Q(0)]*(d+1))],zero=True)
    run_case(d,3,[0],[Q(2)],[(0,[],[Q(1)]*(d+1)),(0,[0,1,2],[Q(0)]*d+[Q(1)]),(0,[0,1,2],[Q(1)])])
    for case in range(20):
        nh=rng.choice([1,2,3]);nl=rng.choice([1,2,3,4])
        origins=[rng.randrange(nh) for _ in range(nl)]
        weights=[rng.choice([Q(1,16),Q(1,8),Q(1,4)]) for _ in range(nl)]
        # Keep multiple-light total below u; single-light heavy cases above.
        if any(sum(weights[l] for l,o in enumerate(origins) if o==v)>Q(3,4) for v in range(nh)):continue
        side_specs=[]
        for j in range(rng.randrange(8)):
            l=rng.randrange(nl);H=[v for v in range(nh) if rng.randrange(2)]
            coeff=[Q(rng.randrange(3),rng.choice([1,2,3])) for _ in range(d+1)]
            if rng.randrange(4)==0:coeff=[Q(0)]*(d+1)
            side_specs.append((l,H,coeff))
        run_case(d,nh,origins,weights,side_specs)

result={'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python_version':platform.python_version(),'command':' '.join(sys.argv),'status':'passed','seed':SEED,'arithmetic':'fractions.Fraction exact','author_code_imported':False,'coverage':counts,'scope':'finite formula/resource implementation checks only; not a proof of real-parameter theorem','alpha_certificate':'(alpha*(d-1)/(alpha-1))**(d-1) <= d**d; d=2 uses exact endpoint 4/3'}
print(json.dumps(result,ensure_ascii=False,indent=2))
