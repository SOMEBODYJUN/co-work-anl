"""Independent definition-level replay of the old 11-unit-client certificate.

Adds the exact actual extra-query matrix and exact LAST minimax certificate.
No canonical game, solver, certificate verifier, numpy, or scipy is imported.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
# Actor/menu/script -> workspaces/customer-attraction/actor/menu: parents[5] is repo.
source=ROOT/'examples/customer_attraction/coverage_opportunity_failure.json'
certfile=ROOT/'evidence/certificates/customer_attraction/coverage_opportunity_failure.json'
obj=json.loads(source.read_text());cert=json.loads(certfile.read_text())
k=len(obj['topics']);m=obj['players']
clients=[frozenset(t['topics']) for t in obj['customers'] for _ in range(t['multiplicity'])]
policy={tuple(t['history']):t['action'] for t in cert['actions']}
assert len(policy)==len(cert['actions'])
assert set(policy)=={h for d in range(m) for h in product(range(k),repeat=d)}
assert all(a in range(k) for a in policy.values())
def terminal(h):
    h=tuple(h)
    while len(h)<m:h+=(policy[h],)
    return h
def pay(z,i):
    return sum((F(1,sum(a in x for a in z)) for x in clients if z[i] in x),F(0))
def extra(z,T):
    return sum((F(1,1+sum(a in x for a in z)) for x in clients if T in x),F(0))
comparisons=[]
for h in policy:
    u=pay(terminal(h),len(h))
    for a in range(k):
        diff=u-pay(terminal(h+(a,)),len(h))
        assert diff>=0
        comparisons.append(diff)
z=terminal(());u=[pay(z,i) for i in range(m)]
W=sum(u);assert z==(0,0,1) and u==[F(5,2),F(5,2),F(3)] and W==8
queries=[extra(z,t) for t in range(k)]
assert queries==[F(5,3),F(3,2),F(3),F(5,2),F(5,2)]
assert m*max(queries)-W==1
# LAST uses b*=2 A, exactly one freely chosen static competitor.  Rows T,
# columns C; every full profile is (A,A,C), no deleted-slot approximation.
K=[[extra((0,0,c),t) for c in range(k)] for t in range(k)]
q=[F(0),F(1,3),F(1,3),F(1,6),F(1,6)]
p=q
row_values=[sum((q[c]*K[t][c] for c in range(k)),F(0)) for t in range(k)]
col_values=[sum((p[t]*K[t][c] for t in range(k)),F(0)) for c in range(k)]
assert max(row_values)==min(col_values)==F(7,3)
assert m*F(7,3)==7<W
# Exact matrices for all actual-position complete menus; columns preserve the
# original ordered prefix, current forced action and every true later reply.
menus=[]
for i in range(m):
    leaves=[terminal(z[:i]+(a,)) for a in range(k)]
    matrix=[[extra(leaf,t) for leaf in leaves] for t in range(k)]
    menus.append({'position':i+1,'forced_leaves':leaves,'matrix':matrix})
report={'identity':'independent recovery of an old finite certificate, not a new instance',
 'source':str(source.relative_to(ROOT)),'certificate':str(certfile.relative_to(ROOT)),
 'unit_clients':len(clients),'all_histories':len(policy),'all_compares':len(comparisons),
 'minimum_IC':str(min(comparisons)),'actual_leaf':z,'payoffs':list(map(str,u)),
 'W':str(W),'actual_extra_queries':list(map(str,queries)),
 'actual_extra_gap':str(m*max(queries)-W),
 'LAST_matrix':[[str(v) for v in row] for row in K],
 'LAST_primal_q':list(map(str,q)),'LAST_dual_p':list(map(str,p)),
 'LAST_primal_row_values':list(map(str,row_values)),
 'LAST_dual_column_values':list(map(str,col_values)),
 'LAST_value':'7/3','LAST_W_minus_mvalue':str(W-7),
 'complete_actual_position_menus':menus,
 'scope':'actual-extra average cap false; this example satisfies LAST and does not refute Mpath/FTA/half'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,default=lambda x:str(x),indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['unit_clients','all_histories','all_compares','actual_leaf','payoffs','W','actual_extra_queries','actual_extra_gap','LAST_value','LAST_W_minus_mvalue']}))
