from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent;S=HERE.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text())
def resolve(rp):
 p=S/rp
 return p if p.is_file() else R/rp
sm=j(HERE/'source-manifest.json');og=j(HERE/'ownership-gate.json');raw=j(HERE/'root-actual-full9-claim.json');proof=j(HERE/'independent-sync-preservation.json')
assert (raw['status'],raw['actor'],len(raw['ids']),raw['remote_tip'],raw['local_sync']['status'])==('pushed','Boss4',9,'62c208d4e39bedb8ca624cd06eb2b58da67f0b8c','needs-attention')
assert og['raw_original_local_sync']==raw['local_sync'] and og['remote_tip']==raw['remote_tip']
assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(a['same'] for a in proof['tracked']) and not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept'] and proof['stash']=='f32474a441f7c8ac7c586de9cbdd968047974719'
ids={'1990d9140791350ba8da','ce434cd1722c392c35d5'};assert sm['primary_sources']==2 and sm['primary_bytes']==30688 and {a['id'] for a in sm['rows']}==ids and ids<=set(raw['ids'])
assert set(og['other_seven_claim_ids_not_processed'])==set(raw['ids'])-ids and len(og['other_seven_claim_ids_not_processed'])==7
for a in sm['rows']:
 p=S/a['target_path'];b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
 ca=j(S/a['acquisition_target'])['source'];assert ca['id']==a['id'] and ca['sha256']==a['sha256'] and ca['blob']==a['blob']
 o=next(x for x in og['owner_records'] if x['id']==a['id']);assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',a['sha256'])
 assert a['first_primary'] and a['current_full_body_read'] and a['worker_actual_normal_shows']==a['current_source_body_rereads']==a['current_source_imports']==a['current_source_runs']==0
assert sm['Root_actual_normal_shows']==2 and sm['worker_actual_normal_shows']==0 and sm['current_first_full_body_reads']==2 and sm['report_first_parse_for_fullreading']==1
assert sm['source_imports']==sm['source_runs']==sm['new_math_runs']==0
inp=j(HERE/'actual-runtime21-input-bindings.json');plan=j(HERE/'complete-runtime-input-reading-scope.json');assert len(inp['rows'])==inp['physical_JSON_files']==21 and inp['original_bytes']==357689 and sum(a['size'] for a in inp['rows'])==357689
assert inp['current_existing_sameSHA_original_reuses']==21 and inp['current_new_normal_shows']==inp['current_new_original_copies']==0 and inp['current_new_complete_semantic_input_reads']==16 and inp['prior_complete_sameSHA_fullread_reuses']==5
assert plan['all_21_consumed_input_contracts_complete'] and plan['actual_complete_view_read_ranges']==['1..486'] and plan['new_complete_semantic_input_reads_finished']==16 and plan['new_complete_semantic_input_reads_pending']==0
new=old=0
for a in inp['rows']:
 p=R/a['published_path'];b=p.read_bytes();assert len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob']
 rd=a['current_read_scope'];assert rd['id']==a['id']
 if rd['prior_complete_fullread_sameSHA_reuse']:old+=1;assert not rd['current_full_input_read'] and not rd['current_JSON_parse']
 else:new+=1;assert rd['current_full_input_read'] and rd['current_JSON_parse']
 assert not a['current_new_normal_show'] and not a['current_new_original_copy'] and not a['current_extra_primary_receipt_or_done']
