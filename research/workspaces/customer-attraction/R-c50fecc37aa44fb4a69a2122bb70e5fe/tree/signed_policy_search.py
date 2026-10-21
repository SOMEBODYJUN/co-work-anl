"""Explore full common signed-customer games, never assert a true CAG counterexample.

Retains every complete-history incentive plus every sharp same-label universal
ratio inequality and nonnegative terminal payoff. Policy search includes signed
instances, so resulting policies need not be actual nonnegative-customer SPE.
"""
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import linprog

BASE=Path(__file__).resolve().parent

def compositions(n,p):
 if p==1:return [(n,)]
 return [(i,)+q for i in range(n+1) for q in compositions(n-i,p-1)]

def prepare(n,p):
 qs=compositions(n,p)
 vs=[(q,a) for q in qs for a in range(p) if q[a]];vid={v:i for i,v in enumerate(vs)}
 incidence=np.array([[B>>a&1 for a in range(p)] for B in range(1,1<<p)])
 den=np.array(qs)@incidence.T
 F=np.array([incidence[:,a]/np.where(den[i],den[i],1) for i,q in enumerate(qs) for a in range(p) if q[a]])
 rows=[]
 for a in range(p):
  inds=[i for i,(q,b) in enumerate(vs) if b==a]
  da=np.array([q for q,b in vs if b==a])@incidence[incidence[:,a]==1].T
  kapa=np.max(da[None,:,:]/da[:,None,:],axis=2)
  fa=F[inds]
  row=(fa[:,None,:]-kapa[:,:,None]*fa[None,:,:]).reshape(-1,len(incidence))
  rows.append(row)
 rows.append(-F)
 universal=np.vstack(rows)
 universal=universal[np.max(np.abs(universal),axis=1)>1e-10]
 # Scale normalization strictly preserves the numerical halfspaces.
 universal/=np.max(np.abs(universal),axis=1)[:,None]
 universal=np.unique(np.round(universal,12),axis=0)
 targets={A:(incidence[:,A].sum(axis=1)>0).astype(float) for A in combinations(range(p),min(n,p))}
 return qs,vs,vid,F,universal,targets

def policy(n,p,w,rng,vid,F,exact=False):
 if exact:
  utilities={v:sum(Fraction(int(B>>v[1]&1))*w[B-1]/sum(v[0][b] for b in range(p) if B>>b&1) for B in range(1,1<<p) if B>>v[1]&1) for v in vid}
 else:utilities={v:float(F[i]@w) for v,i in vid.items()}
 actions={};terminal={}
 for d in range(n,-1,-1):
  for h in product(range(p),repeat=d):
   if d==n:terminal[h]=tuple(h.count(a) for a in range(p));continue
   scores=[utilities[terminal[h+(a,)],a] for a in range(p)]
   best=max(scores)
   candidates=[a for a in range(p) if scores[a]==best] if exact else [a for a in range(p) if scores[a]>=best-1e-8]
   a=int(rng.choice(candidates));actions[h]=a;terminal[h]=terminal[h+(a,)]
 graph=np.array([F[vid[terminal[h+(b,)],b]]-F[vid[terminal[h],a]] for h,a in actions.items() for b in range(p) if b!=a])
 return actions,terminal,graph

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=5);ap.add_argument('--p',type=int,default=6);ap.add_argument('--trials',type=int,default=50);ap.add_argument('--seed',type=int,default=2801);ap.add_argument('--mutate',type=int,default=4);ap.add_argument('--tag',default='');ap.add_argument('--lp-seconds',type=float,default=20);args=ap.parse_args()
 n,p=args.n,args.p;rng=np.random.default_rng(args.seed);start=time.time()
 qs,vs,vid,F,universal,targets=prepare(n,p)
 print(json.dumps(dict(n=n,p=p,vertices=len(vs),universal=len(universal),preparation=time.time()-start)),flush=True)
 best=0;reports=[];warm=None
 for trial in range(args.trials):
  if warm is not None and trial%(args.mutate+1):w=warm
  else:
   w=(rng.integers(1,30,size=len(F[0]))*(rng.random(len(F[0]))<rng.choice([.07,.15,.35,.65]))).astype(float)
  actions,terminal,graph=policy(n,p,w,rng,vid,F)
  root=sum((terminal[()][a]*F[vid[terminal[()],a]] for a in range(p) if terminal[()][a]),np.zeros(len(F[0])))
  # Usually the optimum for the generator; random target permits other supports.
  target=max(targets,key=lambda A:float(targets[A]@w)) if trial%3 else list(targets)[rng.integers(len(targets))]
  obj=targets[target]
  sol=linprog(-obj,A_ub=np.vstack([universal,graph]),b_ub=np.zeros(len(universal)+len(graph)),A_eq=root[None,:],b_eq=[1],bounds=(None,None),method='highs',options={'time_limit':args.lp_seconds})
  value=-sol.fun if sol.success else None
  if sol.success:warm=sol.x
  reports.append(dict(trial=trial,value=value,target=target,root=terminal[()],elapsed=time.time()-start))
  if value is not None and value>best+1e-7:
   best=value
   print(json.dumps(dict(trial=trial,best=best,target=target,root=terminal[()],elapsed=time.time()-start)),flush=True)
   payload=dict(scope='common signed customer relaxation; not a genuine CAG instance',n=n,p=p,seed=args.seed,trial=trial,target=target,value=value,strategy_actions=[dict(history=h,action=a) for h,a in sorted(actions.items())],signed_customer_weights=[dict(mask=B,weight=str(Fraction(float(v)).limit_denominator(10000000))) for B,v in enumerate(sol.x,1) if abs(v)>1e-8])
   (BASE/f'signed_policy_n{n}_p{p}{args.tag}_best.json').write_text(json.dumps(payload,indent=2)+'\n')
  if trial%10==9:print(json.dumps(dict(completed=trial+1,best=best,elapsed=time.time()-start)),flush=True)
  if value is not None and value>2+1e-6:
   print('SIGNED_ABOVE_TWO_CANDIDATE',flush=True);break
 (BASE/f'signed_policy_n{n}_p{p}{args.tag}_run.json').write_text(json.dumps(reports,indent=2)+'\n')
 print(json.dumps(dict(completed=len(reports),best=best,elapsed=time.time()-start)),flush=True)
if __name__=='__main__':main()
