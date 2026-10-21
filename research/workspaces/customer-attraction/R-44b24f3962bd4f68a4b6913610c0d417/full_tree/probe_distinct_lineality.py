"""Discovery-only real-SPE scan, seed840013, up to300 samples.
Candidate certification is in audit_lattice_circulation.py.
"""
from fractions import Fraction as Q
from pathlib import Path
from random import Random
import importlib.util
import sys
import numpy as np
from scipy.optimize import linprog
root=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(root))
from customer_attraction import CustomerType,Instance,ExactSPESolver
path=Path(__file__).resolve().parents[2]/'R-7e9f44beea424d469713364afe7dd180/full_tree_dual/audit_outcome_payoff_graph.py'
spec=importlib.util.spec_from_file_location('graph_audit',path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rng=Random(840013)
for trial in range(300):
 p,n=3,3
 w=tuple(rng.randrange(4) for b in range(1,1<<p))
 if any(not any(w[b-1] and (bool(b>>a&1)!=bool(b>>c&1)) for b in range(1,1<<p)) for a in range(p) for c in range(a)):
  continue
 ins=Instance(tuple(str(j) for j in range(p)),tuple(CustomerType(tuple(j for j in range(p) if b>>j&1),w[b-1]) for b in range(1,1<<p) if w[b-1]),n)
 solver=ExactSPESolver(ins)
 sigma=solver.certificate(rng.choice(tuple(solver.outcomes())),action_selector=lambda h,cs:rng.choice(cs),continuation_selector=lambda h,cs:rng.choice(cs)).actions
 data=g.analyse_strategy(p,n,sigma);G=data['rows'];ks=list(G);arr=np.array([G[k] for k in ks],dtype=float)
 H=data['internal_rows'];rk=g.rank(H)
 for j,k in enumerate(ks):
  row=G[k]
  if g.rank(H+[row])==rk: continue
  res=linprog(np.ones(len(ks)),A_eq=arr.T,b_eq=-arr[j],bounds=(0,None),method='highs')
  if res.success:
   mult=[Q(float(x)).limit_denominator(1000000) for x in res.x]
   if all(sum(v*G[t][i] for v,t in zip(mult,ks))==-row[i] for i in range((1<<p)-1)):
    print('FOUND trial',trial,'types',w,'Hrank',rk,'new',k,'row',row,'sigma',sigma,'lambda',[(t,v) for t,v in zip(ks,mult) if v]);raise SystemExit
print('NO_CANDIDATE',trial+1)
