"""Exact full-SPE outcome sets, numerical PAIR/security screening.

Tests every feasible first two actions of every SPE terminal, rather than one
selected worst path. Security LPs use floating arithmetic and must be replayed
exactly if a negative candidate is found. Finite screens prove no general claim.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
from math import lcm
from pathlib import Path
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog

def counts(k,n):
 for actions in combinations_with_replacement(range(k),n):
  q=[0]*k
  for a in actions:q[a]+=1
  yield tuple(q)

def security(inc,w,k,r,bg):
 f=np.array([(w/(bg+inc@np.array(q)+1))@inc for q in counts(k,r-1)])
 z=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-f,np.ones(len(f))],b_ub=np.zeros(len(f)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
 if not z.success:raise RuntimeError(z.message)
 return z.x[-1],z.x[:-1]

def screen(k,r,weights,prefix=()):
 masks=np.arange(1,1<<k,dtype=np.int64);inc=(masks[:,None]>>np.arange(k))&1;w=np.array(weights,dtype=np.int64);bg=inc@np.bincount(prefix,minlength=k);scale=lcm(*range(1,r+len(prefix)+1))
 terminals=list(counts(k,r));tidx={q:i for i,q in enumerate(terminals)};den=bg+np.array(terminals)@inc.T
 shares=np.zeros_like(den)
 for d in range(1,r+len(prefix)+1):shares[den==d]=scale//d
 pay=(shares*w)@inc
 welfare=np.sum(pay*np.array(terminals),axis=1)
 floors={}
 @lru_cache(None)
 def outcomes(q):
  if sum(q)==r:return (tidx[q],)
  kids=[outcomes(q[:a]+(q[a]+1,)+q[a+1:]) for a in range(k)]
  floor=max(min(int(pay[t,a]) for t in child) for a,child in enumerate(kids));floors[q]=floor
  return tuple(sorted(set(t for a,child in enumerate(kids) for t in child if pay[t,a]>=floor)))
 zero=(0,)*k;root=outcomes(zero);v,p=security(inc,w,k,r,bg);bestW=min(welfare[t]/scale for t in root)
 pairmin={};pairtarget={}
 for a in range(k):
  qa=zero[:a]+(1,)+zero[a+1:];child=outcomes(qa)
  feasible=set(t for t in child if pay[t,a]>=floors[zero])
  for b in range(k):
   qab=qa[:b]+(qa[b]+1,)+qa[b+1:]
   for t in outcomes(qab):
    if t in feasible and pay[t,b]>=floors[qa]:
     key=tuple(sorted((a,b)));z=(int(pay[t,a])+int(pay[t,b]))/scale
     if key not in pairmin or z<pairmin[key]:pairmin[key]=z;pairtarget[key]=(t,a,b)
 best=None;tailLP=0
 for pair,total in sorted(pairmin.items(),key=lambda z:z[1]):
  # Static background embedding proves tail security >= root security.
  if total>=2*v+1e-8:continue
  vp,_=security(inc,w,k,r-2,bg+inc[:,pair].sum(axis=1));tailLP+=1;gap=total+(r-2)*vp-r*v
  if best is None or gap<best['gap']:
   t,a,b=pairtarget[pair];q=zero;path=[a,b]
   for a0 in path:q=q[:a0]+(q[a0]+1,)+q[a0+1:]
   while len(path)<r:
    a0=next(a0 for a0 in range(k) if t in outcomes(q[:a0]+(q[a0]+1,)+q[a0+1:]) and pay[t,a0]>=floors[q]);path.append(a0);q=q[:a0]+(q[a0]+1,)+q[a0+1:]
   best=dict(gap=float(gap),first_pair_total=total,tail_security=float(vp),terminal=terminals[t],ordered_path=path,path_payoffs=[int(pay[t,a0])/scale for a0 in path])
 return dict(k=k,r=r,prefix=prefix,weights=weights,root_outcomes=len(root),static_security=float(v),query=p.tolist(),minimum_tail_total=bestW,aggregate_ratio=bestW/(r*v) if v else 1,pairs=len(pairmin),tailLP=tailLP,best_pair=best)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=8);ap.add_argument('--r',type=int,default=6);ap.add_argument('--samples',type=int,default=500);ap.add_argument('--seconds',type=float,default=180);ap.add_argument('--background',type=int,default=0);ap.add_argument('--seed',type=int,default=26102166);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();rng=random.Random(args.seed);start=time.perf_counter();best=None;bestagg=None;tailLP=0;checked=0
 for sample in range(args.samples):
  density=rng.choice((.01,.03,.1));mode=rng.randrange(3)
  weights=[rng.randint(1,20) if rng.random()<density and (mode==0 or (mask.bit_count()<=3 if mode==1 else mask.bit_count()>=args.k-3)) else 0 for mask in range(1,1<<args.k)]
  prefix=tuple(rng.randrange(args.k) for _ in range(args.background));z=screen(args.k,args.r,weights,prefix);checked+=1;tailLP+=z['tailLP']
  if bestagg is None or z['aggregate_ratio']<bestagg['aggregate_ratio']-1e-10:bestagg=z
  if z['best_pair'] is not None and (best is None or z['best_pair']['gap']<best['best_pair']['gap']-1e-9):best=z;print(json.dumps(dict(sample=sample,gap=z['best_pair']['gap'],aggregate_ratio=z['aggregate_ratio'],path=z['best_pair']['ordered_path'])),flush=True)
  packet=dict(status='exact SPE outcome sets; floating security screening; no general proof',seed=args.seed,k=args.k,r=args.r,background=args.background,samples_requested=args.samples,samples_completed=checked,seconds_requested=args.seconds,elapsed=time.perf_counter()-start,tail_LPs=tailLP,best_pair=best,best_aggregate=bestagg)
  args.output.write_text(json.dumps(packet,indent=2)+'\n')
  if (best is not None and best['best_pair']['gap']<-1e-7) or z['aggregate_ratio']<1-1e-8 or time.perf_counter()-start>args.seconds:break
 print(json.dumps(dict(done=True,samples=checked,tail_LPs=tailLP,elapsed=time.perf_counter()-start,best_pair=best['best_pair']['gap'] if best else None,best_aggregate=bestagg['aggregate_ratio'])),flush=True)

if __name__=='__main__':main()
