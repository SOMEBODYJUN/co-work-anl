"""Discovery-only exact-outcome-set floating probe of two partition factors."""
from cartesian_probe import profiles,utility,outcomes
import argparse,itertools as it,json,time
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--m',type=int,default=5);p.add_argument('--r',type=int,default=5);p.add_argument('--s',type=int,default=4);p.add_argument('--qmax',type=int,default=5);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
k=a.r*a.s;start=time.time()
C=np.zeros((k,a.r+a.s))
for t,(i,c)in enumerate(it.product(range(a.r),range(a.s))):C[t,i]=1;C[t,a.r+c]=1
zs,qs,ix=profiles(k,a.m);ub,wb=utility(qs,C)
records=[]
for q in range(1,a.qmax+1):
 mass=np.r_[np.ones(a.r),q*np.ones(a.s)];u,w=ub@mass,wb@mass
 o,_=outcomes(u,w,k,a.m,ix);j=min(o,key=lambda j:w[j]);W=w[j];O=max(w)
 rec=dict(m=a.m,r=a.r,s=a.s,q=q,W=W,OPT=O,ratio=O/W,target=zs[j],root_outcomes=len(o),status='numerical_only')
 print(json.dumps(rec),flush=True);records.append(rec)
 a.out.write_text(json.dumps(records,indent=2))
print(json.dumps(dict(status='finished',seconds=time.time()-start)),flush=True)
