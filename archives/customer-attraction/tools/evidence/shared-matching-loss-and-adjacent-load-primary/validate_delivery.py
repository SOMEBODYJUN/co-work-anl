"""Read-only structural and exact transport checks; no math rerun."""
from pathlib import Path
import json,hashlib,re,sys
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-shared-matching-loss-and-adjacent-load-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=read(E/'claim-confirmation-original-full-30-ids.json');iv=read(E/'primary-and-owner-verification.json')
assert c['status']=='pushed' and c['actor']=='Boss4' and len(c['ids'])==30 and c['local_sync']['status']=='synced'
assert c['remote_tip']=='f2c7edbda53bae2b977de6042aa4f4cbf598742c'
assert sha(E/'claim-confirmation-original-full-30-ids.json')==iv['raw_receipt_sha256']
ids=set();nbytes=0
for row in iv['primary']:
    z=row['inventory'];p=S/row['raw_target'];b=p.read_bytes();nbytes+=len(b);ids.add(z['id'])
    assert len(b)==z['size'] and sha(p)==z['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==z['blob']
    st=row['observed_progress'];assert st['owner']=='Boss4' and st['disposition']=='in-progress' and st['source_sha256']==z['sha256']
assert nbytes==20983 and len(ids)==5 and ids<=set(c['ids'])
rc=read(W/'semantic-receipts.json');assert len(rc)==5 and {r['id'] for r in rc}==ids
targets=set()
for row in rc:
    assert row['disposition']=='integrated'
    for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert row[key] is True
    for key in ['read_note','comparison_note','decision_note']:assert len(row[key])>50
    for t in row['targets']:assert (S/t).is_file();targets.add(t)
assert len(targets)==3
for t in targets:
    txt=(S/t).read_text();assert txt.startswith('---\n');head=txt.split('---',2)[1]
    for key in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert key in head
    assert len(txt)>1800
links=0
for p in [S/t for t in targets]+[E/'README.md',W/'README.md']:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in target or target.startswith('#'):continue
        target=target.split('#')[0]
        if not target:continue
        q=(p.parent/target).resolve();assert q.exists() or (R/q.relative_to(S)).exists(),(p,target);links+=1
rt=read(E/'runtime-record.json');o=read(E/'new-loss-layers-adjacent-and-727.json')
assert rt['new_math_entries']=={'attempts':1,'successes':1,'failed':0} and rt['original_CLI_entries']==rt['external_solver_calls']==0
assert rt['script_sha256']==sha(E/'check_layers_adjacent_and_727.py') and rt['output_sha256']==sha(E/'new-loss-layers-adjacent-and-727.json')
assert o['status']=='passed' and o['failed_math_attempts']==0
assert o['generic_layers']['combined_cases']==7008 and o['generic_layers']['label_group_layer_identities']==14016
assert o['adjacent']['indexed_lists']==1555 and len(o['adjacent']['all_margin_records'])==798 and o['adjacent']['compatible_pairs']==210
point=o['point727'];assert point['atoms']==len(point['atom_records'])==69 and point['distinct_literal_matchings']==217 and point['strict_tax_atoms']==20
assert sum(len(v['literal_matchings']) for v in point['atom_records'])==217
assert not point['independently_recomputed727_slacks'] and not point['template_optimum_or_fulluniverse_dual_newly_verified']
dm=read(E/'dependency-safe-local-export-manifest.json');assert len(dm['missing'])==19 and len(dm['rows'])==4
for row in dm['rows']:
    p=E/'comparison'/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
    if row['id']=='91a2873f83444dd805ff':
        data=read(p);assert len(data['atoms'])==69 and len(data['slacks'])==727
        assert all(len(a['menus_lh'])==3 and all(len(lh)==2 and all(type(x) is int for x in lh) for lh in a['menus_lh']) for a in data['atoms'])
for row in read(E/'formal-comparison-manifest.json'):
    p=E/'formal-comparison'/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
assert len(read(W/'relations-and-source-routing.json')['relationships'])==8
assert read(W/'mathematical-self-check.json')['status']=='passed-after-full-reading-and-one-new-exact-entry'
nxt=read(W/'next-candidates.json');assert nxt['candidate_count']==5 and all(x['available_for_root_recheck'] for x in nxt['rows'])
if '--final' in sys.argv:
    m=read(S/'copy-files.json');listed={f['path'] for f in m['files']};actual={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}-{'copy-files.json'}
    assert actual==listed and m['file_count']==len(listed) and sum((S/p).stat().st_size for p in listed)==m['bytes']
    for f in m['files']:
        p=S/f['path'];assert p.stat().st_size==f['size'] and sha(p)==f['sha256']
    mode='final-exact-whitelist';count=len(listed)
else:mode='pre-manifest-structural-validation';count=None
print(json.dumps({'status':'passed','mode':mode,'primary_sources':5,'primary_bytes':nbytes,'original_claim_ids':30,'canonical_targets':3,'links_checked':links,'new_math_entries':1,'mathematics_rerun':False,'transport_files':count},ensure_ascii=False))
