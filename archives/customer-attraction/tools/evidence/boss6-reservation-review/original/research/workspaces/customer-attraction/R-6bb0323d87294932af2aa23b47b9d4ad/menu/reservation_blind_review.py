"""Independent definition-level audit of the reservation positive-depth witness.
Reads only raw game, full ordered policy and rational minimax candidates.
No imports from the canonical model/solver, discovery code, or source audit.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'research/workspaces/customer-attraction/R-6bb0323d87294932af2aa23b47b9d4ad'
game=json.loads((BASE/'security/positive_depth_floor_game.json').read_text())
raw=json.loads((BASE/'security/positive_depth_floor_certificate.json').read_text())
m=game['players'];k=len(game['topics']);assert (m,k)==(4,7)
customers=[]
for row in game['customers']:
 assert isinstance(row['multiplicity'],int) and row['multiplicity']>0
 B=frozenset(row['topics']);assert all(isinstance(t,int) and 0<=t<k for t in B)
 customers.extend([B]*row['multiplicity'])
assert len(customers)==53
sets=[frozenset(x for x,B in enumerate(customers) if a in B) for a in range(k)]
assert len(set(sets))==k
assert len(sets[6])==19 and all(not (sets[6]&sets[a]) for a in range(6))
actions={}
for row in raw['strategy']['actions']:
 h=tuple(row['history']);assert h not in actions;actions[h]=row['action']
expected={h for d in range(m) for h in product(range(k),repeat=d)}
assert set(actions)==expected
assert all(isinstance(a,int) and 0<=a<k for a in actions.values())
def payoff(position,z):
 a=z[position]
 return sum((F(1,sum(b in B for b in z)) for B in customers if a in B),F())
def coverage(z):return sum(any(a in B for a in z) for B in customers)
def insertion(a,rivals):
 return sum((F(1,1+sum(b in B for b in rivals)) for B in customers if a in B),F())
# Rebuild every leaf solely from the full ordered policy.
leaf={h:h for h in product(range(k),repeat=m)}
for d in reversed(range(m)):
 for h in product(range(k),repeat=d):leaf[h]=leaf[h+(actions[h],)]
assert tuple(raw['strategy']['terminal_counts'])==tuple(leaf[()].count(a) for a in range(k))
strict=ties=checked=0;minimum=None
for h in sorted(expected,key=lambda h:(len(h),h)):
 own=payoff(len(h),leaf[h])
 for b in range(k):
  alt=payoff(len(h),leaf[h+(b,)])
  gap=own-alt;assert gap>=0,(h,b,gap)
  checked+=1
  if b!=actions[h]:
   if gap>0:strict+=1
   else:ties+=1
   minimum=gap if minimum is None else min(minimum,gap)
z=leaf[()];u=[payoff(i,z) for i in range(m)];W=coverage(z)
assert z==(6,0,3,4) and u==[F(19),F(29,3),F(67,6),F(67,6)]
assert sum(u)==W==51
opt=max(coverage(z) for z in product(range(k),repeat=m));assert opt==53
p=[F(x) for x in raw['security']['primary']]
v=F(raw['security']['value'])
Q=[(tuple(row['rivals']),F(row['probability'])) for row in raw['security']['dual']]
assert len(p)==k and min(p)>=0 and sum(p)==1
assert all(len(r)==m-1 and all(0<=a<k for a in r) and q>=0 for r,q in Q)
assert sum(q for r,q in Q)==1
# Every ordered three-rival tuple, including every repeat and every permutation.
background_values={r:sum((p[a]*insertion(a,r) for a in range(k)),F()) for r in product(range(k),repeat=m-1)}
assert min(background_values.values())==v
assert all(value>=v for value in background_values.values())
dual_values=[sum((q*insertion(a,r) for r,q in Q),F()) for a in range(k)]
assert all(value==v for value in dual_values)
assert v==F(28481,2924) and v-u[1]==F(647,8772)>0
# Additional source-lift hypotheses are verified from the actual finite data;
# the finite policy check above does not rely on the general lift theorem.
old_sizes=[len(sets[a]) for a in range(6)]
delta=[min(len(sets[a]&sets[b]) for b in range(6)) for a in range(6)]
thresholds=[F(old_sizes[a])-F(delta[a],2) for a in range(6)]
eta=min(payoff(len(h),leaf[h]) for h in expected if h and h[0]==6 and all(a<6 for a in h[1:]))
assert F(19,2)<=eta and 19>=max(thresholds) and F(min(old_sizes),2)>F(19,3)
root_deviations=[payoff(0,leaf[(a,)]) for a in range(k)]
output=dict(status='PASS_EXACT_POSITIVE_DEPTH_ORIGINAL_TOTAL_M_FLOOR_COUNTEREXAMPLE_ONLY',
 scope='Refutes for every SPE and every position i>=2, u_i>=v_m(0); does not refute aggregate security, Mfull/Mpath or half.',
 raw_game=str((BASE/'security/positive_depth_floor_game.json').relative_to(ROOT)),
 raw_policy_and_minimax=str((BASE/'security/positive_depth_floor_certificate.json').relative_to(ROOT)),
 customers=len(customers),players=m,topics=k,distinct_catalog_coverages=len(set(sets)),
 full_ordered_decision_histories=len(expected),all_ordered_terminals=k**m,IC_comparisons_including_self=checked,
 nonself_strict=strict,nonself_ties=ties,minimum_nonself_IC_gap=str(minimum),actual_path=list(z),payoffs=list(map(str,u)),W=W,OPT=opt,
 root_forced_payoffs=list(map(str,root_deviations)),
 security_value=str(v),security_primal=list(map(str,p)),security_dual=[dict(rivals=list(r),probability=str(q)) for r,q in Q],
 tested_ordered_rival_tuples=len(background_values),minimum_primal_value=str(min(background_values.values())),
 primal_ordered_tight_count=sum(value==v for value in background_values.values()),dual_query_values=list(map(str,dual_values)),
 positive_depth_position=2,v_minus_u2=str(v-u[1]),aggregate_margin_W_minus_m_v=str(F(W)-m*v),half_margin_2W_minus_OPT=2*W-opt,
 lift_hypotheses=dict(old_sizes=old_sizes,delta=delta,root_reservation_thresholds=list(map(str,thresholds)),eta=str(eta),J=19))
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(output,indent=2));print(json.dumps(output,indent=2))
