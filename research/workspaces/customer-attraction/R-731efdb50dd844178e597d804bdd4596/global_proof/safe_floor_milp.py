from pathlib import Path
import argparse,json,time
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=6);ap.add_argument('--players',type=int,default=3);ap.add_argument('--seconds',type=float,default=45);ap.add_argument('--output',required=True);args=ap.parse_args()
 p,m=args.topics,args.players;n=(1<<p)-1;wit=[(a,B) for a in range(p) for B in combinations_with_replacement([b for b in range(p) if b!=a],m-1)];k=len(wit);M=p*m
 def pay(a,profile):return np.array([bool(mask&(1<<a))/sum(bool(mask&(1<<b)) for b in profile) if mask&(1<<a) else 0 for mask in range(1,1<<p)])
 rows=[];lbs=[];ubs=[]
 def add(w,z,lb=-np.inf,ub=np.inf):rows.append((w,z));lbs.append(lb);ubs.append(ub)
 for a in range(p):add({}, {j:1 for j,(aa,B) in enumerate(wit) if aa==a},1,1)
 for j,(a,B) in enumerate(wit):
  profile=(a,)+B
  add(dict(enumerate(pay(a,profile))),{j:M},ub=1+M)
  for b in set(B):add(dict(enumerate(pay(b,profile))),{j:-M},lb=1-M)
 add({j:1 for j in range(n)},{},ub=M)
 A=lil_matrix((len(rows),n+k))
 for i,(w,z) in enumerate(rows):
  for j,v in w.items():A[i,j]=v
  for j,v in z.items():A[i,n+j]=v
 obj=np.r_[-np.array([int(mask&((1<<m)-1)!=0) for mask in range(1,1<<p)]),np.zeros(k)]
 st=time.time();r=milp(obj,integrality=np.r_[np.zeros(n),np.ones(k)],bounds=Bounds(np.zeros(n+k),np.r_[np.full(n,M),np.ones(k)]),constraints=LinearConstraint(A.tocsr(),lbs,ubs),options={'time_limit':args.seconds,'mip_rel_gap':1e-8})
 out={'scope':'noncredible bad-menu sufficient-lemma attack; no SPE','parameters':vars(args),'status':r.message,'elapsed':time.time()-st,'value':-r.fun if r.fun is not None else None,'dual_bound':-r.mip_dual_bound if hasattr(r,'mip_dual_bound') and r.mip_dual_bound is not None else None}
 if r.x is not None:out.update(weights={str(mask):float(r.x[mask-1]) for mask in range(1,1<<p) if r.x[mask-1]>1e-7},witness={str(a):list(B) for j,(a,B) in enumerate(wit) if r.x[n+j]>.5})
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