assert (new,old)==(16,5)
aux=plan['auxiliary_weight_map_lossless_compression'];assert aux['all4095orderedkeysverified'] and aux['default']==6391 and aux['default_entries']==2509 and aux['exceptions']==1586 and aux['all_exception_values_preserved'] and aux['all4095weights_positive']
rscope=j(HERE/'complete-original-report-reading-scope.json');assert rscope['code_fullread'] and rscope['report_fullread'] and rscope['all_11_original_records_fullread'] and rscope['report_records']==11 and rscope['report_view_lines']==105 and rscope['report_target_counts']==[3,3,3,3,2,2,2,2,2,1,3]
assert rscope['report_record_field_counts']==[6]*11 and rscope['target_fields']==7 and rscope['positive_source_witness_fields']==8 and rscope['physical_runtime_inputs_required']==21 and rscope['main_guard'] and rscope['cap2_slack_not_asserted']
contracts=j(HERE/'mathematical-and-implementation-contracts.json');assert contracts['report_targets']==26 and contracts['positive_source_witnesses']==40 and contracts['reported_original_total_checks']==28481 and contracts['all11_controller_nodes_total']==2911 and contracts['old_report_ratio_max']=='2/3 atfractional_actual_load_failure target3' and contracts['all40_selected_positive_witness_cuts_equal_theirtarget']
assert contracts['current_source_imports']==contracts['current_original_runs']==contracts['new_math_runs']==0 and not contracts['no_primary_receipts_yet']
comps=j(HERE/'current-formal-comparison-bindings.json');assert len(comps['current_full_formal_reads'])==2 and len(comps['sameSHA_prior_full_formal_reads_reused'])==14
for a in comps['current_full_formal_reads']+comps['sameSHA_prior_full_formal_reads_reused']:
 p=R/a['path'];assert p.stat().st_size==a['size'] and sha(p)==a['sha256']
pub=j(HERE/'previous-probe2-actual-publication-binding.json');cp=j(HERE/'actual-probe2-math-checkpoint2YZ.json');dp=j(HERE/'actual-probe2-source-done2YZ.json');assert cp['status']=='pushed' and cp['remote_tip']==pub['actual_math_tip']=='07d79149c1ac016a52814914a09680f491ac2cb4' and dp['status']=='pushed' and dp['remote_tip']==pub['actual_done_tip']=='dcbf7e8b003016262f71d18bdbf7d503ac9dc8de'
assert set(pub['actual_done_IDs'])<=set(dp['ids']) and pub['actual_program_asset'] in [a['asset'] for a in cp['assets']] and sha(R/pub['actual_program_asset']['path'])==pub['actual_program_asset']['sha256']
w=S/'cleanup/workspaces/Boss4/r3-prefix-request-cap-program-and-eleven-original-records-two-primary';receipts=j(w/'semantic-receipts.json');assert {a['id'] for a in receipts}==ids
for a in receipts:
 assert a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'] and a['current_first_full_body_read'] and a['current_source_body_rereads']==a['current_source_imports']==a['current_original_mathematical_entries']==a['current_new_mathematical_entries']==a['extra_runtime_input_primary_done']==0
 for rp in a['targets']:assert resolve(rp).is_file(),rp
missing=[]
for p in S.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#'):continue
  t=link.split('#')[0]
  if not t:continue
  q=(p.parent/t).resolve()
  if q.is_file():continue
  try:rp=q.relative_to(S)
  except ValueError:missing.append([str(p.relative_to(S)),link]);continue
  if not (R/rp).is_file():missing.append([str(p.relative_to(S)),link])
assert not missing,missing
mf=j(HERE/'content-manifest.json')
for a in mf['files']:
 p=S/a['path'];assert p.is_file() and p.stat().st_size==a['size'] and sha(p)==a['sha256']
paths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()};assert set(j(w/'copy-files.json')['files'])==paths
result={'status':'PASS-STRUCTURE-ONLY','primary_sources':2,'primary_bytes':30688,'formal_objects':1,'runtime_physical_JSON_files':21,'runtime_original_bytes':357689,'new_runtime_normal_shows':0,'new_runtime_original_copies':0,'actual_new_semantic_full_input_reads':16,'sameSHA_prior_fullread_input_reuses':5,'source_imports':0,'source_runs':0,'new_math_runs':0,'missing_links':0,'raw_claim_status':'pushed','raw_local_sync_status':'needs-attention','not_a_new_IC_or_request_calculation':True,'content_manifest_files':len(mf['files']),'copy_files':len(paths)}
(HERE/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
