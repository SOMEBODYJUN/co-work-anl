"""Structural readers used in B4; do not replay mature IC or coefficient audits."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]

def walk(x, counts):
    counts[type(x).__name__] = counts.get(type(x).__name__,0)+1
    if isinstance(x,dict):
        for k,v in x.items():
            walk(k,counts)
            walk(v,counts)
    elif isinstance(x,list):
        for v in x:
            walk(v,counts)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def components():
    root = REPO/'archives/customer-attraction/tools/half5-exact/components'
    out = []
    for name in ['deep_root_query.json','background_player2.json','background_player3.json',
                 'priced_player2.json','priced_player3.json','maxroot_four_copy.json',
                 'max_background_player2.json']:
        p=root/name
        x=json.loads(p.read_text())
        counts={}
        walk(x,counts)
        rows=x if isinstance(x,list) else [x]
        records=[]
        for i,r in enumerate(rows):
            m={k:F(v) for k,v in r.get('multipliers',r.get('weights')).items()}
            assert all(v>=0 for v in m.values())
            records.append(dict(index=i,top_fields=list(r),multiplier_count=len(m),
                                positive_keys=[k for k,v in m.items() if v>0],
                                zero_multiplier_keys=[k for k,v in m.items() if v==0]))
        out.append(dict(path=str(p.relative_to(REPO)),sha256=sha(p),bytes=p.stat().st_size,
                        all_nodes_consumed=counts,records=records))
    return dict(purpose='Full structural consumption of seven related component inputs; no coefficient-state replay',
                input_files=out,components=sum(len(r['records']) for r in out),new_coefficient_states=0)

def comparison():
    root=REPO/'archives/customer-attraction/tools/evidence/population-cce-original-diagnostic-two-primary/original'
    ps=[root/'examples/customer_attraction/five_individual_security.json',
        root/'evidence/certificates/customer_attraction/five_individual_security.json']
    g,c=[json.loads(p.read_text()) for p in ps]
    counts={}
    for x in (g,c):
        walk(x,counts)
    pol={tuple(t['history']):t['action'] for t in c['strategy']['actions']}
    assert set(pol)=={h for n in range(5) for h in product(range(10),repeat=n)}
    assert all(0<=a<10 for a in pol.values())
    p=list(map(F,c['security']['primary']))
    assert min(p)>=0 and sum(p)==1
    z=()
    while len(z)<5:
        z+=(pol[z],)
    raw=HERE/'original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/direct/one_k_cone_diagnostic.json'
    assert list(map(str,p))==json.loads(raw.read_text())['p']
    return dict(purpose='Read available comparison inputs completely; no IC or LP replay and no historical-run SHA attribution',
                inputs=[dict(path=str(p.relative_to(REPO)),sha256=sha(p),bytes=p.stat().st_size) for p in ps],
                all_nodes_consumed=counts,players=g['players'],topic_labels=len(g['topics']),
                customer_types=len(g['customers']),unit_customer_count=sum(t['multiplicity'] for t in g['customers']),
                complete_decision_histories=len(pol),actual_path=z,fixed_query_valid=True,
                query_matches_frozen_cone_report=True,new_IC_comparisons=0)

if __name__=='__main__':
    for name,reader in [('component-input-consumption.json',components),('comparison-inputs.json',comparison)]:
        (HERE/name).write_text(json.dumps(reader(),indent=2)+'\n')
