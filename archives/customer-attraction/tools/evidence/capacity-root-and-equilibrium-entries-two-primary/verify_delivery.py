from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-capacity-root-and-equilibrium-entries-two-primary'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,a):
 b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256']
 if 'blob' in a:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
def resolve(rp):return S/rp if (S/rp).is_file() else R/rp
sm=j(E/'source-manifest.json');og=j(E/'ownership-gate.json');raw=j(E/'root-actual-full10-claim.json');proof=j(E/'independent-sync-preservation.json')
ids={'1b2aaca12c4c66b08001','123054d88eacc2bd2371'}
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',10,'536d39fb40885f95f657c064a92c430f1d9256cc','needs-attention')
assert og['raw_original_local_sync']==raw['local_sync'] and og['remote_tip']==raw['remote_tip'] and og['no_25ZO_restoration_event_used'] and set(og['other_eight_claim_ids_not_processed'])==set(raw['ids'])-ids
assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']=='fe36b670d6d78b998f575e12eeb3bc51a950bde2'
assert sm['primary_sources']==2 and sm['primary_bytes']==5857 and {a['id'] for a in sm['rows']}==ids and ids<=set(raw['ids']) and sum(a['size'] for a in sm['rows'])==5857
for a in sm['rows']:
 check(S/a['target_path'],a);sc=j(S/a['capture_target'])['source'];assert (sc['id'],sc['sha256'],sc['blob'])==(a['id'],a['sha256'],a['blob'])
 o=next(x for x in og['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['current_full_body_read'] and a['current_first_full_body_read'] and a['current_source_body_rereads']==a['current_imports']==a['current_runs']==0
assert sm['Root_actual_normal_shows']==sm['current_first_full_body_reads']==2 and sm['worker_primary_normal_shows']==sm['current_original_math_runs']==sm['current_new_math_runs']==0
rel=j(E/'necessary-related-full-reading-manifest.json');assert rel['sources']==len(rel['rows'])==10 and rel['bytes']==sum(x['size'] for x in rel['rows'])==47446 and rel['worker_actual_normal_shows']==10 and rel['all_ten_first_fulltext_reads_complete']
assert rel['code_JSON_originals_fetched_or_run']==rel['additional_primary_receipts']==rel['additional_done']==0
for a in rel['rows']:
 check(S/a['target_path'],a);sc=j(S/a['capture_target'])['source'];assert (sc['id'],sc['sha256'],sc['blob'])==(a['id'],a['sha256'],a['blob'])
 assert a['related_only'] and a['current_full_body_read'] and a['current_first_full_body_read'] and not a['current_extra_primary_receipt'] and not a['current_extra_done'] and a['current_imports']==a['current_runs']==a['current_source_body_rereads']==0
nav=j(E/'all-entry-link-and-backtick-resource-bindings.json');assert nav['records']==len(nav['rows'])==24 and nav['entry1_original_markdown_links']==17 and nav['entry2_backtick_and_report_links']==7
for a in nav['rows']:
 assert not a['current_extra_primary_receipt'] and not a['current_original_run']
 if 'target_path' in a:check(S/a['target_path'],a)
 if a.get('existing_single_original'):check(R/a['existing_single_original'],a)
 if a['route_kind']=='source_historical_navigation_only_unread_current':assert a['source_id']=='7dc3a3c5ddf070e53f18' and not a['current_raw_body_read']
fc=j(E/'full-canonical-mathematical-comparison.json');assert len(fc['rows'])==7 and fc['current_formal_fullreads']==4 and fc['prior_complete_sameSHA_formal_reuses']==3 and fc['current_math_runs']==0
for a in fc['rows']:check(R/a['path'],a)
rec=j(W/'semantic-receipts.json');assert len(rec)==2 and {x['id'] for x in rec}==ids
for a in rec:
 assert a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['current_first_full_body_read'] and a['root_verified_claim_commit']==raw['remote_tip'] and a['root_claim_local_sync']=='needs-attention'
 assert a['current_source_body_rereads']==a['current_original_mathematical_entries']==a['current_new_mathematical_entries']==a['extra_related_primary_done']==0
 for q in a['targets']:assert resolve(q).is_file(),q
nx=j(W/'next-natural-scope-proposal.json');assert nx['sources']==2 and nx['bytes']==10094 and not nx['worker_claimed'] and not nx['primary_receipts_created'] and all(x['current_related_fullread'] for x in nx['rows'])
missing=[]
for p in S.rglob('*.md'):
 if '/original/' in str(p) or '/related-original/' in str(p):continue
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
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':2,'primary_bytes':5857,'formal_objects':1,'related_complete_MD_reads':10,'related_MD_bytes':47446,'new_related_source_normal_shows':10,'source_code_or_JSON_new_reads':0,'source_imports':0,'source_runs':0,'new_math_runs':0,'navigation_records':24,'formal_fullreads':4,'prior_formal_sameSHA_reuses':3,'raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','missing_links':0,'content_manifest_files':len(mf['files']),'copy_files':len(paths),'not_a_new_SPE_LP_or_payment_verification':True}
(E/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
