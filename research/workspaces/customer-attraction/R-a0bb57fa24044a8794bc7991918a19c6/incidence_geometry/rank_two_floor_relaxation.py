"""MILP discovery for the induction-only rank-two theta-floor interface.

Find w>=0 with theta_3>=1, where each root action can be met by a terminal
with root payoff <=1-epsilon and both follower payoffs >=1. No follower
optimality is asserted, so a feasible point is only an interface obstruction.
"""
import argparse
from itertools import combinations,combinations_with_replacement
import json
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--topics',type=int,default=6)
    p.add_argument('--time-limit',type=float,default=50)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    k=args.topics
    supports=[frozenset(s) for r in [1,2] for s in combinations(range(k),r)]
    branches={a:list(combinations_with_replacement([b for b in range(k) if b!=a],2))
              for a in range(k)}
    prefixes=list(combinations_with_replacement(range(k),2))
    nw=len(supports)
    cursor=nw+1
    bi={}
    for a,qs in branches.items():
        for q in qs:bi[a,q]=cursor;cursor+=1
    ti={}
    for q in prefixes:
        for a in range(k):ti[q,a]=cursor;cursor+=1
    rows=[];lbs=[];ubs=[]
    big=1000.
    def pay(h,a):return np.array([h.count(a)*0+int(a in s)/sum(x in s for x in h)
                                 if a in s else 0 for s in supports])
    def row(coeff,lo,hi):rows.append(coeff);lbs.append(lo);ubs.append(hi)
    for a,qs in branches.items():
        c=np.zeros(cursor)
        for q in qs:c[bi[a,q]]=1
        row(c,1,1)
        for q in qs:
            z=bi[a,q];h=(a,)+q
            c=np.zeros(cursor);c[:nw]=pay(h,a);c[nw]=1;c[z]=big
            row(c,-np.inf,1+big)
            for b in set(q):
                c=np.zeros(cursor);c[:nw]=pay(h,b);c[z]=-big
                row(c,1-big,np.inf)
    for q in prefixes:
        c=np.zeros(cursor)
        for a in range(k):c[ti[q,a]]=1
        row(c,1,1)
        for a in range(k):
            c=np.zeros(cursor);c[:nw]=pay(q+(a,),a);c[ti[q,a]]=-big
            row(c,1-big,np.inf)
    objective=np.zeros(cursor);objective[nw]=-1
    lower=np.zeros(cursor);upper=np.ones(cursor);upper[:nw]=20
    integrality=np.ones(cursor);integrality[:nw+1]=0
    result=milp(objective,integrality=integrality,
                bounds=Bounds(lower,upper),
                constraints=LinearConstraint(np.array(rows),lbs,ubs),
                options={'time_limit':args.time_limit})
    report={'topics':k,'status':result.status,'message':result.message,
            'supports':[sorted(s) for s in supports],
            'constraint_rows':len(rows),'variables':cursor,
            'hypothesis':'theta_3>=1, every root query gets <=1-epsilon '
                         'with both arbitrary followers >=1; no follower SPE'}
    if result.x is not None:
        report.update(epsilon=float(result.x[nw]),weights=result.x[:nw].tolist(),
            branches={str(a):q for a,qs in branches.items()
                      for q in qs if result.x[bi[a,q]]>.5},
            theta_menu={str(q):a for q in prefixes for a in range(k)
                        if result.x[ti[q,a]]>.5})
    with args.output.open('x') as f:json.dump(report,f,indent=2)

if __name__=='__main__':main()
