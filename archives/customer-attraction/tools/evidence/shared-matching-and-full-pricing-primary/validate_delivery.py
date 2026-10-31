"""Read-only structural and transport validation; does not rerun mathematics."""
from pathlib import Path
import hashlib, json, re, sys
E=Path(__file__).resolve().parent
S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-shared-matching-and-full-pricing-primary'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
cap=read(E/'claim-confirmation-original-full-12-ids.json')
pres=read(E/'root-sync-preservation-proof.json')
intake=read(E/'primary-and-owner-verification.json')
assert cap['status']=='pushed' and cap['actor']=='Boss4' and len(cap['ids'])==12
assert cap['local_sync']['status']=='needs-attention'
assert sha(E/'claim-confirmation-original-full-12-ids.json')==intake['raw_receipt_sha256']
assert sha(E/'root-sync-preservation-proof.json')==intake['recovery_proof_sha256']
assert not pres['missing'] and not pres['different'] and not pres['unmerged'] and pres['stash_kept']
assert len(pres['tracked'])==2 and pres['untracked_count']==2 and all(x['same'] for x in pres['tracked'])
ids=set()
for row in intake['primary']:
    z=row['inventory'];p=S/row['raw_target'];raw=p.read_bytes();ids.add(z['id'])
    assert len(raw)==z['size'] and sha(p)==z['sha256']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==z['blob']
    assert row['observed_progress']['owner']=='Boss4' and row['observed_progress']['disposition']=='in-progress'
    assert row['observed_progress']['source_sha256']==z['sha256']
assert len(ids)==5 and ids<=set(cap['ids'])
recs=read(W/'semantic-receipts.json');assert len(recs)==5 and {r['id'] for r in recs}==ids
targets=set()
for r in recs:
    for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert r[k] is True
    for k in ['read_note','comparison_note','decision_note']:assert len(r[k])>50
    assert r['disposition']=='integrated'
    for t in r['targets']:assert (S/t).is_file();targets.add(t)
assert len(targets)==3
for rel in targets:
    txt=(S/rel).read_text();assert txt.startswith('---\n') and txt.count('---')>=2
    head=txt.split('---',2)[1]
    for k in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert k in head
    assert len(txt)>3000
checked_links=0
for p in [S/t for t in targets]+[E/'README.md',W/'README.md']:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link or link.startswith('#'):continue
        link=link.split('#')[0]
        if not link:continue
        dest=(p.parent/link).resolve()
        assert dest.is_file() or dest.is_dir() or (R/dest.relative_to(S)).exists(),(p,link)
        checked_links+=1
runtime=read(E/'runtime-record.json');result=read(E/'new-shared-matching-and-60point-check.json')
assert result['status']=='passed' and result['new_definition_entries']==1
assert runtime['actual_entries']=={'new_definition_entry_attempts':1,'new_definition_entry_successes':1,'failed_attempts':0,'original_GO_main_entries':0,'original_437_CLI_entries':0,'external_solver_calls':0}
assert runtime['script_sha256']==sha(E/'check_shared_matching_and_new60.py')
assert runtime['output_sha256']==sha(E/'new-shared-matching-and-60point-check.json')
assert len(result['new60']['all557_slacks_recomputed'])==557
assert len(result['cross_pairs']['totals'])==220 and len(result['cross_pairs']['atom_coefficients'])==13200
assert result['new60']['zero_slacks']==70
assert len(result['cross_pairs']['negative_rows'])==2
assert not runtime['full557_final_dual_new_verification'] and not runtime['67point_or61point_new_verification']
assert not runtime['all162_final_envelopes_new_verification']
dep=read(E/'dependency-safe-local-export-manifest.json');sec=read(E/'secondary-safe-local-export-manifest.json')
assert len(dep['missing'])==15 and len(sec['missing'])==6
for row in dep['rows']:
    p=E/'comparison'/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
for row in read(E/'formal-comparison-manifest.json'):
    p=E/'formal-comparison'/row['path'];assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
assert read(W/'mathematical-self-check.json')['status']=='passed-after-reading-and-new-exact-entry'
assert len(read(W/'relations-and-source-routing.json')['relationships'])==9
nexts=read(W/'next-candidates.json');assert nexts['candidate_count']==5
assert all(x['available_for_root_recheck'] for x in nexts['rows'])
manifest=S/'copy-files.json'
if '--final' in sys.argv:
    m=read(manifest);listed={x['path'] for x in m['files']}
    actual={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}-{'copy-files.json'}
    assert actual==listed and m['file_count']==len(listed) and m['bytes']==sum((S/p).stat().st_size for p in listed)
    for x in m['files']:
        p=S/x['path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
    mode='final-exact-whitelist'
else:mode='pre-manifest-structural-validation'
print(json.dumps({'status':'passed','mode':mode,'primary_count':5,'original_claim_ids':12,'canonical_targets':3,'links_checked':checked_links,'new_math_entries':1,'original_GO_CLI_entries':0,'transport_files':len(listed) if '--final' in sys.argv else None,'mathematics_rerun':False},ensure_ascii=False))
