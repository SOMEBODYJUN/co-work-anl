from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent;S=HERE.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text())
def resolve(rp):
 p=S/rp
 return p if p.is_file() else R/rp
sm=j(HERE/'source-manifest.json');og=j(HERE/'ownership-gate.json');raw=j(HERE/'root-actual-full-claim.json')
assert (raw['status'],raw['actor'])==('pushed','Boss4') and len(raw['remote_tip'])==40
assert len(raw['ids'])==17 and raw['remote_tip']=='2a6bcdebc542a336ff2fa72006980bc91b08da39'
assert og['raw_original_local_sync']==raw['local_sync'] and og['remote_tip']==raw['remote_tip']
sync=raw['local_sync']['status'];assert sync in {'synced','needs-attention'}
if sync=='needs-attention':
 p=j(HERE/'independent-sync-preservation.json');assert not p['missing'] and not p['different'] and not p['unmerged'] and p['stash_kept']
 assert p['untracked_count']==1 and p['tracked']==[] and p['stash']=='81aa465d9ad1e82e00250635b7a1368c23d14cc1'
assert sm['primary_sources']==2 and sm['primary_bytes']==85983 and len(sm['rows'])==2
ids={a['id'] for a in sm['rows']};assert ids=={'52523113cdc7c8cff601','eca2ddadd311de0e4b87'} and ids<=set(raw['ids'])
assert set(og['other_claim_ids_not_processed'])==set(raw['ids'])-ids
for a in sm['rows']:
 p=S/a['target_path'];b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
 cap=j(S/a['acquisition_target'])['source'];assert cap['id']==a['id'] and cap['sha256']==a['sha256'] and cap['blob']==a['blob']
 o=next(x for x in og['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['complete_code_or_report_fullread'] and a['prior_actual_related_fullread_reused']
 assert a['current_normal_shows']==a['current_source_body_rereads']==a['current_source_runs']==a['previous_related_extra_done']==0
for k in ('current_normal_shows','current_source_body_rereads','source_imports','source_runs','new_math_runs','previous_related_extra_done'):assert sm[k]==0
dep=j(HERE/'runtime-input-and-published-predecessor-bindings.json');cp=j(HERE/'actual-author4-math-checkpoint21YN.json');dp=j(HERE/'actual-author4-source-done21YN.json')
assert cp['status']=='pushed' and cp['remote_tip']==dep['author4_math_tip']=='4abbd8bfda4a92fa91dcea47ab96d61422595054'
assert dp['status']=='pushed' and dp['remote_tip']==dep['author4_done_tip']=='355a21ea2bcc492f525a387b757eea74151d4400'
assert set(dep['author4_done_ids'])<=set(dp['ids'])
assets={a['asset']['path']:a['asset'] for a in cp['assets']}
for a in dep['author4_formals']:
 p=R/a['path'];assert p.stat().st_size==a['size'] and sha(p)==a['sha256']==assets[a['path']]['sha256']
a=dep['raw817'];p=R/a['published_path'];assert p.stat().st_size==4080 and sha(p)==a['sha256']==a['actual_asset']['sha256']
assert a['actual_asset']['commit']=='32f586b7cb13b85c9c3386a93e3f530879162937' and not dep['raw817_new_read_parse_show_or_copy']
a=dep['review5068_published_single_original'];p=R/a['target_path'];assert p.stat().st_size==5068 and sha(p)==a['sha256']==assets[a['target_path']]['sha256']
assert not dep['review_original_new_read_show_or_copy']
au=j(HERE/'actual-author-audit3-math-checkpoint14YQ.json');assert au['status']=='pushed' and au['remote_tip']==dep['author_audit3']['actual_math_tip']=='5af7f8a0b6026441878f436d1aa20dc10bc23ed7'
aa=dep['author_audit3']['formal_asset'];assert sha(R/aa['path'])==aa['sha256'] and aa in [x['asset'] for x in au['assets']]
assert dep['author_audit3']['source_done_not_claimed_by_current_package']
for a in j(HERE/'comparison-bindings.json')['full_formal_objects_sameSHA_prior_read_reused']:
 p=R/a['path'];assert p.stat().st_size==a['size'] and sha(p)==a['sha256']
scope=j(HERE/'complete-original-fullread-scope.json');assert scope['code_fullread'] and scope['report_fullread']
assert (scope['report_top_fields'],scope['position_count'],scope['type_rows_counts'],scope['all_IC_rows'])==(34,3,[21,21,21],258)
sc=j(HERE/'saved-report-evidence-contract.json');assert (sc['top_field_count'],sc['position_count'],sc['position_field_count'],sc['type_rows'],sc['type_row_fields'],sc['IC_rows'],sc['IC_row_fields'],sc['original_stdout_field_count'])==(34,3,11,63,6,258,5,14)
assert not sc['source_has_main_guard'] and not sc['source_JSON_reparsed_or_math_recomputed']
assert sc['old_saved_F_sum']=='36019/60' and sc['old_saved_gap']=='199/60' and sc['old_saved_badp_gap_lower']=='9/2' and sc['old_saved_safe_margin_lower_bound']=='0'
assert not sc['badp_is_delta_or_integer_optimal'] and not sc['optimal_query_or_exact_delta_v_solved'] and len(sc['not_established'])==4
w=S/'cleanup/workspaces/Boss4/r3-fractional-global-independent-full-audit-two-primary';rs=j(w/'semantic-receipts.json');assert {a['id'] for a in rs}==ids
for a in rs:
 assert a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['root_claim_local_sync']==sync
 for rp in a['targets']:assert resolve(rp).is_file(),rp
missing=[]
for p in S.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#'):continue
  t=link.split('#')[0]
  if t and not (p.parent/t).is_file():missing.append([str(p.relative_to(S)),link])
assert not missing,missing
mf=j(HERE/'content-manifest.json')
for a in mf['files']:
 p=S/a['path'];assert p.is_file() and p.stat().st_size==a['size'] and sha(p)==a['sha256']
paths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()};assert set(j(w/'copy-files.json')['files'])==paths
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':2,'primary_bytes':85983,'formal_objects':1,'source_imports':0,'source_runs':0,'new_math_runs':0,'original_report_reparsed':False,'missing_links':0,'raw_claim_status':'pushed','raw_local_sync_status':sync,'not_a_new_IC_or_fractional_verification':True,'content_manifest_files':len(mf['files']),'copy_files':len(paths)}
(HERE/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
