from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-admissible-menu-author-independent-review-and-entry-three-primary'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,a):
 b=p.read_bytes();assert sha(p)==a['sha256']
 if 'size' in a:assert len(b)==a['size']
 if 'blob' in a:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
def resolve(q):return S/q if (S/q).is_file() else R/q
sm=j(E/'source-manifest.json');og=j(E/'ownership-gate.json');raw=j(E/'root-actual-full7-claim.json');proof=j(E/'independent-sync-preservation.json');ids={'f4a6bc1c48437e1b5375','aa49bfbe453cf9b801ec','e92c75720313d7f16dcb'};old={'f4a6bc1c48437e1b5375','e92c75720313d7f16dcb'}
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',7,'465ccd2c361c088c513fe96c5a6b532b1cb0cda5','needs-attention') and ids<=set(raw['ids']) and og['raw_original_local_sync']==raw['local_sync'] and set(og['other_four_claim_ids_not_processed'])==set(raw['ids'])-ids
assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']=='3621fd2038a3c370a7ad34cdd6b1ed326c488ccf'
assert sm['primary_sources']==3 and sm['primary_bytes']==sum(x['size'] for x in sm['rows'])==17240 and {x['id'] for x in sm['rows']}==ids and sm['prior_normal_fullread_exact_reuses']==2 and sm['new_normal_fullread_sources']==1 and sm['new_normal_fullread_bytes']==8430 and sm['Root_new_normal_shows']==sm['new_original_copies']==1 and sm['worker_new_normal_shows']==sm['current_source_imports']==sm['current_source_runs']==sm['current_new_math_runs']==0
for a in sm['rows']:
 check(resolve(a['target_path']),a);sc=j(S/a['capture_target'])['source'];assert (sc['id'],sc['sha256'],sc['blob'])==(a['id'],a['sha256'],a['blob'])
 o=next(x for x in og['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['prior_complete_fullread_sameSHA_reused']==(a['id'] in old) and a['current_first_full_body_read']==(a['id'] not in old) and a['current_source_body_rereads']==a['current_original_imports']==a['current_original_runs']==0
pub=j(E/'actual-prior-publication-and-first-primary-binding.json');xc=j(E/'actual48AAH-math-checkpoint-original.json');xd=j(E/'actual48AAH-prior-source-done-original.json')
assert xc['status']=='pushed' and xc['remote_tip']==pub['prior_actual_math_tip']=='d32845d185d0eea59b0f3e7764b489b817c00fac' and xd['status']=='pushed' and xd['remote_tip']==pub['prior_actual_done_tip']=='3e4878ada86c017968097217e3464a91a4795006' and not ids&set(xd['ids']) and set(pub['prior_done_primary_ids'])<=set(xd['ids']) and pub['old_related_originals_published_did_not_mean_old_done'] and not pub['current_source_done']
for a in pub['actual_asset_rows']:assert a in [x['asset'] for x in xc['assets']];check(R/a['path'],a)
cov=j(E/'complete-original-reading-and-mathematical-coverage.json');assert cov['author_original_bytes']==5451 and cov['entry_original_bytes']==3359 and cov['independent_review_original_bytes']==8430 and cov['prior_author_entry_fullread_sameSHA_reused'] and cov['review_all_six_sections_current_fullread'] and cov['current_new_blind_or_external_reviews']==cov['current_original_math_runs']==cov['current_new_math_runs']==0 and len(cov['unfetched_unread_original_programs_and_JSONs'])==6
fc=j(E/'complete-formal-comparison-and-private-repeat-cap.json');assert len(fc['rows'])==4 and fc['canonical_full_formal_reads_current']==3 and fc['prior_resource_sameSHA_fullread_reuses']==1 and fc['pure_signal_aliases_do_not_change_payoffs_private_aliases_do'] and fc['no_ADM_gap_transfer_from_private_fractional_transfers'] and fc['new_original_math_runs']==0
for a in fc['rows']:check(R/a['path'],a)
rc=j(W/'semantic-receipts.json');assert len(rc)==3 and {x['id'] for x in rc}==ids
for a in rc:
 assert a['disposition']==('duplicate' if a['id']=='f4a6bc1c48437e1b5375' else 'retained') and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['root_verified_claim_commit']==raw['remote_tip'] and a['root_claim_local_sync']=='needs-attention' and a['current_source_body_rereads']==a['current_original_mathematical_entries']==a['current_new_mathematical_entries']==a['extra_related_primary_done']==0
 for q in a['targets']:assert resolve(q).is_file(),q
nx=j(W/'next-natural-scope-proposal.json');assert nx['sources']==2 and nx['bytes']==7001 and nx['all_original_bodies_unread'] and not nx['worker_claimed'] and not nx['primary_receipts_created']
missing=[]
for p in S.rglob('*.md'):
 if '/original/' in str(p):continue
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#'):continue
  q=(p.parent/link.split('#')[0]).resolve()
  if q.is_file():continue
  try:rp=q.relative_to(S)
  except ValueError:missing.append([str(p.relative_to(S)),link]);continue
  if not (R/rp).is_file():missing.append([str(p.relative_to(S)),link])
assert not missing,missing
mf=j(E/'content-manifest.json')
for a in mf['files']:check(S/a['path'],a)
paths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()};assert set(j(W/'copy-files.json')['files'])==paths
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':3,'primary_bytes':17240,'duplicate_author_dispositions':1,'retained_review_entry_dispositions':2,'formal_objects':1,'new_review_fullreads':1,'prior_author_entry_sameSHA_fullread_reuses':2,'source_imports':0,'source_runs':0,'new_math_runs':0,'prior_actual_math_tip':xc['remote_tip'],'prior_actual_done_tip':xd['remote_tip'],'current3_not_prior_done':True,'raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','missing_links':0,'content_manifest_files':len(mf['files']),'copy_files':len(paths),'not_a_new_ADM_budget_or_SPE_verification':True}
(E/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
