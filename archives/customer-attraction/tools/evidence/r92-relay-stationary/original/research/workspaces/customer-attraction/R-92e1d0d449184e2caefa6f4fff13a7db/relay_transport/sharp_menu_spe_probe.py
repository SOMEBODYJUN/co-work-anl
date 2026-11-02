"""One discriminating probe: can the sharp r=3 root menu have total negative
stationary defect after ALL actual continuation SPE inequalities are imposed?
No global search or half-counterexample claim.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm
import json
import numpy as np
from scipy.optimize import milp,linprog,Bounds,LinearConstraint

k=4
masks=list(range(1,1<<k))
bc=[(1,2),(0,3),(0,3),(1,2)]
zindex={(i,a,c):15+16*i+4*a+c for i,a,c in product(range(k),repeat=3)}
nv=79

def payoff(a,z):
    return [F(int(bool(T&(1<<a))),sum(bool(T&(1<<t)) for t in z))
            if T&(1<<a) else F(0) for T in masks]

def dif(u,v): return [x-y for x,y in zip(u,v)]

def row(coeff): return [float(x) for x in coeff]+[0.]*(nv-15)

constraints=[]
lower=[]
upper=[]

def add(v,lo,hi):
    constraints.append(v);lower.append(lo);upper.append(hi)

add([1.]*15+[0.]*(nv-15),1,1)
for i,a in product(range(k),repeat=2):
    rr=[0.]*nv
    for c in range(k): rr[zindex[i,a,c]]=1
    add(rr,1,1)
    for c in range(k):
        idx=zindex[i,a,c]
        for t in range(k):
            v=row(dif(payoff(c,(i,a,c)),payoff(t,(i,a,t))))
            v[idx]-=2
            add(v,-2,np.inf)
        b0,c0=bc[i]
        v=row(dif(payoff(b0,(i,b0,c0)),payoff(a,(i,a,c))))
        v[idx]-=2
        add(v,-2,np.inf)
    if a==bc[i][0]:
        rr=[0.]*nv;rr[zindex[i,a,bc[i][1]]]=1
        add(rr,1,1)
d0=payoff(0,(0,*bc[0]))
for i in range(k): add(row(dif(d0,payoff(i,(i,*bc[i])))),0,np.inf)
obj=[F(0)]*15
for i in range(k):
    root=payoff(i,(i,*bc[i]))
    tails=[payoff(a,(i,*bc[i])) for a in bc[i]]
    obj=[q+(d-(u+v)/2)/4 for q,d,u,v in zip(obj,root,*tails)]
c=np.array([float(x) for x in obj]+[0.]*(nv-15))
integ=np.array([0]*15+[1]*(nv-15))
res=milp(c,integrality=integ,bounds=Bounds(np.zeros(nv),np.array([np.inf]*15+[1.]*(nv-15))),
         constraints=LinearConstraint(np.array(constraints),np.array(lower),np.array(upper)),
         options={'time_limit':120})
out={'status':int(res.status),'message':res.message,'objective':None if res.fun is None else float(res.fun)}
if res.x is not None:
    act={(i,a):max(range(k),key=lambda c:res.x[zindex[i,a,c]]) for i,a in product(range(k),repeat=2)}
    exactrows=[]
    for (i,a),c0 in act.items():
        for t in range(k): exactrows.append(dif(payoff(c0,(i,a,c0)),payoff(t,(i,a,t))))
        b0,d=bc[i]
        exactrows.append(dif(payoff(b0,(i,b0,d)),payoff(a,(i,a,c0))))
    for i in range(k): exactrows.append(dif(d0,payoff(i,(i,*bc[i]))))
    rr=linprog([float(x) for x in obj],A_ub=-np.array(exactrows,dtype=float),b_ub=np.zeros(len(exactrows)),
        A_eq=np.ones((1,15)),b_eq=[1],bounds=(0,None),method='highs')
    w=[F(float(x)).limit_denominator(10**7) for x in rr.x]
    den=lcm(*(x.denominator for x in w)); wi=[int(x*den) for x in w]
    valid=all(sum(x*y for x,y in zip(row,wi))>=0 for row in exactrows)
    dd=sum(x*y for x,y in zip(obj,wi))
    out.update({'fixed_selector_objective':float(rr.fun),'exact_valid':valid,'stationary_defect':str(dd),
        'weights':{str(T):v for T,v in zip(masks,wi) if v},
        'terminal_actions':{str((i,a)):c for (i,a),c in act.items()}})
print(json.dumps(out,indent=2))
