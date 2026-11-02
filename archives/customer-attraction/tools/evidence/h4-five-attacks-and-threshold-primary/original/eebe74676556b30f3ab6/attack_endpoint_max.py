"""One sufficient but stronger endpoint-max bridge counterexample proposal."""
from pathlib import Path
from itertools import product
import json, numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
for certfile in ['aggregate_theta_failure','individual_security_failure','root_tax_failure','portfolio_matching_failure','worst_cce_welfare_failure','eight_customer_cce_welfare_gap']:
 p=ROOT/'evidence/certificates/customer_attraction'/f'{certfile}.json'
 if not p.exists(): continue
 obj=json.loads(p.read_text()); st=obj.get('strategy',obj)
 if 'actions' not in st:continue
 acts={tuple(x['history']):x['action'] for x in st['actions']}; m=max(map(len,acts))+1;K=max(max(h,default=0) for h in acts)+1;K=max(K,max(acts.values())+1)
 B=np.array([[(b>>a)&1 for a in range(K)] for b in range(1,1<<K)],dtype=int);D=len(B)
 def leaf(h):
  while len(h)<m:h=h+(acts[h],)
  return h
 def payoff(h,a):
  c=B[:,h].sum(axis=1);return np.divide(B[:,a],c,out=np.zeros(D),where=c>0)
 q=leaf(()); c=B[:,q].sum(axis=1);W=(c>0).astype(float);G=np.divide(W,c+1);e=B/(c[:,None]+1)
 rows=[]
 for h,a in acts.items():
  chosen=payoff(leaf(h),a)
  for b in range(K):
   if a!=b:rows.append(payoff(leaf(h+(b,)),b)-chosen)
 for a in range(K):
  gap=m*e[:,a]-W-G
  res=linprog(-gap,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[W],b_eq=[1],bounds=[(0,None)]*D,method='highs')
  if res.success and -res.fun>1e-8:
   print('POSITIVE',certfile,'m,K,T,gap',m,K,a,-res.fun)
   print({b:round(w,10) for b,w in enumerate(res.x,1) if w>1e-9})
