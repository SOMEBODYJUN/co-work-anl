"""Attack only the stated general residual-gap current-profit candidate.
Reuse one complete valid strategy, enlarge customer-type weights, solve exact-form LP
with floating optimization; any positive witness requires rational full-tree audit.
"""
import json,itertools,sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance
src=ROOT/'evidence/certificates/customer_attraction/prefix_balance_failure.json'
co=json.loads(src.read_text());ad={tuple(x['history']):x['action'] for x in co['actions']}
k=6;m=4;masks=list(range(1,1<<k));n=len(masks)
def leaf(h):
 while len(h)<m:h+=ad[h],
 return h
path=leaf(());occupied=set(path)
def coeff(h,a):
 p=leaf(h+(a,));return np.array([int(bool(mask>>a&1))/sum(bool(mask>>b&1) for b in p) if mask>>a&1 else 0 for mask in masks])
rows=[]
for h,a in ad.items():
 x=coeff(h,a)
 for b in range(k):
  if b!=a:rows.append(np.r_[coeff(h,b)-x,0])
W=np.array([int(any(mask>>a&1 for a in path)) for mask in masks]);eq=np.r_[W,0][None,:]
free=[a for a in range(k) if a not in occupied]
print('path',path,'missed labels',free,'IC rows',len(rows))
for i in range(m):
 r=m-i
 if r>len(free):continue
 u=coeff(path[:i],path[i])
 for top in itertools.combinations(free,r):
  z=np.array([int(not any(mask>>a&1 for a in path) and any(mask>>a&1 for a in top)) for mask in masks])
  constraints=list(rows)
  for small in itertools.combinations(free,r-1):
   zz=np.array([int(not any(mask>>a&1 for a in path) and any(mask>>a&1 for a in small)) for mask in masks])
   constraints.append(np.r_[zz-z,1])
  res=linprog(np.r_[u,-1],A_ub=np.array(constraints),b_ub=np.zeros(len(constraints)),A_eq=eq,b_eq=[1],bounds=[(0,None)]*(n+1),method='highs')
  print('position',i+1,'r',r,'top',top,'status',res.status,'max_gap_minus_u',None if not res.success else -res.fun)
  if res.success and res.fun < -1e-8:
   out={'candidate':'u_i >= f_U(r)-f_U(r-1)','status':'floating_witness_needs_exact_audit','source_strategy':str(src.relative_to(ROOT)),'path':path,'bad_position':i+1,'top':top,'objective':-res.fun,'weights':{str(mask):float(w) for mask,w in zip(masks,res.x[:-1]) if w>1e-8},'d':float(res.x[-1])}
   Path(__file__).with_name('residual_gap_floating_witness.json').write_text(json.dumps(out,indent=2));raise SystemExit
