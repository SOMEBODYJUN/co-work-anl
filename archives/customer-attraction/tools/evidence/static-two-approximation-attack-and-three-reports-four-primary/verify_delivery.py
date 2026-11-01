from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-static-two-approximation-attack-and-three-reports-four-primary'
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,a):
 b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256']
 if 'blob' in a:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
gate=j(E/'MD-prior-fullread-and-publication-gate.json');D=Path(gate['dependency_staging'])
def resolve(q):
 for p in [S/q,R/q,D/q]:
  if p.is_file():return p
 raise AssertionError(q)
sm=j(E/'source-manifest.json');og=j(E/'ownership-gate.json');raw=j(E/'root-actual-full4-claim.json');proof=j(E/'independent-sync-preservation.json')
ids={'a07a0c7e65079e2a7c60','7720d33928d8bc75d15b','e623945c0b964c91cf6d','a264515f4bb961a2562c'}
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',4,'9c21ce85fe4d59edb673710e3a79e800a5a2c989','needs-attention') and set(raw['ids'])==ids and og['raw_original_local_sync']==raw['local_sync']
assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']=='cd3e492b2ddf8124c09f2976b6e698662806769b'
assert sm['primary_sources']==4 and sm['primary_bytes']==15153 and sum(a['size'] for a in sm['rows'])==15153 and {a['id'] for a in sm['rows']}==ids and sm['prior_MD_fullread_exact_reuses']==1 and sm['new_report_fullreads']==3 and sm['new_report_bytes']==9364
assert sm['Root_new_normal_shows']==sm['new_original_copies']==3 and sm['worker_new_normal_shows']==sm['current_original_math_runs']==sm['current_new_math_runs']==0
for a in sm['rows']:
 check(resolve(a['target_path']),a);sc=j(S/a['capture_target'])['source'];assert (sc['id'],sc['sha256'],sc['blob'])==(a['id'],a['sha256'],a['blob'])
 o=next(x for x in og['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['current_original_body_rereads']==a['current_original_imports']==a['current_original_runs']==0
 assert a['prior_complete_fullread_sameSHA_reused']==(a['id']=='a07a0c7e65079e2a7c60') and a['current_first_full_body_read']==(a['id']!='a07a0c7e65079e2a7c60')
rs=j(E/'complete-three-report-reading-and-records.json');assert len(rs['rows'])==3 and rs['all_three_reports_complete_fullread'] and rs['report_top_fields']==11 and rs['LP_row_fields']==5 and rs['complete_LP_records']==44 and rs['current_report_parses_for_reading_and_tables']==3
expected={'e623945c0b964c91cf6d':([0,0,0,5],4,6,63,1295,20,-0.9999999999999998,0,2),'a264515f4bb961a2562c':([0,1,1],3,4,15,63,9,-0.5,0,2),'7720d33928d8bc75d15b':([0,3,4],3,6,63,215,15,-0.7362637362637361,0,5)}
for a in rs['rows']:
 d=a['report'];want=expected[a['id']];assert (d['path'],d['players'],d['topics'],d['type_count'],d['nonzero_IC_rows'],len(d['LPs']),d['best_excess'],d['best_player'],d['best_query'])==want
 assert len(d)==11 and all(len(z)==5 and z['success'] and z['status']=='Optimization terminated successfully. (HiGHS Status 7: Optimal)' for z in d['LPs'])
 assert {(z['player'],z['query']) for z in d['LPs']}=={(i,q) for i in range(d['players']) for q in range(d['topics']) if q!=d['path'][i]}
 assert a['first_complete_rawtext_fullread'] and a['current_report_JSON_parse_for_metadata_and_complete_table']==1 and a['no_solver_or_constraint_recomputation']
scaff=j(E/'exact-prior-certified-scaffold-bindings.json');assert len(scaff['rows'])==5 and scaff['new_normal_shows']==scaff['new_original_copies']==scaff['new_scaffold_semantic_reads']==scaff['new_scaffold_JSON_parses']==scaff['new_scaffold_IC_runs']==0 and scaff['bare_eight_scaffold_is_8clients4topics_not_13clients5topics']
assert {a['id'] for a in scaff['rows']}=={'9e6ad9b5524e57789d9a','75abf77a187270ca9eeb','8ad153389623fee10a3a','91db4f6c6916b3529699','23b69044426c185f1653'}
for a in scaff['rows']:check(R/a['published_original'],a)
fc=j(E/'current-formal-failure-boundary-comparison.json');check(R/fc['formal_path'],fc);assert fc['current_complete_formal_read'] and not fc['original_FAILED_CLAIMS_raw_current_read'] and not fc['current_original_math_run']
assert gate['prior_MD_fullread_record']['current_full_body_read'] and gate['dependency_math_status'].startswith('pending') and gate['must_publish_original_dependency_before_or_same_batch_current_done'] and not gate['current_source_done'] and gate['old_frozen_notes_unchanged']
rec=j(W/'semantic-receipts.json');assert len(rec)==4 and {a['id'] for a in rec}==ids
for a in rec:
 assert a['disposition']=='retained' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['root_verified_claim_commit']==raw['remote_tip'] and a['root_claim_local_sync']=='needs-attention' and a['current_original_body_rereads']==a['current_original_mathematical_entries']==a['current_new_mathematical_entries']==a['extra_scaffold_primary_done']==0
 for q in a['targets']:assert resolve(q).is_file()
nx=j(W/'next-natural-scope-proposal.json');assert nx['sources']==2 and nx['bytes']==6343 and not nx['body_read'] and not nx['worker_claimed'] and not nx['primary_receipts_created']
missing=[]
for p in S.rglob('*.md'):
 if '/original/' in str(p):continue
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#'):continue
  q=(p.parent/link.split('#')[0]).resolve()
  if q.is_file():continue
  try:resolve(q.relative_to(S))
  except (ValueError,AssertionError):missing.append([str(p.relative_to(S)),link])
assert not missing,missing
mf=j(E/'content-manifest.json')
for a in mf['files']:check(S/a['path'],a)
paths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()};assert set(j(W/'copy-files.json')['files'])==paths
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':4,'primary_bytes':15153,'formal_objects':1,'new_report_fullreads':3,'prior_MD_sameSHA_fullread_reuses':1,'LP_records_fullread':44,'report_top_fields':11,'LP_row_fields':5,'certified_scaffold_file_reuses':5,'new_scaffold_semantic_reads':0,'new_scaffold_IC_runs':0,'source_imports':0,'source_runs':0,'new_math_runs':0,'raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','missing_links':0,'content_manifest_files':len(mf['files']),'copy_files':len(paths),'not_LP_optimality_or_new_SPE_verification':True}
(E/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
