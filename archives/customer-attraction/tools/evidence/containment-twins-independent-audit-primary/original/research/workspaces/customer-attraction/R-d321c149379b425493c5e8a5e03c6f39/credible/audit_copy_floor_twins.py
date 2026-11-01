"""Independent Fraction implementation of first-contained-follower DP on twins."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json


def compositions(n,p):
 if p==0:
  if n==0:yield ()
 elif p==1:yield(n,)
 else:
  for z in range(n+1):
   for tail in compositions(n-z,p-1):yield(z,)+tail


def audit(m,K):
 p=2*m
 def ext(b,t,q):
  j=t//2
  core=F(K,1+b[2*j]+b[2*j+1]+q[2*j]+q[2*j+1])
  private=F(1,1+b[t]+q[t])
  return core+private
 def counts(n,allowed):
  for small in compositions(n,len(allowed)):
   q=[0]*p
   for a,z in zip(allowed,small):q[a]=z
   yield tuple(q)
 @lru_cache(None)
 def floor(b,r):
  choices=[]
  for t in range(p):
   noncontained=[a for a in range(p)if a!=t]
   options=[ext(b,t,q)for q in counts(r-1,noncontained)]
   for ell in range(1,r):
    for q in counts(ell-1,noncontained):
     bp=tuple(b[a]+q[a]+(a==t)for a in range(p))
     options.append(floor(bp,r-ell))
   choices.append(min(options))
  return max(choices)
 @lru_cache(None)
 def pathcost(b,r):
  if not r:return F()
  return floor(b,r)+min(pathcost(tuple(b[a]+(a==t)for a in range(p)),r-1)for t in range(p))
 checked=0
 for depth in range(m):
  r=m-depth
  H=sum((F(1,j)for j in range(1,r+1)),F())
  for b in compositions(depth,p):
   assert floor(b,r)==F(K,r)+1,(m,K,b,r,floor(b,r))
   assert pathcost(b,r)==K*H+r
   checked+=1
 # Independently enumerate m chosen themes. All groups one each reach the upper.
 optimal=m*(K+1)
 cover_values=[]
 for q in compositions(m,p):
  cover_values.append(sum(K*int(q[2*j]+q[2*j+1]>0)+int(q[2*j]>0)+int(q[2*j+1]>0)for j in range(m)))
 assert max(cover_values)==optimal
 return {'m':m,'K':K,'legal_prefixes':checked,'floor_formula_verified':True,'G':str(pathcost((0,)*p,m)),'OPT':optimal}

if __name__=='__main__':
 cases=[audit(m,K)for m in range(1,5)for K in (1,3)]
 H5=sum((F(1,j)for j in range(1,6)),F())
 G=12*H5+5;OPT=5*13
 assert G==F(162,5)and G<F(OPT,2)
 out={'scope':'finite exact audit of independently proved DP obstruction; not a SPE counterexample','cases':cases,'first_small_explicit_violation':{'m':5,'K':12,'G':str(G),'OPT':OPT,'half_gap':str(F(OPT,2)-G)}}
 dest=Path(__file__).with_name('audit_copy_floor_twins.json');dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
