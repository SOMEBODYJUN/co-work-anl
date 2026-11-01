"""Read-only structural and byte whitelist checks, never reruns mathematics."""
from pathlib import Path
import json,hashlib,re,sys
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-product-background-and-completion-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=read(E/'claim-confirmation-original-full-20-ids.json');iv=read(E/'primary-and-owner-verification.json')
assert c['status']=='pushed' and c['actor']=='Boss4' and len(c['ids'])==20 and c['local_sync']['status']=='synced'
assert c['remote_tip']=='c4dac6150d909a176c32412d1dc049f04cdc68a9'
assert sha(E/'claim-confirmation-original-full-20-ids.json')==iv['raw_receipt_sha256']
ids=set();nbytes=0
for row in iv['primary']:
    z=row['inventory'];p=S/row['raw_target'];b=p.read_bytes();ids.add(z['id']);nbytes+=len(b)
    assert len(b)==z['size'] and sha(p)==z['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==z['blob']
    st=row['observed_progress'];assert st['owner']=='Boss4' and st['disposition']=='in-progress' and st['source_sha256']==z['sha256']
assert len(ids)==5 and ids<=set(c['ids']) and nbytes==26793
rc=read(W/'semantic-receipts.json');assert len(rc)==5 and {r['id'] for r in rc}==ids
assert sum(r['disposition']=='duplicate' for r in rc)==1 and sum(r['disposition']=='integrated' for r in rc)==4
targets=set();new=set()
for row in rc:
    for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert row[k] is True
    for k in ['read_note','comparison_note','decision_note']:assert len(row[k])>50
    for t in row['targets']:
        assert (S/t).is_file() or (R/t).is_file();targets.add(t)
        if (S/t).is_file():new.add(t)
assert len(new)==4 and len(targets)==5
for t in new:
    txt=(S/t).read_text();assert txt.startswith('---\n');head=txt.split('---',2)[1]
    for k in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert k in head
    assert len(txt)>1500
links=0
for p in [S/t for t in new]+[E/'README.md',W/'README.md']:
    for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in dest or dest.startswith('#'):continue
        dest=dest.split('#')[0]
        if not dest:continue
        q=(p.parent/dest).resolve();assert q.exists() or (R/q.relative_to(S)).exists(),(p,dest);links+=1
rt=read(E/'runtime-record.json');o=read(E/'new-product-completion-and-2016.json')
assert rt['new_math_entries']=={'attempts':1,'successes':1,'failed':0}
assert rt['original_CLI_entries']==rt['external_solver_calls']==0
assert rt['script_sha256']==sha(E/'check_product_completion_and_2016.py') and rt['output_sha256']==sha(E/'new-product-completion-and-2016.json')
assert o['status']=='passed' and o['failed_math_attempts']==0
assert o['product']['parameter_cases']==30 and o['product']['count_vectors']==461 and o['product']['constructed_products']==24
assert o['two_player']['fullSPE_count']==2 and o['two_player']['literal_node_comparisons']==72
z=o['new60_2016'];assert z['rows']==2016 and z['zero_total_slacks']==10 and z['all_nonnegative'] and not z['old557_orGO220_recomputed']
assert len(z['row_order'])==len(set(z['row_order']))==len(z['total_slacks'])==2016
assert len(z['atom_rows'])==60 and all(len(v['coefficients'])==2016 for v in z['atom_rows'])
dep=read(E/'dependency-safe-local-export-manifest.json');assert len(dep['missing'])==17 and dep['rows']==[]
for row in read(E/'formal-comparison-manifest.json'):
    p=E/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
reuse=read(E/'same-sha-reuse-and-comparison.json');assert reuse['current_GX_published_proof_sha256']==reuse['prior_GX_mature_snapshot_sha256']
inp=read(E/'selected60-input-manifest.json');p=E/'comparison'/inp['path'];assert p.stat().st_size==inp['size'] and sha(p)==inp['sha256']==z['input_sha256']
assert len(read(W/'relations-and-source-routing.json')['relationships'])==9
assert read(W/'mathematical-self-check.json')['status']=='passed-after-full-reading-and-one-new-exact-entry'
nxt=read(W/'next-candidates.json');assert nxt['candidate_count']==5 and all(x['available_for_root_recheck'] for x in nxt['rows'])
if '--final' in sys.argv:
    m=read(S/'copy-files.json');listed={f['path'] for f in m['files']};actual={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}-{'copy-files.json'}
    assert actual==listed and m['file_count']==len(listed)
    assert sum((S/p).stat().st_size for p in listed)==m['bytes']
    for f in m['files']:
        p=S/f['path'];assert p.stat().st_size==f['size'] and sha(p)==f['sha256']
    mode='final-exact-whitelist';count=len(listed)
else:mode='pre-manifest-structural-validation';count=None
print(json.dumps({'status':'passed','mode':mode,'primary_sources':5,'primary_bytes':nbytes,'original_claim_ids':20,'new_canonical_targets':4,'already_published_target':1,'dispositions':'4integrated1duplicate','links_checked':links,'new_math_entries':1,'mathematics_rerun':False,'transport_files':count},ensure_ascii=False))
