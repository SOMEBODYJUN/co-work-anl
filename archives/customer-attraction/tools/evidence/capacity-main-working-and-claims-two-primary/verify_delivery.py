from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-capacity-main-working-and-claims-two-primary'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,a):
 b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256']
 if 'blob' in a:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
sm=j(E/'source-manifest.json');og=j(E/'ownership-gate.json');raw=j(E/'root-actual-full13-claim.json');proof=j(E/'independent-sync-preservation.json');dep=j(E/'exact-predecessor-publication-gate.json');D=Path(dep['dependency_staging'])
def resolve(rp):
 for p in [S/rp,R/rp,D/rp]:
  if p.is_file():return p
 raise AssertionError(rp)
ids={'c40ab6544814fe34987c','f88a286ea0c61b5e40e5'}
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',13,'821631982dac886fe558e6c5a477f7e0a6410f29','needs-attention')
assert og['raw_original_local_sync']==raw['local_sync'] and og['remote_tip']==raw['remote_tip'] and set(og['other_eleven_claim_ids_not_processed'])==set(raw['ids'])-ids and og['current_actual_gate_is13ZZ_not_failed16ZZ'] and og['no_pushed_status_inferred_from_owner']
assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']=='cd2e76bb1894e237fe87c57315336b06cb83d7e0'
assert sm['primary_sources']==2 and sm['primary_bytes']==10094 and {a['id'] for a in sm['rows']}==ids and sm['prior_complete_fullread_reuses']==2
assert sm['current_new_normal_shows']==sm['current_new_original_copies']==sm['current_original_body_reads']==sm['current_original_parses']==sm['current_original_math_runs']==sm['current_new_math_runs']==0
prior=j(E/'prior-complete-related-reading-manifest.json')
for a in sm['rows']:
 old=next(x for x in prior['rows'] if x['id']==a['id']);assert old['sha256']==a['sha256'] and old['current_full_body_read'] and old['current_first_full_body_read']
 check(resolve(a['target_path']),a);sc=j(S/a['prior_normal_capture_target'])['source'];assert (sc['id'],sc['sha256'],sc['blob'])==(a['id'],a['sha256'],a['blob'])
 o=next(x for x in og['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['prior_complete_fullread_sameSHA_reused'] and a['original_is_previous_package_single_copy'] and not any(a[k] for k in ['current_new_original_copy','current_new_normal_show','current_original_body_read','current_original_parse','current_original_import','current_original_run'])
assert dep['dependency_math_status_at_current_freeze'].startswith('pending') and dep['must_publish_dependency_before_or_same_batch_as_current_done'] and not dep['current_source_done'] and dep['dependency_frozen_notes_not_modified']
assert sha(D/dep['copylist'])==dep['copylist_sha256']=='94a656caa205032fc615b5765153b52bcdad856e0e1ee62adedd7e8f4439e6f9'
check(resolve(dep['resource_path']),{'size':dep['resource_size'],'sha256':dep['resource_sha256']})
for a in dep['source_originals']:check(resolve(a['path']),a)
route=j(E/'complete-mathematical-source-to-object-routing.json');assert len(route['source_to_object_rows'])==11 and route['first_primary_sources']==2 and not route['actual_primary_gate_not_yet_received'] and route['source_primary_receipts_created'] and not route['current_source_done']
assert {a['id'] for a in route['source_to_object_rows']}==ids and route['target_resource_sha256']==dep['resource_sha256']
rec=j(W/'semantic-receipts.json');assert len(rec)==2 and {a['id'] for a in rec}==ids
for a in rec:
 assert a['disposition']=='duplicate' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['prior_complete_fullread_sameSHA_reused'] and a['root_verified_claim_commit']==raw['remote_tip'] and a['root_claim_local_sync']=='needs-attention'
 assert a['current_new_body_reads']==a['current_original_parses']==a['current_new_normal_shows']==a['current_original_mathematical_entries']==a['current_new_mathematical_entries']==a['extra_related_primary_done']==0
 for q in a['targets']:assert resolve(q).is_file()
nx=j(W/'next-natural-scope-proposal.json');assert nx['sources']==1 and nx['bytes']==5789 and not nx['worker_claimed'] and not nx['primary_receipt_created']
missing=[]
for p in S.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#'):continue
  q=(p.parent/link.split('#')[0]).resolve()
  if q.is_file():continue
  try:rp=q.relative_to(S);resolve(rp)
  except (ValueError,AssertionError):missing.append([str(p.relative_to(S)),link])
assert not missing,missing
mf=j(E/'content-manifest.json')
for a in mf['files']:check(S/a['path'],a)
paths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()};assert set(j(W/'copy-files.json')['files'])==paths
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':2,'primary_bytes':10094,'duplicate_dispositions':2,'source_complete_fullread_reuses':2,'new_formal_objects':0,'new_original_copies':0,'new_normal_shows':0,'original_body_rereads':0,'original_parses':0,'source_imports':0,'source_runs':0,'new_math_runs':0,'all_source_section_routes':11,'dependency_actual_math_at_freeze':'pending Root checkpoint; gate required before done','raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','missing_links':0,'content_manifest_files':len(mf['files']),'copy_files':len(paths),'not_new_math_or_publication_verification':True}
(E/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
