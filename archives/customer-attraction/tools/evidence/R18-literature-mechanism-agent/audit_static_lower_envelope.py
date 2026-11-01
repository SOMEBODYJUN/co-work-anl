"""Definition-level exact audit; does not import the CAG implementation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
HERE=Path(__file__).parent
obj=json.loads((HERE/'static_lower_envelope_counterexample_min.json').read_text())
p=obj['p'];m=obj['m']
# Expand all unit clients, then compute payoffs without count compression.
clients=[frozenset(a for a in range(p) if mask>>a&1) for mask,n in enumerate(obj['types'],1) for _ in range(n)]
actions={tuple(x['history']):x['action'] for x in obj['certificate']['actions']}
def utility(z,i):
    return sum((F(1,sum(a in c for a in z)) for c in clients if z[i] in c),F())
def welfare(z):return sum(any(a in c for a in z) for c in clients)
def rollout(h):
    z=tuple(h)
    while len(z)<m:z=z+(actions[z],)
    return z
history_records=[]
for depth in range(m):
    for h in product(range(p),repeat=depth):
        actual=rollout(h);v=utility(actual,depth)
        vals=[utility(rollout(h+(a,)),depth) for a in range(p)]
        assert all(v>=x for x in vals)
        history_records.append({'history':h,'action':actions[h],'payoff':str(v),'deviation_values':list(map(str,vals))})
# Enumerate ordered static profiles, classify PNE, and retain a profitable witness
# for every non-equilibrium. This proves the minimum PNE welfare exactly.
pnes=[];non_pnes=[]
for z in product(range(p),repeat=m):
    witnesses=[]
    for i in range(m):
        for a in range(p):
            zz=z[:i]+(a,)+z[i+1:]
            if utility(zz,i)>utility(z,i):witnesses.append([i,a,str(utility(zz,i)-utility(z,i))])
    if not witnesses:pnes.append({'profile':z,'welfare':welfare(z)})
    else:non_pnes.append({'profile':z,'profitable_deviation':witnesses[0]})
actual=rollout(())
assert len(actions)==sum(p**i for i in range(m))==21
assert len(history_records)*p==84
assert welfare(actual)==21
assert {x['welfare'] for x in pnes}=={25}
assert max(welfare(z) for z in product(range(p),repeat=m))==25
report={'customers':len(clients),'histories':len(history_records),'comparisons':len(history_records)*p,'actual':actual,'actual_payoffs':[str(utility(actual,i)) for i in range(m)],'actual_welfare':welfare(actual),'static_equilibria':pnes,'non_equilibrium_witnesses':non_pnes,'history_checks':history_records,'opt':25}
(HERE/'static_lower_envelope_exact_audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['history_checks','non_equilibrium_witnesses']},indent=2))
