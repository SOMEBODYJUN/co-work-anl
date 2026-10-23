"""One finite MILP simplification of the already found menu obstruction."""
import itertools, math, json
from fractions import Fraction as F
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

K=4
TYPES=list(range(1,1<<K))
MENU=[(0,2),(1,2),(2,3),(2,3)]
P=[F(1,4),F(2,5),F(7,40),F(7,40)]
Q=[[F(0),F(1,3),F(1,3),F(1,3)],
   [F(1,3),F(0),F(1,3),F(1,3)],
   [F(1,6),F(3,10),F(0),F(8,15)],
   [F(1,6),F(3,10),F(8,15),F(0)]]

def feature(a,z):
    return [F(1,sum(bool(t&(1<<b)) for b in z)) if t&(1<<a) else F(0) for t in TYPES]

def add(*vectors): return [sum(x) for x in zip(*vectors)]
def scale(c,v): return [c*x for x in v]

root=[feature(a,(a,)+MENU[a]) for a in range(K)]
cover=[F(any(t&(1<<b) for b in (2,2,3))) for t in TYPES]
rows=[]; lower=[]
def constraint(row,strict=False):
    denominator=math.lcm(*(x.denominator for x in row))
    rows.append([int(x*denominator) for x in row]); lower.append(1 if strict else 0)
for a in range(K):
    constraint(add(root[2],scale(-1,root[a])))
    tail=add(*(feature(b,(a,)+MENU[a]) for b in MENU[a]))
    for c in range(K):
        local=add(*(scale(Q[a][b],feature(c,(a,b,c))) for b in range(K)))
        constraint(add(tail,scale(-2,local)))
for b in itertools.combinations_with_replacement(range(K),2):
    value=add(*(scale(P[a],feature(a,(a,)+b)) for a in range(K)))
    constraint(add(scale(3,value),scale(-1,cover)),strict=True)
r=milp(np.ones(len(TYPES)),integrality=np.ones(len(TYPES)),bounds=Bounds(0,np.inf),
       constraints=LinearConstraint(np.array(rows,float),np.array(lower,float),np.inf),
       options={'time_limit':30})
print(json.dumps({'success':r.success,'message':r.message,'total':r.fun,
                  'weights':None if r.x is None else {str(t):int(round(x)) for t,x in zip(TYPES,r.x) if round(x)}},indent=2))
