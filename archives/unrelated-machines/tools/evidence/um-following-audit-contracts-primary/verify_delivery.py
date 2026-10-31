"""Saved bytes and result consistency only; never imports/runs mathematical sources."""
from pathlib import Path
import argparse,ast,hashlib,json,re
ER=Path('archives/unrelated-machines/tools/evidence/um-following-audit-contracts-primary');WS=Path('cleanup/workspaces/Boss4/r3-um-following-audit-contracts-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(r):
  r=Path(r);assert not r.is_absolute() and '..' not in r.parts
  x=root/r;return x if x.is_file() else fallback/r
 def load(r):return json.loads(resolve(r).read_text())
 groups=[load(ER/x)['sources'] for x in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,4,15];items={x['id']:x for g in groups for x in g};assert len(items)==24;checks=[]
 for sid,x in items.items():
  raw=resolve(x['preserved_repo_path']).read_bytes();assert len(raw)==x['source_size'] and sha(raw)==x['source_sha256'];assert x['full_file_reviewed'] and 'pending' not in x['read_scope'];checks.append(dict(id=sid,size=len(raw),sha256=sha(raw),passed=True))
 claim=load(ER/'claim-confirmation.json');ids={x['id'] for x in groups[0]};assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(claim['ids'])==ids
 assert claim['local_sync']['status']=='needs-attention'
 res=load(ER/'independent-sync-resolution.json');assert res['status']=='independently-resolved-after-original-needs-attention' and res['original_receipt_unchanged'] and res['all_stashed_bytes_exact'] and res['unmerged']=='' and res['actual_head']==claim['remote_tip'] and set(res['actual_ids'])==ids
 preservation=load(ER/'sync-preservation.json');assert preservation['missing']==[] and preservation['different']==[] and preservation['unmerged']=='' and preservation['untracked_count']==2 and len(preservation['tracked'])==2 and all(x['same'] for x in preservation['tracked'])
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==5 and {x['id'] for x in owners}==ids and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==items[x['id']]['source_sha256'] for x in owners)
 runs=load(ER/'runs/execution-manifest.json')['executions'];assert len(runs)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in runs) and {x['source_sha256'] for x in runs}=={x['source_sha256'] for x in groups[0]}
 for x in runs:assert resolve(x['stdout']).is_file() and resolve(x['stderr']).read_bytes()==b''
 art=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(art)==16
 for x in art:
  raw=resolve(x['repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256']
 history=load(ER/'historical-comparison-and-version-scope.json');hist=history['JSON_comparisons'];assert len(hist)==3
 for x in hist:
  old=load(x['historical']);old=old[x['historical_subobject']] if x['historical_subobject'] else old;assert x['all_fields_equal'] and load(x['current'])==old
 macro=history['macro_text_and_code_version_comparison'];old=load(macro['historical']);assert resolve(macro['current']).read_text().strip()==old['output'] and macro['output_text_equal'] and not macro['same_code_version'] and macro['old_reported_script_sha256']==old['script_sha256'] and macro['current_code_sha256']==groups[0][0]['source_sha256'] and macro['current_code_sha256']!=macro['old_reported_script_sha256']
 scope=load(ER/'mathematical-execution-scope.json');assert (scope['primary_CLI_executions_this_batch'],scope['supplemental_mathematical_process_executions_this_batch'],scope['total_mathematical_process_executions_this_batch'])==(5,0,5) and scope['imported_unguarded_audit_body_evaluations']==0 and scope['primary_top_level_unguarded_audit_entries']==['coalition-gluing','independent-diluted'] and scope['these_two_included_in_five_not_extra']
 hs=load(ER/'runs/hs-effects.stdout');inc=ast.literal_eval(resolve(ER/'runs/incidence-tiny.stdout').read_text());co=load(ER/'runs/coalition-gluing.stdout');di=load(ER/'runs/independent-diluted.stdout')
 assert (hs['latent_actual_schedules'],hs['V1_dimension'],hs['full_trace_defect'])==(210,17,'66') and hs['full_HS_greedy']['actual_loads']==['1','2','0'] and hs['rank_one_state_greedy']['actual_loads']==['1','1','1'] and len(hs['full_HS_greedy']['history'])==len(hs['rank_one_state_greedy']['history'])==9
 assert inc=={'incidence_components_checked':4,'status':'ok'} and scope['incidence']['brute_queries']==7 and scope['incidence']['distinct_original_matrices']==5 and not scope['incidence']['feedback_branching_or_leaf_elimination_or_cycle_DP_implemented']
 assert co['coalition_exact_checks']==scope['coalition']['four_cases'] and sum(x['coalitions'] for x in co['coalition_exact_checks'])==1265 and sum(x['joint_states'] for x in co['coalition_exact_checks'])==10360 and co['path_orientation_cases']==3556 and co['baseline_sha256']==items['e57947bc795251d373c3']['source_sha256']
 assert [di[k] for k in ['machines','jobs','old_edges','added_edges','all_config_columns_checked','old_actual_points_checked','new_actual_points_checked','all_GHMR_big_queries_with_independent_full_matching','largest_matching_size','independent_z_optional_matching_size','all_star_queries_with_independent_full_matching']]==[427,521,4562,352,4571,58,44,4394,6,352,4914] and di['independent_unused_z_schedule_value']=='7/4' and di['peer_GHMR_sha256']==items['2dd3413231d9b1499f4c']['source_sha256'] and scope['diluted']['peer_GHMR']=='hash only; not imported or called'
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}==ids
 for x in rec:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']);assert x['disposition']=='retained' and all(resolve(t).is_file() for t in x['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==5 and not rel['formal_hypergraph_written'];formal=[]
 for x in rel['formal_comparison_snapshots']:
  raw=resolve(x['preserved_snapshot_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256'];formal.append(dict(repo_path=x['repo_path'],preserved_snapshot_path=x['preserved_snapshot_path'],passed=True))
 assert len(formal)==8
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
 out=dict(check_kind='saved bytes and saved-result consistency only; no mathematical execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=4,comparison_source_count=15,source_byte_checks=checks,runtime_artifact_hash_count=len(art),historical_JSON_comparison_count=3,macro_same_output_but_different_source_hash_retained=True,original_needs_attention_receipt_unchanged=True,independent_sync_resolution_and_owner_checks_passed=True,formal_comparison_snapshot_hash_checks=formal,receipt_count=len(rec),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_CLI_executions_observed=5,supplemental_mathematical_process_executions_observed=0,total_mathematical_process_executions_this_batch=5,imported_unguarded_audit_body_evaluations=0,two_original_top_level_audit_entries_included_in_five=True,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_JSON_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_mathematical_process_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
