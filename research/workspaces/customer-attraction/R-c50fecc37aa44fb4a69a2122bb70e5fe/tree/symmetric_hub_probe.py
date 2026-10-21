"""Signed all-hub policy LP. Not a real customer-attraction counterexample."""
from itertools import product,combinations
from fractions import Fraction as Q
from pathlib import Path
import json,numpy as np
from scipy.optimize import linprog
from signed_policy_search import prepare,compositions
BASE=Path(__file__).resolve().parent
n,p=4,5;qs,vs,vid,F,universal,targets=prepare(n,p)
orbits=[(h,k) for h in range(2) for k in range(5) if h or k]
O=np.array([[int((B&1,B.bit_count()-(B&1))==orb) for orb in orbits]for B in range(1,1<<p)])
rows=[]
for d in range(n):
 for h in compositions(d,p):
  root=tuple(h[a]+(n-d if a==0 else 0) for a in range(p))
  for b in range(1,p):
   dev=tuple(h[a]+(n-d-1 if a==0 else 1 if a==b else 0) for a in range(p))
   rows.append(F[vid[dev,b]]-F[vid[root,0]])
for local in [False,True]:
 extra=[]
 if local:
  for k in range(1,min(n,p)+1):
   for A in combinations(range(p),k):
    maskA=sum(1<<a for a in A)
    for j in range(1,k+1):
     for X in combinations(A,j):
      maskX=sum(1<<a for a in X);extra.append([-int(B&maskA==maskX) for B in range(1,1<<p)])
 a=np.vstack([universal,np.array(rows)]+([np.array(extra)]if extra else []))@O
 a=a[np.max(np.abs(a),axis=1)>1e-9];a=np.unique(np.round(a,12),axis=0)
 root=np.array([int(B&1!=0) for B in range(1,1<<p)])@O
 obj=np.array([int(B>>1!=0) for B in range(1,1<<p)])@O
 sol=linprog(-obj,A_ub=a,b_ub=np.zeros(len(a)),A_eq=root[None,:],b_eq=[1],bounds=(None,None),method='highs')
 print('local',local,'value',-sol.fun if sol.success else sol.message,flush=True)
 if sol.success:
  vals=[str(Q(float(v)).limit_denominator(1000000)) for v in sol.x]
  print(list(zip(orbits,vals)),flush=True)
  out=dict(scope='signed symmetric all-hub game, not CAG',m=n,p=p,hub=0,orbits=[dict(h=h,k=k,per_type_weight=v)for (h,k),v in zip(orbits,vals)],objective=float(-sol.fun),local_atoms=local)
  (BASE/f'symmetric_hub_local{int(local)}.json').write_text(json.dumps(out,indent=2)+'\n')
