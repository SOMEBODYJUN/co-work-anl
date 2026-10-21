"""Finite floating discovery search, not an exact certificate/proof."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from itertools import combinations_with_replacement
import json,time,sys
from pathlib import Path

class Search:
 def __init__(self,n,p):
  self.n=n;self.p=p;self.masks=np.arange(1,1<<p)
  self.inc=((self.masks[:,None]>>np.arange(p))&1)
  self.levels=[]; self.maps=[]
  for r in range(n+1):
   cs=[]
   for z in combinations_with_replacement(range(p),r):cs.append(tuple(np.bincount(z,minlength=p)))
   self.levels.append(cs);self.maps.append({c:i for i,c in enumerate(cs)})
  self.children=[]
  for r in range(n):
   ch=[]
   for c in self.levels[r]:
    ch.append([self.maps[r+1][tuple(v+int(a==j) for j,v in enumerate(c))] for a in range(p)])
   self.children.append(ch)
  self.loads=np.array(self.levels[n])@self.inc.T
  self.cov=(self.loads>0).astype(float)
  self.coef=np.divide(self.inc.T[None,:,:],self.loads[:,None,:],out=np.zeros((len(self.loads),p,len(self.masks))),where=self.loads[:,None,:]>0)
  den=1+(n-1)/n*self.loads
  self.obj=np.array([n*self.inc[:,a][None,:]/den-self.cov-self.cov/den for a in range(p)])
 def evaluate(self,w):
  U=self.coef@w
  outcomes=[np.array([i]) for i in range(len(self.loads))]
  for r in range(self.n-1,-1,-1):
   nxt=[]
   for ch in self.children[r]:
    sets=[outcomes[j] for j in ch]
    floor=max(np.min(U[s,a]) for a,s in enumerate(sets))
    nxt.append(np.unique(np.concatenate([s[U[s,a]>=floor-1e-9] for a,s in enumerate(sets)])))
   outcomes=nxt
  outs=outcomes[0]
  vals=(self.obj[:,outs,:]@w)
  if '--individual' in sys.argv:
   for j,t in enumerate(outs):
    vals[:,j]+=(self.cov[t]@w)-self.n*min(U[t,a] for a,c in enumerate(self.levels[self.n][t]) if c)
  ai,ti=np.unravel_index(np.argmax(vals),vals.shape)
  term=int(outs[ti]);W=self.cov[term]@w
  return float(vals[ai,ti]/max(W,1e-9)),ai,term,W

if __name__=='__main__':
 n=int(sys.argv[1]) if len(sys.argv)>1 else 5
 p=int(sys.argv[2]) if len(sys.argv)>2 else 7
 runs=int(sys.argv[3]) if len(sys.argv)>3 else 1000
 rng=np.random.default_rng(275578095)
 s=Search(n,p);best=(-1,None);start=time.time()
 for i in range(runs):
  if i%4==0 or best[1] is None:
   w=rng.exponential(1,len(s.masks))*(rng.random(len(s.masks))<rng.uniform(.05,.7))
  else:
   w=best[1].copy()
   edits=rng.choice(len(w),size=rng.integers(1,10),replace=False)
   w[edits]*=np.exp(rng.normal(0,.7,len(edits)))
   if rng.random()<.25:w[edits]=rng.exponential(1,len(edits))
  if not w.sum():continue
  w/=w.sum()
  val,a,t,W=s.evaluate(w)
  if val>best[0]+1e-10:
   best=(val,w.copy());data={'n':n,'p':p,'iteration':i,'normalized_gap':val,'query':int(a),'terminal':list(map(int,s.levels[n][t])),'W':float(W),'weights':[(int(mask),float(x)) for mask,x in zip(s.masks,w) if x>0]}
   Path(__file__).with_name(f'random_refined_n{n}p{p}{"_individual" if "--individual" in sys.argv else ""}.json').write_text(json.dumps(data,indent=2)+'\n')
   print(i,round(val,9),'query',a,'term',s.levels[n][t],'elapsed',round(time.time()-start,1),flush=True)
 print('END',best[0],time.time()-start,flush=True)
