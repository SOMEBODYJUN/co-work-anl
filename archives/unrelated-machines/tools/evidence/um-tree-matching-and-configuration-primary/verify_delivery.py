"""Saved-byte/JSON/link integrity only; no mathematical source import or execution."""
from pathlib import Path
import argparse,hashlib,json,re,random
ER=Path('archives/unrelated-machines/tools/evidence/um-tree-matching-and-configuration-primary');WS=Path('cleanup/workspaces/Boss4/r3-um-tree-matching-and-configuration-primary')
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(r):
  r=Path(r);assert not r.is_absolute() and '..' not in r.parts
  x=root/r;return x if x.is_file() else fallback/r
 def load(r):return json.loads(resolve(r).read_text())
 groups=[load(ER/x)['sources'] for x in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,1,14];items={x['id']:x for g in groups for x in g};assert len(items)==20;checks=[]
 for sid,x in items.items():
  raw=resolve(x['preserved_repo_path']).read_bytes();assert len(raw)==x['source_size'] and sha(raw)==x['source_sha256'] and x['full_file_reviewed'] and 'pending' not in x['read_scope'];checks.append(dict(id=sid,size=len(raw),sha256=sha(raw),passed=True))
 ids={x['id'] for x in groups[0]};claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==ids
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==5 and {x['id'] for x in owners}==ids and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==items[x['id']]['source_sha256'] for x in owners)
 runs=load(ER/'runs/execution-manifest.json')['executions'];assert len(runs)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in runs) and {x['source_sha256'] for x in runs}=={x['source_sha256'] for x in groups[0]}
 for x in runs:assert resolve(x['stdout']).is_file() and resolve(x['stderr']).read_bytes()==b''
 artifacts=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(artifacts)==16
 for x in artifacts:
  raw=resolve(x['repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256']
 history=load(ER/'historical-comparison-and-version-scope.json');assert len(history['comparisons'])==5
 for x in history['comparisons']:
  prev=load(x['historical']);prev=prev[x['historical_subobject']] if x['historical_subobject'] else prev;assert x['all_fields_equal'] and load(x['current'])==prev
 old=load(ER/'comparison/evidence/runs/unrelated_machines/joint_matching_completion_audit.json');rng=random.Random(20261016);u=[(a,b,c) for a in range(3) for b in range(3) for c in range(3)];samples=[[list(t) for t in rng.sample(u,rng.randint(1,12))] for _ in range(50)];assert samples==old['actual_q3_sampled_tripartite_inputs'] and history['all50_frozen_q3_examples_equal_current_deterministic_seed_recipe']
 manuscript=resolve(ER/'comparison/research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md').read_text();section=manuscript[manuscript.index('## 3a.'):manuscript.index('\n## 4.')];assert sha(section.encode())==history['joint_versions']['current_section3a_sha256']=='ce73c48ce55266921f1de53708fe9847a4a63922059e8b6172eed93745968237' and sha(manuscript.encode())==history['joint_versions']['current_whole_sha256']=='8cf637c20618062a98d4038e7873987acf06bf426a583a6a678d974d7b103ba3'
 scope=load(ER/'mathematical-execution-scope.json');assert [scope[k] for k in ['primary_CLI_executions_this_batch','supplemental_mathematical_process_executions_this_batch','total_mathematical_process_executions_this_batch']]==[5,0,5] and scope['imported_unguarded_audit_body_evaluations']==0 and not scope['production_main_rerun_by_independent_import'] and not scope['baseline_main_executed']
 ma=load(ER/'runs/tree-markov-independent.stdout');jo=load(ER/'runs/joint-completion.stdout');ji=load(ER/'runs/joint-completion-independent.stdout');k5=load(ER/'runs/K5-config-slots.stdout');kn=load(ER/'runs/knapsack-envelope.stdout')
 assert ma['independent_complete_assignments_enumerated']==32 and ma['integer_optimum']=='1' and len(ma['glued_support'])==4 and ma['probability_of_best_completion_2']=='1/4'
 assert [jo[k] for k in ['reduction_instances','yes_instances','exhaustive_oracle_search_nodes']]==[309,194,24927] and len(jo['fractional_rounding_cases'])==4
 assert [x['independent_schedule_search_states'] for x in ji['reduction']]==[4,12,26065] and sum(x['positive_delta_queries'] for x in ji['reduction'])==518 and len(ji['conditional_rounding']['exact_fractional_cases'])==3 and ji['conditional_rounding']['empty_task_case']
 assert sum(x['star_escape_patterns'] for x in ji['block_cuts']['path_orientation_enumeration'])==2728 and sum(x['floor_interval_samples'] for x in ji['block_cuts']['exact_interval_checks'])==246 and all(x['r_at_threshold']==1 for x in ji['block_cuts']['exact_interval_checks'])
 assert [k5[x] for x in ['K','job_count','machine_count','primary_envelope','refuted_factorial_bound','strict_excess','OPT']]==[5,15,16,'287/144','239/120','1/720','1'] and k5['bad_actual_complete_ST_matching']['makespan']=='287/144' and k5['good_actual_complete_ST_matching']['makespan']=='1' and len(k5['jobs'])==15 and len(k5['all_ST_slots_and_positive_edges'])==16
 assert sum(x['truth_tables_examined'] for x in kn['rows'])==32906 and sum(y['tuples_examined'] for x in kn['rows'] for y in x['p'])==20881 and sum(len(x['p']) for x in kn['rows'])==14 and [x['admissible_matroid_count'] for x in kn['rows']]==[2,4,8,16]
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}==ids
 for x in rec:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']) and x['disposition']=='retained' and all(resolve(t).is_file() for t in x['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==4 and not rel['formal_hypergraph_written'];formal=[]
 for x in rel['formal_comparison_snapshots']:
  raw=resolve(x['preserved_snapshot_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256'];formal.append(dict(repo_path=x['repo_path'],preserved_snapshot_path=x['preserved_snapshot_path'],passed=True))
 assert len(formal)==5;links=[]
 for doc in [Path(x) for x in rel['new_computation_objects']]+[ER/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute() and '..' not in Path(f).parts and (root/f).is_file()
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root)) for x in root.rglob('*') if x.is_file())
 out=dict(check_kind='saved bytes, saved JSON, seed-input recipe and links only; no mathematical source execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=1,comparison_source_count=14,source_byte_checks=checks,runtime_artifact_hash_count=len(artifacts),historical_comparison_count=5,all50_frozen_q3_inputs_equal_current_recipe=True,section3a_hash_and_formal_scope_preserved=True,formal_comparison_snapshot_hash_checks=formal,receipt_count=len(rec),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_CLI_executions_observed=5,supplemental_mathematical_process_executions_observed=0,total_mathematical_process_executions_this_batch=5,imported_unguarded_audit_body_evaluations=0,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_mathematical_process_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
