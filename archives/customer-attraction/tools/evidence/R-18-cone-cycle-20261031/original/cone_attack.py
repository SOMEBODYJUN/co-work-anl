"""Complete policy cone LP scouting; integer + exact independent audit mandatory."""
import itertools,json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from search_terminal import Scout
class ConeScout(Scout):
 def policy(self,w):
  u=self.C@w;W=self.W@w
  R={q:np.array([self.tidx[q]],dtype=int) for q in self.terms};F={}
  for q in reversed(self.states):
   if q not in self.children:continue
   ch=[R[c] for c in self.children[q]]
   f=max(u[a,r].min() for a,r in enumerate(ch));F[q]=f
   R[q]=np.unique(np.concatenate([r[u[a,r]>=f-1e-7] for a,r in enumerate(ch)]))
  return u,W,R,F
 def path(self,t,R,F,u):
  root=(0,)*self.n;targets={root:(float('inf'),())};best=None
  for depth in range(self.m):
   nxt={}
   for q,(v,path) in targets.items():
    for a,c in enumerate(self.children[q]):
     if u[a,t]+1e-7<F[q] or t not in R[c]:continue
     p=path+(a,)
     if depth==self.m-1:
      score=.5*u[a,t]-v
      if best is None or score>best[0]:best=(score,p)
     else:
      v1=min(v,u[a,t])
      if c not in nxt or v1<nxt[c][0]:nxt[c]=(v1,p)
   targets=nxt
  return best[1]
 def constraints(self,t,path,R,F,u):
  rows=[];done=set();actions={}
  def descend(q,t,suffix):
   if q not in self.children:return
   key=(q,t,suffix)
   if key in done:return
   done.add(key)
   adm=[a for a,c in enumerate(self.children[q]) if t in R[c] and u[a,t]>=F[q]-1e-7]
   a=suffix[0] if suffix else adm[0]
   for b,c in enumerate(self.children[q]):
    if b==a:tb=t
    else:
     options=R[c];tb=int(options[np.argmin(u[b,options])])
    rows.append(self.C[a,t]-self.C[b,tb])
    descend(c,tb,suffix[1:] if suffix and b==a else ())
  descend((0,)*self.n,t,path)
  return np.unique(np.round(np.array(rows),12),axis=0)
def main():
 n,m,steps=map(int,sys.argv[1:]);s=ConeScout(n,m);rng=np.random.default_rng(612+n)
 parent=Path(__file__).parent;best=-1;start=time.time()
 eligible=np.where(s.masks.sum(axis=1)<=3)[0]
 for it in range(steps):
  w=np.zeros((1<<n)-1);ch=rng.choice(eligible,size=rng.integers(n,min(len(eligible)+1,4*n)),replace=False);w[ch]=rng.integers(1,100,len(ch))
  u,W,R,F=s.policy(w);t=int(rng.choice(R[(0,)*n]));path=s.path(t,R,F,u)
  rows=s.constraints(t,path,R,F,u)
  results=[]
  for i in range(m-1):
   obj=.5*s.C[path[-1],t]-s.C[path[i],t]
   sol=linprog(-obj,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=s.W[t:t+1],b_eq=[1],bounds=(0,None),method='highs')
   if sol.success:results.append((-sol.fun,i,sol))
  if not results:continue
  _,i,sol=max(results,key=lambda r:r[0])
  if not sol.success:print('FAIL',it,sol.message,flush=True);continue
  score=-sol.fun
  if score>best+1e-8:
   best=score;rec={'n':n,'m':m,'iteration':it,'objective':score,'path':path,'early_index':i,'seed_weights':w.tolist(),'lp_weights':sol.x.tolist(),'rows':len(rows)}
   (parent/f'cone_best_{n}_{m}.json').write_text(json.dumps(rec,indent=2));print({k:v for k,v in rec.items() if 'weights' not in k},flush=True)
  if it%10==0:print('progress',it,'elapsed',time.time()-start,flush=True)
  if score>1e-7:break
if __name__=='__main__':main()
