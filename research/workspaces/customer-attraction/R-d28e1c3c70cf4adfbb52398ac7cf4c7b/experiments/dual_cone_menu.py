"""Fixed-policy cone attacks on proposed static background supports.
Numerical discovery only, exact certificates are checked separately.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations
import json,sys
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]

def policy_matrix(name):
 game=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
 cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
 k,n=len(game['topics']),game['players']; masks=np.arange(1,1<<k)
 pol={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
 @lru_cache(None)
 def finish(h): return h if len(h)==n else finish(h+(pol[h],))
 bits=np.array([[(T>>a)&1 for T in masks] for a in range(k)])
 def rho(a,z):
  load=sum(bits[b] for b in z)
  return bits[a]/np.maximum(load,1)
 G=np.array([rho(pol[h],finish(h))-rho(a,finish(h+(a,))) for h in pol for a in range(k)])
 z=finish(()); c=(sum(bits[b] for b in z)>0).astype(float)
 men=set(tuple(sorted(finish(z[:i]+(a,))[:i]+finish(z[:i]+(a,))[i+1:])) for i in range(n) for a in range(k))
 dels=set(tuple(sorted(z[:i]+z[i+1:])) for i in range(n))
 return k,n,masks,bits,G,c,z,men,dels

def run(name,how='deletions',iters=100):
 k,n,masks,bits,G,c,z,men,dels=policy_matrix(name)
 Bset=sorted(dels if how=='deletions' else men)
 bet=np.array([bits/(1+sum(bits[b] for b in B)) for B in Bset])
 rng=np.random.default_rng(20261021)
 ps=[np.ones(k)/k]+[np.eye(k)[a] for a in range(k)]+[(np.eye(k)[a]+np.eye(k)[b])/2 for a,b in combinations(range(k),2)]+list(rng.dirichlet(np.ones(k)*.6,iters))
 best=-1
 for j,p in enumerate(ps):
  M=np.einsum('bat,a->bt',bet,p)
  A=np.r_[np.c_[-G,np.zeros(len(G))],np.c_[-M,np.ones(len(M))]]
  lp=linprog(np.r_[np.zeros(len(masks)),-1.],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[c,0]],b_eq=[1],bounds=[(0,None)]*(len(masks)+1),method='highs')
  if not lp.success: raise ValueError(lp.message)
  value=lp.x[-1]
  if value>best+1e-10:
   best=value
   rec={'name':name,'how':how,'n':n,'k':k,'z':z,'cap_lower':best,'strong_gap':best-1/n,'half_gap':best-1/(n-.5),'p':p.tolist(),'weights':{int(T):float(w) for T,w in zip(masks,lp.x[:-1]) if w>1e-8},'iteration':j,'menu':[list(B) for B in Bset]}
   print(json.dumps(rec),flush=True)
   if rec['half_gap']>1e-7:
    out=Path(__file__).with_name('dual_cone_menu_candidate.json');out.write_text(json.dumps(rec,indent=2));return rec
 return rec
if __name__=='__main__':
 for name in sys.argv[1:] or ['aggregate_theta_failure','individual_security_failure','local_security_increment','root_tax_failure','global_decorrelation_failure']:
  run(name)
