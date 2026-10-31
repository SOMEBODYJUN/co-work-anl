from fractions import Fraction as F
from itertools import product
import json, argparse
import numpy as np
from scipy.optimize import linprog

def rows(m):
 k=m-2
 for bits in product(range(2),repeat=m):
  es=bits[:k]; a,b=bits[-2:]; p=sum(es); c=p+a+b; w=int(c>0)
  uj=[F(e,c) if e else F(0) for e in es]; ub=F(b,c) if b else F(0)
  R=[];L=[]; bj=0
  for j,e in enumerate(es):
   R.append(uj[j]-(F(a,bj+m-j) if a else 0))
   L.append(ub-F(e,p+a+1))
   bj+=e
  alpha=F(a,c) if a else F(0);beta=ub
  for d,l in [(0,0),(0,m),(1,0),(1,m),(m,0),(m,m)]:
   G=m*alpha+beta/2-F(d,p+1)-F(l,2*m*(p+a+1))+F(d*l,m*(p+1)*(p+2))
   q=2*w-int(d>0)-G
   yield bits,d,l,R+L,q

def solve(m):
 rr=list(rows(m)); res=linprog(np.zeros(2*(m-2)),A_ub=np.array([[float(x) for x in r[3]] for r in rr]),b_ub=np.array([float(r[4]) for r in rr]),bounds=(0,None),method='highs')
 ans={'m':m,'success':res.success,'message':res.message,'rows':len(rr)}
 if res.success:
  sol=[F(float(x)).limit_denominator(1000000) for x in res.x]
  worst=min((r[4]-sum(x*y for x,y in zip(r[3],sol)),r[:3]) for r in rr)
  ans.update(coeff=[str(x) for x in sol],worst=str(worst))
 else:
  # Minimax uniform row violation for diagnostic, no proof of infeasibility.
  mat=np.c_[np.array([[float(x) for x in r[3]] for r in rr]),-np.ones(len(rr))]
  obj=np.zeros(2*(m-2)+1);obj[-1]=1
  fit=linprog(obj,A_ub=mat,b_ub=np.array([float(r[4]) for r in rr]),bounds=[(0,None)]*(2*(m-2))+[(None,None)],method='highs')
  if fit.success:
   ans.update(min_slack=float(fit.x[-1]),relaxed_coeff=[float(x) for x in fit.x[:-1]])
   ans['active']=[{'type':list(rr[i][:3]),'dual':float(v)} for i,v in enumerate(fit.ineqlin.marginals) if abs(v)>1e-8]
 return ans

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--max-m',type=int,default=10);ap.add_argument('--output');a=ap.parse_args()
 ans=[solve(m) for m in range(3,a.max_m+1)]
 print(json.dumps(ans,indent=2))
 if a.output:
  with open(a.output,'x') as f:json.dump(ans,f,indent=2)
