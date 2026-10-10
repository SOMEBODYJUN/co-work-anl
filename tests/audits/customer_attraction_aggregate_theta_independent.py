"""Direct expansion of the 36 distinct unit customers, with no solver imports."""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[2]
INPUT=ROOT/'examples/customer_attraction/aggregate_theta_failure.json'
CERTIFICATE=ROOT/'evidence/certificates/customer_attraction/aggregate_theta_failure.json'
X,Y=tuple(range(3)),tuple(range(3,6))
labels=X+Y
# Each list entry is one individual, unweighted customer. Repeated interest
# sets in this list are distinct unit customers, not weighted customers.
customers=[frozenset([a,b]) for a in X for b in Y]
customers += [frozenset(a+b) for a in combinations(X,2)
              for b in combinations(Y,2) for copy in range(3)]
assert len(customers)==36
themes={a:frozenset(i for i,c in enumerate(customers) if a in c) for a in labels}
assert {len(t) for t in themes.values()}=={21}

def payoff(i,outcome):
    return sum((Q(1,sum(x in themes[a] for a in outcome))
                for x in themes[outcome[i]]),Q())

def coverage(outcome):
    return len(set().union(*(themes[a] for a in outcome)))

def group(a): return X if a in X else Y
def policy(h):
    if not h: return 0
    if len(h)==1: return min(Y if h[0] in X else X)
    a,b=h
    return min(set(group(b))-set(h))

def terminal(h):
    while len(h)<3: h += (policy(h),)
    return h

input_data=json.loads(INPUT.read_text())
certificate=json.loads(CERTIFICATE.read_text())
assert input_data['players']==3 and len(input_data['topics'])==6
assert {tuple(row['history']):row['action'] for row in certificate['strategy']['actions']}=={
    h:policy(h) for k in range(3) for h in product(labels,repeat=k)}
input_customers=[frozenset(row['topics']) for row in input_data['customers']
                 for copy in range(row['multiplicity'])]
assert sorted(map(sorted,input_customers))==sorted(map(sorted,customers))

rows=[]
last_table={}
second_table={}
for k in range(3):
    for h in product(labels,repeat=k):
        outcome=terminal(h)
        actual=payoff(k,outcome)
        deviations=[]
        for a in labels:
            deviation=terminal(h+(a,))
            u=payoff(k,deviation)
            assert actual>=u,(h,a,actual,u)
            rows.append(actual-u)
            deviations.append(str(u))
        if k==2: last_table[str(h)]=deviations
        if k==1: second_table[str(h)]=deviations

theta_by_h={h:max(payoff(2,h+(a,)) for a in labels)
            for h in product(labels,repeat=2)}
theta=min(theta_by_h.values())
root=terminal(())
W=coverage(root)
OPT=max(coverage(s) for s in product(labels,repeat=3))
assert root==(0,3,4) and W==34 and OPT==36 and theta==12
assert [payoff(i,root) for i in range(3)]==[10,12,12]
assert {v for h,v in theta_by_h.items() if h[0]==h[1]}=={Q(15)}
assert {v for h,v in theta_by_h.items() if h[0]!=h[1]}=={Q(12)}
result={
    'review':'independently expanded all 36 individual unit customers; no solver imports',
    'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [INPUT,CERTIFICATE,Path(__file__).resolve()]},
    'unit_customers':36,'theme_sizes':[len(themes[a]) for a in labels],
    'all_history_nodes':43,'exact_SPE_inequalities':len(rows),
    'min_SPE_slack':str(min(rows)),
    'root_outcome':root,'root_payoffs':[str(payoff(i,root)) for i in range(3)],
    'root_action_deviation_payoffs':[str(payoff(0,terminal((a,)))) for a in labels],
    'W':W,'OPT':OPT,'theta':str(theta),'n_theta':str(3*theta),
    'aggregate_deficit':str(3*theta-W),
    'distinct_prefix_best_reply':'12','repeat_prefix_best_reply':'15',
    'second_action_deviation_payoffs_after_0':second_table[str((0,))],
    'last_action_payoffs_after_00':last_table[str((0,0))],
    'last_action_payoffs_after_01':last_table[str((0,1))],
    'last_action_payoffs_after_03':last_table[str((0,3))],
    'status':'VALID aggregate-floor counterexample; halfcoverage satisfied'
}
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
report=json.dumps(result,indent=2)+'\n'
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as handle:
        handle.write(report)
print(report,end='')
