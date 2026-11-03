"""Necessary branch relaxation for maximal-cardinality root topic.
No full-SPE claim: optimize one explicit threshold inequality only.
"""
from itertools import product
from scipy.optimize import linprog
import numpy as np,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
cols=[v+(o,) for v in product(range(2),repeat=5) for o in range(2) if any(v) or o]
size=np.array([[v[i] for v in cols] for i in range(5)],float)
util=np.array([[v[i]/sum(v[:5]) if v[i] else 0 for v in cols] for i in range(5)],float)
opt=np.array([v[5] for v in cols],float)
last=[[util[4][i]-(v[j]/(sum(v[:4])+1) if v[j] else 0) for i,v in enumerate(cols)] for j in range(5)]
lastopt=5*util[4]-np.array([v[5]/(sum(v[:4])+1) for v in cols])
A0=[*size[1:],*[-np.array(x) for x in last],-lastopt]
b0=[1]*4+[0]*6
for j in range(1,4):
 A0.append(-util[j]);b0.append(-.2)
res=[]
for t in [0.2,.21,.22,.23,.24,.25,.26,.28,.3,.32,.35,.4,.45,.5,.6,.75]:
 r=linprog(-opt,A_ub=np.array(A0+[util[0]]),b_ub=np.array(b0+[t]),A_eq=np.array([size[0]]),b_eq=[1],bounds=(0,None),method='highs')
 if r.success:
  d={'t':t,'O':-r.fun,'dual':r.ineqlin.marginals.tolist(),'eq':r.eqlin.marginals.tolist(),'support':[(cols[i],r.x[i]) for i in range(len(cols)) if r.x[i]>1e-8]}
  print({k:v for k,v in d.items() if k not in ('support','dual','eq')},flush=True);res.append(d)
 else: print(t,r.message)
(HERE/'max_topic_branch_lp.json').write_text(json.dumps(res,indent=2)+'\n')
