#!/usr/bin/env python3
"""Finite legal-background diagnosis: F_r(b)-P <= r min remaining payoff."""
from fractions import Fraction as F
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, ExactSPESolver
from bellman_diagnostic import counts

def check(ins):
    k=ins.topic_count;m=ins.players;sol=ExactSPESolver(ins);sol.outcomes();least=None;wit=None;checks=0
    for i in range(m):
      for b in counts(k,i):
        r=m-i;fr=F(0);bestq=None
        for q in counts(k,r):
            p=sum((F(x.multiplicity*sum(q[t] for t in x.topics),sum((b[t]+q[t]) for t in x.topics)) for x in ins.customers if sum(q[t] for t in x.topics)),F())
            if p>fr:fr=p;bestq=q
        for c in sol.outcomes(b):
            q=tuple(v-w for v,w in zip(c,b));pay=ins.topic_payoffs(c);u=min(pay[t] for t in range(k) if q[t]);p=sum((q[t]*pay[t] for t in range(k)),F());slack=p+r*u-fr;checks+=1
            if least is None or slack<least:least=slack;wit={'prefix':b,'terminal':c,'r':r,'minimum_payoff':str(u),'profit':str(p),'F_r':str(fr),'optimal':bestq,'slack':str(slack)}
    return least,wit,checks
if __name__=='__main__':
    agg={'instances':0,'checks':0};best=None
    for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        ins=Instance.from_dict(json.loads(p.read_text()))
        if ins.players>5 or ins.topic_count>7:continue
        slack,wit,num=check(ins);agg['instances']+=1;agg['checks']+=num
        print(json.dumps({'source':p.name,'slack':str(slack),'checks':num}),flush=True)
        if best is None or slack<best:best=slack;agg['minimum']=str(slack);agg['witness']={'source':str(p.relative_to(ROOT)),**wit}
        if slack<0:print(json.dumps({'FAILURE':{'source':str(p.relative_to(ROOT)),**wit}}),flush=True);break
    print(json.dumps(agg,indent=2))
