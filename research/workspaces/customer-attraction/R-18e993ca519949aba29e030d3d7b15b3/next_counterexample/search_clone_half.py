import json,sys,time
from pathlib import Path
import numpy as np
from search_terminal import Scout
class CloneScout(Scout):
 def run(self,w):
  u=self.C@w;W=self.W@w
  R={q:np.array([self.tidx[q]],dtype=int) for q in self.terms};floors={}
  for q in reversed(self.states):
   if q not in self.children:continue
   child=[R[c] for c in self.children[q]]
   floor=max(u[a,r].min() for a,r in enumerate(child));floors[q]=floor
   R[q]=np.unique(np.concatenate([r[u[a,r]>=floor-1e-7] for a,r in enumerate(child)]))
  root=(0,)*self.n;outs=R[root];best=None
  for t in outs:
   targets={root:(float('inf'),())}
   for depth in range(self.m):
    nxt={}
    for q,(v,path) in targets.items():
     for a,c in enumerate(self.children[q]):
      if u[a,t]+1e-7<floors[q] or t not in R[c]:continue
      p=path+(a,)
      if depth==self.m-1:
       ratio=u[a,t]/(2*v) if v else 0
       if best is None or ratio>best[0]:best=(ratio,p,int(t))
      else:
       v1=min(v,u[a,t])
       if c not in nxt or v1<nxt[c][0]:nxt[c]=(v1,p)
    targets=nxt
  return best,float(W.max()/W[outs].min()) if W[outs].min() else 1,u,W

def main():
 n,m,steps=map(int,sys.argv[1:]);s=CloneScout(n,m);rng=np.random.default_rng(737+n)
 best=0;besthalf=0;parent=Path(__file__).parent;start=time.time();save=None
 eligible=np.where((s.masks.sum(axis=1)<=3))[0]
 for it in range(steps):
  if it%7==0:
   w=np.zeros((1<<n)-1,dtype=int);chosen=rng.choice(eligible,size=rng.integers(n,min(len(eligible)+1,4*n)),replace=False);w[chosen]=rng.integers(0,100,len(chosen))
  elif best and it%7<6:
   w=save.copy();j=rng.choice(eligible);w[j]=max(0,w[j]+rng.integers(-40,41))
  else:w=rng.integers(0,12,size=(1<<n)-1)
  b,half,u,W=s.run(w)
  if b[0]>best+1e-8:
   best=b[0];save=w.copy();rec={'n':n,'m':m,'iteration':it,'bridge_violation_ratio':best,'half_ratio':half,'path':b[1],'weights':w.tolist()}
   (parent/f'clone_best_{n}_{m}.json').write_text(json.dumps(rec,indent=2));print(json.dumps({k:v for k,v in rec.items() if k!='weights'}),flush=True)
  if half>besthalf:besthalf=half
  if it%1000==0:print('progress',it,'best half',besthalf,'elapsed',time.time()-start,flush=True)
if __name__=='__main__':main()
