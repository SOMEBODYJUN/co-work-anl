"""Compact count-Markov SPE cones for counterexample discovery only.

The policy itself may be Markov; the general theorem is not restricted.
At every count state all action children are compared at their true policy
terminal states, so its lift to every ordered history is a full pure SPE.
Floating LP output requires an independent exact audit before any claim.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import json
from math import lcm
from pathlib import Path
import random
import numpy as np
from scipy.optimize import linprog


def structures(p,m):
    incidence=((np.arange(1,1<<p)[:,None]>>np.arange(p))&1).astype(int)
    paths=tuple(combinations_with_replacement(range(p),m))
    counts=np.array([[z.count(a) for a in range(p)] for z in paths],dtype=int)
    loads=counts@incidence.T
    D=lcm(*range(1,m+1))
    inv=np.array([0]+[D//i for i in range(1,m+1)])
    rows=inv[loads[:,:,None]]*incidence[None,:,:]
    rows=np.moveaxis(rows,1,2) # terminal, query, customer type
    cover=(loads>0).astype(int)
    index={tuple(z):i for i,z in enumerate(counts)}
    supports=tuple(combinations(range(p),m))
    target_cover=np.array([(incidence[:,t].sum(axis=1)>0).astype(int) for t in supports])
    return incidence,counts,rows,D,cover,index,supports,target_cover


def policy(weights,p,m,st,rng):
    incidence,counts,rows,D,cover,index,supports,target_cover=st
    payoffs=rows@weights
    welfare=cover@weights
    actions={};terminal={}
    @lru_cache(None)
    def solve(c):
        if sum(c)==m:
            terminal[c]=index[c]
        else:
            children=[]
            for a in range(p):
                q=list(c);q[a]+=1
                children.append(solve(tuple(q)))
            best=max(payoffs[z,a] for a,z in enumerate(children))
            opts=[a for a,z in enumerate(children) if payoffs[z,a]==best]
            # Favor low welfare among the current mover's indifferent choices.
            low=min(welfare[children[a]] for a in opts)
            opts=[a for a in opts if welfare[children[a]]==low]
            a=rng.choice(opts);actions[c]=a;terminal[c]=children[a]
        return terminal[c]
    actual=solve((0,)*p)
    return actions,terminal,actual


def cone(st,actions,terminal,actual,target,m):
    incidence,counts,rows,D,cover,index,supports,target_cover=st
    p=incidence.shape[1];nm=len(incidence)
    constraints=[]
    for c,a in actions.items():
        live=rows[terminal[c],a]
        for b in range(p):
            if b!=a:
                child=list(c);child[b]+=1
                constraints.append(np.r_[(rows[terminal[tuple(child)],b]-live)/D,0])
    # All size-m supports suffice: every smaller support extends to one and
    # coverage is monotone. Strict uniqueness among size-m supports implies
    # no smaller support can be optimal (when p>m).
    o=target_cover[target]
    for j,other in enumerate(target_cover):
        if j!=target:
            constraints.append(np.r_[other-o,1])
    c=incidence@counts[actual]
    d=incidence[:,supports[target]].sum(axis=1)
    addition=d/(1+c)
    constraints.append(np.r_[cover[actual]-addition,1])
    constraints=np.array(constraints)
    result=linprog(np.r_[np.zeros(nm),-1],A_ub=constraints,b_ub=np.zeros(len(constraints)),
                   A_eq=[np.r_[cover[actual],0]],b_eq=[1],
                   bounds=[(0,None)]*nm+[(None,None)],method='highs')
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--players',type=int,default=5)
    ap.add_argument('--topics',type=int,default=7)
    ap.add_argument('--games',type=int,default=100)
    ap.add_argument('--seed',type=int,default=10214)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();p,m=a.topics,a.players
    assert 1<=m<p
    rng=random.Random(a.seed);st=structures(p,m);best=-float('inf');checked=0;candidate=None
    for g in range(a.games):
        # Vary density, preserving distinct unit customers by integer mass.
        density=(0.08,0.25,0.6,1.0)[g%4]
        weights=np.array([rng.randrange(1,16) if rng.random()<density else 0 for _ in range(1,(1<<p))])
        if not weights.any():weights[rng.randrange(len(weights))]=1
        actions,terminal,actual=policy(weights,p,m,st,rng)
        target_values=st[-1]@weights;opt=max(target_values)
        for target in np.flatnonzero(target_values==opt):
            checked+=1;r=cone(st,actions,terminal,actual,int(target),m)
            if r.success:
                best=max(best,float(r.x[-1]))
                if r.x[-1]>1e-7:
                    candidate=dict(original_weights=weights.tolist(),weights=r.x[:-1].tolist(),
                                   actual=st[1][actual].tolist(),target=st[-2][target],gap=float(r.x[-1]),
                                   actions={','.join(map(str,c)):a for c,a in actions.items()})
                    break
        if candidate:break
    out=dict(status='floating_candidate_requires_exact_audit' if candidate else 'no_floating_separator_in_finite_sample',
             games_processed=g+1,policy_target_pairs=checked,largest_gap=best,
             parameters=vars(a)|{'output':str(a.output)},candidate=candidate)
    with a.output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k!='candidate'}))


if __name__=='__main__':main()
