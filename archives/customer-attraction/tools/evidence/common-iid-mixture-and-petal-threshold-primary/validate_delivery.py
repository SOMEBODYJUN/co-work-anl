"""Read-only structural validation; never executes the math certificate."""
from pathlib import Path
import hashlib,json,re,sys
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-common-iid-mixture-and-petal-threshold-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
claim=read(E/'claim-confirmation-original-full-23-ids.json');recov=read(E/'root-sync-preservation-proof.json');intake=read(E/'primary-and-owner-verification.json')
assert claim['status']=='pushed' and claim['actor']=='Boss4' and len(claim['ids'])==23
assert claim['remote_tip']=='7891451cbd07d36981ec193061e5107a20dbddd8'
assert claim['local_sync']['status']=='needs-attention'
assert sha(E/'claim-confirmation-original-full-23-ids.json')==intake['raw_receipt_sha256']
assert sha(E/'root-sync-preservation-proof.json')==intake['recovery_proof_sha256']
assert recov['stash']=='aad9b887a8a70fc30fb8cb633bc074f76de9d437'
assert recov['untracked_count']==2 and len(recov['tracked'])==2 and all(x['same'] for x in recov['tracked'])
assert not recov['missing'] and not recov['different'] and not recov['unmerged'] and recov['stash_kept']
ids=set();total=0
for row in intake['primary']:
    z=row['inventory'];p=S/row['raw_target'];raw=p.read_bytes();ids.add(z['id']);total+=len(raw)
    assert len(raw)==z['size'] and sha(p)==z['sha256']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==z['blob']
    state=row['observed_progress'];assert state['owner']=='Boss4' and state['disposition']=='in-progress' and state['source_sha256']==z['sha256']
assert len(ids)==5 and total==26929 and ids<=set(claim['ids'])
receipts=read(W/'semantic-receipts.json');assert len(receipts)==5 and {r['id'] for r in receipts}==ids
assert sum(r['disposition']=='duplicate' for r in receipts)==1 and sum(r['disposition']=='integrated' for r in receipts)==4
targets=set();new=set()
for r in receipts:
    for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert r[key] is True
    for key in ['read_note','comparison_note','decision_note']:assert len(r[key])>50
    for t in r['targets']:
        assert (S/t).is_file() or (R/t).is_file();targets.add(t)
        if (S/t).is_file():new.add(t)
assert len(new)==3 and len(targets)==4
for t in new:
    text=(S/t).read_text();assert text.startswith('---\n');head=text.split('---',2)[1]
    for k in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert k in head
    assert len(text)>2500
count=0
for p in [S/t for t in new]+[E/'README.md',W/'README.md']:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link or link.startswith('#'):continue
        link=link.split('#')[0]
        if not link:continue
        q=(p.parent/link).resolve();assert q.exists() or (R/q.relative_to(S)).exists(),(p,link);count+=1
runtime=read(E/'runtime-record.json');out=read(E/'new-petal-threshold-certificates.json')
assert out['status']=='passed' and out['new_definition_entry_successes']==1 and out['failed_math_attempts']==0
assert runtime['new_math_entries']=={'attempts':1,'successes':1,'failed':0}
assert runtime['original_audit_CLI_entries']==runtime['external_solver_calls']==runtime['full_policy_new_enumerations']==0
assert runtime['script_sha256']==sha(E/'check_new_petal_threshold_certificates.py') and runtime['output_sha256']==sha(E/'new-petal-threshold-certificates.json')
assert out['new_fixed100']['reverse_margin_over_weak_threshold_strict_lower']=='189/2000'
assert out['m_equals_K_cases'][0]['weak_bridge_reverse_margin_strict_lower']=='3/424'
assert '正的三次项' in (S/'archives/customer-attraction/state/证明/花瓣弱iid反族的显式阈值与渐近机制--证明.md').read_text()
dm=read(E/'dependency-safe-local-export-manifest.json');assert len(dm['missing'])==10 and len(dm['rows'])==1
for row in dm['rows']:
    p=E/'comparison'/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
for row in read(E/'formal-comparison-manifest.json'):
    p=E/'formal-comparison'/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
assert read(W/'mathematical-self-check.json')['status']=='passed-after-complete-reading-and-one-new-exact-certificate'
assert len(read(W/'relations-and-source-routing.json')['relationships'])==8
nc=read(W/'next-candidates.json');assert nc['candidate_count']==5 and all(x['available_for_root_recheck'] for x in nc['rows'])
if '--final' in sys.argv:
    manifest=read(S/'copy-files.json');listed={f['path'] for f in manifest['files']}
    actual={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}-{'copy-files.json'}
    assert actual==listed and len(listed)==manifest['file_count']
    assert sum((S/p).stat().st_size for p in listed)==manifest['bytes']
    for f in manifest['files']:
        p=S/f['path'];assert p.stat().st_size==f['size'] and sha(p)==f['sha256']
    mode='final-exact-whitelist';files=len(listed)
else:mode='pre-manifest-structural-validation';files=None
print(json.dumps({'status':'passed','mode':mode,'primary_sources':5,'primary_bytes':total,'original_claim_ids':23,'new_canonical_targets':3,'already_published_target':1,'receipt_dispositions':'4integrated/1duplicate','links_checked':count,'new_math_entries':1,'original_CLI_entries':0,'mathematics_rerun':False,'transport_files':files},ensure_ascii=False))
