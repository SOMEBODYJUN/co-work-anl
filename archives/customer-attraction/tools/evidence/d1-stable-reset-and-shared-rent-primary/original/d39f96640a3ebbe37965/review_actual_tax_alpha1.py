"""Independent alpha=1 consequence of the old 13-player compact SPE packet.

Every ordered history is interpreted as an automaton run. All nodes and all
six observed-action transitions are checked, so exponential history expansion
is unnecessary. Does not import the old verifier, game model, or constructor.
"""
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import gzip, json
ROOT=Path(__file__).resolve().parents[5]
packet=ROOT/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
with gzip.open(packet,'rt') as f:data=json.load(f)
inst=data['instance'];m=inst['players'];k=len(inst['topics']);nodes=data['nodes'];root=data['root']
clients=[frozenset(t['topics']) for t in inst['customers'] for _ in range(t['multiplicity'])]
assert m==13 and k==6 and len(clients)==36
assert nodes[root]['counts']==[0]*k
assert all(isinstance(v,int) and v>=0 for row in nodes for v in row['counts'])
seen=set();pending=[root]
while pending:
    j=pending.pop()
    if j in seen:continue
    seen.add(j);node=nodes[j];counts=node['counts'];depth=sum(counts)
    assert len(counts)==k and depth<=m
    if depth==m:
        assert node.get('terminal') and not node.get('children')
    else:
        assert not node.get('terminal') and len(node['children'])==k
        assert node['action'] in range(k)
        for a,child in enumerate(node['children']):
            assert isinstance(child,int) and child in range(len(nodes))
            expected=[v+int(b==a) for b,v in enumerate(counts)]
            assert nodes[child]['counts']==expected
            pending.append(child)
assert seen==set(range(len(nodes)))
# Each player has unit weight. Integer scale computes exact 1/load for every
# expanded unit client. No sampled or partial action-history checks occur.
scale=lcm(*range(1,m+1));paycache={}
def utility(counts,a):
    key=(counts,a)
    if key not in paycache:
        value=0
        for likes in clients:
            if a in likes:
                c=sum(counts[b] for b in likes)
                assert c>0 and scale%c==0
                value+=scale//c
        paycache[key]=value
    return paycache[key]
leaf={};comparisons=0;min_gap=None
for j in sorted(seen,key=lambda j:sum(nodes[j]['counts']),reverse=True):
    node=nodes[j]
    if node.get('terminal'):
        leaf[j]=tuple(node['counts']);continue
    a=node['action'];children=node['children'];leaf[j]=leaf[children[a]]
    actual=utility(leaf[j],a)
    for b,child in enumerate(children):
        gap=actual-utility(leaf[child],b)
        assert gap>=0,(j,b,gap)
        min_gap=gap if min_gap is None else min(min_gap,gap)
        comparisons+=1
j=root;path=[]
while not nodes[j].get('terminal'):
    a=nodes[j]['action'];path.append(a);j=nodes[j]['children'][a]
assert path==[5]*10+[0,0,1]
counts=leaf[root];payoffs=[F(utility(counts,a),scale) for a in path]
assert payoffs==[F(5,2)]*12+[F(3)]
loads=[sum(counts[b] for b in likes) for likes in clients]
W=sum(c>0 for c in loads);G=sum((F(1,1+c) for c in loads if c>0),F(0))
g=[sum((F(1,1+c) for likes,c in zip(clients,loads) if a in likes),F(0)) for a in range(k)]
assert W==33 and G==F(359,66) and max(g)==3
assert m*max(g)-W-G==F(37,66)>0
report={'identity':'independent exact replay plus alpha=1 arithmetic consequence of old packet',
 'packet':str(packet.relative_to(ROOT)),'all_nodes_reachable':len(seen),
 'decision_nodes':sum(not n.get('terminal',False) for n in nodes),
 'all_exact_IC_comparisons':comparisons,'minimum_IC':str(F(min_gap,scale)),
 'actual_path':path,'payoffs':list(map(str,payoffs)),'W':W,'G_alpha1':str(G),
 'queries_alpha1':list(map(str,g)),'mmaxquery_minus_W_G':str(m*max(g)-W-G),
 'm_lastpayoff_minus_W_G':str(m*payoffs[-1]-W-G),
 'scope':'refutes actual-load tax bridges at alpha=1; does not refute LAST, Mpath, FTA, or half'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
