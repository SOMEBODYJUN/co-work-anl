"""Narrow exact check of six attachment repairs; no mathematical replay."""
from pathlib import Path
import copy
import hashlib
import json

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
prefix=ROOT/'research/runs/n6-boss3-20261118/studio/freezes'
f1=read(prefix/'boss3-B-publication-v1/a3b9567feaa1db69ce19e39e47d13dc444742dca41dff06821a72ca3d2dea56c.json')
f2=read(prefix/'boss3-B-publication-v2/c6cd6c74ad193338d935f372da3686a6faaefff80b513b5d833988cfef16b695.json')
ledger=[]
for ref in f2['content_refs']:
    assert sha(ROOT/ref['path'])==ref['sha256']
    ledger.append({**ref,'actual_sha256':ref['sha256'],'match':True})
for ref in f1['content_refs']:
    assert sha(ROOT/ref['path'])==ref['sha256']
base=ROOT/'research/workspaces/n6-boss3-20261118/records'
b1=read(base/'B-registration-batch.json')
b2=read(base/'B-registration-batch-v2.json')
expected=copy.deepcopy(b1)
repairs=[]
for i,row in enumerate(expected['materials']):
    if i:
        assert row['path'].startswith('tools/evidence/six-five-extra-B-prefix/')
        assert row['disposition']=='objects'
        row['disposition']='attachment'
        repairs.append({'json_path':'/materials/'+str(i)+'/disposition',
                        'path':row['path'],'old':'objects','new':'attachment'})
assert len(repairs)==6 and expected==b2
assert b2['materials'][0]['disposition']=='objects'
assert b1['objects']==b2['objects']
a1=read(ROOT/f1['artifact_ref']['path'])
a2=read(ROOT/f2['artifact_ref']['path'])
expected_a=copy.deepcopy(a1)
expected_a['publication_refs'][0]={'path':'research/workspaces/n6-boss3-20261118/records/B-registration-batch-v2.json','sha256':sha(base/'B-registration-batch-v2.json')}
expected_a['line_event_id']=a2['line_event_id']
assert expected_a==a2
assert all(f1[k]==f2[k] for k in ['spec_pin','packet_pins','application_refs','unpaid_obligation_ids','target_remaining','authors','state'])
same1={r['path']:r['sha256'] for r in f1['content_refs']}
same2={r['path']:r['sha256'] for r in f2['content_refs']}
assert all(same1[p]==same2[p] for p in same1.keys()&same2.keys())
edge=read(ROOT/'map/edges/n6-boss3-20261118/B-prefix-half-contribution.json')
assert edge['endpoint_pins'][b2['objects'][0]['object_id']]==pin(b2['objects'][0])
assert edge['relation_mode']=='conditional' and 'whole_result' not in edge
assert set(edge['contribution'])=={'result','remaining'}
assert a2['statement']==a1['statement']
result={'freeze_revision_pin':'c6cd6c74ad193338d935f372da3686a6faaefff80b513b5d833988cfef16b695',
        'hash_checks':ledger,'different_frozen_files':len(same2),
        'exact_six_batch_repairs':repairs,'all_other_batch_fields_unchanged':True,
        'artifact_changes_only_batch_publication_ref_and_real_line_event':True,
        'mathematical_and_edge_bytes_unchanged':True,'old_v1_frozen_bytes_preserved':True,
        'source_endpoint_pin_remains_valid':True,
        'scope':'Narrow repair only; same-byte complete proof, rational verification, migration and conditional contribution already audited in prior B reports. local-result only.'}
(OUT/'repair-audit-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='hash_checks'},indent=2))
