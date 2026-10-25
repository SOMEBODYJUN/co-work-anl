"""Designed 5-cycle omitted customers with disjoint banking topics.
First solve every unavoidable path security constraint (including exact last BR).
The LP is necessary, and no feasible LP point is claimed to be a SPE.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog
OUT=Path(__file__).with_suffix('.json')
P=8; M=5
path=(0,0,1,1,2)
# 15 bank types: every bank belongs to one actual bank and a single optimal T.
# Five missed types: adjacent optimal T memberships, no banking topic.
types=[(a,3+j) for a in range(3) for j in range(5)] + [(3+j,3+(j+1)%5) for j in range(5)]
q=[path.count(a) for a in range(P)]
def row(q,a):
    return [F(1,sum(q[b] for b in typ)) if a in typ else F(0) for typ in types]
rows=[];labels=[]
for i,a in enumerate(path):
    old=[path[:i].count(b) for b in range(P)]
    actual=row(q,a)
    r=M-i
    for t in range(P):
        # All r new movers choose query t: the largest attainable per-client load.
        dev=old[:]; dev[t]+=r
        rows.append([x-y for x,y in zip(actual,row(dev,t))]);labels.append((i+1,t))
W=[F(j<15) for j in range(20)]
L=[F(j>=15) for j in range(20)]
res=linprog(-np.array(L,float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=[np.array(W,float)],b_eq=[1],bounds=(0,None),method='highs')
assert res.success,res.message
x=[F(float(t)).limit_denominator(10**6) for t in res.x]
beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**6)
mu=[F(float(-t)).limit_denominator(10**6) for t in res.ineqlin.marginals]
residual=[beta*W[j]-sum(mu[k]*rows[k][j] for k in range(len(rows)))-L[j] for j in range(20)]
dot=lambda a,b:sum((v*w for v,w in zip(a,b)),F(0))
primal=all(t>=0 for t in x) and dot(W,x)==1 and all(dot(r,x)>=0 for r in rows)
dual=all(t>=0 for t in mu) and all(t>=0 for t in residual)
report={'model':'five providers, eight topics, AABBC; disjoint banks with singleton optimal membership; 5-cycle omitted pair membership','status':'necessary security relaxation only; no SPE claim','types':types,'path':path,'objective_L':str(dot(L,x)),'beta':str(beta),'primal_exact':primal,'dual_exact':dual,'point':{str(types[j]):str(v) for j,v in enumerate(x) if v},'dual':[(labels[k],str(v)) for k,v in enumerate(mu) if v],'residual':[str(v) for v in residual]}
OUT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
