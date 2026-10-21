"""Finite numerical discovery over full BI policy cones, with an explicit root menu.
None of these bounded runs is a general theorem. Seed, scope and trace saved.
"""
from pathlib import Path
from itertools import product
from functools import lru_cache
import argparse, json, math
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=4);ap.add_argument('--p',type=int,default=5);ap.add_argument('--games',type=int,default=40);ap.add_argument('--starts',type=int,default=10);ap.add_argument('--factor',type=float);ap.add_argument('--seed',type=int,default=373801);args=ap.parse_args()
 n,k=args.m,args.p;factor=args.factor if args.factor is not None else n-.5;rng=np.random.default_rng(args.seed)
 masks=np.arange(1,1<<k);bits=np.array([[(t>>a)&1 for a in range(k)]for t in masks],float);cst=math.lcm(*range(1,n+1));hs=[h for d in range(n)for h in product(range(k),repeat=d)]
 trace=[];best=None
 for game in range(args.games):
  density=float(rng.choice([.15,.4,1.]));weights=rng.integers(0,13,size=len(bits))*(rng.random(len(bits))<density)
  if not weights.any():continue
  @lru_cache(None)
  def payoff(z):
   load=bits@z
   return bits.T@(weights/np.maximum(load,1))
  actions={}
  @lru_cache(None)
  def out(h):
   if len(h)==n:return tuple(np.bincount(h,minlength=k))
   zs=[out(h+(a,))for a in range(k)];vals=np.array([payoff(z)[a]for a,z in enumerate(zs)])
   cand=np.flatnonzero(vals>=max(vals)-1e-10);a=int(rng.choice(cand));actions[h]=a
   return zs[a]
  out(())
  def row(a,z):return bits[:,a]/np.maximum(bits@z,1)
  rows=[tuple(np.rint(cst*(row(actions[h],out(h))-row(a,out(h+(a,))))).astype(int))for h in hs for a in range(k)if a!=actions[h]]
  gamma=np.array(sorted(set(rows)),float)/cst;gamma=gamma[np.any(gamma!=0,axis=1)]
  bg=np.unique([np.array(out((a,)))-np.eye(k,dtype=int)[a]for a in range(k)],axis=0)
  coeff=bits[None,:,:]/(1+bg@bits.T)[:,:,None];cover=(bits@out(())>0).astype(float)
  for start in range(args.starts):
   p=rng.dirichlet(np.ones(k)*.3) if start else np.ones(k)/k;last=None
   for it in range(10):
    beta=coeff@p
    r=linprog(np.r_[cover,-factor],A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]],b_ub=np.zeros(len(gamma)+len(beta)),A_eq=[np.r_[np.ones(len(cover)),0]],b_eq=[1],bounds=[(0,None)]*len(cover)+[(None,None)],method='highs')
    if not r.success:raise RuntimeError(r.message)
    w=r.x[:-1];mat=np.einsum('bta,t->ba',coeff,w)
    q=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-mat,np.ones(len(mat))],b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
    if not q.success:raise RuntimeError(q.message)
    p=q.x[:-1];v=q.x[-1];gap=factor*v-cover@w
    item=dict(game=game,start=start,it=it,gap=float(gap),W=float(cover@w),cap=float(v),weights={int(t):float(x)for t,x in zip(masks,w)if x>1e-9},query=p.tolist())
    trace.append(item)
    if best is None or gap>best['gap']+1e-9:
     best=item|{'actions':[{'history':list(h),'action':a}for h,a in actions.items()],'root':list(map(int,out(()))),'backgrounds':bg.tolist()};print(json.dumps({key:best[key]for key in item}),flush=True)
     (HERE/f'policy_cap_m{n}p{k}_factor{factor}_seed{args.seed}.json').write_text(json.dumps(dict(scope='finite floating full policy cones; candidate requires exact followup',parameters=vars(args),best=best,trace=trace),indent=2))
    if last is not None and abs(last-gap)<1e-10:break
    last=gap
  if best['gap']>1e-7:break
 (HERE/f'policy_cap_m{n}p{k}_factor{factor}_seed{args.seed}.json').write_text(json.dumps(dict(scope='finite floating full policy cones; candidate requires exact followup',parameters=vars(args),best=best,trace=trace),indent=2))
if __name__=='__main__':main()
