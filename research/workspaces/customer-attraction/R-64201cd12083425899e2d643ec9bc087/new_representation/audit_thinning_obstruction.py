"""Independent exact arithmetic replay; imports no canonical game/solver code.
Finite arithmetic checks support the explicit witness. Unbounded lifting and
moment claims are proved in thinning_transfer_obstruction.md, not by this run.
"""
from fractions import Fraction
from itertools import product,combinations_with_replacement
from pathlib import Path
import json

BASE=Path(__file__).parent
spec=json.loads((BASE/'kernel_no_common_parameter.json').read_text())
labels=spec['topics'];p=len(labels);m=spec['players']
assert (p,m)==(4,3)
customers=[frozenset(c['topics']) for c in spec['customers'] for _ in range(c['multiplicity'])]
assert len(customers)==13
sigma={tuple(h):a for h,a in spec['actions']}
assert set(sigma)=={h for d in range(m) for h in product(range(p),repeat=d)}

def terminal(history):
    while len(history)<m:
        history=history+(sigma[history],)
    return history

def payoff(outcome,player):
    a=outcome[player]
    return sum((Fraction(1,sum(b in B for b in outcome)) for B in customers if a in B),Fraction(0))

def kernel(outcome,player):
    row=[0]*m
    for B in customers:
        if outcome[player] in B:
            row[sum(b in B for b in outcome)-1]+=1
    return row

comparisons=0
rows=[]
min_slack=None
for d in range(m):
    for h in product(range(p),repeat=d):
        actual=terminal(h)
        values=[]
        for a in range(p):
            dev=terminal(h+(a,))
            actual_value=payoff(actual,d)
            dev_value=payoff(dev,d)
            slack=actual_value-dev_value
            assert slack>=0,(h,a,actual,dev,slack)
            k1=kernel(actual,d);k2=kernel(dev,d)
            polynomial=[x-y for x,y in zip(k1,k2)]
            assert sum((Fraction(c,j+1) for j,c in enumerate(polynomial)),Fraction(0))==slack
            comparisons+=1;values.append(str(dev_value))
            min_slack=slack if min_slack is None else min(min_slack,slack)
        rows.append({'history':[labels[a] for a in h],'action':labels[sigma[h]],'deviation_payoffs':values})

expected={((1,0),3):[0,-2,3],((3,0),2):[-2,4,0],((3,3),1):[1,0,-3]}
for (h,a),wanted in expected.items():
    actual=kernel(terminal(h),len(h));deviation=kernel(terminal(h+(a,)),len(h))
    assert [x-y for x,y in zip(actual,deviation)]==wanted
    assert sum(Fraction(c,j+1) for j,c in enumerate(wanted))==0
# Exact incompatibility: middle row t≥1/2; first then t≥2/3;
# third imposes t²≤1/3, but (2/3)²>1/3.
assert Fraction(2,3)**2>Fraction(1,3)
path=terminal(())
assert path==(1,2,3)
values=[payoff(path,i) for i in range(m)]
assert values==[Fraction(5),Fraction(9,2),Fraction(7,2)]
welfare=sum(any(a in B for a in path) for B in customers)
opt=max(sum(any(a in B for a in actions) for B in customers) for actions in combinations_with_replacement(range(p),m))
assert welfare==opt==13

# Arithmetic sanity checks for the uniform-in-m all-big construction.
for total in range(1,41):
    for r in range(1,total+1):
        for b in range(total-r+1):
            assert Fraction(total,b+r)>=1
for t in [Fraction(0),Fraction(1,2),Fraction(9,10),Fraction(99,100)]:
    total=2
    while total*t**(total-1)>=1:
        total+=1
    assert total*t**(total-1)<1

report={'status':'passed','unit_customers':len(customers),'ordered_decision_histories':len(sigma),'exact_one_step_comparisons':comparisons,'minimum_harmonic_slack':str(min_slack),'root_path':[labels[a] for a in path],'root_payoffs':list(map(str,values)),'root_welfare':welfare,'OPT':opt,'incompatible_component_rows':[{'history':[labels[x] for x in h],'deviation':labels[a],'coefficients':v} for (h,a),v in expected.items()],'all_history_payoff_table':rows,'scope':'Explicit complete 3-player witness audited exactly; unbounded lifting and moment obstruction are analytic proofs in the accompanying note.'}
(BASE/'audit_thinning_obstruction.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='all_history_payoff_table'},indent=2))
