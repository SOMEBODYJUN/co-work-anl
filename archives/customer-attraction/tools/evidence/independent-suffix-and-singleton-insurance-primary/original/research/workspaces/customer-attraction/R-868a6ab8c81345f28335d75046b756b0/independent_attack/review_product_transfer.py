"""Independent expanded-unit-client audit of sibling's product certificate.
Does not import its constructor, canonical solver, model or auditor.
"""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'dynamic_matching/product_transfer_certificate.json'
payload=json.loads(SOURCE.read_text())
labels=payload['instance']['topics']; m=payload['instance']['players']; p=len(labels)
clients=[]
for row in payload['instance']['customers']:
    clients.extend([frozenset(row['topics'])]*row['multiplicity'])
policy={tuple(labels.index(a) for a in row['history']):labels.index(row['action']) for row in payload['policy']}
expected={h for d in range(m) for h in product(range(p),repeat=d)}
assert set(policy)==expected

def u(path,i):
    return sum((F(1,sum(a in inc for a in path)) for inc in clients if path[i] in inc),F(0))

def leaf(h):
    while len(h)<m:h=h+(policy[h],)
    return h

minimum=None;nrows=0
for h in sorted(expected,key=lambda h:(len(h),h)):
    depth=len(h); actual=u(leaf(h),depth)
    for a in range(p):
        slack=actual-u(leaf(h+(a,)),depth)
        assert slack>=0,(h,a,slack)
        minimum=slack if minimum is None else min(minimum,slack)
        nrows+=1

# All suffix SPE ordered leaves, not count-cached and independent of policy.
def suffix_outcomes(h):
    if len(h)==m:return {h}
    i=len(h);children=[suffix_outcomes(h+(a,)) for a in range(p)]
    floors=[min(u(z,i) for z in c) for c in children]
    threshold=max(floors)
    return {z for c in children for z in c if u(z,i)>=threshold}

bb=labels.index('BB'); prod_L=min(u(z,0) for z in suffix_outcomes((bb,)))
assert prod_L==F(5,2)
forced=leaf((bb,));assert tuple(labels[a] for a in forced)==('BB','BC','CA')
assert tuple(u(forced,i) for i in range(m))==(F(5,2),F(3),F(9,2))

# Analytic four-point menu in §4, checked from five explicit component clients.
base=(frozenset((1,)),frozenset((0,1)),frozenset((2,)),frozenset((0,2)),frozenset((0,2)))
def ub(z,i):
    return sum((F(1,sum(a in inc for a in z)) for inc in base if z[i] in inc),F(0))
points=[];floors=[]
for b in range(3):
    val=max(ub((1,b,c),2) for c in range(3))
    cs=[c for c in range(3) if ub((1,b,c),2)==val]
    floors.append(min(ub((1,b,c),1) for c in cs))
    for c in cs:
        points.append((ub((1,b,c),0),ub((1,b,c),1),b,c))
theta=max(floors);assert theta==F(3,2)
assert points==[(F(3,2),F(3,2),0,2),(F(1),F(1),1,2),(F(3,2),F(2),2,0),(F(2),F(3,2),2,2)]
assert all(d>=v/2+F(1,2) for d,v,*_ in points)
single_L=min(d for d,v,*_ in points if v>=theta)
vals=[d for d,v,*_ in points if v>=theta]
for j,point in enumerate(points):
    d,v,*_=point
    for e,w,*_ in points[:j]:
        if (v-theta)*(w-theta)<0:
            prob=(theta-w)/(v-w)
            vals.append(prob*d+(1-prob)*e)
barL=min(vals)
assert single_L==F(3,2) and barL==F(5,4)

actual=leaf(())
report={
 'scope':'Independent finite witness verification plus separate analytic review of the all-m rounding lemma; no half counterexample.',
 'decision_histories':len(expected),'all_action_comparisons':nrows,'minimum_slack':str(minimum),
 'actual_path':[labels[a] for a in actual], 'actual_payoffs':[str(u(actual,i)) for i in range(m)],
 'actual_W':sum(any(a in inc for a in actual) for inc in clients),
 'component_L_B':str(single_L),'component_barL_B':str(barL),'product_L_BB':str(prod_L),
 'forced_BB_path':[labels[a] for a in forced],
 'forced_BB_payoffs':[str(u(forced,i)) for i in range(m)]}
(HERE/'review_product_transfer_exact.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
