"""Materialize all histogram orbits in the parent's ROW3 relaxation, then
compute faithful entire pure-SPE outcome sets for its 18-theme three-player
subgame. This tests whether the relaxed prescribed response motif is credible;
it is not a five-player counterexample or a proof of ROW3.
"""
import itertools,json,math,sys
from pathlib import Path
from functools import lru_cache
import numpy as np
BASE=Path(__file__).resolve().parent
SRC=BASE.parent/'parent'/'row3_relaxation.json'
rows=json.loads(SRC.read_text())['support']
weights={}
for item in rows:
 p,c,d,e,h=item['state'];assert p==0
 atoms=tuple(itertools.chain.from_iterable([[(j//4,(j//2)%2,j%2)]*n for j,n in enumerate(h)]))
 perms=set(itertools.permutations(atoms))
 for types in perms:
  mask=c+2*d+4*e
  for j,(t,r,s) in enumerate(types):
   mask|=(t<<(3+j))|(r<<(8+j))|(s<<(13+j))
  weights[mask]=weights.get(mask,0)+item['weight']/len(perms)
K=18;N=3; masks=list(weights);w=np.array([weights[m] for m in masks]);bits=np.array([[(m>>a)&1 for m in masks] for a in range(K)],float)
term={};mins={};floor={}
def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
@lru_cache(None)
def pay(q):
 cnt=np.asarray(q)@bits
 return np.divide(bits,cnt,out=np.zeros_like(bits),where=cnt>0)@w
@lru_cache(None)
def R(q):
 if sum(q)==N:return frozenset([q])
 children=[R(inc(q,a)) for a in range(K)]
 mn=tuple(min(pay(z)[a] for z in children[a]) for a in range(K)); f=max(mn)
 mins[q]=mn;floor[q]=f
 return frozenset(z for a in range(K) for z in children[a] if pay(z)[a]>=f-1e-10)
def W(q):return float(((np.asarray(q)@bits)>0)@w)
def count(seq):return tuple(seq.count(a) for a in range(K))
root=(0,)*K;out=R(root); actual=count([0,1,2]);opt=tuple(range(3,8));
row_relaxed=sum(pay(count([3+j,8+j,13+j]))[3+j] for j in range(5))
O=W(count(list(opt)))
result={"scope":"float diagnostic on full three-player outcome sets; not a certificate","topics":K,"customer_types":len(weights),"root_outcomes":len(out),"target_CDE_is_SPE":actual in out,"target_W":W(actual),"comparison_union":O,"relaxed_row":float(row_relaxed),"relaxed_O_minus_row":float(O-row_relaxed),"actual_node_floor":float(floor[root]),"actual_CDE_payoffs":pay(actual).tolist(),"query_minima":[float(mins[root][a]) for a in opt]}
# All branches Tj,Rj,Sj must be SPE from the Tj node, not merely fit the
# aggregate tax and BR rows. Identify exact source of any failure.
result['motif_child_failures']=[]
for j in range(5):
 q=count([3+j]);z=count([3+j,8+j,13+j])
 result['motif_child_failures'].append({"j":j,"terminal_in_child_R":z in R(q),"R_payoff":float(pay(z)[8+j]),"child_floor":float(floor[q])})
best=None
for z in out:
 gap=O-W(z)
 for a in range(K):
  if z in R(inc(root,a)) and pay(z)[a]>=floor[root]-1e-10:
   row=sum(mins[root][t] for t in opt)+(pay(z)[a]-mins[root][a])*(a in opt)
   val=row-gap
   if best is None or val<best['row_slack']:
    best={"terminal_counts":z,"first_action":a,"W":W(z),"row":float(row),"row_slack":float(val)}
result['best_true_ROW_root']=best
(BASE/'materialized_relaxation_audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
