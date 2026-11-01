"""Numerical hierarchy attacks on the interval relaxation, never SPE evidence."""
import itertools,json,random,time
from functools import lru_cache
from pathlib import Path
import numpy as np
from hierarchical_ceiling_probe import rows_for
BASE=Path(__file__).resolve().parent

def screen(q,m,rows):
 member=np.array([[(mask>>a)&1 for a in range(q)] for mask,w in rows],dtype=float)
 wt=np.array([w for mask,w in rows],dtype=float)
 @lru_cache(None)
 def dp(b):
  if sum(b)==m:
   load=member@b
   payoff=member.T@np.divide(wt,load,out=np.zeros(len(rows)),where=load>0)
   payoff=np.where(np.array(b)>0,payoff,0.)
   return payoff,payoff,0.
  children=[]
  for a in range(q):
   d=list(b);d[a]+=1;children.append(dp(tuple(d)))
  floor=max(children[a][0][a] for a in range(q))
  allowed=[a for a in range(q) if children[a][1][a]>=floor-1e-10]
  lo=np.min([children[a][0] for a in allowed],axis=0)
  hi=np.max([children[a][1] for a in allowed],axis=0)
  return lo,hi,floor+min(children[a][2] for a in allowed)
 G=dp((0,)*q)[2]
 opt=0.
 for size in range(min(q,m)+1):
  for ss in itertools.combinations(range(q),size):
   hit=member[:,ss].sum(axis=1)>0 if ss else np.zeros(len(rows),dtype=bool)
   opt=max(opt,float(wt[hit].sum()))
 return G,opt,dp.cache_info().currsize

def run(q,m,trials,seed):
 rng=random.Random(seed);best=None;start=time.time()
 for t in range(trials):
  rows=rows_for(q,rng);G,opt,states=screen(q,m,rows)
  if not opt:continue
  ratio=G/opt
  if best is None or ratio<best['ratio']-1e-10:
   best={'q':q,'m':m,'trial':t,'seed':seed,'ratio':ratio,'G_float':G,'OPT':int(opt),'states':states,'rows':rows}
   (BASE/f'interval_hierarchical_best_q{q}m{m}.json').write_text(json.dumps(best,indent=2)+'\n')
   print('BEST',t,ratio,'elapsed',round(time.time()-start,2),flush=True)
  if ratio<.5-1e-7:break
 ans={'trials_executed':t+1,'seed':seed,'q':q,'m':m,'best':best,'elapsed':time.time()-start}
 (BASE/f'interval_hierarchical_summary_q{q}m{m}.json').write_text(json.dumps(ans,indent=2)+'\n')
 print('DONE',json.dumps(ans),flush=True)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--q',type=int,default=8);p.add_argument('--m',type=int,default=8);p.add_argument('--trials',type=int,default=40);p.add_argument('--seed',type=int,default=977333)
 a=p.parse_args();run(a.q,a.m,a.trials,a.seed)
