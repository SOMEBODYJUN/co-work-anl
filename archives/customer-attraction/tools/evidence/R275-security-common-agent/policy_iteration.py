"""Floating policy-cone exploration of refined bridge (no universal proof)."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from scipy.optimize import linprog
import json,sys,time
from pathlib import Path
from random_refined_scan import Search

def policy(s,w,rng):
 U=s.coef@w
 terms=np.arange(len(s.loads));pol=[];allterms=[None]*(s.n+1);allterms[s.n]=terms
 for r in range(s.n-1,-1,-1):
  choices=[];t=[]
  for ch in s.children[r]:
   scores=np.array([U[terms[j],a] for a,j in enumerate(ch)])
   best=np.flatnonzero(scores>=max(scores)-1e-10)
   a=int(rng.choice(best));choices.append(a);t.append(terms[ch[a]])
  pol.append(choices);terms=np.array(t);allterms[r]=terms
 pol=pol[::-1]
 gamma=[]
 for r in range(s.n):
  for i,ch in enumerate(s.children[r]):
   chosen=pol[r][i];base=s.coef[allterms[r][i],chosen]
   for a,j in enumerate(ch):
    if a!=chosen:gamma.append(base-s.coef[allterms[r+1][j],a])
 gamma=np.unique(np.round(gamma,14),axis=0)
 return gamma,pol,int(allterms[0][0])

if __name__=='__main__':
 n=int(sys.argv[1]);p=int(sys.argv[2]);restarts=int(sys.argv[3]);steps=int(sys.argv[4]);individual='--individual' in sys.argv
 s=Search(n,p);rng=np.random.default_rng(103628);best=-1;start=time.time()
 for re in range(restarts):
  w=rng.exponential(1,len(s.masks))*(rng.random(len(s.masks))<rng.uniform(.1,.7));w/=w.sum()
  for step in range(steps):
   gamma,pol,t=policy(s,w,rng)
   U=s.coef@w
   objs=s.obj[:,t,:]
   if '--common-min' in sys.argv:
    load=s.loads[t];covered=s.cov[t]
    denom=np.where(load>0,(n+1)/(load+1),n)
    objs=np.concatenate([s.inc.T*denom-covered-s.coef[t,a] for a,c in enumerate(s.levels[n][t]) if c])
   elif individual:
    objs=np.concatenate([objs+s.cov[t]-n*s.coef[t,a] for a,c in enumerate(s.levels[n][t]) if c])
   # Solve only current worst query plus one fresh query to keep broad search fast.
   chosen={int(np.argmax(objs@w)),int(rng.integers(len(objs)))}
   candidate=None
   for a in chosen:
    res=linprog(-objs[a],A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=np.ones((1,len(w))),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:raise RuntimeError(res.message)
    if candidate is None or -res.fun>candidate[0]:candidate=(-res.fun,res.x,a)
   gap,w,a=candidate
   if gap>best+1e-9:
    best=gap
    d={'n':n,'p':p,'individual':individual,'restart':re,'step':step,'gap':gap,'query_index':a,'root':list(map(int,s.levels[n][t])),'weights':[(int(mask),float(v)) for mask,v in zip(s.masks,w) if v>1e-9],'policy':[{','.join(map(str,c)):int(pol[r][i]) for i,c in enumerate(s.levels[r])} for r in range(n)]}
    Path(__file__).with_name(f'policy_iteration_n{n}p{p}{"_common_min" if "--common-min" in sys.argv else "_individual" if individual else ""}.json').write_text(json.dumps(d,indent=2)+'\n')
    print('BEST',re,step,round(gap,9),'root',s.levels[n][t],'rows',len(gamma),'elapsed',round(time.time()-start,1),flush=True)
   # Small noise leaves the present cone, while a mostly LP point explores its face.
   noise=rng.exponential(1,len(w))*(rng.random(len(w))<.1);noise/=max(noise.sum(),1e-9)
   w=.999*w+.001*noise
 print('END',best,'seconds',time.time()-start,flush=True)
