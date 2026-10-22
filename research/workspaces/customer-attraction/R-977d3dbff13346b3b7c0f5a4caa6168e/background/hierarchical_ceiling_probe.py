"""Float screening of an exactly specified min-vector ceiling relaxation.
No SPE counterexample is claimed; a strict separation requires exact replay.
"""
import itertools,json,random,time
from functools import lru_cache
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent

def screen(q,m,rows):
 membership=np.array([[(mask>>a)&1 for a in range(q)] for mask,w in rows],dtype=float)
 wt=np.array([w for mask,w in rows],dtype=float)
 @lru_cache(None)
 def dp(b):
  load=membership@b
  if sum(b)==m:
   payoff=membership.T@np.divide(wt,load,out=np.zeros(len(rows)),where=load>0)
   payoff=np.where(np.array(b)>0,payoff,0.)
   return payoff,0.
  children=[]
  for a in range(q):
   d=list(b);d[a]+=1;children.append(dp(tuple(d)))
  floor=max(children[a][0][a] for a in range(q))
  myopic=membership.T@(wt/(load+1))
  allowed=[a for a in range(q) if myopic[a]>=floor-1e-10]
  minimum=np.min([children[a][0] for a in allowed],axis=0)
  return minimum,floor+min(children[a][1] for a in allowed)
 G=dp((0,)*q)[1]
 opt=0.
 for size in range(min(q,m)+1):
  for ss in itertools.combinations(range(q),size):
   hit=membership[:,ss].sum(axis=1)>0 if ss else np.zeros(len(rows),dtype=bool)
   opt=max(opt,float(wt[hit].sum()))
 return G,opt,dp.cache_info().currsize

def rows_for(q,rng):
 # Dyadic ancestor groups plus private leaf groups and optional crossing groups.
 rows={}
 block=1
 while block<=q:
  for start in range(0,q,block):
   mask=sum(1<<a for a in range(start,min(q,start+block)))
   rows[mask]=rng.choice([0,1,2,3,5,8,13,21,34,55,89])
  block*=2
 if rng.random()<.5:
  for a in range(q):
   mask=(1<<a)|(1<<((a+1)%q))
   rows[mask]=rows.get(mask,0)+rng.choice([0,1,3,8,21])
 return [(mask,w) for mask,w in sorted(rows.items()) if w]

def run(q,m,trials,seed):
 rng=random.Random(seed);best=None;start=time.time()
 for t in range(trials):
  rows=rows_for(q,rng);G,opt,states=screen(q,m,rows)
  if not opt:continue
  ratio=G/opt
  if best is None or ratio<best['ratio']-1e-10:
   best={'q':q,'m':m,'trial':t,'seed':seed,'ratio':ratio,'G_float':G,'OPT':int(opt),'states':states,'rows':rows}
   (BASE/f'hierarchical_best_q{q}m{m}.json').write_text(json.dumps(best,indent=2)+'\n')
   print('BEST',t,ratio,'elapsed',round(time.time()-start,2),flush=True)
  if ratio<.5-1e-7:break
 ans={'trials_executed':t+1,'seed':seed,'q':q,'m':m,'best':best,'elapsed':time.time()-start}
 (BASE/f'hierarchical_summary_q{q}m{m}.json').write_text(json.dumps(ans,indent=2)+'\n')
 print('DONE',json.dumps(ans),flush=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--q',type=int,default=8);p.add_argument('--m',type=int,default=8);p.add_argument('--trials',type=int,default=30);p.add_argument('--seed',type=int,default=977133)
 a=p.parse_args();run(a.q,a.m,a.trials,a.seed)
