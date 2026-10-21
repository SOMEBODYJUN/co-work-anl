"""Exact finite model interface for the mean-deviation relaxation (floating search only).
A continuation SET is cached by counts; choices remain independent at ordered histories.
This is a weaker object than SPE and cannot produce a target counterexample.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import random,json,sys
import numpy as np

def solve(p,n,r,J):
 masks=np.arange(1,1<<p)
 mem=np.array([[(b>>a)&1 for a in range(p)] for b in masks],float)
 @lru_cache(None)
 def utility(q):
  loads=mem@np.asarray(q)
  return mem.T@(np.asarray(r)/np.where(loads>0,loads,1))
 @lru_cache(None)
 def welfare(q):return sum(r[b-1] for b in masks if any(q[a] and b&(1<<a) for a in range(p)))
 @lru_cache(None)
 def rec(q):
  if sum(q)==n:return (q,)
  children=[]
  for a in range(p):
   qq=list(q);qq[a]+=1;children.append(rec(tuple(qq)))
  minima={b:min(utility(t)[b] for t in children[b]) for b in J}
  sm=sum(minima.values());out=set()
  for a in range(p):
   rhs=sm-(minima[a] if a in J else 0);factor=len(J)-(a in J)
   for t in children[a]:
    if factor*utility(t)[a]+1e-8>=rhs:out.add(t)
  assert out
  return tuple(out)
 F=rec((0,)*p);worst=min(F,key=welfare);O=sum(r[b-1] for b in masks if any(b&(1<<a) for a in J))
 return O/welfare(worst) if welfare(worst) else 0,worst,O,welfare(worst),len(F),rec.cache_info().currsize

rng=random.Random(230710);best=0;winner=None
for p,n,N in [(5,4,100),(6,5,200),(7,5,100),(7,6,100),(8,6,60)]:
 for trial in range(N):
  # Variety of sparse nonnegative integer populations.
  r=[0]*(2**p-1)
  for _ in range(rng.randrange(p,5*p)):
   b=rng.randrange(1,2**p);r[b-1]+=rng.randrange(1,10)
  J=tuple(range(min(n,p)))
  ratio,q,O,W,nF,states=solve(p,n,r,J)
  if ratio>best+1e-8:
   best=ratio;winner={'p':p,'n':n,'J':J,'r':r,'ratio':ratio,'q':q,'OPT':int(O),'W':int(W),'outcomes':nF,'states':states}
   print(p,n,trial,ratio,q,O,W,nF,states,flush=True)
  if ratio>2.000001:break
 if best>2.000001:break
Path(__file__).with_name('mean_reply_search.json').write_text(json.dumps({'scope':'finite mean-deviation relaxation, not SPE','best':winner},indent=2))
