"""Definition-level exact audit of a specified old 34-customer policy.
Does not import the canonical model, solver, or the source's audit code.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json'
data=json.loads(SOURCE.read_text())
obj=data['instance']; labels=obj['topics']; m=obj['players']; n=len(labels)
customers=[frozenset(t['topics']) for t in obj['customers'] for _ in range(t.get('multiplicity',1))]
actions={tuple(t['history']):t['action'] for t in data['certificate']['actions']}
expected={h for k in range(m) for h in product(range(n),repeat=k)}
assert set(actions)==expected

def play(prefix=()):
    z=tuple(prefix)
    while len(z)<m:z+=actions[z],
    return z

def loads(z):return tuple(sum(a in s for a in z) for s in customers)
def payoff(a,z):return sum((F(1,c) for s,c in zip(customers,loads(z)) if a in s),F(0))
def entry(a,z):return sum((F(1,c+1) for s,c in zip(customers,loads(z)) if a in s),F(0))

checked=0
for h in expected:
    chosen=actions[h]; own=payoff(chosen,play(h+(chosen,)))
    for a in range(n):
        if a==chosen:continue
        assert own>=payoff(a,play(h+(a,)))
        checked+=1
path=play(); W=sum(c>0 for c in loads(path)); B=F(W,m)
endpoints={(i,a):play(path[:i]+(a,)) for i in range(m) for a in range(n)}
E=labels.index('Empty'); X2=labels.index('X2')
actual_col=[entry(a,path) for a in range(n)]
root_empty=endpoints[(0,E)]
diffs=[a-b for a,b in zip(loads(path),loads(root_empty))]
assert min(diffs)>=0
assert max(actual_col)==F(17,2)<B
assert path==(0,3,4) and root_empty==(6,0,1)
D=sum((payoff(X2,endpoints[(i,X2)]) for i in range(m)),F(0))
H=sum((entry(X2,endpoints[(i,E)]) for i in range(m)),F(0))
G=sum((entry(X2,endpoints[(i,X2)]) for i in range(m)),F(0))
assert (D,H,G)==(F(63,2),F(65,2),F(41,2))
e=F(1,24); strong_D=e*D; strong_G=e*(1-e)*H+e*e*G
assert strong_D-strong_G==F(-1,48)
# This is the FULL minimum over all actual positions and forced actions.
min_X2=min(entry(X2,z) for z in endpoints.values())
assert min_X2==F(13,2)
report={
 'scope':'One specified old 34-unit-customer complete pure SPE; exact all-history audit and all-query pure-column rescue. No general half or unrestricted-menu theorem.',
 'source':str(SOURCE.relative_to(ROOT)), 'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'customers':len(customers),'players':m,'topics':n,'checked_histories':len(expected),'checked_nonself_deviations':checked,
 'path':list(path),'actual_payoffs':[str(payoff(a,path)) for a in path], 'welfare':W,'budget_W_over_m':str(B),
 'all_endpoint_count_with_duplicates':len(endpoints),'distinct_endpoints':len(set(endpoints.values())),
 'actual_column_entries':dict(zip(labels,map(str,actual_col))), 'actual_column_maximum':str(max(actual_col)),
 'root_empty_endpoint':list(root_empty),'actual_minus_root_empty_customer_loads':diffs,
 'D_q':str(D),'H_empty_q':str(H),'G_q':str(G),'epsilon':str(e),'strong_D':str(strong_D),'strong_G':str(strong_G),'strong_D_minus_G':str(strong_D-strong_G),
 'min_all_positions_all_actions_query_X2':str(min_X2),'empty_diluted_full_minimum_at_epsilon':str(e*min_X2),
 'all_endpoints':[{'position':i+1,'forced_action':labels[a],'terminal':list(z),'entries':[str(entry(t,z)) for t in range(n)]} for (i,a),z in sorted(endpoints.items())],
 'all_checks_passed':True,
}
out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['checked_histories','checked_nonself_deviations','welfare','budget_W_over_m','actual_column_maximum','D_q','H_empty_q','G_q','min_all_positions_all_actions_query_X2','all_checks_passed']},indent=2))
