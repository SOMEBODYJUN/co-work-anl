"""Read-only exact publication migration/binding audit; no registry mutation."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).parent
def read(path):
    return json.loads(path.read_text())
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def pin(obj):
    return digest(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())

freeze = read(ROOT/'research/runs/n6-boss3-20261118/studio/freezes/boss3-B-publication-v1/a3b9567feaa1db69ce19e39e47d13dc444742dca41dff06821a72ca3d2dea56c.json')
frozen_by_path = {}
ledger=[]
for ref in freeze['content_refs']:
    raw=(ROOT/ref['path']).read_bytes()
    assert digest(raw)==ref['sha256']
    if 'section' in ref:
        titles=[line.lstrip('#').strip() for line in raw.decode().splitlines()
                if line.startswith('#')]
        assert titles.count(ref['section'])==1
    frozen_by_path[ref['path']]=ref['sha256']
    ledger.append({**ref,'actual_sha256':digest(raw),'bytes':len(raw),'match':True})

batch=read(ROOT/'research/workspaces/n6-boss3-20261118/records/B-registration-batch.json')
edge=read(ROOT/'map/edges/n6-boss3-20261118/B-prefix-half-contribution.json')
artifact=read(ROOT/freeze['artifact_ref']['path'])
obj=batch['objects'][0]
assert len(batch['objects'])==1 and obj['truth_status']=='proved'
assert obj['object_id']=='CA-SIX-DISJOINT-MAXIMA-FIVE-EXTRAS-B-PREFIX-v1'
assert len(obj['sources'])==2 and all(isinstance(s,str) and s.strip() for s in obj['sources'])
assert edge['source_ids']==[obj['object_id']]
assert edge['target_ids']==['customer-attraction/six-providers/exact-six-full-history-half-cover']
assert edge['relation_mode']=='conditional' and edge['premises_mode']=='all'
assert set(edge['contribution'])=={'result','remaining'} and 'whole_result' not in edge
assert 'A' in edge['contribution']['remaining'] and 'C' in edge['contribution']['remaining']
assert not artifact['unpaid_obligation_ids'] and artifact['applications']==[]
assert artifact['state']=='established'

# Exact transfer of complete already-reviewed mathematical bytes.
mathematical=ROOT/'research/workspaces/n6-boss3-20261118/informed-b'
canonical=ROOT/'tools/evidence/six-five-extra-B-prefix'
pairs=[(ROOT/'research/runs/n6-boss3-20261118/studio/artifact-notes/1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b.md',ROOT/obj['body']['path'])]
for name in ['verify_B_all_orbits.py','B-all-orbit-rational-certificates.json',
             'B-1365-to-69-orbit-map.json','B-all-orbit-exact-replay.json',
             'certify_B_all_orbits.py','B-all-orbit-discovery-summary.json']:
    pairs.append((mathematical/name,canonical/name))
migration=[]
for old,new in pairs:
    assert old.read_bytes()==new.read_bytes()
    migration.append({'source':str(old.relative_to(ROOT)),
                      'destination':str(new.relative_to(ROOT)),
                      'sha256':digest(new.read_bytes()),'byte_identical':True})

# Check explicit reference closure, including the original target object.
registry=read(ROOT/'research/registry.json')
target=next(o for o in registry['objects'] if o['object_id']==edge['target_ids'][0])
def refs(value):
    if isinstance(value,dict):
        if {'path','sha256'}<=value.keys():
            yield value
        for v in value.values():
            yield from refs(v)
    elif isinstance(value,list):
        for v in value:
            yield from refs(v)
closure=[]
for label,record in [('batch',batch),('edge',edge),('artifact',artifact),('target',target)]:
    for ref in refs(record):
        assert frozen_by_path.get(ref['path'])==ref['sha256'],(label,ref)
        closure.append({'record':label,'path':ref['path'],'sha256':ref['sha256']})
assert target['truth_status'] in ('open','conjecture','unassessed')
assert edge['endpoint_pins']=={obj['object_id']:pin(obj),target['object_id']:pin(target)}
assert edge['evidence_pins']=={r['path']:r['sha256'] for r in edge['evidence']}
assert edge['review_digest']==pin({k:v for k,v in edge.items()
                                 if k not in ('endpoint_pins','evidence_pins','review_digest')})

# The discovered contract issue is recorded, not silently repaired.
materials={m['path']:m for m in batch['materials']}
assert materials[obj['body']['path']]['disposition']=='objects'
wrong_attachments=[m['path'] for m in batch['materials']
                   if m['path'].startswith('tools/evidence/six-five-extra-B-prefix/')
                   and m['disposition']!='attachment']
assert len(wrong_attachments)==6
assert all(materials[p]['object_ids']==[obj['object_id']] for p in wrong_attachments)

# Test changed relative BASE routing without running the file's writing main.
spec=importlib.util.spec_from_file_location('canonical_B_readonly_verifier',canonical/'verify_B_all_orbits.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.BASE==canonical
replay=module.verify()
assert replay==read(canonical/'B-all-orbit-exact-replay.json')
(OUT/'canonical-readonly-replay.json').write_text(json.dumps(replay,indent=2)+'\n')
result={'freeze_revision_pin':'a3b9567feaa1db69ce19e39e47d13dc444742dca41dff06821a72ca3d2dea56c',
        'hash_checks':ledger,'different_frozen_files':len(frozen_by_path),
        'byte_identical_migrations':migration,'explicit_reference_closure':closure,
        'source_and_target_endpoint_pins_match':True,'edge_evidence_and_review_digest_match':True,
        'target_truth_status_preserved':target['truth_status'],
        'canonical_readonly_replay_matches':True,
        'confirmed_attachment_disposition_mismatches':wrong_attachments,
        'scope':'Metadata/migration/reference closure only; mathematical proof accepted separately in review-B-math-v1.md. Local-result only, not whole target.'}
(OUT/'publication-audit-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()
                  if k not in ('hash_checks','byte_identical_migrations','explicit_reference_closure')},indent=2))
