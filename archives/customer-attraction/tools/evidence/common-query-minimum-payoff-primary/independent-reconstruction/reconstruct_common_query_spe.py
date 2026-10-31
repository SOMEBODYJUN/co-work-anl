"""New independent exact reconstruction; missing historical DAG is not recreated bytewise.
All outcome sets are computed from backward induction over count prefixes.
The emitted count-and-target DAG is separately checked on 30 expanded clients.
No original builder, solver, optimization library, or network is imported.
"""
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
from time import perf_counter
import json

START=perf_counter();M=6;P=9;SCALE=60
NAMES=['A','B','T','D','E','P0','P1','P2','P3']
TYPES=[(9,2),(17,2),(2,3),(4,3),(26,2),(28,2)]+[(1<<a,4) for a in range(5,9)]
CLIENTS=[mask for mask,n in TYPES for _ in range(n)]
assert len(CLIENTS)==30

def counts(n):
    for z in combinations_with_replacement(range(P),n):
        q=[0]*P
        for a in z:q[a]+=1
        yield tuple(q)

def extend(k,a):
    q=list(k);q[a]+=1;return tuple(q)

terminals=list(counts(M));PAY={};W={}
for c in terminals:
    pay=[0]*P;covered=0
    for mask,n in TYPES:
        load=sum(c[a] for a in range(P) if mask>>a&1)
        if load:
            covered+=n
            for a in range(P):
                if mask>>a&1:pay[a]+=n*(SCALE//load)
    PAY[c]=pay;W[c]=covered
# Exact recurrence: children histories may independently select any SPE outcome.
R={c:{c} for c in terminals};LOW={};candidates=0
for d in range(M-1,-1,-1):
    for k in counts(d):
        children=[R[extend(k,a)] for a in range(P)]
        lo=[min(PAY[c][a] for c in children[a]) for a in range(P)]
        threshold=max(lo);out=set()
        for a in range(P):
            for c in children[a]:
                candidates+=1
                if PAY[c][a]>=threshold:out.add(c)
        assert out
        R[k]=out;LOW[k]=lo
root=(0,)*P;target=(1,1,0,0,0,1,1,1,1);path=[5,6,7,8,0,1]
assert target in R[root]
preferred={};k=root
for a in path:preferred[k]=a;k=extend(k,a)
nodes=[];cache={}

def build(k,c):
    key=(k,c)
    if key in cache:return cache[key]
    i=len(nodes);cache[key]=i;node={'prefix':list(k),'target':list(c)};nodes.append(node)
    if sum(k)==M:
        assert k==c;return i
    options=[a for a in range(P) if c in R[extend(k,a)] and PAY[c][a]>=max(LOW[k])]
    assert options
    a=preferred[k] if c==target and k in preferred and preferred[k] in options else min(options)
    node['action']=a;children=[]
    for b in range(P):
        kb=extend(k,b)
        cb=c if b==a else min(R[kb],key=lambda z:(PAY[z][b],z))
        children.append(build(kb,cb))
    node['children']=children;return i
root_id=build(root,target)
# Separate verifier uses literal clients, not PAY, R, LOW or grouped coefficients.
checks=0;decisions=0;leaves=0

def literal_profit(c,a):
    val=0
    for mask in CLIENTS:
        if mask>>a&1:
            load=sum(c[b] for b in range(P) if mask>>b&1)
            assert load>0;val+=60//load
    return val
for node in nodes:
    k=node['prefix'];c=node['target'];assert len(k)==len(c)==P and sum(c)==M and all(0<=a<=b for a,b in zip(k,c))
    if sum(k)==M:
        assert k==c and 'action' not in node;leaves+=1;continue
    decisions+=1;a=node['action'];assert len(node['children'])==P
    assert nodes[node['children'][a]]['target']==c
    own=literal_profit(c,a)
    for b,j in enumerate(node['children']):
        child=nodes[j];assert tuple(child['prefix'])==extend(tuple(k),b)
        assert own>=literal_profit(child['target'],b)
        checks+=1
z=[];i=root_id
while 'action' in nodes[i]:
    a=nodes[i]['action'];z.append(a);i=nodes[i]['children'][a]
assert z==path and nodes[i]['target']==list(target)
pay_actual=[literal_profit(target,a)//60 for a in z]
assert pay_actual==[4,4,4,4,4,5]
# The number of ordered histories follows every action edge including repeats.
ways={root_id:1}
for d in range(M):
    nxt={}
    assert sum(ways.values())==P**d
    for i,n in ways.items():
        for j in nodes[i]['children']:nxt[j]=nxt.get(j,0)+n
    ways=nxt
assert sum(ways.values())==P**M
opt=max(W.values());assert opt==26 and W[target]==25
frozen=sum(literal_profit(extend(tuple(target[b]-(1 if b==a else 0) for b in range(P)),2),2) for a in path)
assert frozen==30*60
report={'status':'passed','provenance':'new definition-level reconstruction from original mathematical note; historical source DAG/code absent; no byte-reproduction claim','players':M,'topics':NAMES,'unit_customers':len(CLIENTS),'count_prefix_states':len(R),'all_count_prefix_states_expected':comb(15,9),'root_reachable_terminal_count_vectors':len(R[root]),'candidate_action_terminal_checks':candidates,'new_dag_nodes':len(nodes),'new_dag_decisions':decisions,'new_dag_leaves':leaves,'new_dag_including_self_IC':checks,'new_dag_nonself_IC':checks-decisions,'ordered_nonterminal_histories':sum(P**d for d in range(M)),'ordered_leaves':P**M,'actual_path':[NAMES[a] for a in z],'actual_utilities':pay_actual,'W':W[target],'OPT6':opt,'all_six_slot_multisets':len(terminals),'F_T':frozen//60,'CQ_min_rhs':29,'CQ_min_violation':1,'original_program_entries':0,'new_independent_program_entries':1,'optimization_calls':0,'elapsed_seconds':perf_counter()-START}
destination=Path(__file__).resolve().parent
(destination/'reconstructed-dag.json').write_text(json.dumps({'topics':NAMES,'types':TYPES,'root':root_id,'nodes':nodes},separators=(',',':'))+'\n')
(destination/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
