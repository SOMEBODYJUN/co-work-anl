"""Exact standalone audit of a monotone concave DR potential bridge failure.

No input from the discovery file and no optimization library. The potential
and supporting supergradients are hardcoded integers on sum(q)<=4.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

F = {
 (0,0,0):0,
 (0,0,1):12,(0,1,0):16,(1,0,0):20,
 (0,0,2):22,(0,1,1):28,(0,2,0):32,(1,0,1):28,(1,1,0):36,(2,0,0):34,
 (0,0,3):22,(0,1,2):38,(0,2,1):44,(0,3,0):48,(1,0,2):34,
 (1,1,1):44,(1,2,0):48,(2,0,1):41,(2,1,0):48,(3,0,0):48,
 (0,0,4):22,(0,1,3):38,(0,2,2):54,(0,3,1):60,(0,4,0):48,
 (1,0,3):34,(1,1,2):50,(1,2,1):56,(1,3,0):48,(2,0,2):41,
 (2,1,1):52,(2,2,0):48,(3,0,1):48,(3,1,0):48,(4,0,0):48,
}
G = {
 (0,0,0):(20,16,12),
 (0,0,1):(20,16,12),(0,1,0):(20,16,12),(1,0,0):(20,16,12),
 (0,0,2):(12,16,0),(0,1,1):(18,16,10),(0,2,0):(20,16,12),
 (1,0,1):(14,16,8),(1,1,0):(12,12,12),(2,0,0):(14,16,8),
 (0,0,3):(12,16,0),(0,1,2):(12,16,0),(0,2,1):(18,16,10),
 (0,3,0):(0,0,12),(1,0,2):(7,16,0),(1,1,1):(14,16,8),
 (1,2,0):(0,0,12),(2,0,1):(7,16,0),(2,1,0):(0,0,12),(3,0,0):(0,4,0),
 (0,0,4):(12,16,0),(0,1,3):(12,16,0),(0,2,2):(2,6,0),
 (0,3,1):(0,0,0),(0,4,0):(0,0,12),(1,0,3):(7,16,0),
 (1,1,2):(2,6,0),(1,2,1):(0,4,0),(1,3,0):(0,0,12),
 (2,0,2):(7,16,0),(2,1,1):(0,4,0),(2,2,0):(0,0,12),
 (3,0,1):(0,4,0),(3,1,0):(0,0,12),(4,0,0):(0,4,0),
}
PLANES=[
 (0,20,16,12),(2,18,16,10),(6,14,16,8),(12,12,12,12),
 (22,12,16,0),(27,7,16,0),(42,2,6,0),(48,0,0,12),
 (48,0,4,0),(60,0,0,0),
]
def add(q,a):return tuple(x+int(i==a)for i,x in enumerate(q))
def sub(q,a):return tuple(x-int(i==a)for i,x in enumerate(q))
def counts(h):return tuple(h.count(a)for a in range(3))
assert set(F)==set(G)=={q for q in product(range(5),repeat=3)if sum(q)<=4}
assert all(F[q]==min(h+sum(g*x for g,x in zip(v,q))for h,*v in PLANES)for q in F)
assert all(x>=0 for g in G.values()for x in g)
support_slacks=[]
for q in F:
 for r in F:
  support_slacks.append(F[q]+sum(G[q][a]*(r[a]-q[a])for a in range(3))-F[r])
assert min(support_slacks)>=0
monotone=[];dr=[]
for q in F:
 if sum(q)<4:
  monotone.extend(F[add(q,a)]-F[q]for a in range(3))
 if sum(q)<3:
  for a in range(3):
   for b in range(a,3):
    dr.append(F[add(q,a)]+F[add(q,b)]-F[q]-F[add(add(q,a),b)])
assert min(monotone)>=0 and min(dr)>=0

# Full ordered strategy. Two histories with the same counts may be assigned
# the same action in this particular witness; no restriction is imposed on CAG.
POLICY={
 (0,0,0):1,
 (1,0,0):0,(0,1,0):2,(0,0,1):1,
 (2,0,0):0,(1,1,0):0,(1,0,1):1,
 (0,2,0):0,(0,1,1):1,(0,0,2):1,
}
def sigma(h):return POLICY[counts(h)]
def finish(h):
 while len(h)<3:h+=(sigma(h),)
 return h
def u(h,a):
 q=counts(h)
 assert q[a]>0
 return F[q]-F[sub(q,a)]
comparisons=[]
for d in range(3):
 for h in product(range(3),repeat=d):
  a=sigma(h);pay=u(finish(h),a)
  vals=[u(finish(h+(b,)),b)for b in range(3)]
  assert pay==vals[a] and pay>=max(vals)
  comparisons.append(dict(history=h,action=a,payoff=pay,deviation_payoffs=vals))
actual=finish(());q=counts(actual)
payoffs=[u(actual,a)for a in actual];W=sum(payoffs)
entries=[F[add(q,a)]-F[q]for a in range(3)]
J=sum(q[a]*entries[a]for a in range(3));credit=W-J;M=max(entries)
assert actual==(1,2,1)and payoffs==[16,12,16]and W==44
assert entries==[12,16,10]and J==42 and credit==2
assert 3*M-(W+credit)==2

# This is not even a harmonic CAG potential with signed customer coefficients:
# duplicating a single theme must multiply its singleton value by H_2.
assert F[(2,0,0)]==34 and Q(3,2)*F[(1,0,0)]==30
# A completely monotone sharing kernel would be convex as a sequence. Here
# the single-label-1 forward differences are 16,16,16,0, violating convexity.
increments=[F[(0,k,0)]-F[(0,k-1,0)]for k in range(1,5)]
assert increments==[16,16,16,0]
assert increments[3]-2*increments[2]+increments[1]==-16

report=dict(status='EXACT_WIDER_CONCAVE_POTENTIAL_COUNTEREXAMPLE',
 scope='Not CAG; does not refute the CAG insertion-credit bridge or Q-CAG-HALF',
 grid_points=len(F),affine_pieces=len(PLANES),supporting_plane_comparisons=len(support_slacks),
 minimum_support_slack=min(support_slacks),monotonicity_comparisons=len(monotone),
 minimum_monotone_increment=min(monotone),DR_comparisons=len(dr),minimum_DR_slack=min(dr),
 ordered_histories=len(comparisons),SPE_action_comparisons=3*len(comparisons),
 all_history_table=comparisons,actual=actual,actual_counts=q,payoffs=payoffs,W=W,
 entry_values=entries,J=J,credit=credit,M=M,VI_gap=3*M+J-2*W,
 harmonic_single_clone_gap=str(Q(F[(2,0,0)])-Q(3,2)*F[(1,0,0)]),
 complete_monotone_convexity_gap=increments[3]-2*increments[2]+increments[1])
out=Path(__file__).with_name('concave_potential_exact_audit.json')
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='all_history_table'},indent=2))
