"""Expanded unit-customer audit; does not import the repository model/oracle.

The frozen full strategy was discovered with the exact oracle, but its validity
and the local-credit violation are recomputed directly from definitions here.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import json
BASE=Path(__file__).resolve().parent
inst=json.loads((BASE/'exclusive_credit_four_instance.json').read_text())
cert=json.loads((BASE/'exclusive_credit_four_certificate.json').read_text())
labels=inst['topics'];p=len(labels);m=inst['players']
likes=[]
for row in inst['customers']:
 likes.extend([frozenset(row['topics'])]*row['multiplicity'])
actions={tuple(x['history']):x['action'] for x in cert['actions']}
expected={h for depth in range(m) for h in product(range(p),repeat=depth)}
assert set(actions)==expected
assert all(0<=a<p for a in actions.values())
def terminal(h):
 while len(h)<m:h+=(actions[h],)
 return h
def utility(a,z):
 return sum((F(1,sum(t in x for t in z)) for x in likes if a in x),F(0))
checks=[]
for h in sorted(expected,key=lambda h:(len(h),h)):
 a=actions[h];good=utility(a,terminal(h))
 for b in range(p):
  alt=utility(b,terminal(h+(b,)));assert good>=alt,(h,a,b,good,alt)
  checks.append(good-alt)
z=terminal(());assert z==(0,0,1,2)
loads=[sum(a in x for a in z) for x in likes]
W=sum(c>0 for c in loads)
G=sum((F(1,c+1) for c in loads if c),F(0))
queries=[sum((F(1,c+1) for x,c in zip(likes,loads) if a in x),F(0)) for a in range(p)]
exclusive=sum((F(1,2) for x,c in zip(likes,loads) if z[0] in x and c==1),F(0))
OPT=max(sum(any(a in x for a in seq) for x in likes) for seq in product(range(p),repeat=m))
root=utility(z[0],z)
assert root==F(13,4) and exclusive==0 and max(queries)==F(37,10)
assert root+exclusive-max(queries)==-F(9,20)
assert W==OPT==16
result={'status':'direct_definition_audit_passed','unit_customers':len(likes),'histories':len(expected),'including_self_action_comparisons':len(checks),'proper_deviations':len(expected)*(p-1),'minimum_incentive_slack':str(min(checks)),'actual':[labels[a] for a in z],'payoffs':[str(utility(a,z)) for a in z],'W':W,'OPT':OPT,'G1':str(G),'entrant_values':dict(zip(labels,map(str,queries))),'exclusive_first_credit':str(exclusive),'local_credit_gap':str(root+exclusive-max(queries)),'global_credit_gap':str(W+G-m*max(queries))}
print(json.dumps(result,indent=2))
(BASE/'exclusive_credit_audit.json').write_text(json.dumps(result,indent=2)+'\n')
