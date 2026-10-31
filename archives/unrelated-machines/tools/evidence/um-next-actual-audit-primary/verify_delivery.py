"""Integrity and saved-result consistency only; never imports or runs math sources."""
from pathlib import Path
import argparse,ast,hashlib,json,re
ER=Path('archives/unrelated-machines/tools/evidence/um-next-actual-audit-primary');WS=Path('cleanup/workspaces/Boss4/r3-um-next-actual-audit-primary')
def sha(r):return hashlib.sha256(r).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(r):
  r=Path(r);assert not r.is_absolute() and '..' not in r.parts
  x=root/r;return x if x.is_file() else fallback/r
 def load(r):return json.loads(resolve(r).read_text())
 groups=[load(ER/x)['sources'] for x in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,2,11];items={x['id']:x for g in groups for x in g};assert len(items)==18;checks=[]
 for sid,x in items.items():
  raw=resolve(x['preserved_repo_path']).read_bytes();assert len(raw)==x['source_size'] and sha(raw)==x['source_sha256'];assert x['full_file_reviewed'] and 'pending' not in x['read_scope'];checks.append(dict(id=sid,size=len(raw),sha256=sha(raw),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])=={x['id'] for x in groups[0]}
 runs=load(ER/'runs/execution-manifest.json')['executions'];assert len(runs)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in runs) and {x['source_sha256'] for x in runs}=={x['source_sha256'] for x in groups[0]}
 for x in runs:assert resolve(x['stdout']).is_file() and resolve(x['stderr']).read_bytes()==b''
 art=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(art)==16
 for x in art:
  raw=resolve(x['repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256']
 hist=load(ER/'historical-comparison-and-version-scope.json')['comparisons'];assert len(hist)==4
 for x in hist:
  now=load(x['current']);old=load(x['historical']);assert x['all_current_fields_equal_old'] and all(now[k]==old[k] for k in now);assert x['old_only_fields']==sorted(old.keys()-now.keys());assert x['structurally_equal']==(now==old)
  if x['name']=='price-convexification':assert x['old_only_fields']==['base_commit','command'] and {d['path'] for d in x['differences']}=={'/base_commit','/command'}
  else:assert x['structurally_equal'] and x['differences']==[]
 scope=load(ER/'mathematical-execution-scope.json');assert (scope['primary_CLI_executions_this_batch'],scope['supplemental_mathematical_process_executions_this_batch'],scope['total_mathematical_process_executions_this_batch'])==(5,0,5) and scope['unguarded_import_audit_body_evaluations']==0 and not scope['candidate_Hall_main_audit_run'] and not scope['baseline_main_audit_run']
 hj=load(ER/'runs/hall-joint-independent.stdout');hp=load(ER/'runs/hall-promise-independent.stdout');fo=ast.literal_eval(resolve(ER/'runs/forest-integrality.stdout').read_text());pr=load(ER/'runs/price-convexification.stdout');ma=load(ER/'runs/matching-residual.stdout')
 assert [hj[k] for k in ['instances','original_T_feasible','success','rejection','explicit_invalid_rejections']]==[8123,3688,4066,4057,7] and hj['source_sha256']==items['9fa5bc2e0157bd3693a9']['source_sha256'] and hj['review_sha256']==groups[0][0]['source_sha256']
 assert [hp[k] for k in ['sampled_inputs','exact_OPT_promise_cases','successful_outputs','strict_t_less_than_OPT_cases']]==[301,122,122,1]
 assert fo['fractional_loads']==['3','3'] and fo['integral_makespans']==['4','4'] and fo['dual_value']=='3' and fo['feedback_rank']==0 and len(fo['near_two_family'])==4
 assert len(pr['primal_dual_fixtures'])==13 and pr['dual_common_heavy_faces']==5 and pr['expanded_tree_checks'][1]['common']=='5/3' and pr['expanded_tree_checks'][1]['T']=='4/3'
 assert [ma[k] for k in ['matrix_count','threshold_tests','preserved_feasible_schedules_with_threshold_multiplicity','random_rational_cases','boundary_cases','rejected_invalid_cases']]==[3375,16875,36224,120,5,7] and ma['expanded_k4']['escape_machines']==171 and ma['expanded_k4']['escape_jobs']==265 and ma['expanded_k4']['escape_deleted_edges']==0 and [x['k'] for x in ma['compressed_parameters']]==list(range(4,65))
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}=={x['id'] for x in groups[0]}
 for x in rec:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']);assert x['disposition']=='retained' and all(resolve(t).is_file() for t in x['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==4 and not rel['formal_hypergraph_written'];formal=[]
 for x in rel['formal_comparison_snapshots']:
  raw=resolve(x['preserved_snapshot_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256'];formal.append(dict(repo_path=x['repo_path'],preserved_snapshot_path=x['preserved_snapshot_path'],passed=True))
 assert len(formal)==7
 links=[]
 for doc in [Path(x) for x in rel['new_computation_objects']]+[ER/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute() and '..' not in Path(f).parts and (root/f).is_file()
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:
  mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root)) for x in root.rglob('*') if x.is_file())
 out=dict(check_kind='saved bytes and result consistency only; not another mathematical execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=2,comparison_source_count=11,source_byte_checks=checks,runtime_artifact_hash_count=len(art),historical_comparison_count=len(hist),complete_matching_parameter_rows_compared=61,formal_comparison_snapshot_hash_checks=formal,receipt_count=len(rec),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_CLI_executions_observed=5,supplemental_mathematical_process_executions_observed=0,total_mathematical_process_executions_this_batch=5,unguarded_import_audit_body_evaluations=0,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_mathematical_process_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
