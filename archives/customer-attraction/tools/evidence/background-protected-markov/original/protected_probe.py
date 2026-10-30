"""Finite Markov cone attack on protected coverage and background invariants.

All cones contain every count-state SPE comparison; each count policy lifts to
one legitimate ordered-history policy. Numerical screening is not a proof.
"""
import argparse, itertools, json, random, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parent

def comps(n,q):
 if q==1:
  yield (n,); return
 for j in range(n+1):
  for t in comps(n-j,q-1): yield (j,)+t

def run(q,k,trials,seed,background,mode):
 rng=random.Random(seed)
 masks=np.arange(1,1<<q)
 member=np.array([[(int(b)>>a)&1 for a in range(q)] for b in masks])
 states=[c for n in range(k) for c in comps(n,q)]
 terminals=list(comps(k,q)); ti={c:j for j,c in enumerate(terminals)}
 loads=np.array([member@np.array(c) for c in terminals])
 comparison=list(comps(k,q)) if mode=='profit' else list(itertools.combinations(range(q),min(k,q)))
 start=time.time(); tested=0; maxratio=0.
 for trial in range(trials):
  prefix=[0]*q
  for _ in range(rng.randrange(background+1)):
   prefix[rng.randrange(q)]+=1
  bg=member@np.array(prefix); total=loads+bg
  coeff=np.divide(member[None,:,:],total[:,:,None],out=np.zeros((len(terminals),len(masks),q)),where=total[:,:,None]>0)
  w=np.array([rng.randrange(1,51) if rng.random()<rng.uniform(.08,.7) else 0 for _ in masks])
  pay=np.einsum('tma,m->ta',coeff,w)
  policy={}; out={c:c for c in terminals}
  for c in reversed(states):
   child=[]
   for a in range(q):
    d=list(c); d[a]+=1; child.append(out[tuple(d)])
   vals=[pay[ti[child[a]],a] for a in range(q)]; mx=max(vals)
   a=rng.choice([a for a in range(q) if abs(vals[a]-mx)<1e-8]); policy[c]=a; out[c]=child[a]
  actual=out[(0,)*q]; at=ti[actual]
  P=np.divide(loads[at],total[at],out=np.zeros(len(masks)),where=total[at]>0)
  fresh=(bg==0)
  rows=[]
  for c in states:
   a=policy[c]; on=coeff[ti[out[c]],:,a]
   for b in range(q):
    if b==a: continue
    d=list(c); d[b]+=1
    rows.append(on-coeff[ti[out[tuple(d)]],:,b])
  rows=np.array(rows)
  selected=rng.sample(comparison,min(12,len(comparison)))
  for comp in selected:
   if mode=='profit':
    cmp_load=member@np.array(comp)
    objective=np.divide(cmp_load,bg+cmp_load,out=np.zeros(len(masks)),where=bg+cmp_load>0)
   else:
    hit=member[:,comp].sum(axis=1)>0
    objective=(fresh*hit).astype(float)
    if mode=='protected': objective=objective*(loads[at]==0)
   base=P+fresh*(loads[at]>0) if mode=='global' else P
   res=linprog(-objective,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=[base],b_eq=[1.],bounds=(0,None),method='highs')
   tested+=1
   if not res.success: continue
   ratio=-float(res.fun)
   if ratio>maxratio+1e-8:
    maxratio=ratio
    data={'mode':mode,'q':q,'k':k,'trial':trial,'seed':seed,'background_limit':background,'prefix':prefix,'actual':actual,'comparison':comp,'ratio':ratio,'policy':[[c,a] for c,a in policy.items()],'weights':{int(b):float(v) for b,v in zip(masks,res.x) if v>1e-9}}
    (ROOT/f'{mode}_best_q{q}k{k}.json').write_text(json.dumps(data,indent=2))
    print('BEST',trial,ratio,'elapsed',round(time.time()-start,2),flush=True)
   threshold=2. if mode=='profit' else 1.
   if ratio>threshold+1e-7:
    print('CANDIDATE',mode,ratio,'tested',tested,flush=True); return
  if trial%25==0: print('progress',trial,'tested',tested,'best',maxratio,'elapsed',round(time.time()-start,2),flush=True)
 summary={'mode':mode,'q':q,'k':k,'seed':seed,'trials':trials,'tested':tested,'maxratio':maxratio,'elapsed':time.time()-start,'background_limit':background}
 (ROOT/f'{mode}_summary_q{q}k{k}.json').write_text(json.dumps(summary,indent=2))
 print('DONE',json.dumps(summary),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--q',type=int,default=6); p.add_argument('--k',type=int,default=3); p.add_argument('--trials',type=int,default=100); p.add_argument('--seed',type=int,default=513823); p.add_argument('--background',type=int,default=5); p.add_argument('--mode',choices=['protected','global','profit'],default='protected'); a=p.parse_args(); run(a.q,a.k,a.trials,a.seed,a.background,a.mode)
