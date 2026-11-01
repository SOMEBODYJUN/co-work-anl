from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent;S=HERE.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text())
def resolve(rp):
 p=S/rp
 return p if p.is_file() else R/rp
sm=j(HERE/'source-manifest.json');og=j(HERE/'ownership-gate.json');raw=j(HERE/'root-actual-full-claim.json');proof=j(HERE/'independent-sync-preservation.json')
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',20,'5ccaa56066cb6971948dec93190cbe59ac0d8308','needs-attention')
assert og['raw_original_local_sync']==raw['local_sync'] and og['remote_tip']==raw['remote_tip']
assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(a['same'] for a in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']=='a4de73558ff05ccd6f3b672b58294f72b23af5f3'
ids={'df2203209254d4f8c97a','67a9f8b0763e5057f217'};assert len(sm['rows'])==sm['primary_sources']==2 and sm['primary_bytes']==3835 and {a['id'] for a in sm['rows']}==ids and ids<=set(raw['ids'])
assert set(og['other_claim_ids_not_processed'])==set(raw['ids'])-ids and len(og['other_claim_ids_not_processed'])==18
for a in sm['rows']:
 p=S/a['target_path'];b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
 cap=j(S/a['acquisition_target'])['source'];assert cap['id']==a['id'] and cap['sha256']==a['sha256'] and cap['blob']==a['blob']
 ow=next(x for x in og['owner_records'] if x['id']==a['id']);assert (ow['owner'],ow['disposition'],ow['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['source_fullread'] and a['previous_related_extra_done']==0 and a['current_normal_shows']==a['current_source_body_rereads']==a['current_source_runs']==a['current_source_imports']==0 and not a['current_source_JSON_reparse']
for k in ('current_normal_shows','current_source_body_rereads','current_source_JSON_reparses','source_imports','source_runs','new_math_runs','previous_related_extra_done'):assert sm[k]==0
dep=j(HERE/'existing-runtime-certificate-binding.json');a=dep['certificate'];p=R/a['existing_single_original'];b=p.read_bytes();assert len(b)==4339 and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
assert sha(R/dep['old_published_dependency_metadata_path'])==dep['old_published_dependency_metadata_sha256'] and dep['matching_metadata_row']['sha256']==a['sha256']
assert not dep['current_new_show'] and not dep['current_source_body_reread'] and not dep['current_source_JSON_reparse'] and not dep['current_new_copy'] and not dep['extra_primary_receipt_or_done']
pub=j(HERE/'published-author-and-original-audit-bindings.json');au=j(HERE/'actual-author-audit3-math-checkpoint14YQ.json');assert au['status']=='pushed' and au['remote_tip']==pub['author_audit3_actual_math_tip']=='5af7f8a0b6026441878f436d1aa20dc10bc23ed7'
aa=pub['author4_published_full_math_capture_asset'];assert aa in [x['asset'] for x in au['assets']] and sha(R/pub['author4_published_full_math_capture_path'])==aa['sha256']
ac=j(R/pub['author4_published_full_math_capture_path']);assert ac['status']=='pushed' and ac['remote_tip']==pub['author4_actual_math_tip']=='4abbd8bfda4a92fa91dcea47ab96d61422595054'
cmp=j(HERE/'comparison-bindings.json')
for a in cmp['sameSHA_prior_full_formal_objects']:
 p=R/a['path'];assert p.stat().st_size==a['size'] and sha(p)==a['sha256']
ix=j(HERE/'actual-independent2-math-checkpoint10YS.json');ixd=j(HERE/'actual-independent2-source-done10YS.json');ind=cmp['same_frozen_independent2_object'];assert ix['status']=='pushed' and ix['remote_tip']==ind['actual_math_tip']=='f6f576419f32bd3fe10b12792626f72174db9124' and ixd['status']=='pushed' and ixd['remote_tip']==ind['actual_done_tip']=='05e2a9df0cb0ff15eb2cb3ec65c18a7fde1ed10a'
assert {'52523113cdc7c8cff601','eca2ddadd311de0e4b87'}<=set(ixd['ids']) and ind['actual_asset'] in [x['asset'] for x in ix['assets']] and sha(R/ind['path'])==ind['sha256']==ind['actual_asset']['sha256']
sc=j(HERE/'original-numerical-and-exact-evidence-scope.json');assert (sc['m'],sc['k'],sc['types'],sc['ordered_histories'],sc['IC_rows'],sc['successful_original_report_top_fields'],sc['failed_normal_LP_report_fields'])==(3,6,63,43,258,10,4)
assert not sc['code_has_main_guard'] and sc['fixed_controller'] and sc['query_not_optimized'] and sc['customer_weights_optimized'] and not sc['current_source_JSON_reparsed']
assert sc['saved_report']['exact_gap']=='199/60' and sc['saved_report']['minimum_exact_ic']=='0' and sc['saved_report']['unit_customers']==817 and sc['saved_report']['exact_witness']
w=S/'cleanup/workspaces/Boss4/r3-fractional-global-fixed-cone-discovery-probe-two-primary';rs=j(w/'semantic-receipts.json');assert {a['id'] for a in rs}==ids
for a in rs:
 assert a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['root_claim_local_sync']=='needs-attention' and not a['current_source_JSON_reparse']
 for rp in a['targets']:assert resolve(rp).is_file(),rp
nxt=j(w/'next-candidates.json');assert nxt['COPY2_code2_reserved_to_Root_do_not_touch']==['ebb03405d94cb26ceeec','d4aa1e5bbfcadc0d6bfd'] and nxt['bytes']==30688 and not nxt['source_body_read'] and not nxt['worker_claimed']
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
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':2,'primary_bytes':3835,'formal_objects':1,'source_imports':0,'source_runs':0,'new_math_runs':0,'original_report_reparsed':False,'existing_certificate_recopied':False,'missing_links':0,'raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','not_a_new_LP_or_exact_IC_verification':True,'content_manifest_files':len(mf['files']),'copy_files':len(paths)}
(HERE/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
