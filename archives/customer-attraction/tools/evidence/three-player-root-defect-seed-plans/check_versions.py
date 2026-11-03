"""Bind three primary files and expose their exact policy differences.

This performs byte/schema/version checks and one targeted tie calculation.
It does not rerun the existing whole-tree IC audit, OPT enumeration, or LP.
"""
from fractions import Fraction
from hashlib import sha1, sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path('/workspace/scratch/4703f6521547/co-work-anl-boss7')
PRIMARY = Path('/workspace/scratch/4703f6521547/primary')
IDS = ['3579af6fc8f8b90861b2', '9dd59c749e43339e4bf9', '1a6abcbdd7fcd287fb8d']
inventory = {r['id']: r for r in map(json.loads, (REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
old = REPO/'archives/customer-attraction/tools/evidence/root-regret-discovery-and-frozen-audit-four-primary/original'
records, objs = [], {}
for id_ in IDS:
    meta = inventory[id_]
    raw = (PRIMARY/(id_+'.json')).read_bytes()
    receipt = json.loads((PRIMARY/(id_+'.receipt.json')).read_text())
    assert receipt['source'] == meta
    assert len(raw) == meta['size']
    assert sha256(raw).hexdigest() == meta['sha256']
    assert sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == meta['blob']
    assert (old/meta['path']).read_bytes() == raw
    obj = json.loads(raw)
    actions = {tuple(h):a for h,a in obj['actions']}
    assert len(actions) == len(obj['actions']) == 31
    assert set(actions) == {h for d in range(3) for h in product(range(5), repeat=d)}
    assert all(type(a) is int and 0 <= a < 5 for a in actions.values())
    assert obj['instance']['topics'] == list(map(str, range(5)))
    assert obj['instance']['players'] == 3
    for c in obj['instance']['customers']:
        assert type(c['multiplicity']) is int and c['multiplicity'] > 0
        assert c['topics'] and len(set(c['topics'])) == len(c['topics'])
        assert all(type(a) is int and 0 <= a < 5 for a in c['topics'])
    leaf = []
    while len(leaf) < 3:
        leaf.append(actions[tuple(leaf)])
    assert leaf == obj['actual']
    filename = Path(meta['path']).name
    (HERE/'original'/filename).write_bytes(raw)
    objs[filename] = obj
    records.append({**meta, 'actual_read_from': str(PRIMARY/(id_+'.json')),
        'compared_existing_copy': str(old/meta['path']),
        'preserved_primary': 'original/'+filename,
        'all_11_fields_read': len(obj)==11,
        'ordered_action_count': len(actions),
        'customer_rows': len(obj['instance']['customers']),
        'unit_customer_total': sum(c['multiplicity'] for c in obj['instance']['customers'])})

def differences(a, b):
    aa = {tuple(h):v for h,v in a['actions']}
    bb = {tuple(h):v for h,v in b['actions']}
    assert set(aa) == set(bb)
    return [{'history':list(h), 'left_action':aa[h], 'right_action':bb[h]}
            for h in sorted(aa, key=lambda h:(len(h),h)) if aa[h] != bb[h]]

previous_path = old/'research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/seed_source_m3_v0_0.json'
previous = json.loads(previous_path.read_text())
v0 = objs['seed_source_m3_v0_1.json']
v10 = objs['seed_source_m3_v1_0.json']
v11 = objs['seed_source_m3_v1_1.json']
assert previous['instance'] == v0['instance']
assert v10['instance'] == v11['instance']
dv0 = differences(previous, v0)
dv1 = differences(v10, v11)
assert dv0 == [{'history':[4,0], 'left_action':0, 'right_action':3}]
assert dv1 == [{'history':[], 'left_action':3, 'right_action':0},
               {'history':[0,1], 'left_action':2, 'right_action':1}]

def utility(obj, a, leaf):
    return sum((Fraction(c['multiplicity'], sum(t in c['topics'] for t in leaf))
                for c in obj['instance']['customers'] if a in c['topics']), Fraction())

# This isolates the tie that is invisible in the identical saved root-payoff vectors.
last_payoffs = [str(utility(v10, a, [0,1,a])) for a in range(5)]
assert last_payoffs == ['10/3','22/3','22/3','22/3','3']
second_rows = []
for obj in (v10, v11):
    actions = {tuple(h):a for h,a in obj['actions']}
    row = [str(utility(obj, a, [0,a,actions[(0,a)]])) for a in range(5)]
    second_rows.append(row)
assert second_rows == [['10/3','31/3','22/3','22/3','3'],
                       ['10/3','22/3','22/3','22/3','3']]
report = {'scope':'byte/schema/version binding and the single history (0,1) tie only; no whole-tree IC/OPT/LP replay',
    'sources':records,
    'version_differences':[
        {'left':'seed_source_m3_v0_0.json','right':'seed_source_m3_v0_1.json','same_instance':True,'actions':dv0},
        {'left':'seed_source_m3_v1_0.json','right':'seed_source_m3_v1_1.json','same_instance':True,'actions':dv1}],
    'targeted_tie':{'history':[0,1], 'last_player_payoffs_by_action_0_to_4':last_payoffs,
        'second_player_payoffs_after_first_0':second_rows},
    'existing_exact_audit_used':'archives/customer-attraction/tools/evidence/root-regret-discovery-and-frozen-audit-four-primary/original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/frozen_sources_exact_audit.json',
    'existing_audit_rerun':False, 'LP_runs':0, 'whole_tree_IC_replays':0, 'OPT_enumerations':0}
(HERE/'source-and-version-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'primary_count':3,'primary_bytes':sum(r['size'] for r in records),
                  'version_differences':[dv0,dv1], 'targeted_tie':report['targeted_tie'],
                  'whole_tree_IC_replays':0,'OPT_enumerations':0,'LP_runs':0}, ensure_ascii=False))
