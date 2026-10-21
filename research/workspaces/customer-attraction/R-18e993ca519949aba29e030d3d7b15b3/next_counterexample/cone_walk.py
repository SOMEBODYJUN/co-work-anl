"""Boundary policy-cone walk, scouting only."""
import json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from cone_attack import ConeScout
class Walker(ConeScout):
 def constraints(self,t,path,R,F,u,rng):
  rows=[];done=set()
  def descend(q,t,suffix):
   if q not in self.children:return
   key=(q,t,suffix)
   if key in done:return
   done.add(key)
   adm=[a for a,c in enumerate(self.children[q]) if t in R[c] and u[a,t]>=F[q]-1e-7]
   a=suffix[0] if suffix else rng.choice(adm)
   for b,c in enumerate(self.children[q]):
    if b==a:tb=t
    else:
     options=R[c];mini=u[b,options].min();options=options[u[b,options]<=mini+1e-8];tb=int(rng.choice(options))
    rows.append(self.C[a,t]-self.C[b,tb])
    descend(c,tb,suffix[1:] if suffix and b==a else ())
  descend((0,)*self.n,t,path)
  return np.unique(np.round(np.array(rows),12),axis=0)
 def random_path(self,t,R,F,u,rng):
  q=(0,)*self.n;p=()
  for depth in range(self.m):
   adm=[a for a,c in enumerate(self.children[q]) if t in R[c] and u[a,t]>=F[q]-1e-7]
   a=int(rng.choice(adm));p+=(a,);q=self.children[q][a]
  return p

def main():
 n,m,steps=map(int,sys.argv[1:4]);mode=sys.argv[4] if len(sys.argv)>4 else 'half';s=Walker(n,m);rng=np.random.default_rng(518+n)
 parent=Path(__file__).parent;best=-1;start=time.time();eligible=np.where(s.masks.sum(axis=1)<=3)[0]
 for it in range(steps):
  if it%15==0:
   w=np.zeros((1<<n)-1);ch=rng.choice(eligible,size=rng.integers(n,min(len(eligible)+1,3*n)),replace=False);w[ch]=rng.integers(1,100,len(ch))
  u,W,R,F=s.policy(w);out=R[(0,)*n]
  if mode=='half':
   low=W[out].min();options=out[W[out]<=low+1e-8];t=int(rng.choice(options));comp=int(np.argmax(W));path=s.random_path(t,R,F,u,rng);obj=s.W[comp]
  else:
   choices=[]
   for t1 in out:
    p1=s.path(int(t1),R,F,u);i=min(range(m-1),key=lambda i:u[p1[i],t1]);choices.append(((.5*u[p1[-1],t1]-u[p1[i],t1])/max(W[t1],1e-12),int(t1),p1,i))
   _,t,path,i=max(choices);obj=.5*s.C[path[-1],t]-s.C[path[i],t];comp=None
  rows=s.constraints(t,path,R,F,u,rng)
  sol=linprog(-obj,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=s.W[t:t+1],b_eq=[1],bounds=(0,None),method='highs')
  if not sol.success:print('FAIL',it,sol.message,flush=True);continue
  score=-sol.fun
  if score>best+1e-7:
   best=score;rec={'n':n,'m':m,'iteration':it,'objective':score,'mode':mode,'path':path,'comp':comp,'seed_weights':w.tolist(),'lp_weights':sol.x.tolist(),'rows':len(rows)}
   (parent/f'walk_{mode}_best_{n}_{m}.json').write_text(json.dumps(rec,indent=2));print({k:v for k,v in rec.items() if 'weights' not in k},flush=True)
  w=np.maximum(sol.x,0)
  if it%10==0:print('progress',it,'elapsed',time.time()-start,flush=True)
  if score>(2.00001 if mode=='half' else 1e-5):break
if __name__=='__main__':main()
