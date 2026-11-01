"""Metadata/hash/blob/capture/owner/whole-JSON-schema/link checks; no original or mathematical run."""
from pathlib import Path
import hashlib,json,re,sys

def main():
 s=Path(sys.argv[1]).resolve();r=Path(sys.argv[2]).resolve()
 e=s/'archives/customer-attraction/tools/evidence/reserve-probes-and-cone-records-four-primary'
 w=s/'cleanup/workspaces/Boss4/r3-reserve-probes-and-cone-records-four-primary'
 read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 resolve=lambda p:s/p if (s/p).is_file() else r/p
 for j in read(e/'content-manifest.json')['files']:
  p=s/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 raw=read(e/'root-actual-claim6-receipt.json');gate=read(e/'ownership-gate.json');proof=read(e/'independent-sync-preservation.json')
 assert (raw['actor'],raw['status'],len(raw['ids']),raw['remote_tip'])==('Boss4','pushed',6,'e3076230395d39af8467f8d7b65ef0dcb847c452')
 assert raw['local_sync']['status']==gate['claim_local_sync']=='needs-attention' and raw['local_sync']==gate['raw_local_sync_unmodified']
 assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(j['same'] for j in proof['tracked'])
 assert not proof['missing'] and not proof['different'] and not proof['unmerged'] and proof['stash_kept']
 assert proof['stash']==gate['independent_proof']['stash']=='48503c90846a171e6c88dd68999096249a5284ac'
 rows=read(e/'source-manifest.json')['rows'];owners={j['id']:j for j in gate['owner_records']}
 assert len(rows)==4 and sum(j['size'] for j in rows)==7782 and set(owners)=={j['id'] for j in rows}
 assert set(gate['other_two_claim_ids_not_processed'])==set(raw['ids'])-set(owners)
 for j in rows:
  p=s/j['target_path'];b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes()
  assert cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256'] and cj['source']['blob']==j['blob']
  o=owners[j['id']];assert (o['owner'],o['disposition'],o['source_sha256'])==('Boss4','in-progress',j['sha256'])
  assert j['full_file_read'] and j['current_source_imports']==j['current_source_runs']==0
 inp=read(e/'runtime-input-bindings.json');assert len(inp['rows'])==6 and sum(j['size'] for j in inp['rows'])==47809
 assert inp['read_only_normal_show_calls']==6 and inp['already_published_originals_reused']==4 and inp['new_related_raw_copies']==2 and inp['new_related_raw_bytes']==12534
 assert inp['current_related_claims']==inp['current_related_done']==0 and inp['missing_runtime_inputs']==[] and not inp['replay_layout_prepared']
 assert inp['required_external_files_saved_program']==6 and inp['cone_external_input_files']==0 and inp['cone_external_packages']==['numpy','scipy.optimize.linprog'] and inp['author_code_imports']==[]
 for j in inp['rows']:
  p=resolve(Path(j['target_path']));b=p.read_bytes();assert len(b)==j['size'] and sha(p)==j['sha256'] and b==Path(j['local_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['blob']
  cap=s/j['acquisition_target'];cj=read(cap);assert cap.read_bytes()==Path(j['actual_normal_show_capture']).read_bytes() and cj['source']['id']==j['id'] and cj['source']['sha256']==j['sha256']
  assert j['full_file_read'] and j['current_normal_show_exit_code']==0 and j['related_only'] and not j['current_claim'] and not j['current_done']
  obj=read(p);assert list(obj)==j['all_original_top_fields']
  if j['policy_action_rows']:
   acts=obj.get('policy',obj.get('strategy'));acts=acts.get('actions') if isinstance(acts,dict) else acts
   assert len(acts)==j['policy_action_rows'] and len({tuple(a['history']) for a in acts})==len(acts)
 assert sorted(j['policy_action_rows'] for j in inp['rows'])==[0,0,31,43,43,259]
 rf=read(e/'full-report-field-binding.json');sv=read(s/next(j['target_path'] for j in rows if j['id']=='fa1c3c1d21076f265f1a'));co=read(s/next(j['target_path'] for j in rows if j['id']=='5b30a9cde6593ee61594'))
 assert sv==rf['saved_full_original'] and co==rf['cone_full_original'] and rf['saved_fields']==36 and rf['cone_top_and_case_fields']==26 and not rf['arithmetics_or_policy_replay_performed']
 assert len(sv)==4 and all(len(x)==9 for x in sv) and [x['W'] for x in sv]==[33,41,597,26] and [x['violations'] for x in sv]==[0]*4
 assert [x['max_F_minus_2W_plus_U_past'] for x in sv]==['-61/6','-7/2','-156','0']
 assert list(co)==['status','tests'] and len(co['tests'])==6 and all(len(x)==4 and x['cones_tested']==12 for x in co['tests'])
 cb=read(e/'comparison-bindings.json');assert len(cb['full_formal_objects_read'])==7 and cb['current_full_formal_reads']==5 and cb['sameSHA_prior_full_formal_reads_reused']==2
 for j in cb['full_formal_objects_read']+[cb['status_only_half5_reference']]:
  p=r/j['path'];assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'],j['path']
 assert not cb['status_only_half5_reference']['full_file_read_in_this_batch'] and not cb['raw245_and_eb_primary_done_inferred']
 assert len(cb['pending_reserve3_formal_bodies'])==2
 for j in cb['pending_reserve3_formal_bodies']:
  p=Path(j['frozen_path']);assert p.is_file() and p.stat().st_size==j['size'] and sha(p)==j['sha256'] and j['publication_status'].startswith('pending') and j['remote_math_tip'] is None
 con=read(e/'mathematical-and-runtime-contracts.json');assert con['cone']['attempts']==72 and con['cone']['LP_failures_count_as_None'] and not con['cone']['negative_has_LP_success_counts'] and not con['cone']['negative_exact_certificate'] and not con['cone']['candidate_exact_nonnegative_normalization_IC_gap_reaudit']
 assert con['io']['main_guards'] and con['io']['help_runs_main'] and not con['io']['stale_opposite_output_removed'] and not con['io']['replay_layout_prepared']
 receipts=read(w/'semantic-receipts.json');assert len(receipts)==4 and {j['id'] for j in receipts}==set(owners) and all(j['disposition']=='retained' for j in receipts)
 for j in receipts:
  assert j['full_file_reviewed'] and j['related_material_checked'] and j['unique_content_accounted_for'] and j['root_claim_local_sync']=='needs-attention' and j['current_original_mathematical_entries']==j['current_new_mathematical_entries']==0
  for rp in j['targets']:assert resolve(Path(rp)).is_file(),rp
 links=0;ids=[]
 for p in s.rglob('*.md'):
  if '/original/' in str(p) or '/related-original/' in str(p):continue
  t=p.read_text()
  if '/state/' in str(p):
   assert t.startswith('---\n');front=t.split('---',2)[1]
   for k in ('id','kind','type_tag','title','status','summary','source_refs'):assert re.search('^'+k+':',front,re.M),(p,k)
   ids.append(re.search(r'^id:\s*(.+)$',front,re.M).group(1))
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
   if target.startswith(('http:','https:','#')):continue
   q=(p.parent/target.split('#')[0]).resolve();rp=q.relative_to(s);assert resolve(rp).is_file(),(p,target);links+=1
 assert len(ids)==len(set(ids))==1
 actual=sorted(str(p.relative_to(s)) for p in s.rglob('*') if p.is_file());assert sorted(read(w/'copy-files.json'))==actual
 result=dict(status='PASS-STRUCTURE-ONLY',primary_files=4,primary_bytes=7782,formal_objects=1,semantic_receipts=4,actual_related_input_files=6,actual_related_input_bytes=47809,read_only_normal_show_calls=6,already_published_input_reuses=4,new_related_raw_copies=2,new_related_raw_bytes=12534,related_primary_done_inferred=False,full_input_policy_action_rows=376,saved_report_cases=4,saved_fields=36,cone_groups=6,cone_top_and_case_fields=26,comparison_full_objects=7,pending_reserve3_formal_objects=2,raw_local_sync='needs-attention-unmodified',independent_preservation='3untracked/2tracked same; no missing/different/unmerged; stash kept',markdown_links=links,copy_files=len(actual),source_imports=0,CLI_runs=0,Fraction_verification_runs=0,LP_runs=0,BI_runs=0,IC_replays=0,menu_replays=0,new_mathematical_program_runs=0,note='Only hash/blob/normalcapture/owner/JSONliteral/strategyrow schema/links; no profit/IC/SPE/LP/BI/oldnegative probe run, no new mathematical certification.')
 (e/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
