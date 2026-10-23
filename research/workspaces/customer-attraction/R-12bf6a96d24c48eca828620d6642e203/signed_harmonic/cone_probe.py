"""Discovery LP on complete count policies; exact counterexamples require audit."""
from pathlib import Path
from itertools import combinations_with_replacement
from math import lcm
from fractions import Fraction
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
HERE=Path(__file__).parent

def comps(n,p):
 if p==1:yield (n,);return
 for v in range(n+1):
  for t in comps(n-v,p-1):yield(v,)+t

def main(p,m,trials,seed,linear,all_opt,no_opt):
 rng=random.Random(seed);masks=np.arange(1,1<<p);member=np.array([[(int(mask)>>a)&1 for a in range(p)] for mask in masks]);states=[q for n in range(m) for q in comps(n,p)];terms=list(comps(m,p));ti={t:i for i,t in enumerate(terms)};loads=np.array([member@np.array(t) for t in terms]);cover=loads>0
 coeff=np.divide(member[None,:,:],loads[:,:,None],out=np.zeros((len(terms),len(masks),p)),where=loads[:,:,None]!=0)
 H=np.array([0.]+[sum(1/j for j in range(1,i+1)) for i in range(1,2*m+1)])
 compset=[]
 for t in terms:
  if all_opt or max(t)<=1:compset.append(t)
 for trial in range(trials):
  w=np.array([rng.randrange(0,30) if rng.random()<.35 else 0 for _ in masks]);pay=np.einsum('tka,k->ta',coeff,w);policy={};out={t:t for t in terms}
  for q in reversed(states):
   children=[]
   for a in range(p):
    c=list(q);c[a]+=1;children.append(out[tuple(c)])
   vals=[pay[ti[children[a]],a] for a in range(p)];v=max(vals);a=rng.choice([a for a in range(p) if abs(vals[a]-v)<1e-8]);policy[q]=a;out[q]=children[a]
  actual=out[(0,)*p];at=ti[actual];rows=[]
  for q in states:
   a=policy[q];on=coeff[ti[out[q]],:,a]
   for b in range(p):
    if a==b:continue
    c=list(q);c[b]+=1;rows.append(on-coeff[ti[out[tuple(c)]],:,b])
  gamma=np.array(rows);candidate_comps=compset.copy();rng.shuffle(candidate_comps)
  for d in candidate_comps:
   dt=ti[d];c=loads[at];k=loads[dt];budget=cover[at].astype(float)+(cover[at]&~cover[dt]).astype(float)
   F=k/(c+1) if linear else H[c+k]-H[c];obj=budget-F
   if min(obj)>-1e-9:continue
   optimality=cover[dt].astype(float)-cover.astype(float);allrows=gamma if no_opt else np.vstack([gamma,optimality]);res=linprog(obj,A_ub=-allrows,b_ub=np.zeros(len(allrows)),A_eq=[np.ones(len(masks))],b_eq=[1.],bounds=(0,None),method='highs')
   if res.success and res.fun<-1e-7:
    print('FOUND',trial,res.fun,'a',actual,'d',d,flush=True)
    # Integer recovery enforces all exact rational rows after LCM scaling.
    den=lcm(*range(1,2*m+1));G=np.rint(allrows*den).astype(np.int64);J=np.rint(obj*den).astype(np.int64)
    rec=milp(np.ones(len(masks)),integrality=np.ones(len(masks)),bounds=Bounds(0,np.inf),constraints=[LinearConstraint(G,0,np.inf),LinearConstraint(-J,1,np.inf)],options={'time_limit':30})
    vals=np.rint(rec.x).astype(int).tolist() if rec.x is not None else None
    data=dict(p=p,m=m,seed=seed,trial=trial,linear=linear,no_opt=no_opt,actual=actual,optimal=d,policy=[[q,a] for q,a in policy.items()],weights={int(mask):float(v) for mask,v in zip(masks,res.x) if v>1e-10},integer_weights=None if vals is None else {int(mask):v for mask,v in zip(masks,vals) if v},objective=float(res.fun),integer_recovery_success=bool(rec.success))
    (HERE/('linear_candidate.json' if linear else 'harmonic_candidate.json')).write_text(json.dumps(data,indent=2)+'\n');return
  if trial%20==0:print('trial',trial,flush=True)
 print('NONE',p,m,trials,seed,linear,flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--p',type=int,default=6);a.add_argument('--m',type=int,default=3);a.add_argument('--trials',type=int,default=200);a.add_argument('--seed',type=int,default=78631);a.add_argument('--linear',action='store_true');a.add_argument('--all-opt',action='store_true');a.add_argument('--no-opt',action='store_true');v=a.parse_args();main(v.p,v.m,v.trials,v.seed,v.linear,v.all_opt,v.no_opt)
