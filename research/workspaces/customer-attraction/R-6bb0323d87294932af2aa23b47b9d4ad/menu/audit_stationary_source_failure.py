"""Definition-level audit of named stationary-source restriction failure only.
No imports from customer_attraction, SPE solver, or exploratory numerical test.
"""
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5]
SRC=ROOT/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json'
d=json.loads(SRC.read_text());ins=d['instance'];nodes=d['nodes'];m=ins['players'];k=len(ins['topics'])
# Expand each positive multiplicity into separate, unit-value customer supports.
customers=[frozenset(c['topics']) for c in ins['customers'] for _ in range(c['multiplicity'])]
def payoff(a,q):return sum((F(1,sum(q[t] for t in B)) for B in customers if a in B),F())
def insertion(a,q):return sum((F(1,1+sum(q[t] for t in B)) for B in customers if a in B),F())
reachable=set();stack=[d['root']];comparisons=0;minimum=None
while stack:
 ni=stack.pop()
 if ni in reachable:continue
 reachable.add(ni);v=nodes[ni];counts=v['counts'];target=v['target'];a=v['action']
 assert len(counts)==len(target)==k and all(isinstance(x,int) and x>=0 for x in counts+target)
 assert sum(target)==m
 if sum(counts)==m:
  assert counts==target and a is None and not v['children'];continue
 assert sum(counts)<m and 0<=a<k and len(v['children'])==k
 assert nodes[v['children'][a]]['target']==target
 own=payoff(a,target)
 for b,ci in enumerate(v['children']):
  child=nodes[ci];expect=list(counts);expect[b]+=1;assert child['counts']==expect
  slack=own-payoff(b,child['target']);assert slack>=0
  minimum=slack if minimum is None else min(minimum,slack);comparisons+=1;stack.append(ci)
assert len(reachable)==len(nodes)
root=nodes[d['root']];cols=[nodes[ci]['target'] for ci in root['children']]
assert cols==d['root_columns'];u=payoff(root['action'],root['target'])
P=[[F(col[t]-(t==a),m-1) for a,col in enumerate(cols)] for t in range(k)]
K=[[insertion(t,col) for col in cols] for t in range(k)]
q=[F(3,14),F(1,14),F(1,7),F(1,14)]*2
assert sum(q)==1 and all(sum(P[t][a]*q[a] for a in range(k))==q[t] for t in range(k))
# General coordinate stationary equations: with block mass alpha,
# 7q_A=2-alpha, 7q_B=1-alpha, 7q_C=1, 7q_D=alpha.
# Their sum gives 8alpha=4. Verify these equations directly as linear forms.
for j in range(2):
 ids=list(range(4*j,4*j+4));A,B,C,D=ids
 expected={A:[F(2)-F(a in ids) for a in range(k)],B:[F(1)-F(a in ids) for a in range(k)],C:[F(1)]*k,D:[F(a in ids) for a in range(k)]}
 for t in ids:
  # 8q_t - E[count_t] = 7q_t - rhs; equality of coefficients.
  assert all(F(8*(a==t)-cols[a][t])==F(7*(a==t))-expected[t][a] for a in range(k))
query=[sum(K[t][a]*q[a] for a in range(k)) for t in range(k)];cap=max(query)
assert cap==F(2773,840) and u==F(13,4) and cap-u==F(43,840)
free=[F(),F(),F(1,14),F(3,7)]*2
fquery=[sum(K[t][a]*free[a] for a in range(k)) for t in range(k)]
assert max(fquery)==F(851,280)<u
out=dict(status='EXACT_NAMED_RESTRICTION_FAILURE_NOT_MFULL_OR_HALF',source=str(SRC.relative_to(ROOT)),customers=len(customers),players=m,topics=k,dag_nodes=len(nodes),all_ordered_decision_histories=sum(k**i for i in range(m)),local_comparisons=comparisons,minimum_IC_slack=str(minimum),root_u=str(u),Q=list(map(str,q)),query=list(map(str,query)),cap=str(cap),cap_minus_u=str(cap-u),stationary_uniqueness='coordinate equations force each block mass alpha=1/2',free_Q=list(map(str,free)),free_query=list(map(str,fquery)),free_cap=str(max(fquery)))
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
