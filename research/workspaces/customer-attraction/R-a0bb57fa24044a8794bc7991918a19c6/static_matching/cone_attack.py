"""Fixed-full-policy LP attack on the static optimal-assignment conjecture.

Floating LP locates candidates only. A claimed failure must be rationalized,
expanded to unit customers, and independently checked at every ordered node.
The objective requires a unique optimal m-element support, so alternative
optimal portfolios cannot silently repair a purported matching obstruction.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import random
import sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def probe(instance, certificate, target, query_factor=1.0):
    p,m=instance.topic_count,instance.players
    masks=tuple(range(1,1<<p));nm=len(masks)
    types=tuple(tuple(a for a in range(p) if mask>>a&1) for mask in masks)
    def terminal(h):
        while len(h)<m:h=h+(certificate.actions[h],)
        return h
    def row(a,z):
        return np.array([sum(t in T for t in z)**-1 if a in T else 0.0
                         for T in types])
    actual=terminal(())
    c=np.array([float(any(a in T for a in actual)) for T in types])
    o=np.array([float(any(a in T for a in target)) for T in types])
    Aub=[]
    for h,a in certificate.actions.items():
        live=row(a,terminal(h))
        for b in range(p):
            if b!=a:Aub.append(np.r_[row(b,terminal(h+(b,)))-live,0])
    for size in range(1,m+1):
        for support in combinations(range(p),size):
            if support==target:continue
            oo=np.array([float(any(a in T for a in support)) for T in types])
            Aub.append(np.r_[oo-o,1])
    for assignment in permutations(target):
        query=sum((row(b,actual[:i]+(b,)+actual[i+1:])
                   for i,b in enumerate(assignment)),np.zeros(nm))
        Aub.append(np.r_[query_factor*c-query,1])
    result=linprog(np.r_[np.zeros(nm),-1.0],A_ub=np.array(Aub),
                   b_ub=np.zeros(len(Aub)),A_eq=[np.r_[c,0]],b_eq=[1],
                   bounds=[(0,None)]*nm+[(None,None)],method='highs')
    return result, actual


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=100)
    ap.add_argument('--topics',type=int,default=6);ap.add_argument('--players',type=int,default=4)
    ap.add_argument('--seed',type=int,default=1022);ap.add_argument('--output',type=Path)
    ap.add_argument('--query-factor',type=Fraction,default=Fraction(1))
    a=ap.parse_args()
    if a.games<1 or not 1<=a.players<=a.topics:ap.error('positive games and 1<=players<=topics required')
    rng=random.Random(a.seed);best=-float('inf');checked=0;candidate=None
    for g in range(a.games):
        active=rng.sample(range(1,1<<a.topics),min(10,(1<<a.topics)-1))
        customers=tuple(CustomerType(frozenset(j for j in range(a.topics) if mask>>j&1),rng.randrange(1,16)) for mask in active)
        ins=Instance(tuple(map(str,range(a.topics))),customers,a.players);sol=ExactSPESolver(ins)
        targets=[t for t in combinations(range(a.topics),a.players)
                 if ins.welfare(ins.counts(t))==ins.optimal_welfare()]
        for z in sol.worst_outcomes():
            cert=sol.certificate(z)
            for target in targets:
                checked+=1;r,actual=probe(ins,cert,target,float(a.query_factor))
                if r.success:
                    best=max(best,float(r.x[-1]))
                    if r.x[-1]>1e-7:
                        candidate=dict(instance=ins.to_dict(),certificate=cert.to_dict(),target=target,
                                       actual=actual,weights=r.x[:-1].tolist(),gap=float(r.x[-1]))
                        break
            if candidate:break
        if candidate:break
    out=dict(status='floating_candidate_requires_exact_audit' if candidate else 'no_floating_separator_in_finite_sample',
             games_processed=g+1,policy_target_pairs=checked,largest_gap=best,
             parameters=vars(a)|{'output':str(a.output),'query_factor':str(a.query_factor)},candidate=candidate)
    if a.output:
        with a.output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k!='candidate'}))


if __name__=='__main__':main()
