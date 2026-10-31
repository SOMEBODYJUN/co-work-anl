"""Targeted complete-cone attack of a necessary all-input residual cut.
No random policies or scans.  The sole source is the existing root-tax policy.
For the fixed optimal multiset ABCD, seek nonnegative customer weights for
which every permutation violates the same owner-causal suffix inventory cut.
An optimum <=0 is only a fixed-cone failure to separate.
"""
from fractions import Fraction as F
from itertools import product, permutations, combinations_with_replacement
from functools import lru_cache
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
P=Path(__file__).resolve().parent
ROOT=P.parents[5]
src=ROOT/'evidence/certificates/customer_attraction/root_tax_failure.json'
data=json.loads(src.read_text())['strategy']
s={tuple(z['history']):z['action'] for z in data['actions']}
m=1+max(map(len,s)); k=1+max(a for h in s for a in h+(s[h],))
likes=tuple(frozenset(a for a in range(k) if mask>>a&1) for mask in range(1,1<<k))
@lru_cache(None)
def finish(h):return h if len(h)==m else finish(h+(s[h],))
def pay(z,i):
 return tuple(F(int(z[i] in L),sum(a in L for a in z)) if z[i] in L else F() for L in likes)
def cover(z):return tuple(F(any(a in L for a in z)) for L in likes)
B=finish(()); U=[pay(B,i) for i in range(m)]
rows=[]
for h in s:
 on=pay(finish(h),len(h))
 for a in range(k):
  if a!=s[h]:
   alt=pay(finish(h+(a,)),len(h));rows.append(tuple(v-u for u,v in zip(on,alt)))
icn=len(rows)
T0=(0,1,2,3); O=cover(T0)
for T in combinations_with_replacement(range(k),m):rows.append(tuple(a-b for a,b in zip(cover(T),O)))
optrows=len(rows)-icn
Ts=tuple(permutations(T0))
def cut(T,start):
 result=[]
 for L in likes:
  b=sum(a in L for a in B);t=sum(a in L for a in T)
  val=F()
  if t:
   for i in range(m):
    if T[i] not in L:continue
    d=b+1-int(B[i] in L)
    pb=sum(B[j] in L and T[j] not in L for j in range(m) if j!=i)
    if i>=start:val+=F(1,t)-F(pb,t*d)
    for j in range(start,m):
     if j!=i and B[j] in L and T[j] not in L:val+=F(1,t*d)
  val-=2*sum(U[j][len(result)] for j in range(start,m))
  result.append(val)
 return tuple(result)
outputs=[]
for start in range(1,m):
 cuts=[cut(T,start) for T in Ts]
 # max z s.t. every permutation cut(w)>=z and sum weights=1.
 A=[tuple(v)+(F(),) for v in rows]+[tuple(-v for v in c)+(F(1),) for c in cuts]
 obj=[0.]*len(likes)+[-1.]
 fit=linprog(obj,A_ub=np.array(A,dtype=float),b_ub=np.zeros(len(A)),A_eq=[[1.]*len(likes)+[0.]],b_eq=[1.],bounds=[(0,None)]*len(likes)+[(None,None)],method='highs')
 assert fit.success,fit.message
 w=tuple(F(float(v)).limit_denominator(10**7) for v in fit.x[:-1])
 exact_ic=min(-sum((a*b for a,b in zip(row,w)),F()) for row in rows)
 gap=min(sum((a*b for a,b in zip(c,w)),F()) for c in cuts)
 outputs.append({'first_suffix_role_1based':start+1,'numeric_max_min_cut_violation':-fit.fun,'rationalized_min_constraint_slack':str(exact_ic),'rationalized_min_cut_gap':str(gap),'positive_separator':bool(exact_ic>=0 and gap>0)})
out={'scope':'Targeted necessary-cut attack, not a HALF proof or counterexample.','source_strategy':str(src.relative_to(ROOT)),'fixed_optimal_multiset':T0,'actual_path':B,'players':m,'topics':k,'customer_incidence_variables':len(likes),'all_ordered_IC_rows':icn,'optimality_rows':optrows,'permutations':len(Ts),'results':outputs}
with (P/'suffix_inventory_cone_attack.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
