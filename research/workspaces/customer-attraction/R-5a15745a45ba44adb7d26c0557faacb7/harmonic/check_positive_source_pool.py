"""Exact definition-level verification of the all-depth shared source pool.
This tests a universal algebraic lemma; finite checks are not its proof.
"""
from fractions import Fraction as F
from random import Random
import json
rng=Random(20261024)
checked=0
for m in range(1,13):
 for run in range(150):
  n=rng.randrange(14)
  B=[{x for x in range(n) if rng.randrange(2)} for _ in range(m)]
  c=[sum(x in S for S in B) for x in range(n)]
  pB=[sum((F(1,c[x]) for x in S),F()) for S in B]
  branches=[]
  for k in range(rng.randrange(1,12)):
   i=rng.randrange(m)
   W=B[:i]+[{x for x in range(n) if rng.randrange(2)} for _ in range(m-i)]
   d=[sum(x in S for S in W) for x in range(n)]
   pW=[sum((F(1,d[x]) for x in W[j]),F()) for j in range(m)]
   q={}; e={}
   for j in range(i):
    R={x:sum(x in B[l] and x not in W[l] for l in range(i,m)) for x in B[j]}
    q[j]=[sum((F(1,c[x]*d[x]) for x in B[j] & (B[l]-W[l])),F()) for l in range(i,m)]
    e[j]=sum((F(c[x]-R[x],c[x]*d[x]) for x in B[j]),F())
    assert sum(q[j],F())+e[j]==pW[j]
    assert sum(q[j],F())<=F(m-i,m-i+1)*pW[j]
    added=sum((F(sum(x in W[l] and x not in B[l] for l in range(i,m)),c[x]*d[x]) for x in B[j]),F())
    assert sum(q[j],F())==pW[j]-pB[j]+added
   branches.append((i,pW,q,e))
  lam={}
  for j in range(m):
   eligible=[k for k,(i,pW,q,e) in enumerate(branches) if j<i]
   raw={k:F(rng.randrange(8),rng.randrange(1,8)) for k in eligible}
   spent=sum((raw[k]*branches[k][1][j] for k in eligible),F())
   scale=min(F(1),pB[j]/spent) if spent else F(1)
   for k in eligible:lam[k,j]=scale*raw[k]
  Q=sum((lam[k,j]*sum(q[j],F()) for k,(i,pW,q,e) in enumerate(branches) for j in range(i)),F())
  E=sum((lam[k,j]*e[j] for k,(i,pW,q,e) in enumerate(branches) for j in range(i)),F())
  W=sum(pB,F()); last=pB[-1]
  pos=sum((F(m-j-1,m-j)*pB[j] for j in range(m-1)),F())
  assert Q+E<=W-last
  assert Q<=pos<=F(m-1,m)*(W-last)<=W
  checked+=1
for r in range(1,25):
 assert sum((F(1,(r+1)*1) for _ in range(r)),F())==F(r,r+1)
print(json.dumps({'status':'PASS','random_legal_leaf_instances':checked,'exact_arithmetic':'Fraction','local_sharpness_r':24,'scope':'definition-level finite verification; proof remains in markdown'}))
