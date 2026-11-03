"""Read every saved field; rebuild finite maps, never solve or import old code."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

REPO = next(p for p in Path(__file__).resolve().parents if (p/'cleanup/inventory.jsonl').is_file())
WORK = Path(__file__).resolve().parent
EVID = REPO/'archives/customer-attraction/tools/evidence/iterative-fixed-strategy-20261103b'
EVID.mkdir(parents=True, exist_ok=True)
inventory = {x['id']: x for x in map(json.loads, (REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
primary = [('92673436af2a98f8b6fc','iteration_m5p7.json'),('b1883658b123519c0645','iterative_search.py'),('8ece575448dc70e766a8','m5p7_path00011.json')]
related = [('1e831bf3e7df4a75596d','markov_joint.py'),('1d6be437e6381566d008','workspace_README.md')]

def write(name, value):
    (EVID/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def preserve(items, acquisition, dest):
    manifest=[]
    for sid, name in items:
        record=deepcopy(inventory[sid]); data=(WORK/acquisition/name).read_bytes()
        assert len(data)==record['size'] and sha256(data).hexdigest()==record['sha256']
        path=EVID/dest/name; path.parent.mkdir(parents=True, exist_ok=True);path.write_bytes(data)
        record['preserved_path']=str(path.relative_to(REPO));manifest.append(record)
    return manifest

write('source-manifest.json',preserve(primary,'acquisition','original'))
write('related-manifest.json',preserve(related,'related','related'))
deps=[]
for record in inventory.values():
    if record['path'] not in {'customer_attraction/__init__.py','customer_attraction/model.py','customer_attraction/exact.py','customer_attraction/certificate.py','tests/audits/customer_attraction_strategy_lp.py','tests/audits/cone_attack_credible_variants.py'}:continue
    src=REPO/'archives/customer-attraction/tools/evidence/strategy-cones/original'/record['path']
    data=src.read_bytes();assert len(data)==record['size'] and sha256(data).hexdigest()==record['sha256']
    dst=EVID/'dependencies'/record['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
    deps.append(record|{'existing_path':str(src.relative_to(REPO)),'preserved_path':str(dst.relative_to(REPO))})
assert len(deps)==6
write('dependency-manifest.json',deps)
reviews={};readings={}
for _,name in (primary[0],primary[2]):
    original=json.loads((EVID/'original'/name).read_text());view=deepcopy(original)
    batch=original['batches'][0];p,m=batch['topics'],batch['players'];record=batch['cone_proofs'][0]
    items=record['strategy']['actions'];expected=[h for d in range(m) for h in product(range(p),repeat=d)]
    assert [tuple(x['history']) for x in items]==expected
    assert all(set(x)=={'history','action'} and type(x['action']) is int and x['action'] in range(p) for x in items)
    actions={tuple(x['history']):x['action'] for x in items};groups={}
    for h,a in actions.items():
        q=tuple(h.count(t) for t in range(p));groups.setdefault(q,set()).add(a)
    assert all(len(a)==1 for a in groups.values())
    table=[{'counts':list(q),'action':next(iter(groups[q]))} for q in sorted(groups,key=lambda q:(sum(q),q))]
    current=()
    while len(current)<m:current+=(actions[current],)
    counts=[current.count(a) for a in range(p)]
    assert counts==record['root_counts']==record['strategy']['terminal_counts']
    proof=record['portfolio_proofs'][0];clones=proof['integer_clones']
    assert len(clones)==(1<<p)-1 and all(type(c) is int and c>=0 for c in clones)
    sparse=[[mask,c] for mask,c in enumerate(clones,1) if c]
    compressed=view['batches'][0]['cone_proofs'][0]['strategy']
    del compressed['actions']
    compressed['action_representation']={'encoding':'all-ordered-histories-from-count-table','order':'depth-then-lex','count_table':table}
    cloneview=view['batches'][0]['cone_proofs'][0]['portfolio_proofs'][0]
    del cloneview['integer_clones'];cloneview['integer_clones_sparse']={'length':len(clones),'default':0,'nonzero':sparse}
    decoded=deepcopy(view);z=decoded['batches'][0]['cone_proofs'][0]
    t={tuple(x['counts']):x['action'] for x in z['strategy'].pop('action_representation')['count_table']}
    z['strategy']['actions']=[{'history':list(h),'action':t[tuple(h.count(a) for a in range(p))]} for h in expected]
    cv=z['portfolio_proofs'][0];sp=cv.pop('integer_clones_sparse');full=[sp['default']]*sp['length']
    for mask,c in sp['nonzero']:full[mask-1]=c
    cv['integer_clones']=full
    assert decoded==original
    readings[name]=view
    reviews[name]={'json_round_trip_equal':True,'all_history_keys_and_actions_consumed':len(items),'history_count_by_depth':dict(Counter(len(h) for h in actions)),
                   'action_histogram':dict(Counter(actions.values())),'count_states':len(table),'actual_path':list(current),'actual_counts':counts,
                   'all_127_clone_coordinates_consumed':len(clones),'nonzero_clones':sparse,'customers':sum(clones),
                   'all_saved_proof_fields':deepcopy(proof)}
    del reviews[name]['all_saved_proof_fields']['integer_clones']
    if name.startswith('m5'):
        assert sparse==[[127,1]]
        write('markov-count-table.json',table)
oldbase=REPO/'archives/customer-attraction/tools/evidence/r8e450-counter-base-policy-and-ten-records'
oldpath=next((oldbase/'original').glob('**/best_policy.json'));old=json.loads(oldpath.read_text())
new=json.loads((EVID/'original/iteration_m5p7.json').read_text())['batches'][0]['cone_proofs'][0]
assert old['strategy']==new['strategy']
for key,value in new['portfolio_proofs'][0].items():assert old[key]==value,(key,value,old[key])
reviews['existing_exact_audit_binding']={'prior_input':str(oldpath.relative_to(REPO)),'prior_input_sha256':sha256(oldpath.read_bytes()).hexdigest(),
 'same_complete_strategy':True,'same_every_portfolio_proof_field':True,'existing_fixed_audit':str((oldbase/'fixed-audit.json').relative_to(REPO)),
 'existing_execution_event':str((oldbase/'fixed-audit-execution.json').relative_to(REPO)),
 'new_original_import_BI_LP_MILP_random_search_or_full_payoff_verifier_executions':0}
write('lossless-reading.json',readings);write('saved-review.json',reviews)
print(json.dumps({k:{a:b for a,b in v.items() if a!='all_saved_proof_fields'} for k,v in reviews.items()},ensure_ascii=False,indent=2))
print('MARKOV COMPLETE COUNT TABLE (seven decimal counts : action):')
table=json.loads((EVID/'markov-count-table.json').read_text())
for start in range(0,len(table),10):
    print(' '.join(''.join(map(str,x['counts']))+':'+str(x['action']) for x in table[start:start+10]))
