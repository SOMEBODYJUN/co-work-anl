import itertools, functools, numpy as np, random, json, time
from pathlib import Path

def counts(p,n):
 if p==1: yield (n,); return
 for i in range(n+1):
  for c in counts(p-1,n-i): yield (i,)+c
class Fast:
 def __init__(self,p,n):
  self.p,self.n=p,n; self.C=np.array(list(counts(p,n)),dtype=int); self.M=np.array([[bool(i&(1<<a)) for a in range(p)] for i in range(1,1<<p)],dtype=int)
  self.den=self.C@self.M.T; self.coefs=np.divide(self.M.T[None,:,:],self.den[:,None,:],out=np.zeros((len(self.C),p,len(self.M))),where=self.den[:,None,:]>0)
  self.cov=self.den>0
  self.ids={tuple(c):i for i,c in enumerate(self.C)}
 def run(self,w):
  U=self.coefs@w
  @functools.lru_cache(None)
  def R(k):
   if sum(k)==self.n:return np.array([self.ids[k]],dtype=int)
   ch=[R(k[:a]+(k[a]+1,)+k[a+1:]) for a in range(self.p)]
   th=max(U[x,a].min() for a,x in enumerate(ch))
   return np.unique(np.concatenate([x[U[x,a]>=th-1e-8] for a,x in enumerate(ch)]))
  root=R((0,)*self.p); opt=(self.cov@w).max()
  V=np.where(self.C[root]>0,U[root],np.inf)
  v=V.min(); at=np.unravel_index(V.argmin(),V.shape); c=self.C[root[at[0]]].tolist()
  return v*2*self.n/opt if opt else 1, v,opt,c
if __name__=='__main__':
 rng=np.random.default_rng(2277); best=2
 for p,n,total in [(5,3,3000),(6,3,3000),(6,4,2000),(7,4,1000),(7,5,500)]:
  f=Fast(p,n)
  for k in range(total):
   # sparse and disparate types
   w=rng.choice([0,0,0,0,1,1,2,4,8,16],len(f.M))
   if k%3==0: w=rng.integers(0,2,len(f.M))*rng.integers(0,31,len(f.M))
   ratio,v,opt,c=f.run(w)
   if ratio<best:
    best=ratio; print(p,n,k,best,v,opt,c,flush=True)
    Path(__file__).with_name('floor_best.json').write_text(json.dumps(dict(p=p,n=n,weights=w.tolist(),ratio=best,v=v,opt=int(opt),c=c)))
   if ratio<1-1e-7: print('FAIL',flush=True);raise SystemExit
 print('DONE',best)
