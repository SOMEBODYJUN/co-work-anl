"""Attack residual portfolio through full two-provider strategies on six labels."""
import itertools,json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
bits=list(itertools.product((0,1),repeat=6))
W=np.array([int(z[0]+z[1]>0) for z in bits])
O=np.array([int(not(z[0]+z[1]) and z[2]+z[3]>0) for z in bits])
def U(x,y):return F(x,1+y) if x else F(0)
best=(1,None)
for q0,q1 in itertools.product(range(6),repeat=2):
 replies=[1,0,4,5,q0,q1]
 # Reply to B=0 is arbitrary initially; enumerate it too if promising later.
 for rb in range(6):
  replies[1]=rb
  labels=[]; rows=[]
  for a in range(6):
   for t in range(6):
    rows.append([float(U(z[replies[a]],z[a])-U(z[t],z[a])) for z in bits])
    labels.append(('last',a,t))
   rows.append([float(U(z[0],z[1])-U(z[a],z[replies[a]])) for z in bits])
   labels.append(('root',a))
  lp=linprog(W,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[O],b_eq=[1],bounds=(0,None),method='highs')
  if lp.success and lp.fun<best[0]-1e-8:
   best=(lp.fun,{'replies':replies[:],'types':[(z,str(F(float(v)).limit_denominator(100000))) for z,v in zip(bits,lp.x) if v>1e-8]})
   print(best,flush=True)
   Path(__file__).with_suffix('.json').write_text(json.dumps(best,indent=2))
print('best',best)
