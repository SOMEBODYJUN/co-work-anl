"""Explore W(SPE) >= minimum static coarse-correlated welfare.
Numerical LP only until an exact dual certificate is independently verified.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import random,sys,json
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate

def min_cce(g):
 k,m=g.topic_count,g.players
 qs=[tuple(t.count(a) for a in range(k)) for t in combinations_with_replacement(range(k),m)]
 W=[g.welfare(q) for q in qs];A=[]
 U={q:g.topic_payoffs(q) for q in qs}
 for a in range(k):
  row=[]
  for q,w in zip(qs,W):
   d=F(0)
   for b in range(k):
    if q[b]:
     r=list(q);r[b]-=1;r[a]+=1;d+=q[b]*U[tuple(r)][a]
   row.append(float(d-w))
  A.append(row)
 r=linprog(W,A_ub=A,b_ub=[0]*k,A_eq=[np.ones(len(qs))],b_eq=[1],bounds=(0,None),method='highs')
 assert r.success,r.message
 return r,qs,W

def main():
 rng=random.Random(44004);total=0;best=1e9
 for m,k,runs in [(2,3,100),(3,4,600),(4,5,600),(5,7,300)]:
  for run in range(runs):
   w={}
   for _ in range(rng.randrange(3,18)):
    mask=rng.randrange(1,1<<k);w[mask]=rng.randrange(1,15)
   g=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k)if mask>>a&1),v)for mask,v in sorted(w.items())),m)
   s=ExactSPESolver(g);sw=s.minimum_welfare();r,qs,W=min_cce(g);total+=1
   if r.fun>sw+1e-7:
    cert=s.certificate(min(s.worst_outcomes()));verify_certificate(g,cert).assert_valid()
    print(json.dumps({'status':'numerical-bridge-counterexample-needs-exact-dual','seed':44004,'trials':total,'instance':g.to_dict(),'spe_welfare':sw,'min_cce_lp':r.fun,'lp_dual':r.ineqlin.marginals.tolist(),'lp_equality_dual':r.eqlin.marginals.tolist(),'certificate':cert.to_dict()},indent=2));return
   best=min(best,(sw-r.fun)/max(1,sw))
  print(json.dumps({'trials':total,'m':m,'k':k,'best_relative_gap':best}),file=sys.stderr,flush=True)
 print(json.dumps({'status':'finite-no-counterexample','trials':total,'seed':44004,'best_relative_gap':best}))
if __name__=='__main__':main()
