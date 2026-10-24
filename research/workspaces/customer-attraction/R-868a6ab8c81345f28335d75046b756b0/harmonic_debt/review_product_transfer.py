"""Independent review of dynamic_matching's complete product certificate.
Reads only the deliverable instance/policy. No discovery script, expected
payoffs, canonical model, BI solver, or verifier is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'dynamic_matching'/'product_transfer_certificate.json'
x=json.loads(SOURCE.read_text()); ins=x['instance'];labels=ins['topics'];K=len(labels);m=ins['players']
unit=[frozenset(row['topics']) for row in ins['customers'] for _ in range(row['multiplicity'])]
policy={tuple(labels.index(a) for a in row['history']):labels.index(row['action']) for row in x['policy']}
expected={h for depth in range(m) for h in product(range(K),repeat=depth)}
assert len(policy)==len(x['policy']) and set(policy)==expected and len(unit)==10 and K==9 and m==3
# The product data must literally be disjoint copies of five unit customers.
base=(frozenset((1,)),frozenset((0,1)),frozenset((2,)),frozenset((0,2)),frozenset((0,2)))
vectors=tuple(product(range(3),repeat=2));assert labels==[''.join('ABC'[a] for a in v) for v in vectors]
expected_inc=[frozenset(t for t,v in enumerate(vectors) if v[k] in inc) for k in range(2) for inc in base]
assert sorted(map(sorted,unit))==sorted(map(sorted,expected_inc))
def utility(path,i,customers=unit):
 return sum((F(1,sum(a in inc for a in path)) for inc in customers if path[i] in inc),F())
def leaf(h):
 while len(h)<m:h=h+(policy[h],)
 return h
slacks=[]
for h in expected:
 z=leaf(h);u=utility(z,len(h))
 for a in range(K):slacks.append(u-utility(leaf(h+(a,)),len(h)))
assert min(slacks)>=0 and len(slacks)==819
# Derive component all terminal best-reply leaves from the five unit customers.
leaves=[];thresholds=[]
for a in range(3):
 values=[utility((1,a,b),2,base) for b in range(3)];mx=max(values)
 opts=[b for b,v in enumerate(values) if v==mx]
 thresholds.append(min(utility((1,a,b),1,base) for b in opts))
 for b in opts:
  leaves.append((a,b,utility((1,a,b),0,base),utility((1,a,b),1,base)))
theta=max(thresholds);assert theta==F(3,2)
component_L=min(d for a,b,d,v in leaves if v>=theta);assert component_L==F(3,2)
assert all(d>=v/2+F(1,2) for a,b,d,v in leaves)
# All product terminal BR leaves factor, because action vectors are unrestricted.
# Each such selected leaf is attainable by a tail SPE iff the second player's
# realized value is >= max_{vector action} min_{terminal BR vector} value =3.
product_theta=2*theta
feasible=[(p,q,p[2]+q[2],p[3]+q[3]) for p,q in product(leaves,repeat=2) if p[3]+q[3]>=product_theta]
product_L=min(row[2] for row in feasible);assert product_L==F(5,2)
bb=labels.index('BB');forced=leaf((bb,));assert [labels[a] for a in forced]==['BB','BC','CA']
assert [utility(forced,i) for i in range(3)]==[F(5,2),F(3),F(9,2)]
root=leaf(());w=len({c for c,inc in enumerate(unit) if any(a in inc for a in root)})
report={'review_status':'Exact independent audit passed; additivity of all-continuation L is false, no welfare or matching counterexample claimed.','component_best_reply_leaves':[{'second':'ABC'[a],'last':'ABC'[b],'root':str(d),'second_utility':str(v)} for a,b,d,v in leaves],'component_thresholds':list(map(str,thresholds)),'component_L_B':str(component_L),'product_threshold':str(product_theta),'product_L_BB':str(product_L),'exact_nonadditivity_gap':str(2*component_L-product_L),'all_product_BR_leaf_pairs':len(leaves)**2,'tail_SPE_feasible_pairs':len(feasible),'complete_histories':len(policy),'all_comparisons_including_self':len(slacks),'minimum_IC_slack':str(min(slacks)),'forced_path':[labels[a] for a in forced],'forced_payoffs':[str(utility(forced,i)) for i in range(3)],'root_path':[labels[a] for a in root],'root_payoffs':[str(utility(root,i)) for i in range(3)],'root_welfare':w}
(HERE/'product_transfer_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
