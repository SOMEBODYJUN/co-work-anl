"""Independent finite ordered-tree check of the frozen best case only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parent
old=json.loads((root/'original/asymmetric_t2.json').read_text())
new=json.loads((root/'asymmetric_t2.replay.json').read_text())
assert old==new
b=old['best']; k=3;t=2;m=5
names=b['names']; index={s:i for i,s in enumerate(names)}
# Distinct unit customers with physical topic memberships, not coefficient rows.
clients=[]
for i in range(k):
    clients += [frozenset([f'C{i}',f'A{i}']+[f'B{i}_{r}' for r in range(t)]) for _ in range(b['x'])]
    clients += [frozenset([f'A{i}']) for _ in range(b['a'])]
for r,(z,v) in enumerate(b['reserves']):
    clients += [frozenset([f'D{r}']+[f'B{i}_{r}' for i in range(k)]) for _ in range(z)]
    clients += [frozenset([f'D{r}']) for _ in range(v)]
assert len(clients)==32
pay={}
for suffix in product(names, repeat=3):
    terminal=('C0','C1')+suffix
    val=[]
    for action in terminal:
        val.append(sum((F(1,sum(a in c for a in terminal)) for c in clients if action in c),F()))
    pay[terminal]=tuple(val)
nodes=0
floors={}
def outcomes(h):
    global nodes
    nodes+=1
    if len(h)==m:return {h}
    child={a:outcomes(h+(a,)) for a in names}
    i=len(h)
    floor=max(min(pay[z][i] for z in rs) for rs in child.values())
    floors[h]=floor
    return {z for rs in child.values() for z in rs if pay[z][i]>=floor}
rs=outcomes(('C0','C1'))
def counts(z):return tuple(z.count(a) for a in names)
zs={counts(z) for z in rs}
target=tuple(int(s.startswith('C') or s.startswith('D')) for s in names)
assert len(zs)==b['R_size']==5
assert str(floors[('C0','C1')])==b['last_C_threshold']
assert (target in zs)==b['last_C_actual_target_achievable']==False
# This child was already visited in the full ordered recursion above.
a2=[z for z in pay if z[:3]==('C0','C1','A2')]
# Recompute its child only with a separately named subtree to retrieve its set;
# no original-module import or canonical-count caching is used.
start_nodes=nodes
ars=outcomes(('C0','C1','A2'))
min_a=min(pay[z][2] for z in ars)
witness=min(counts(z) for z in ars if pay[z][2]==min_a)
assert str(min_a)==b['deviate_own_A_min']=='7/2'
assert list(witness)==b['own_A_min_terminal']
report={'scope':'one saved best instance, independent unit-customer ordered-history set-valued backward induction; not arbitrary inputs or a new general theorem','original_and_replay_byte_identical':(root/'original/asymmetric_t2.json').read_bytes()==(root/'asymmetric_t2.replay.json').read_bytes(),'report_fields_equal':old==new,'k':k,'t':t,'players':m,'unit_clients':len(clients),'catalog_topics':len(names),'prefix':['C0','C1'],'root_tree_nodes':start_nodes,'all_terminal_ordered_histories':len(pay),'attainable_ordered_histories':len(rs),'attainable_terminal_counts':len(zs),'root_threshold':str(floors[('C0','C1')]),'target_counts_achievable':target in zs,'own_A2_min':str(min_a),'own_A2_min_terminal_counts':list(witness),'all_assertions_passed':True}
(root/'independent-best-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
