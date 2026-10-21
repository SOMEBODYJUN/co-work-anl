"""Finite attacks in larger exact-potential classes, not CAG counterexamples.

Modes:
 capped: Phi=sum w_T min(load_T,k_T), monotone DR and own-congestion.
 quadratic: symmetric entrywise nonnegative C, diagonal >= each row entry;
            Phi=K sum q -.5 q^T C q; monotone on |q|<=n, DR, own-congestion.
"""
from itertools import combinations_with_replacement
from fractions import Fraction
import random
import argparse
import json
from pathlib import Path
from anonymous_attack import equilibrium,security
from payoff_state_flow import counts,PayoffGraph


def build(p,n,rng,mode):
    states=[counts(z,p) for z in combinations_with_replacement(range(p),n)]
    if mode=='capped':
        resources=[(rng.randrange(1,1<<p),rng.randrange(1,n+1),rng.randrange(1,30))
                   for _ in range(rng.randrange(1,2*p+1))]
        def potential(q):
            return sum(w*min(sum(q[a] for a in range(p) if mask&(1<<a)),k)
                       for mask,k,w in resources)
        desc={'resources':resources}
    elif mode=='quadratic':
        C=[[0]*p for _ in range(p)]
        for a in range(p):
            for b in range(a):C[a][b]=C[b][a]=rng.randrange(0,30)
        for a in range(p):C[a][a]=max(C[a])+rng.randrange(0,10)
        K=n*max(map(max,C))+10
        offsets=[rng.randrange(0,30) for _ in range(p)]
        def potential(q):
            return Fraction(sum(2*(K+offsets[a])*q[a]-sum(C[a][b]*q[a]*q[b]
                           for b in range(p)) for a in range(p)),2)
        desc={'quadratic_C':C,'K':K,'offsets':offsets}
    else:raise ValueError(mode)
    value={}
    for q in states:
        for a in range(p):
            if q[a]:
                b=list(q);b[a]-=1
                value[q,a]=potential(q)-potential(tuple(b))
    assert all(x>=0 for x in value.values())
    return value,desc


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=4)
    ap.add_argument('--players',type=int,default=3);ap.add_argument('--samples',type=int,default=3000)
    ap.add_argument('--mode',default='capped');ap.add_argument('--output')
    args=ap.parse_args();rng=random.Random(20261021);max_ratio=0
    for i in range(args.samples):
        value,desc=build(args.topics,args.players,rng,args.mode)
        actions,root=equilibrium(args.topics,args.players,value,rng)
        welfare=sum(root[a]*value[root,a] for a in range(args.topics) if root[a])
        v,query=security(args.topics,args.players,value)
        if welfare:max_ratio=max(max_ratio,args.players*v/float(welfare))
        if float(welfare)+1e-6<args.players*v:
            result={'status':'abstract_exact_potential_counterexample_NOT_CAG',
                    'iteration':i,'topics':args.topics,'players':args.players,
                    'root':root,'welfare':str(welfare),'security_float':v,'query_float':list(query),
                    'potential':desc,
                    'payoffs':[{'q':q,'a':a,'u':str(u)} for (q,a),u in value.items()],
                    'actions':[{'history':h,'action':a} for h,a in actions.items()]}
            if args.output:Path(args.output).write_text(json.dumps(result,indent=2))
            print(json.dumps(result,indent=2));return
    result={'status':'finite_no_obstruction','samples':args.samples,'mode':args.mode,
            'maximum_n_security_over_welfare':max_ratio}
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2))
    print(json.dumps(result))


if __name__=='__main__':main()
