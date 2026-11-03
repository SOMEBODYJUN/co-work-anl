#!/usr/bin/env python3
"""Targeted finite diagnosis of OPT-W <= m min_i u_i and insertion floor."""
from fractions import Fraction as F
from pathlib import Path
import json, random, sys
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver

def check(ins):
    sol=ExactSPESolver(ins);opt=ins.optimal_welfare();res=[]
    for c in sol.outcomes():
        w=ins.welfare(c);pay=ins.topic_payoffs(c);u=min(pay[a] for a in range(ins.topic_count) if c[a])
        insert=max(sum((F(x.multiplicity,1+sum(c[t] for t in x.topics)) for x in ins.customers if a in x.topics),F()) for a in range(ins.topic_count))
        res.append((ins.players*u+w-opt,u-insert,c,w,str(u),str(insert)))
    return min(res), min(res,key=lambda z:z[1]),len(res)
if __name__=='__main__':
    best=None;bf=None;num=0
    for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        ins=Instance.from_dict(json.loads(p.read_text()))
        if ins.players>6 or ins.topic_count>10:continue
        gap,floor,count=check(ins);num+=count
        print(json.dumps({'source':p.name,'gap_slack':str(gap[0]),'insertion_slack':str(floor[1]),'outcomes':count}),flush=True)
        if best is None or gap[0]<best[0]:best=gap;bf=p.name
        if gap[0]<0:print(json.dumps({'WEAK_GAP_FAILURE':gap,'source':p.name},default=str),flush=True);break
    print(json.dumps({'minimum_gap':best,'source':bf,'outcomes':num},default=str,indent=2))
