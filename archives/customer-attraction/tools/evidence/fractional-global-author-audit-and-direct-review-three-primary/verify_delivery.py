from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
S=HERE.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text())
def resolve(rp):
 p=S/rp
 return p if p.exists() else R/rp
sm=j(HERE/'source-manifest.json');owner=j(HERE/'ownership-gate.json');raw=j(HERE/'root-actual-full12-claim.json')
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',12,'9d7878925f63ad769b947889f3d9d875dfcb3960','synced')
assert owner['raw_original_local_sync']==raw['local_sync'] and len(owner['other_nine_claim_ids_not_processed'])==9
assert sm['primary_files']==3 and sm['primary_bytes']==11034 and len(sm['rows'])==3
assert {x['id'] for x in sm['rows']} <= set(raw['ids'])
for a in sm['rows']:
 p=resolve(a['target_path']);b=p.read_bytes()
 assert len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
 cap=j(resolve(a['acquisition_target']))['source'];assert cap['id']==a['id'] and cap['sha256']==a['sha256'] and cap['blob']==a['blob']
 o=next(x for x in owner['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['previous_related_done']==0 and a['current_normal_shows']==0 and a['current_source_body_rereads']==0
assert sum(a['new_original_copy'] for a in sm['rows'])==2 and sum(a['published_original_reused'] for a in sm['rows'])==1
published=j(HERE/'runtime-input-and-published-author-bindings.json');cp=j(HERE/'actual-author4-math-checkpoint21YN.json');dp=j(HERE/'actual-author4-source-done21YN.json')
assert cp['status']=='pushed' and cp['remote_tip']==published['actual_author4_math_tip']=='4abbd8bfda4a92fa91dcea47ab96d61422595054'
assert dp['status']=='pushed' and dp['remote_tip']==published['actual_author4_done_tip']=='355a21ea2bcc492f525a387b757eea74151d4400'
assert set(published['actual_author4_done_ids'])<=set(dp['ids']) and len(published['actual_author4_done_ids'])==4
assets={a['asset']['path']:a['asset'] for a in cp['assets']}
for a in published['author4_formal_objects']:
 p=R/a['path'];assert sha(p)==a['sha256']==assets[a['path']]['sha256'] and p.stat().st_size==a['size']
for a in sm['rows']:
 if a['published_original_reused']:assert assets[a['target_path']]['sha256']==a['sha256'] and a['actual_published_asset']==assets[a['target_path']]
inp=published['runtime_input'];p=R/inp['published_path'];assert p.stat().st_size==4080 and sha(p)==inp['sha256'] and inp['actual_asset']['sha256']==inp['sha256']
assert inp['actual_asset']['commit']=='32f586b7cb13b85c9c3386a93e3f530879162937'
assert sha(R/published['published_raw_binding_path'])==published['published_raw_binding_asset']['sha256']==assets[published['published_raw_binding_path']]['sha256']
for a in j(HERE/'comparison-bindings.json')['full_formal_objects_sameSHA_prior_read_reused']:
 p=R/a['path'];assert p.stat().st_size==a['size'] and sha(p)==a['sha256']
scope=j(HERE/'original-program-and-complete-report-scope.json');assert (scope['JSON_top_fields'],scope['JSON_rows'],scope['JSON_row_fields'])==(18,3,9)
assert scope['report']['fractional_sum']=='36019/60' and scope['report']['fractional_sum_minus_W']=='199/60' and scope['report']['minimum_ic']=='0'
assert not scope['code']['main_guard'] and scope['code']['import_runs_everything'] and scope['status_is_old_saved_not_current_run']
ind=j(HERE/'independent-large-two-related-read-boundary.json');assert (ind['report_top_fields'],ind['type_rows'],ind['IC_rows'],ind['current_extra_primary_receipts'],ind['current_extra_done'])==(34,63,258,0,0)
assert ind['code_fullread'] and ind['report_fullread'] and ind['original_copies_in_this_stage']==0
for a in ind['related_rows']:
 p=Path(a['local_path']);assert p.stat().st_size==a['size'] and sha(p)==a['sha256']
for key in ('current_normal_show_runs','current_source_body_rereads','previous_extra_related_done','source_imports','source_runs','new_math_runs'):assert sm[key]==0
w=S/'cleanup/workspaces/Boss4/r3-fractional-global-author-audit-and-direct-review-three-primary'
receipts=j(w/'semantic-receipts.json');assert {a['id'] for a in receipts}=={a['id'] for a in sm['rows']}
for a in receipts:
 assert a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['root_claim_local_sync']=='synced'
 for rp in a['targets']:assert resolve(rp).is_file(),rp
missing=[]
for p in S.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#'):continue
  target=link.split('#')[0]
  if target and not (p.parent/target).is_file():missing.append([str(p.relative_to(S)),link])
assert not missing,missing
manifest=j(HERE/'content-manifest.json')
for a in manifest['files']:
 p=S/a['path'];assert p.is_file() and p.stat().st_size==a['size'] and sha(p)==a['sha256']
copy=j(w/'copy-files.json');paths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}
assert set(copy['files'])==paths
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':3,'primary_bytes':11034,'complete_formal_objects':1,'new_original_copies':2,'published_original_reuses':1,'source_imports':0,'source_runs':0,'new_mathematical_runs':0,'missing_links':0,'raw_claim_status':'pushed','raw_local_sync_status':'synced','not_a_new_IC_or_fractional_verification':True,'content_manifest_files':len(manifest['files']),'copy_files':len(paths)}
(HERE/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
