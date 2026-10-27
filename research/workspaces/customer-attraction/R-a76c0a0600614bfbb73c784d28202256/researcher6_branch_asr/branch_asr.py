import sys,itertools,random,math,json
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
sys.path.insert(0,'co-work-anl/scratch_extract_r5');import seven_checkpoint_review.independent_seat_assets as a
n=6
route=(0,0,0,0,1,0); K=125
D,A,B=a.setup(n); C=a.columns(n,route)
# base rows
base=a.descriptions(n,[0,5,3,4])
def base_row(I,J,d): return float(a.row(n,I,J,d,D,A,B))/D
# exact ASR row for (t,owner,H) where H seats top r-1 (list (j,k))
def asr(I,J,t,owner,H):
 r=n-t; den=6*r+1; pj=[route[:t].count(j) for j in range(7)]; pI=sum(pj[j] for j in range(7) if (I>>j)&1)
 q=F(0)
 for j in range(7):
  if (I>>j)&1:
   if I.bit_count()==1:q+=sum(F(1,pj[j]+k) for k in range(1,r+1))
   else:q+=r*F(1,pI+r)
 sub=sum(F(1,pj[j]+k) for j,k in H if (I>>j)&1)
 share=F(1,J.bit_count()) if J>>t&1 else F(0)
 return float(share-(q-sub)/den)
def g_row(I,J,t,h,l):
 r=n-t;pj=[route[:t].count(j) for j in range(7)];j,k=h;j2,k2=l
 return float(F(int(I>>j&1),pj[j]+k)-F(int(I>>j2&1),pj[j2]+k2))
def solve(Hs):
 rows=[]; names=[]
 for d in base: names.append(d);rows.append(np.array([base_row(*c,d) for c in C]))
 # add exact ASR one row per owner,t
 for t,H in enumerate(Hs):
  for owner in range(7): names.append(('ASR',t,owner));rows.append(np.array([asr(*c,t,owner,H) for c in C]))
 # add order constraints g>=0 as rows for H vs outside; include as nonneg slacks
 for t,H in enumerate(Hs):
  r=n-t; allh=[(j,k) for j in range(7) for k in range(1,r+1)]
  for h in H:
   for l in allh:
    if l in H: continue
    names.append(('ord',t,h,l));rows.append(np.array([g_row(*c,t,h,l) for c in C]))
 M=np.array(rows).T;b=np.array([float(bool(J))-0.5*float(bool(I&K)) for I,J in C])
 Aub=np.hstack([M,np.ones((len(C),1))]);c=np.r_[np.zeros(M.shape[1]),-1]
 res=linprog(c,A_ub=Aub,b_ub=b,bounds=[(0,None)]*M.shape[1]+[(None,None)],method='highs')
 return res

def topHs(s):
 Hs=[]
 for t in range(n):
  r=n-t;pj=[route[:t].count(j) for j in range(7)]; seats=[(s[j]/(pj[j]+k),j,k) for j in range(7) for k in range(1,r+1)]
  seats.sort(reverse=True); Hs.append([(j,k) for _,j,k in seats[:r-1]])
 return Hs
for z in range(100):
 s=[10**random.uniform(-2,2) for _ in range(7)]
 Hs=topHs(s);res=solve(Hs)
 print(z,res.status,res.x[-1] if res.success else None, Hs[0], flush=True)
 if res.success and res.x[-1]>0.0001: break
# no
