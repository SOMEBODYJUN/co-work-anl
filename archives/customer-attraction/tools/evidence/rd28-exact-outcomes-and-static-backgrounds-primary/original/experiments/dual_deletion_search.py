"""Finite exact-SPE outcome search for deletion-support static-cap bridge.
BI is exact integer; minimax LP scores are numerical discovery only.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog
from cex_exact_sweep import IntegerSetSolver


def deletion_cap(q,weights):
 k=len(q);m=sum(q);masks=range(1,1<<k)
 bits=np.array([[(T>>a)&1 for T in masks] for a in range(k)])
 Bs=[tuple(q[j]-(j==a) for j in range(k)) for a in range(k) if q[a]]
 vals=np.array([(bits/(1+np.array(B)@bits))@weights for B in Bs]).T
 out=linprog(np.r_[np.zeros(len(Bs)),1.],A_ub=np.c_[vals,-np.ones(k)],b_ub=np.zeros(k),A_eq=[np.r_[np.ones(len(Bs)),0]],b_eq=[1],bounds=[(0,None)]*len(Bs)+[(None,None)],method='highs')
 assert out.success
 return out.fun, Bs, out.x[:-1], -out.ineqlin.marginals


def run(k,m,trials,seed):
 rng=random.Random(seed);solver=IntegerSetSolver(k,m)
 base=[0]*((1<<k)-1);base[0]=m
 for a in range(1,min(k,m)): base[(1<<a)-1]=1
 champ=base.copy();best=0;records=[];count=0;start=time.monotonic()
 for i in range(trials):
  if not i:w=base.copy()
  elif i%20==0: w=[rng.randrange(1,21) if rng.random()<.15 else 0 for _ in base]
  elif i%13==0:
   w=[0]*len(base)
   for a in range(k):w[(1<<a)-1]=rng.randrange(1,m+2)
   for _ in range(rng.randrange(1,k+1)):w[rng.randrange(len(base))]+=rng.randrange(1,m+2)
  else:
   w=champ.copy()
   for _ in range(rng.randrange(1,5)):
    j=rng.randrange(len(w));w[j]=max(0,w[j]+rng.choice([-3,-2,-1,1,2,3]))
  roots=solver.solve(w)['root_outcomes']
  ibest=0
  for q in roots:
   idx=solver.tindex[q];W=int(solver.last_welfare[idx]);count+=1
   if not W:continue
   cap,Bs,Q,p=deletion_cap(q,w)
   ratio=cap*(m-.5)/W
   if ratio>ibest:ibest=ratio
   if ratio>best+1e-9:
    best=ratio
    row={'trial':i,'ratio':ratio,'cap':cap,'W':W,'q':q,'w':w,'p':p.tolist(),'backgrounds':Bs,'Q':Q.tolist()}
    records.append(row);print(json.dumps(row),flush=True)
    if ratio>1+1e-7:return {'status':'CANDIDATE','record':row,'tested_outcomes':count,'seconds':time.monotonic()-start}
  if ibest>=best-1e-9 and (ibest>best-1e-7 or rng.random()<.2): champ=w.copy()
 return {'status':'NO_COUNTEREXAMPLE_IN_FINITE_SEARCH','topics':k,'players':m,'trials':trials,'seed':seed,'best_ratio':best,'tested_outcomes':count,'seconds':time.monotonic()-start,'records':records}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--trials',type=int,default=300);ap.add_argument('--seed',type=int,default=20261022);ap.add_argument('--output',type=Path)
 a=ap.parse_args();r=run(a.topics,a.players,a.trials,a.seed)
 if a.output:
  with a.output.open('x') as f:json.dump(r,f,indent=2)
 print(json.dumps({k:v for k,v in r.items() if k!='records'}),flush=True)
