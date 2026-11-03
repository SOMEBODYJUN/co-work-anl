#!/usr/bin/env python3
"""Diagnose one variable-r background Bellman candidate; exact finite oracle only."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json, random, sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver

def counts(k,n):
    for seq in combinations_with_replacement(range(k),n):
        c=[0]*k
        for a in seq:c[a]+=1
        yield tuple(c)

def check(ins):
    k=ins.topic_count; m=ins.players; solver=ExactSPESolver(ins);solver.outcomes()
    fcache={}
    def fp(b):
        if b in fcache:return fcache[b]
        r=m-sum(b); best=F(0);arg=None
        for q in counts(k,r):
            p=F(0)
            for x in ins.customers:
                c=sum(q[t] for t in x.topics)
                if c:p+=F(x.multiplicity*c,c+sum(b[t] for t in x.topics))
            if p>best:best=p;arg=q
        fcache[b]=(best,arg)
        return best,arg
    least=None;wit=None;checks=0
    for t in range(m):
        for b in counts(k,t):
            fr,arg=fp(b);floor=solver.threshold(b)
            for a in range(k):
                ba=list(b);ba[a]+=1;ba=tuple(ba)
                ft,arga=fp(ba)
                for c in solver.outcomes(ba):
                    u=ins.topic_payoff(a,c)
                    if u<floor:continue
                    slack=2*u+ft-fr;checks+=1
                    if least is None or slack<least:
                        least=slack;wit={'prefix':b,'action':a,'terminal':c,'r':m-t,'u':str(u),'F_r':str(fr),'F_tail':str(ft),'optimal':arg,'tail_optimal':arga,'slack':str(slack)}
    return least,wit,checks

if __name__=='__main__':
    agg={'instances':0,'checks':0,'minimum':None,'witness':None};best=None
    for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        ins=Instance.from_dict(json.loads(p.read_text()))
        if ins.topic_count>7 or ins.players>5:continue
        slack,wit,num=check(ins);agg['instances']+=1;agg['checks']+=num
        if best is None or slack<best:best=slack;agg['minimum']=str(slack);agg['witness']={'source':str(p.relative_to(ROOT)),**wit}
        print(json.dumps({'source':p.name,'slack':str(slack),'checks':num}),flush=True)
        if slack<0:
            print(json.dumps({'COUNTEREXAMPLE':{'source':str(p.relative_to(ROOT)),**wit}}),flush=True)
            break
    print(json.dumps(agg,indent=2))
