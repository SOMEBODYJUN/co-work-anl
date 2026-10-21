"""Floating fixed-policy/full-type cone attack of first-two security for arbitrary group sizes."""
from pathlib import Path
from itertools import product,combinations_with_replacement
import json,argparse,time
import numpy as np
from scipy.optimize import linprog

def attack(t,starts,seed):
 k=2*t;n=3;d=(1<<k)-1;rng=np.random.default_rng(seed)
 masks=np.arange(1,1<<k);M=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
 actions={():0}
 for a in range(k):
  actions[a,]=t if a<t else 0
  for b in range(k):actions[a,b]=next(c for c in (range(t) if b<t else range(t,k)) if c not in (a,b))
 def terminal(h):
  while len(h)<n:h=h+(actions[h],)
  return h
 def rho(a,h):return M[a]/np.maximum(M[list(h)].sum(axis=0),1)
 G=[]
 for h,a in actions.items():
  z=terminal(h)
  for b in range(k):
   if b!=a:G.append(rho(a,z)-rho(b,terminal(h+(b,))))
 G=np.unique(np.array(G),axis=0)
 bs=list(combinations_with_replacement(range(k),n-1));nb=len(bs)
 static=np.array([M/(1+M[list(bg)].sum(axis=0)) for bg in bs])
 root=terminal(());budget=rho(root[0],root)+rho(root[1],root)
 out={'scope':'floating fixed full-history strategy cone; not universal proof','t':t,'k':k,'positive':False,'max_gap':0.,'root':root,'starts':starts,'seed':seed}
 began=time.time()
 for rep in range(starts):
  p=np.ones(k)/k if rep==0 else rng.dirichlet(np.ones(k)*(.2 if rep%2 else 1))
  for it in range(10):
   beta=np.einsum('a,bat->bt',p,static)
   ans=linprog(np.r_[budget,-2],A_ub=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[-beta,np.ones(nb)]]),b_ub=np.zeros(len(G)+nb),A_eq=[np.r_[np.ones(d),0]],b_eq=[1.],bounds=(0,None),method='highs')
   if not ans.success:raise RuntimeError(ans.message)
   gap=-float(ans.fun)
   if gap>out['max_gap']+1e-9:
    out.update(max_gap=gap,positive=gap>1e-7,w=ans.x[:-1].tolist(),p=p.tolist(),t_lower=float(ans.x[-1]),pair=float(budget@ans.x[:-1]),start=rep,iteration=it)
    print(json.dumps({x:out[x] for x in ['t','max_gap','positive','start','iteration']}),flush=True)
   mat=np.einsum('bat,t->ba',static,ans.x[:-1]);sr=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-mat,np.ones(nb)],b_ub=np.zeros(nb),A_eq=[np.r_[np.ones(k),0]],b_eq=[1.],bounds=(0,None),method='highs')
   if max(abs(sr.x[:-1]-p))<1e-9:break
   p=sr.x[:-1]
  if out['positive']:break
 out.update(completed=rep+1,seconds=time.time()-began)
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--group',type=int,default=4);ap.add_argument('--starts',type=int,default=100);ap.add_argument('--seed',type=int,default=9013);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();o=attack(a.group,a.starts,a.seed);a.output.write_text(json.dumps(o,indent=2)+'\n');print({k:v for k,v in o.items() if k not in ('w','p')})
