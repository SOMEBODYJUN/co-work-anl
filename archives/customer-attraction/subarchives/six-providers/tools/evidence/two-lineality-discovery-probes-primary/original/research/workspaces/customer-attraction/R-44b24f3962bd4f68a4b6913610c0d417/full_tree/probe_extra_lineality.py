"""Discovery-only formal-policy scan; first found example forces equal covers.
No universal claim is inferred from this numerical search.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import importlib.util
import numpy as np
from scipy.optimize import linprog
# Resolve colleague's already reviewed graph utility from the actor sibling.
path=Path(__file__).resolve().parents[2]/'R-7e9f44beea424d469713364afe7dd180/full_tree_dual/audit_outcome_payoff_graph.py'
spec=importlib.util.spec_from_file_location('graph_audit',path)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
for p,n in [(2,3),(2,4)]:
 hs=[h for d in range(n) for h in product(range(p),repeat=d)]
 for idx,acts in enumerate(product(range(p),repeat=len(hs))):
  sigma=dict(zip(hs,acts));data=g.analyse_strategy(p,n,sigma)
  G=data['rows'];ks=list(G);arr=np.array([G[k] for k in ks],dtype=float)
  H=data['internal_rows'];rk=g.rank(H)
  for j,k in enumerate(ks):
   row=G[k]
   if g.rank(H+[row])==rk: continue
   res=linprog(np.ones(len(ks)),A_eq=arr.T,b_eq=-arr[j],bounds=(0,None),method='highs')
   if res.success:
    mult=[Q(float(x)).limit_denominator(1000000) for x in res.x]
    if all(sum(v*G[t][i] for v,t in zip(mult,ks))==-row[i] for i in range((1<<p)-1)):
     print('FOUND',p,n,idx,'Hrank',rk,'new',k,'row',row,'sigma',sigma,'lambda',[(t,v) for t,v in zip(ks,mult) if v]);raise SystemExit
 print('finished',p,n)
