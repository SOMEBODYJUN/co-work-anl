"""Exploratory LP on fixed two-player menu, not a general proof."""
from fractions import Fraction
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog

p=5
masks=list(range(1,1<<p))
rho=(1,2,1,2,0)
actual=(4,0)
comparison=(1,3)

def u(path,i,B):
    if not B>>path[i]&1:return Fraction(0)
    return Fraction(1,sum(B>>a&1 for a in path))

def out(first):return (first,rho[first])
rows=[]
for a in range(p):
  for b in range(p):
    rows.append([u(out(a),1,B)-u((a,b),1,B) for B in masks])
for b in range(p):
    rows.append([u(actual,0,B)-u(out(b),0,B) for B in masks])
C=[int(any(B>>a&1 for a in actual)) for B in masks]
R=[int(not any(B>>a&1 for a in actual) and any(B>>a&1 for a in comparison)) for B in masks]
res=linprog(np.array(C)-np.array(R),A_ub=-np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),A_eq=[C],b_eq=[1],bounds=(0,None),method='highs')
if not res.success:print(res.message)
else:
  weights={B:Fraction(float(x)).limit_denominator(100000) for B,x in zip(masks,res.x) if x>1e-8}
  checks=[sum(a*weights.get(B,0) for B,a in zip(masks,row)) for row in rows]
  result={'status':'exploratory exact-rechecked fixed-menu LP point','weights':{str(k):str(v) for k,v in weights.items()},'minimum_spe_slack':str(min(checks)),'W':str(sum(c*weights.get(B,0) for B,c in zip(masks,C))),'R':str(sum(r*weights.get(B,0) for B,r in zip(masks,R))),'root_path':actual,'reply':rho,'comparison':comparison}
  print(json.dumps(result,indent=2))
