"""One targeted attack on LAST: m*v2(actual last prefix)<=W.
Fixes the already verified six-action full-history formal strategy. The query
p is a rationalization of the actual LAST dual optimum of the old817 witness.
Its sole purpose is falsification of this precise all-input candidate.
A nonpositive numerical result is not a theorem or a cone certificate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import lcm,gcd
from functools import reduce
import json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
d=json.loads((BASE/'round3_general/equilibrium/fractional_global_raw.json').read_text())
m=d['players'];k=len(d['topics']);pol={tuple(r['history']):r['action'] for r in d['policy']}
types=list(range(1,1<<k))
p=[F(a,10000) for a in (0,3036,856,0,3073,3035)]
assert sum(p)==1

def leaf(h):
 h=list(h)
 while len(h)<m:h.append(pol[tuple(h)])
 return tuple(h)
def load(t,z):return sum((t>>a)&1 for a in z)
def util(t,z,i):
 c=load(t,z)
 return F((t>>z[i])&1,c) if c else F(0)
z=leaf(())
IC=[]
for i in range(m):
 for h in product(range(k),repeat=i):
  y=leaf(h)
  for a in range(k):
   yy=leaf(h+(a,));IC.append([util(t,y,i)-util(t,yy,i) for t in types])
Kp=[]
for a in range(k):
 Kp.append([sum(p[T]*F((t>>T)&1,1+load(t,z[:-1])+((t>>a)&1)) for T in range(k)) for t in types])
W=[int(bool(load(t,z))) for t in types]
# tvalue<=all six column expectations, so it lower-bounds exact LAST.
A=[[-x for x in row]+[F(0)] for row in IC]+[[-x for x in row]+[F(1)] for row in Kp]
obj=W+[F(-m)]
res=linprog(np.array(obj,dtype=float),A_ub=np.array(A,dtype=float),b_ub=np.zeros(len(A)),A_eq=np.array([[1.]*len(types)+[0.]]),b_eq=[1.],bounds=[(0,None)]*len(types)+[(None,None)],method='highs')
r={'candidate':'LAST: m*v2(actual first m-1 actions)<=actual W','fixed_strategy_source':'round3_general/equilibrium/fractional_global_raw.json','fixed_p':list(map(str,p)),'status':res.message}
if res.success:
 r['numerical_maximum_m_query_floor_minus_W']=-res.fun
 v=[F(float(x)).limit_denominator(10**7) if x>1e-9 else F(0) for x in res.x[:-1]]
 den=lcm(*(x.denominator for x in v));ws=[int(x*den) for x in v];gg=reduce(gcd,ws);ws=[x//gg for x in ws]
 r['proposed_counts']={str(t):w for t,w in zip(types,ws) if w}
 r['exact_minimum_IC']=str(min(sum(x*w for x,w in zip(row,ws)) for row in IC))
 floor=min(sum(x*w for x,w in zip(row,ws)) for row in Kp)
 welfare=sum(x*w for x,w in zip(W,ws))
 r['exact_query_floor']=str(floor);r['exact_W']=welfare;r['exact_gap']=str(m*floor-welfare)
(HERE/'last_actual_menu_probe.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
