"""Definition-level exact audit, independent of customer_attraction package."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path
p=Path(__file__).with_name('residual_counterexample.json')
data=json.loads(p.read_text());obj=data['instance'];labels=obj['topics'];customers=obj['customers']
actions={tuple(item['history']):item['action'] for item in data['certificate']['actions']}
assert len(actions)==7

def pay(path,j):
    return sum((F(item['multiplicity'],sum(a in item['topics'] for a in path))
                for item in customers if path[j] in item['topics']),F(0))
def cover(path):
    return {c for c,item in enumerate(customers) if any(a in item['topics'] for a in path)}
def mass(cs):return sum(customers[c]['multiplicity'] for c in cs)
for a in range(6):
    chosen=actions[(a,)]
    vals=[pay((a,b),1) for b in range(6)]
    assert vals[chosen]==max(vals)
    assert pay((a,chosen),0)==6
assert actions[()]==0
actual=(0,actions[(0,)])
C=cover(actual);O=cover((2,3));W=mass(C);residual=mass(O-C)
opt=max(mass(cover(pair)) for pair in combinations_with_replacement(range(6),2))
assert actual==(0,1) and W==13 and residual==14 and opt==14
assert not C&O
assert 2*W>=opt
# Complete ordered one-step comparisons: 6 root + 6*6 last-node comparisons.
comparisons=6+6*6
print(json.dumps({'valid':True,'decision_nodes':len(actions),'comparisons':comparisons,
                  'unit_customers':sum(i['multiplicity'] for i in customers),
                  'actual_welfare':W,'residual_union':residual,'optimal_welfare':opt},indent=2))
