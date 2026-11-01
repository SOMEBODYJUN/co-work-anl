from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-copy-half-independent-root-unit-audit-two-primary'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,a):
 b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256']
 if 'blob' in a:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
def resolve(q):return S/q if (S/q).is_file() else R/q
sm=j(E/'source-manifest.json');og=j(E/'ownership-gate.json');raw=j(E/'root-actual-full11-claim.json');proof=j(E/'independent-sync-preservation.json');ids={'7dc3a3c5ddf070e53f18','5edf28db5c5fa50b9cc7'}
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',11,'35b9558784f13f7b322449e5187e8af74f0b931d','needs-attention') and ids<=set(raw['ids']) and og['raw_original_local_sync']==raw['local_sync'] and set(og['other_nine_claim_ids_not_processed'])==set(raw['ids'])-ids
assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']=='db836711713a7d8fca85580057875d0dc109f6e4'
assert sm['primary_sources']==2 and sm['primary_bytes']==sum(a['size'] for a in sm['rows'])==6343 and {a['id'] for a in sm['rows']}==ids and sm['Root_actual_new_normal_shows']==sm['current_first_full_body_reads']==2 and sm['worker_new_normal_shows']==sm['current_source_imports']==sm['current_source_runs']==sm['current_new_math_runs']==0
for a in sm['rows']:
 check(S/a['target_path'],a);sc=j(S/a['capture_target'])['source'];assert (sc['id'],sc['sha256'],sc['blob'])==(a['id'],a['sha256'],a['blob'])
 o=next(x for x in og['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['current_first_full_body_read'] and a['current_original_body_rereads']==a['current_original_imports']==a['current_original_runs']==0
c=j(E/'complete-code-and-report-reading-contracts.json');assert c['code_complete_fulltext_read'] and c['report_complete_fulltext_read'] and c['code_AST_parses']==c['report_JSON_parses_for_complete_reading']==1 and c['file_report_fields']==17 and c['stdout_fields_excluding_complete_policy']==16 and c['no_main_guard'] and c['import_executes_BI_IC_OPT_write_and_print'] and c['no_external_runtime_inputs']
d=c['stored_report'];assert len(d)==17 and set(c['code_summary_fields'])==set(d) and d['decision_histories']==len(d['complete_policy'])==31 and d['IC_checks_including_self']==155 and d['minimum_IC_slack']=='0' and d['actual']==[0,1,2] and d['payoffs']==['18','8','9'] and d['copy_leaf']==[0,0,3] and d['copy_profit']=='8' and d['half_earlier_profit']=='9' and d['OPT']==d['welfare']==35
assert c['all_31_complete_policy_records_fullread'] and not c['all155_payoff_comparands_saved'] and not c['nonself_minimum_slack_saved'] and not c['historical_process_identity_bound'] and c['current_source_imports']==c['current_source_runs']==c['current_new_math_runs']==0
fc=j(E/'full-mathematical-and-implementation-comparison.json');check(R/fc['current_complete_formal_read']['path'],fc['current_complete_formal_read']);check(R/fc['prior_complete_sameSHA_math_resource']['path'],fc['prior_complete_sameSHA_math_resource']);assert fc['prior_two_raw_code_sources_not_newly_read'] and fc['root_is_third_distinct_implementation_same_old35_math'] and fc['current_math_runs']==0
rc=j(W/'semantic-receipts.json');assert len(rc)==2 and {a['id'] for a in rc}==ids
for a in rc:
 assert a['disposition']=='retained' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['current_first_full_body_read'] and a['root_verified_claim_commit']==raw['remote_tip'] and a['root_claim_local_sync']=='needs-attention' and a['current_original_body_rereads']==a['current_original_mathematical_entries']==a['current_new_mathematical_entries']==a['extra_related_primary_done']==0
 for q in a['targets']:assert resolve(q).is_file(),q
nx=j(W/'next-natural-scope-proposal.json');assert nx['sources']==3 and nx['bytes']==17240 and not nx['worker_claimed'] and not nx['primary_receipts_created']
missing=[]
for p in S.rglob('*.md'):
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
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':2,'primary_bytes':6343,'formal_objects':1,'source_fullreads':2,'code_AST_parses':1,'report_reading_JSON_parses':1,'report_fields':17,'stdout_fields':16,'full_report_policy_records':31,'new_BI_IC_or_OPT_runs':0,'source_imports':0,'source_runs':0,'new_math_runs':0,'raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','missing_links':0,'content_manifest_files':len(mf['files']),'copy_files':len(paths),'not_new_SPE_or_historical_process_identity_verification':True}
(E/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
