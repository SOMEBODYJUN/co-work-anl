"""One-cone attack on the universal PURE self-consistent query shortcut.

Discovery only. The exact witness, if any, is checked independently below.
No input scanning: the single 43-node policy is fixed throughout.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp, linprog

M,K=3,6
MASKS=list(range(1,1<<K))
def action(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    return next(a for a in (range(3) if h[1]<3 else range(3,6)) if a not in h)
def finish(h):
    while len(h)<M:h+=(action(h),)
    return h
def unit(z,i,s):
    return F((s>>z[i])&1, sum((s>>a)&1 for a in z)) if (s>>z[i])&1 else F(0)
IC=[]
for d in range(M):
 for h in product(range(K),repeat=d):
  y=finish(h)
  for a in range(K):
   if a!=action(h):IC.append([unit(y,d,s)-unit(finish(h+(a,)),d,s) for s in MASKS])
z=finish(())
G=[]
for a in range(K):
 row=[]
 for b in range(K):
  coeff=[]
  for s in MASKS:
   mu=sum(sum((s>>v)&1 for j,v in enumerate(finish(z[:i]+(a,))) if j!=i) for i in range(M))
   coeff.append(F(3,3+mu) if (s>>b)&1 else F(0))
  row.append(coeff)
 G.append(row)
PAIRS=[(a,b) for a in range(K) for b in range(K) if a!=b]
n=len(MASKS);eps=n;start=n+1;nv=start+len(PAIRS)
rows=[];lo=[];hi=[]
for ic in IC:
 rows.append(list(map(float,ic))+[0.]*(nv-n));lo.append(0);hi.append(np.inf)
for j,(a,b) in enumerate(PAIRS):
 r=np.zeros(nv);r[:n]=[float(v-u) for u,v in zip(G[a][a],G[a][b])];r[eps]=-1;r[start+j]=-2
 rows.append(r);lo.append(-2);hi.append(np.inf)
for a in range(K):
 r=np.zeros(nv)
 for j,(aa,b) in enumerate(PAIRS):
  if aa==a:r[start+j]=1
 rows.append(r);lo.append(1);hi.append(np.inf)
r=np.zeros(nv);r[:n]=1;rows.append(r);lo.append(1);hi.append(1)
c=np.zeros(nv);c[eps]=-1
res=milp(c,integrality=np.r_[np.zeros(start),np.ones(len(PAIRS))],
 bounds=Bounds(np.zeros(nv),np.r_[np.full(start,np.inf),np.ones(len(PAIRS))]),
 constraints=LinearConstraint(np.array(rows),np.array(lo),np.array(hi)),
 options={"time_limit":90,"mip_rel_gap":1e-8})
out={"fixed_policy":"six_topic_group_policy", "milp_status":int(res.status),"message":res.message}
if res.x is not None:
 out["milp_margin"]=float(res.x[eps])
 counts=res.x[:n]
 challengers=[]
 for a in range(K):
  bs=[b for b in range(K) if b!=a]
  challengers.append(max(bs,key=lambda b:sum(float(v-u)*w for u,v,w in zip(G[a][a],G[a][b],counts))))
 # Fix the discovered six challengers, then extract a basic LP point.
 aub=[[-float(v) for v in ic]+[0.] for ic in IC]
 for a,b in enumerate(challengers):aub.append([float(u-v) for u,v in zip(G[a][a],G[a][b])]+[1.])
 c2=np.zeros(n+1);c2[-1]=-1
 rr=linprog(c2,A_ub=aub,b_ub=np.zeros(len(aub)),A_eq=[np.r_[np.ones(n),0]],b_eq=[1],bounds=[(0,None)]*(n+1),method="highs")
 out["challengers"]=challengers
 if rr.success:
  # Recover the exact basic point from its active rational equations.
  support=[j for j,t in enumerate(rr.x[:n]) if t>1e-8]
  eqrows=[[F(1) for _ in support]+[F(0)]];eqrhs=[F(1)]
  for ic in IC:
   if abs(sum(float(v)*t for v,t in zip(ic,rr.x[:n])))<1e-7:
    eqrows.append([ic[j] for j in support]+[F(0)]);eqrhs.append(F(0))
  for a,b in enumerate(challengers):
   diff=[v-u for u,v in zip(G[a][a],G[a][b])]
   if abs(sum(float(v)*t for v,t in zip(diff,rr.x[:n]))-rr.x[-1])<1e-7:
    eqrows.append([diff[j] for j in support]+[F(-1)]);eqrhs.append(F(0))
  basis={};dim=len(support)+1
  for vals,rhs in zip(eqrows,eqrhs):
   row=vals+[rhs]
   for pivot in sorted(basis):
    if row[pivot]:
     mul=row[pivot];row=[x-mul*y for x,y in zip(row,basis[pivot])]
   pivot=next((j for j in range(dim) if row[j]),None)
   if pivot is not None:
    mul=row[pivot];basis[pivot]=[x/mul for x in row]
   if len(basis)==dim:break
  assert len(basis)==dim
  sol=[F(0)]*dim
  for pivot in sorted(basis,reverse=True):
   sol[pivot]=basis[pivot][-1]-sum(basis[pivot][j]*sol[j] for j in range(pivot+1,dim))
  ww=[F(0) for _ in MASKS]
  for j,v in zip(support,sol[:-1]):ww[j]=v
  scale=np.lcm.reduce([v.denominator for v in ww]) if False else 1
  # Fraction arithmetic reports whether rationalization is itself a proof.
  mingap=min(sum(a*w for a,w in zip(ic,ww)) for ic in IC)
  gaps=[sum((v-u)*w for u,v,w in zip(G[a][a],G[a][b],ww)) for a,b in enumerate(challengers)]
  from math import lcm,gcd
  den=lcm(*(v.denominator for v in ww));ints=[int(v*den) for v in ww]
  divisor=gcd(*ints);ints=[v//divisor for v in ints]
  out.update({"rational_ic_min":str(mingap),"rational_query_gaps":list(map(str,gaps)),
              "integer_counts":{str(s):w for s,w in zip(MASKS,ints) if w},
              "rationalization_exactly_verified":mingap>=0 and min(gaps)>0})
# Readability reduction of the SAME six-challenger certificate. This is not a
# second policy or a scan. Exact integer-scaled constraints admit tiny margins.
if out.get("rationalization_exactly_verified"):
 from math import lcm
 crows=[];clo=[]
 for ic in IC:
  den=lcm(*(v.denominator for v in ic));crows.append([int(v*den) for v in ic]);clo.append(0)
 for a,b in enumerate(out["challengers"]):
  diff=[v-u for u,v in zip(G[a][a],G[a][b])]
  den=lcm(*(v.denominator for v in diff));crows.append([int(v*den) for v in diff]);clo.append(1)
 small=milp(np.ones(n),integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.full(n,np.inf)),
            constraints=LinearConstraint(np.array(crows,dtype=float),np.array(clo,dtype=float),np.full(len(clo),np.inf)),
            options={"time_limit":90,"mip_rel_gap":0.})
 if small.x is not None:
  ints=[int(round(v)) for v in small.x]
  icmin=min(sum(v*w for v,w in zip(ic,ints)) for ic in IC)
  gaps=[sum((v-u)*w for u,v,w in zip(G[a][a],G[a][b],ints)) for a,b in enumerate(out["challengers"])]
  out["small_certificate"]={"counts":{str(s):w for s,w in zip(MASKS,ints) if w},"total_clients":sum(ints),
      "exact_ic_min":str(icmin),"exact_query_gaps":list(map(str,gaps)),
      "verified":icmin>=0 and min(gaps)>0,"optimization_status":int(small.status),"optimization_message":small.message}
print(json.dumps(out,indent=2))
