"""Exact literal-unit QA of FLOOR/NET/COPY/BUBBLE, not general HALF proof."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

def check_case(name,sets,m):
 sets=tuple(frozenset(s) for s in sets);k=len(sets);thresholds={}
 @lru_cache(None)
 def profits(z):
  counts={x:sum(x in sets[a] for a in z) for s in sets for x in s}
  return tuple(sum((F(1,counts[x]) for x in sets[a]),F(0)) for a in z)
 @lru_cache(None)
 def ends(h):
  if len(h)==m:return frozenset((h,))
  i=len(h);children=[ends(h+(a,)) for a in range(k)]
  floor=max(min(profits(z)[i] for z in c) for c in children)
  thresholds[h]=floor
  return frozenset(z for c in children for z in c if profits(z)[i]>=floor)
 roots=ends(())
 def net(i,z):
  u=profits(z)
  return u[i]-sum((u[j]-thresholds[z[:j]] for j in range(i+1,m)),F(0))
 def load_without(z,i):
  return {x:sum(x in sets[a] for j,a in enumerate(z) if j!=i) for s in sets for x in s}
 fc=cc=bc=0
 for d in range(m+1):
  for h in product(range(k),repeat=d):
   eh=ends(h)
   for tail in product(range(k),repeat=m-d):
    z=h+tail
    assert (z in eh)==all(profits(z)[j]>=thresholds[z[:j]] for j in range(d,m))
    fc+=1
 for i in range(m):
  for h in product(range(k),repeat=i):
   for a in range(k):
    for z in ends(h+(a,)):
     u=profits(z)
     for j in range(i+1,m):
      for zp in ends(z[:j]+(a,)):
       up=profits(zp)
       if u[j]<up[j] or (a==z[j] and zp!=z):continue
       assert up[i]==up[j]
       sd=lambda zz,uu:sum((uu[t]-thresholds[zz[:t]] for t in range(j+1,m)),F(0))
       rhs=u[j]-u[i]+sum((u[t]-up[t] for t in range(i+1,j)),F(0))+sd(z,u)-sd(zp,up)
       assert net(i,zp)-net(i,z)==rhs
       cc+=1
 for actual in roots:
  for i in range(m-1):
   h=actual[:i];bi=actual[i]
   for a in range(k):
    for z in ends(h+(a,bi)):
     w=h+(bi,a)+z[i+2:]
     assert w in ends(h+(bi,a))
     assert load_without(z,i)==load_without(w,i+1)
     assert profits(z)[i]==profits(w)[i+1]
     assert net(i,z)-net(i+1,w)==thresholds[h+(a,)]-profits(z)[i+1]
     bc+=1
 return dict(name=name,m=m,catalog=k,root_SPE_leaves=len(roots),floor_iff=fc,copy_net=cc,actual_prefix_bubble=bc)
if __name__=='__main__':
 cases=[('empty_m1',[set()],1),('zero_m3',[set()],3),('disjoint_3_2',[{0,1,2},{3,4}],2),('compact10',[set(range(6)),set(range(7)),set(range(6))|{7},{7,8,9}],3),('core_and_petals',[{0,1,2},{3},{4}],3)]
 r={'scope':'Finite exact implementation QA only, not HALF evidence','cases':[check_case(*c) for c in cases]}
 with Path(__file__).with_name('netcap_bubble_exact_audit.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
 print(json.dumps(r,indent=2))
