"""Float scouting only: every candidate requires ExactSPESolver certification."""
import itertools, json, math, sys, time
from pathlib import Path
import numpy as np

def counts(n,m):
 if n==1:return [(m,)]
 return [(i,)+r for i in range(m+1) for r in counts(n-1,m-i)]
class Scout:
 def __init__(self,n,m):
  self.n,self.m=n,m
  self.terms=counts(n,m);self.tidx={q:i for i,q in enumerate(self.terms)}
  self.masks=np.array([[(m>>a)&1 for a in range(n)] for m in range(1,1<<n)],dtype=float)
  self.loads=np.array(self.terms)@self.masks.T
  self.C=np.array([np.divide(self.masks[:,a],self.loads,out=np.zeros_like(self.loads),where=self.loads>0) for a in range(n)])
  self.W=(self.loads>0).astype(float)
  self.states=[q for s in range(m+1) for q in counts(n,s)]
  self.children={q:[q[:a]+(q[a]+1,)+q[a+1:] for a in range(n)] for q in self.states if sum(q)<m}
 def run(self,w):
  u=self.C@w;W=self.W@w
  R={q:np.array([self.tidx[q]],dtype=int) for q in self.terms};floors={}
  for q in reversed(self.states):
   if q not in self.children:continue
   child=[R[c] for c in self.children[q]]
   floor=max(u[a,r].min() for a,r in enumerate(child));floors[q]=floor
   R[q]=np.unique(np.concatenate([r[u[a,r]>=floor-1e-7] for a,r in enumerate(child)]))
  root=(0,)*self.n;outs=R[root]
  best=None
  for t in outs:
   targets={root:()}
   for depth in range(self.m):
    nxt={}
    for q,path in targets.items():
     for a,c in enumerate(self.children[q]):
      if u[a,t]+1e-7<floors[q] or t not in R[c]:continue
      p=path+(a,)
      if depth==self.m-1:
       ratio=(self.m+1)*u[a,t]/(2*W[t]) if W[t] else 0
       if best is None or ratio>best[0]:best=(ratio,p,int(t))
      else:nxt[c]=p
    targets=nxt
  return best,float(W.max()/W[outs].min()) if W[outs].min() else 1,u,W

def main():
 n,m,steps=map(int,sys.argv[1:]);s=Scout(n,m);rng=np.random.default_rng(223)
 best=0;besthalf=0;parent=Path(__file__).parent;start=time.time()
 for it in range(steps):
  if it%5==0:w=rng.integers(0,80,size=(1<<n)-1)*(rng.random((1<<n)-1)<rng.uniform(.07,.5))
  elif best and it%5<4:
   w=save.copy();j=rng.integers(len(w));w[j]=max(0,w[j]+rng.integers(-30,31))
  else:w=rng.integers(0,12,size=(1<<n)-1)
  b,half,u,W=s.run(w)
  if b[0]>best+1e-8:
   best=b[0];save=w.copy();rec={'n':n,'m':m,'iteration':it,'bridge_violation_ratio':best,'half_ratio':half,'path':b[1],'weights':w.tolist()}
   (parent/f'terminal_best_{n}_{m}.json').write_text(json.dumps(rec,indent=2));print(json.dumps({k:v for k,v in rec.items() if k!='weights'}),flush=True)
  if half>besthalf:besthalf=half
  if it%100==0:print('progress',it,'best half',besthalf,'elapsed',time.time()-start,flush=True)
if __name__=='__main__':main()
