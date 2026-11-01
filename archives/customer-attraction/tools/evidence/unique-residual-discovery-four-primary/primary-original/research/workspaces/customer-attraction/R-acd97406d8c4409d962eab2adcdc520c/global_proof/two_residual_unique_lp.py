import itertools,random,json
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
k=6; masks=list(range(1,1<<k));rng=random.Random(811)
def p(a,b):return np.array([(int(mask>>a&1)*(2-int(mask>>b&1))) for mask in masks],dtype=float)
W=np.array([int(mask&3!=0) for mask in masks],dtype=float)
R=np.array([int(mask&3==0 and mask&((1<<2)|(1<<5))!=0) for mask in masks],dtype=float)
for z in range(10000):
 reply=[1]+[rng.randrange(k) for a in range(1,k)]
 if z==0:reply=[1,3,3,4,3,4]
 root=p(0,1); rows=[]
 for a in range(k):
  for b in range(k):rows.append(p(reply[a],a)-p(b,a))
  rows.append(root-p(a,reply[a]))
 O=np.array([int(mask&((1<<2)|(1<<5))!=0) for mask in masks],dtype=float)
 rhs=[0.0]*len(rows)
 for a,b in itertools.combinations_with_replacement(range(k),2):
  if (a,b)==(2,5):continue
  Oab=np.array([int(mask&((1<<a)|(1<<b))!=0) for mask in masks],dtype=float)
  rows.append(O-Oab);rhs.append(0.001)
 A=np.array(rows)
 objective=R-W # twice root utility == coefficient root
 res=linprog(-objective,A_ub=-A,b_ub=-np.array(rhs),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
 if res.success and -res.fun>1e-6:
  rat=[F(float(x)).limit_denominator(1000000) for x in res.x]
  import math,functools
  scale=functools.reduce(math.lcm,(x.denominator for x in rat),1)
  weights=[int(x*scale) for x in rat]
  print('found',z,reply,'adv',-res.fun,'W',scale,'weights',{mask:w for mask,w in zip(masks,weights) if w},flush=True)
  obj={'reply':reply,'weights':{mask:w for mask,w in zip(masks,weights) if w},'W':scale,'objective':str(sum(F(int(c))*w for c,w in zip(objective,weights)))}
  open('research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/residual_unique_bridge_lp.json','w').write(json.dumps(obj,indent=2));break
 if z%1000==0:print(z,flush=True)
