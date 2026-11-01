from pathlib import Path
import json,math
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
D=Path(__file__).resolve().parent
r=json.loads((D/'largest_incumbent_n3p6_best.json').read_text());n=3;p=6;L=6;A={tuple(z['history']):z['action'] for z in r['strategy']['actions']}
@lru_cache(None)
def term(h):return h if len(h)==n else term(h+(A[h],))
def row(z,a):return [L//sum(b==j for b in z for j in range(p) if mask>>j&1) if mask>>a&1 else 0 for mask in range(1,1<<p)]
G=[]
for h in A:
 if not h:continue
 own=np.array(row(term(h),A[h]))
 for a in range(p):G.append(own-np.array(row(term(h+(a,)),a)))
for a in range(1,p):G.append(np.array([int(mask&1>0)-int(mask>>a&1) for mask in range(1,1<<p)]))
weights=[0]*((1<<p)-1)
for t in r['instance']['customers']:weights[sum(1<<a for a in t['topics'])-1]=t['multiplicity']
J=max(combinations(range(p),n),key=lambda J:sum(w for mask,w in enumerate(weights,1) if any(mask>>a&1 for a in J)))
o=np.array([int(any(mask>>a&1 for a in J)) for mask in range(1,1<<p)])
G.append(L*o-(2*n-1)*np.array(row(term(()),0)))
mat=np.array(G,dtype=float);lb=np.zeros(len(G));lb[-1]=1
res=milp(np.ones(2**p-1),integrality=np.ones(2**p-1),bounds=Bounds(np.zeros(2**p-1),np.full(2**p-1,np.inf)),constraints=LinearConstraint(mat,lb,np.full(len(G),np.inf)),options={'time_limit':120})
if res.x is None:print(res.message);raise SystemExit
w=[round(x) for x in res.x]
assert np.all(mat@w>=lb)
game={'topics':list(map(str,range(p))),'players':n,'customers':[{'topics':[a for a in range(p) if mask>>a&1],'multiplicity':v} for mask,v in enumerate(w,1) if v]}
def u(z,a):return sum((F(v,sum(b in t['topics'] for b in z)) for t in game['customers'] for v in [t['multiplicity']] if a in t['topics']),F(0))
def W(z):return sum(t['multiplicity'] for t in game['customers'] if any(a in t['topics'] for a in z))
checks=[]
for h in A:
 if not h:continue
 for a in range(p):
  slack=u(term(h),A[h])-u(term(h+(a,)),a);assert slack>=0
  checks.append(str(slack))
sizes=[sum(t['multiplicity'] for t in game['customers'] if a in t['topics']) for a in range(p)];assert sizes[0]==max(sizes)
O=max(W(J) for J in combinations(range(p),n));actual=term(());x=u(actual,0);assert O>(2*n-1)*x
out={'scope':'Counterexample only to maximum-cardinality theme as a guaranteed action; root is forced and need not be optimal. Every positive-depth history is SPE. Not a full SPE or half-coverage counterexample.','instance':game,'strategy':{'actions':[{'history':list(h),'action':a} for h,a in sorted(A.items())]},'actual':actual,'topic_sizes':sizes,'u_forced_incumbent':str(x),'OPT':O,'W':W(actual),'ratio':str(F(O,x)),'all_suffix_comparisons':len(checks),'root_deviation_values':[str(u(term((a,)),a)) for a in range(p)],'milp_status':res.message}
(D/'largest_incumbent_small_counterexample.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['strategy','instance']}));print(game)
