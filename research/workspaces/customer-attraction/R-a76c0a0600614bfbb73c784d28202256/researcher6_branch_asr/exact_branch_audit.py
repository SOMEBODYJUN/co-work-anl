import sys,random,json
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
from math import gcd
sys.path.insert(0,'co-work-anl/scratch_extract_r5'); import seven_checkpoint_review.independent_seat_assets as a
n=6; route=(0,0,0,0,1,0); K=125; D,A,B=a.setup(n); C=a.columns(n,route)
base=a.descriptions(n,[0,5,3,4])
def asr(I,J,t,owner,H):
 r=n-t; pj=[route[:t].count(j) for j in range(7)]; pI=sum(pj[j] for j in range(7) if (I>>j)&1)
 q=F(0)
 for j in range(7):
  if I>>j&1:
   q += sum(F(1,pj[j]+k) for k in range(1,r+1)) if I.bit_count()==1 else r*F(1,pI+r)
 sub=sum(F(1,pj[j]+k) for j,k in H if I>>j&1)
 sh=F(1,J.bit_count()) if J>>t&1 else F(0)
 return sh-(q-sub)/F(6*r+1)
def grow(I,t,h,l):
 pj=[route[:t].count(j) for j in range(7)];j,k=h;j2,k2=l
 return F(int(I>>j&1),pj[j]+k)-F(int(I>>j2&1),pj[j2]+k2)
def topHs(s):
 H=[]
 for t in range(n):
  r=n-t;pj=[route[:t].count(j) for j in range(7)]
  seats=sorted([(s[j]/(pj[j]+k),j,k) for j in range(7) for k in range(1,r+1)],reverse=True)
  H.append([(j,k) for _,j,k in seats[:r-1]])
 return H
random.seed(0); s=[10**random.uniform(-2,2) for _ in range(7)]; Hs=topHs(s)
names=[]; rows=[]
for d in base:names.append(('base',d));rows.append([F(a.row(n,I,J,d,D,A,B),D) for I,J in C])
for t,H in enumerate(Hs):
 for owner in range(7):names.append(('ASR',t,owner,H));rows.append([asr(I,J,t,owner,H) for I,J in C])
for t,H in enumerate(Hs):
 r=n-t;allh=[(j,k) for j in range(7) for k in range(1,r+1)]
 for h in H:
  for l in allh:
   if l not in H:names.append(('ORD',t,h,l));rows.append([grow(I,t,h,l) for I,J in C])
M=np.array([[float(v) for v in row] for row in rows]).T;b=np.array([float(bool(J))-0.5*float(bool(I&K)) for I,J in C])
res=linprog(np.r_[np.zeros(len(rows)),-1],A_ub=np.hstack([M,np.ones((len(C),1))]),b_ub=b,bounds=[(0,None)]*len(rows)+[(None,None)],method='highs')
assert res.success; x=res.x[:-1]; t=res.x[-1]
# rationalize all support; drop tiny
rx=[F(float(v)).limit_denominator(10**9) if v>1e-10 else F(0) for v in x]
# exact min residual and witness
mins=None; arg=None
for ci,(I,J) in enumerate(C):
 rr=F(int(bool(J)),1)-F(int(bool(I&K)),2)-sum(rx[q]*rows[q][ci] for q in range(len(rows)))
 if mins is None or rr<mins:mins=rr;arg=(I,J)
print(json.dumps({'status':str(res.status),'float_t':t,'exact_min':str(mins),'arg':arg,'rows':len(rows),'cols':len(C),'nz':sum(v>0 for v in rx),'Hs':Hs,'s':s},indent=2))
out={'route':route,'K':K,'Hs':Hs,'float_t':t,'exact_min':str(mins),'arg':arg,'rows':len(rows),'cols':len(C),'weights':[]}
for q,w in enumerate(rx):
 if w:out['weights'].append({'index':q,'name':str(names[q]),'weight':str(w)})
open('co-work-anl/scratch_extract_r5/exact_branch_audit.json','w').write(json.dumps(out,indent=2)+'\n')
