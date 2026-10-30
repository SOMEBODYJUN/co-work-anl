#!/usr/bin/env python3
"""Exact resource audit for the post-review AS+B abstraction and boundaries."""
from fractions import Fraction as Q
from itertools import product
import hashlib, platform, sys
from pathlib import Path
import json

def run(name,degree,alpha,F,G,include_side=True,side_hubs=(0,)):
    u=w=Q(1)
    def p(c,x):return sum((a*x**k for k,a in enumerate(c)),Q(0))
    # One hub and its unique light; every resource is recomputed after moves.
    fees={('A',0):F,('A',1):F}
    if include_side:fees.update({('B',0):G,('B',1):G})
    actions=[[],[]]
    for b in [0,1]:
        actions[0].append({('A',b)}|({('B',b)} if include_side and 0 in side_hubs else set()))
        actions[1].append({('A',b)}|({('B',1-b)} if include_side else set()))
    def cost(h,l):
        s=(h,l);load={e:Q(0) for e in fees}
        for i in range(2):
            for e in actions[i][s[i]]:load[e]+=1
        return tuple(sum((p(fees[e],load[e]) for e in actions[i][s[i]]),Q(0)) for i in range(2))
    m=len(side_hubs) if include_side else 0
    old=p(F,w)+(p(G,w+m*u) if include_side else 0)
    new=p(F,u+w)+(p(G,w) if include_side else 0)
    AS=old<=alpha*new
    UF=new>=alpha*old
    H=sum((max(p(G,w+r*u)-alpha*p(G,r*u),Q(0)) for r in range(1,m+1)),Q(0)) if include_side else Q(0)
    M=alpha*p(F,u+w)-p(F,u)
    assert AS and H<=M
    # All anti profiles are exactly the two hub-localmin profiles here:
    # the contracted potential is invariant under global exchange of bits.
    anti_checks=0
    exact_all_states=True
    for h,l in product([0,1],repeat=2):
        cc=cost(h,l)
        for i in range(2):
            hh,ll=(1-h,l) if i==0 else (h,1-l)
            other=cost(hh,ll)[i]
            exact_all_states &= cc[i]<=other
            if l==1-h:
                assert cc[i]<=alpha*other
                anti_checks+=1
    return {'name':name,'degree':degree,'alpha':str(alpha),'AS':AS,'UF':UF,'H':str(H),'M':str(M),'anti_true_deviation_checks':anti_checks,'all_profiles_exact_PNE':bool(exact_all_states)}

results=[]
results.append(run('degree-zero positive constant costs; non-UF',0,Q(2),(Q(1),),(Q(1),)))
results.append(run('quadratic alpha below A2; non-UF',2,Q(11,10),(Q(0),Q(0),Q(1)),(Q(0),Q(0),Q(1))))
assert Q(11,10)<Q(4,3)
assert not results[0]['UF'] and not results[1]['UF']
# Boundary alpha=1, nonzero quadratic costs.
results.append(run('alpha-one boundary nonzero quadratic',2,Q(1),(Q(0),Q(0),Q(1)),(Q(0),Q(0),Q(1))))
# Degree zero, alpha one, no sides; constant player costs.
results.append(run('degree-zero alpha-one no-side boundary',0,Q(1),(Q(1),),(Q(0),),False,()))
# All-zero costs, empty participating hub subset.
results.append(run('all-zero empty-H boundary',0,Q(1),(Q(0),),(Q(0),),True,()))
print(json.dumps({'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python_version':platform.python_version(),'command':' '.join(sys.argv),'seed':None,'status':'passed','arithmetic':'fractions.Fraction exact','results':results,'scope':'explicit finite examples and boundary implementation checks; abstract proof reviewed separately'},indent=2))
