"""Exhaust all 4-topic last-reply policies, collision-free actual (C,D).
Floating LP only proposes a ray; exact reconstruction independently verifies.
"""
from itertools import product,combinations
from fractions import Fraction
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
P=Path(__file__).resolve().parent
p=4
masks=[v for v in range(1,1<<p) if not (v&(1<<2) and v&(1<<3))]
mem=np.array([[(v>>a)&1 for a in range(p)]for v in masks],dtype=float)
def u(a,b):return mem[:,a]/(1+mem[:,b])
best=1
count=0
for replies in product(range(p),repeat=p):
 if replies[2]!=3:continue
 rows=[]
 for a in range(p):
  for b in range(p):rows.append(u(replies[a],a)-u(b,a))
 for a in range(p):rows.append(mem[:,2]-u(a,replies[a]))
 rows=np.array(rows)
 W=mem[:,2]+mem[:,3]
 for opt in combinations(range(p),2):
  O=(mem[:,opt].sum(axis=1)>0).astype(float)
  sol=linprog(-O,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=[W],b_eq=[1.],bounds=(0,None),method='highs')
  count+=1
  if sol.success and -sol.fun>best+1e-8:
   best=-sol.fun
   weights=[Fraction(float(x)).limit_denominator(100000)for x in sol.x]
   def ef(a,b):return sum(w*Fraction((v>>a)&1,1+((v>>b)&1))for v,w in zip(masks,weights))
   assert all(ef(replies[a],a)>=ef(b,a)for a in range(p)for b in range(p))
   assert all(ef(2,3)>=ef(a,replies[a])for a in range(p))
   ww=sum(w for v,w in zip(masks,weights)if v&(1<<2|1<<3))
   oo=sum(w for v,w in zip(masks,weights)if any(v&(1<<a)for a in opt))
   data={'topics':['A','B','C','D'],'replies':replies,'actual':[2,3],'comparison':opt,'ratio':str(oo/ww),'types':[[v,str(w)]for v,w in zip(masks,weights)if w]}
   (P/'two_player_collision_free_best.json').write_text(json.dumps(data,indent=2))
   print(data,flush=True)
print('LPs',count,'best',best)
