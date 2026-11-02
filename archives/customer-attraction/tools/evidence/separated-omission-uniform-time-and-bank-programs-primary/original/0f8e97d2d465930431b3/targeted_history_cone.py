"""Targeted existing complex strategies, reoptimized customer cones.
Finite diagnostic only. Complete ordered-history strategy is held fixed.
"""
import sys,json,time
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction.certificate import StrategyCertificate
from cone_time_attack import query_oracle,cone_oracle

def load(name):
 inst=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text());raw=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text());raw=raw.get('strategy',raw)
 cert=StrategyCertificate.from_dict(raw);m=inst['players'];k=len(inst['topics']);masks=np.arange(1,1<<k);inc=((masks[:,None]>>np.arange(k))&1).astype(float)
 @lru_cache(None)
 def terminal(h):return h if len(h)==m else terminal(h+(cert.actions[h],))
 @lru_cache(None)
 def payoff(z):
  c=inc@np.bincount(z,minlength=k);return np.divide(inc,c[:,None],out=np.zeros_like(inc),where=c[:,None]>0).T
 @lru_cache(None)
 def extra(z):return (inc/(1+inc@np.bincount(z,minlength=k))[:,None]).T
 rows=[]
 for h,a in cert.actions.items():
  own=payoff(terminal(h))[a]
  for b in range(k):
   row=payoff(terminal(h+(b,)))[b]-own
   if np.max(np.abs(row))>1e-12:rows.append(row)
 z=terminal(());W=(inc@np.bincount(z,minlength=k)>0).astype(float)
 cols=np.stack([np.stack([extra(terminal(z[:i]+(a,))) for a in range(k)]) for i in range(m)])
 w=np.zeros(len(masks))
 for cust in inst['customers']:w[sum(1<<t for t in cust['topics'])-1]=cust['multiplicity']
 return m,k,np.stack(rows),cols,W,w/w.sum(),z

def main():
 start=time.time();records=[];rng=np.random.default_rng(9912381)
 for name in ['aggregate_theta_failure','individual_security_failure','optimal_last_query_failure']:
  m,k,rows,cols,W,original,z=load(name);print('GAME',name,m,k,'rows',len(rows),flush=True)
  for t in range(1+m):
   lam=np.ones(m)/m if t==0 else np.eye(m)[t-1];best=-999
   for init in range(12):
    if init==0:w=original.copy()
    else:
     # Random direction in the exact fixed SPE cone, not new strategy samples.
     out=linprog(rng.normal(size=len(original)),A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=[np.ones(len(original))],b_eq=[1],bounds=[(0,None)]*len(original),method='highs');assert out.success;w=out.x
    for it in range(7):
     p,_,_=query_oracle(cols,w,lam);w1,psi,gap=cone_oracle(rows,cols,W,p,lam)
     best=max(best,gap)
     if gap>1e-8:
      records.append(dict(name=name,time=t,weights=w1.tolist(),p=p.tolist(),psi=psi.tolist(),W=float(W@w1),gap=gap,actual=z));print('POSITIVE',name,t,gap,flush=True)
     if np.max(np.abs(w-w1))<1e-8:break
     w=w1
   print('RESULT',name,t,best,flush=True)
 Path(__file__).with_suffix('.json').write_text(json.dumps(dict(records=records,seconds=time.time()-start,scope='Fixed complete-history SPE cones; weights and queries optimized by finite coordinate LP; negative results prove no general claim.'),indent=2))
if __name__=='__main__':main()
