from fractions import Fraction
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog
p=6;masks=list(range(1,1<<p));actual=(0,1);comp=(2,3)
def utility(a,b,i):
  return np.array([Fraction(int(B>>(a,b)[i]&1),int(B>>a&1)+int(B>>b&1)) if B>>(a,b)[i]&1 else Fraction(0) for B in masks],dtype=float)
U={(a,b,i):utility(a,b,i) for a,b,i in product(range(p),range(p),range(2))}
C=np.array([int(any(B>>a&1 for a in actual)) for B in masks])
R=np.array([int(not any(B>>a&1 for a in actual) and any(B>>a&1 for a in comp)) for B in masks])
best=0
for tail in product(range(p),repeat=p-1):
  rho=(1,)+tail
  rows=[U[a,rho[a],1]-U[a,b,1] for a,b in product(range(p),repeat=2)]
  rows.extend(U[0,1,0]-U[b,rho[b],0] for b in range(p))
  res=linprog(C-R,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[C],b_eq=[1],bounds=(0,None),method='highs')
  if res.success and res.fun<best-1e-8:
    best=res.fun
    weights={B:Fraction(float(x)).limit_denominator(100000) for B,x in zip(masks,res.x) if x>1e-8}
    print(json.dumps({'best':best,'rho':rho,'weights':{str(k):str(v) for k,v in weights.items()}},ensure_ascii=False),flush=True)
print('DONE',best)
