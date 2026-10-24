"""One exact old input tests a precise proposed all-input normal form.

Not a search over inputs or player counts. Customers are distinct unit clients.
The full ordered-history SPE endpoint correspondence follows directly from
the max-of-child-minima gluing condition proved in the accompanying notes.
"""
from fractions import Fraction as F
from itertools import product
import json

COUNTS={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2}
CLIENTS=[s for s,n in COUNTS.items() for _ in range(n)]
M,K=3,6

def utility(z,i):
    return sum((F(1,sum((s>>a)&1 for a in z)) for s in CLIENTS if (s>>z[i])&1),F(0))
def welfare(z):
    return sum(any((s>>a)&1 for a in z) for s in CLIENTS)

NODES=[]
def endpoints(h):
    if len(h)==M:return [h]
    children={a:endpoints(h+(a,)) for a in range(K)}
    i=len(h)
    minima=[min(utility(z,i) for z in children[a]) for a in range(K)]
    threshold=max(minima)
    result=[z for a in range(K) for z in children[a] if utility(z,i)>=threshold]
    assert result
    NODES.append({"history":h,"child_minima":minima,"threshold":threshold,
                  "SPE_endpoints":result})
    return result

root=endpoints(())
W=min(map(welfare,root))
worst=[z for z in root if welfare(z)==W]
patterns=sorted(set(tuple(utility(z,i) for i in range(M)) for z in worst))
last_min=min(utility(z,M-1) for z in worst)
assert len(CLIENTS)==34 and len(NODES)==43 and len(root)==40
assert W==32 and len(worst)==8
assert patterns==[(F(29,3),F(67,6),F(67,6))]
assert last_min>F(W,M)
report={"tested_all_input_candidate":"There exists a minimum-welfare full SPE with last utility <= W/m",
        "candidate_false_on_this_old_input":True,"unit_clients":len(CLIENTS),
        "customer_mask_multiplicities":COUNTS,"players":M,"topics":K,
        "ordered_decision_histories":len(NODES),"ordered_terminal_profiles":K**M,
        "all_root_SPE_endpoints":root,"minimum_SPE_welfare":W,
        "all_minimum_welfare_endpoints":worst,"all_minimum_welfare_pay_patterns":patterns,
        "minimum_last_utility_among_worst_SPE":last_min,"W_divided_by_m":F(W,M),
        "optimal_coverage":max(welfare(z) for z in product(range(K),repeat=M)),
        "ordered_history_endpoint_certificate":sorted(NODES,key=lambda v:(len(v['history']),v['history'])),
        "scope":"Only the new normalization shortcut is false. The input and its full SPE mechanism are old. HALF remains open."}
print(json.dumps(report,default=str,indent=2))
