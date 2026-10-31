"""Saved-byte/JSON/link integrity only; never import or execute mathematical sources."""
from pathlib import Path
import argparse, hashlib, json, re
ER=Path('archives/unrelated-machines/tools/evidence/um-normalized-rails-and-gates-primary')
WS=Path('cleanup/workspaces/Boss4/r3-um-normalized-rails-and-gates-primary')
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(r):
  r=Path(r);assert not r.is_absolute() and '..' not in r.parts
  x=root/r;return x if x.is_file() else fallback/r
 def raw(r):return resolve(r).read_bytes()
 def load(r):return json.loads(raw(r))
 groups=[load(ER/x)['sources'] for x in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,1,11]
 items={x['id']:x for g in groups for x in g};assert len(items)==17;checks=[]
 for sid,x in items.items():
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size'] and sha(b)==x['source_sha256'] and x['full_file_reviewed'] and 'pending' not in x['read_scope'];checks.append(dict(id=sid,size=len(b),sha256=sha(b),passed=True))
 ids={x['id'] for x in groups[0]};claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(claim['ids'])==ids and claim['local_sync']['status']=='needs-attention'
 resolution=load(ER/'independent-sync-resolution.json');assert resolution['status']=='independently-resolved-for-CD-source-processing; separate older-remote-tree-rollback-repair-active' and resolution['actual_head']==claim['remote_tip'] and set(resolution['actual_ids'])==ids and resolution['untracked_192_files_exact'] and resolution['unmerged']=='' and resolution['original_receipt_unchanged']
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==5 and {x['id'] for x in owners}==ids and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==items[x['id']]['source_sha256'] for x in owners)
 execution=load(ER/'runs/execution-manifest.json');runs=execution['executions'];assert len(runs)==5 and all(x['exit_code']==0 and not x['timed_out'] and x['mathematical_program_execution'] for x in runs) and {x['source_sha256'] for x in runs}=={x['source_sha256'] for x in groups[0]}
 for x in runs:
  assert resolve(x['stdout']).is_file() and raw(x['stderr'])==b''
  assert load(ER/('runs/'+x['name']+'.execution.json'))==x
 assert execution['source_CLI_invocations_including_nested_guard']==6 and execution['successful_primary_audit_body_executions']==5 and execution['nested_expected_refusal_CLI_invocations']==1 and execution['nested_refusal_executed_mathematical_audit_body'] is False
 artifacts=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(artifacts)==20
 for x in artifacts:
  b=raw(x['repo_path']);assert len(b)==x['size'] and sha(b)==x['sha256']
 history=load(ER/'historical-comparison-and-version-scope.json');assert len(history['comparisons'])==5
 for x in history['comparisons']:
  current=load(x['current']);old=load(x['historical'])
  for key in x['historical_keys']:old=old[key]
  diff=sorted(k for k in set(current)|set(old) if current.get(k)!=old.get(k));assert diff==x['difference_keys']
  assert (current==old)==x['all_fields_equal']
  if x['name']=='dual-rail-flow':
   assert diff==['runtime_seconds'] and x['all_mathematical_fields_equal'] and {k:v for k,v in current.items() if k!='runtime_seconds'}=={k:v for k,v in old.items() if k!='runtime_seconds'} and x['runtime_values']==dict(current=current['runtime_seconds'],historical=old['runtime_seconds'])
  else:
   assert diff==[]
   if x.get('byte_equal'):assert raw(x['current'])==raw(x['historical'])
 scope=load(ER/'mathematical-execution-scope.json');assert [scope[k] for k in ['successful_primary_CLI_executions_this_batch','primary_mathematical_audit_body_executions_this_batch','supplemental_mathematical_audit_executions_this_batch','nested_expected_refusal_source_CLI_invocations','total_source_CLI_invocations_including_guard','total_mathematical_audit_body_executions_this_batch','imported_unguarded_mathematical_audit_bodies']]==[5,5,0,1,6,5,0] and scope['nested_refusal_executes_mathematical_body'] is False and scope['source_bytes_modified'] is False and scope['new_blind_reviews']==0
 nf=load(ER/'runs/nearflat-moments.payload.json');assert nf['source_sha256']==items['905f727f1ab4e879f71d']['source_sha256'] and len(nf['cases'])==6
 accepted=[x['result'] for x in nf['cases'] if not x['result'].get('certificate_rejected')];rejected=[x['result'] for x in nf['cases'] if x['result'].get('certificate_rejected')]
 assert len(accepted)==5 and len(rejected)==1 and [len(x['certificate']['moments']) for x in accepted]==[4521,4521,5682,4521,81] and rejected[0]['trace_defect']=='5' and 'certificate' not in rejected[0]
 assert all(set(['G','A','D','rho','beam','moments'])<=set(x['certificate']) and len(x['certificate']['beam'])==x['n'] and len(x['selected_losses'])==x['n'] for x in accepted)
 assert [x['ranks'] for x in accepted+rejected]==[[3,3],[3,4],[3,4],[3,4],[3,4],[3,4]] and accepted[4]['T']=='0'
 half=load(ER/'runs/dual-rail-half.stdout');flow=load(ER/'runs/dual-rail-flow.stdout');assert half['code_sha256']==items['e28cf851ec5849b0c84a']['source_sha256'] and flow['code_sha256']==items['12180265294156d43522']['source_sha256']
 assert half['seed']==558437 and len(half['random_trials'])==250 and half['giant_A_bit_length']==258 and half['sharp']['all_sigma_makespan_histogram']=={'3/2':13824,'2':18944} and half['sharp']['exhaustive_assignment_count']==32768 and len(half['sharp']['all_source_assignments'])==8 and half['sharp']['exact_OPT']=='3/2'
 assert flow['seed']==110723 and flow['counts']==scope['dual_flow']['counts'] and flow['variable_case_counts']==scope['dual_flow']['variable_cases']
 assert [flow['sharp_repeated_occurrence_instance'][k] for k in ['machines','jobs','all_assignment_states','exact_optimum']]==[10,15,32768,'3/2']
 welfare=load(ER/'runs/gated-welfare.payload.json');ind=load(ER/'runs/gated-independent.payload.json');targetsha=items['f3baaa435db0db5b9f86']['source_sha256'];inputpath=items['86f59227811df6eaaa43']['preserved_repo_path'];inputsha=items['86f59227811df6eaaa43']['source_sha256']
 assert welfare['code_sha256']==ind['code_sha256']==targetsha and ind['code_sha256']!=items['750c51a80fb992b9c1dd']['source_sha256']
 assert welfare['summary']=={'support_cases':36,'certified_optimal_welfare_lp_cases':72,'general_fractional_state_cases':2,'general_nontrivial_incidence_cases':0,'deliberate_optimal_nonbasic_coin_cases':3,'nontrivial_coin_decisions':20,'brute_um_cases':12,'max_observed_ratio':'153/130'} and welfare['ratio_grid']['points']==1025
 assert [len(welfare[k]) for k in ['support_cases','general_cases','coin_cases','brute_um_cases','large_denominator_cases']]==[36,72,3,12,2]
 assert [ind[k] for k in ['semantic_primal_dual_certificates','all_rounding_cases_with_independent_outcome_expectation','independent_expectation_calls','all_jobs_load_rechecks','independently_complete_um_instances','total_complete_schedules','existing_output_rejected_exit']]==[75,113,904,113,12,10600,2]
 assert ind['complete_legal_schedule_counts']==[8,64,16,256,24,576,96,9216,8,64,16,256] and sum(ind['complete_legal_schedule_counts'])==10600 and ind['existing_output_sha256_unchanged']==inputsha and sha(raw(inputpath))==inputsha and raw(ER/'runs/gated-welfare.payload.json')==raw(inputpath)
 guard=load(ER/'runs/nested-refusal-observation.json');assert guard['observed_exit_code']==2 and guard['source_main_audit_body_executed'] is False and guard['additional_mathematical_audit_execution'] is False and guard['input_before_and_after_sha256']==inputsha and guard['child_stdout_stderr_and_separate_duration_retained_by_original'] is False
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}==ids
 for x in rec:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']) and x['disposition']=='retained' and x['targets'] and all(resolve(t).is_file() for t in x['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==3 and not rel['formal_hypergraph_written'];formal=[]
 for x in rel['formal_comparison_snapshots']:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size'] and sha(b)==x['sha256'] and x['not_modified'];formal.append(dict(repo_path=x['repo_path'],preserved_snapshot_path=x['preserved_snapshot_path'],passed=True))
 assert len(formal)==4;links=[]
 for doc in [Path(x) for x in rel['new_computation_objects']]+[ER/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute() and '..' not in Path(f).parts and (root/f).is_file()
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root)) for x in root.rglob('*') if x.is_file())
 out=dict(check_kind='saved bytes, complete saved JSON and links only; no mathematical source execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=1,comparison_source_count=11,source_byte_checks=checks,runtime_artifact_hash_count=len(artifacts),historical_comparison_count=5,flow_only_runtime_seconds_differs=True,original_needs_attention_receipt_preserved=True,separate_independent_sync_resolution_verified=True,formal_comparison_snapshot_hash_checks=formal,receipt_count=len(rec),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),successful_primary_CLI_executions_observed=5,nested_expected_refusal_source_CLI_invocations=1,total_source_CLI_invocations_including_guard=6,total_mathematical_audit_body_executions_this_batch=5,supplemental_mathematical_audit_executions_this_batch=0,imported_unguarded_mathematical_audit_bodies=0,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_source_CLI_invocations_including_guard','total_mathematical_audit_body_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
