"""Joint search restricted to count-dependent complete SPE strategies.

This restriction is a genuine subset, NOT a reduction of full-history SPE.
Conditional constants m are inherited from the canonical full-history MILP.
Floating MILP proposes actions only; exact rational strategy-cone recovery and
all ordered-history one-step-deviation checks certify any returned witness.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row,serializable,integer_clones,instance_from_clones,independently_verify

def counts(p,total):
    if p==1:
        yield (total,);return
    for first in range(total+1):
        for tail in counts(p-1,total-first):yield (first,)+tail

def increment(k,a):return k[:a]+(k[a]+1,)+k[a+1:]

def candidate(p,path,portfolio,seconds,threshold=None):
    m=len(path);n=(1<<p)-1
    nodes=tuple(k for depth in range(m) for k in counts(p,depth))
    u={};z={};idx=n
    for k in nodes:
        for a in range(p):u[k,a]=idx;idx+=1
    for k in nodes:
        for a in range(p):z[k,a]=idx;idx+=1
    lo=np.zeros(idx);hi=np.full(idx,m,dtype=float);integrality=np.zeros(idx,dtype=np.uint8)
    for v in z.values():hi[v]=1;integrality[v]=1
    k=(0,)*p
    for a in path:
        lo[z[k,a]]=hi[z[k,a]]=1;k=increment(k,a)
    root=k;zero=(0,)*p
    hi[u[zero,path[0]]]=1
    ri=[];ci=[];data=[];lbs=[];ubs=[]
    def add(row,lb=-np.inf,ub=np.inf):
        rowidx=len(lbs)
        for col,value in row.items():
            if value:ri.append(rowidx);ci.append(col);data.append(float(value))
        lbs.append(lb);ubs.append(ub)
    def child_expr(k,t):
        if sum(k)<m:return {u[k,t]:1}
        if not k[t]:return {}
        return {j:x for j,x in enumerate(payoff_row(p,k,t)) if x}
    def difference(k,t,child,ct):
        row={u[k,t]:1}
        for j,x in child_expr(child,ct).items():row[j]=row.get(j,0)-x
        return row
    actual=coverage_row(p,(a for a,x in enumerate(root) if x))
    objective=coverage_row(p,portfolio)
    add({j:x for j,x in enumerate(actual) if x},1,1)
    add({j:1 for j in range(n)},ub=m*p)
    if threshold is not None:add({j:x for j,x in enumerate(objective) if x},lb=threshold)
    for a in range(p):
        row={j:1 for j in range(n) if (j+1)&(1<<a)};row[u[zero,path[0]]]=-m
        add(row,ub=0)
    add({u[zero,a]:q for a,q in enumerate(root) if q},1,1)
    for k in nodes:
        add({z[k,a]:1 for a in range(p)},1,1)
        for a in range(p):
            action=z[k,a];child=increment(k,a)
            for t in range(p):
                row=difference(k,t,child,t);row[action]=m;add(row,ub=m)
                row=difference(k,t,child,t);row[action]=-m;add(row,lb=-m)
            for b in range(p):
                if b==a:continue
                row=difference(k,a,increment(k,b),b);row[action]=-m;add(row,lb=-m)
    matrix=coo_matrix((data,(ri,ci)),shape=(len(lbs),idx)).tocsc()
    c=np.zeros(idx);c[:n]=-np.array(objective,dtype=float)
    start=time.monotonic()
    res=milp(c,integrality=integrality,bounds=Bounds(lo,hi),constraints=LinearConstraint(matrix,np.array(lbs),np.array(ubs)),options={'time_limit':seconds,'mip_rel_gap':0,'presolve':True})
    meta={'status':int(res.status),'message':res.message,'count_states':len(nodes),'binary_actions':len(z),'rows':len(lbs),'variables':idx,'elapsed':time.monotonic()-start,'floating_objective':float(-res.fun) if res.fun is not None else None,'floating_dual_bound':float(-res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None,'floating_only':True}
    if res.x is None:return None,meta
    policy={k:max(range(p),key=lambda a:res.x[z[k,a]]) for k in nodes}
    actions={h:policy[tuple(h.count(a) for a in range(p))] for depth in range(m) for h in product(range(p),repeat=depth)}
    return StrategyCone(p,m,actions),meta

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--topics',type=int,default=7)
    parser.add_argument('--path',default='0,0,1,1,2')
    parser.add_argument('--portfolio',default='2,3,4,5,6')
    parser.add_argument('--seconds',type=float,default=45)
    parser.add_argument('--threshold',type=float)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    path=tuple(map(int,args.path.split(',')));portfolio=tuple(map(int,args.portfolio.split(',')))
    cone,meta=candidate(args.topics,path,portfolio,args.seconds,args.threshold)
    report={'scope':'joint count-dependent SPE subset; not all full-history SPE','players':len(path),'topics':args.topics,'path':path,'portfolio':portfolio,'milp':meta,'proof':None}
    if cone is not None:
        result=cone.optimize(portfolio)
        if result['certified']:
            clones=integer_clones(result['values'])
            assert independently_verify(cone,clones)
            instance=instance_from_clones(args.topics,len(path),clones)
            cert=StrategyCertificate(cone.actions,cone.root)
            verify_certificate(instance,cert).assert_valid()
            welfare=instance.welfare(cone.root);opt=instance.optimal_welfare()
            report['proof']={'integer_clones':clones,'strategy':cert.to_dict(),'welfare':welfare,'optimum':opt,'ratio':Fraction(opt,welfare),'cone_comparison_optimum':result['value'],'exact_dual_optimal':result['dual_optimal'],'dual_support':result['dual_support'],'dual_bound':result['dual_bound'],'all_ordered_histories':len(cone.actions)}
    args.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
    print(json.dumps(serializable({k:v for k,v in report.items() if k!='proof'})))
    if report['proof']:print(json.dumps(serializable({k:v for k,v in report['proof'].items() if k not in ('integer_clones','strategy','dual_support')})))

if __name__=='__main__':main()
