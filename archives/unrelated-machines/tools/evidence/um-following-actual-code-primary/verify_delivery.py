"""Integrity of saved source/result files only; never execute mathematical audits."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/unrelated-machines/tools/evidence/um-following-actual-code-primary')
WS=Path('cleanup/workspaces/Boss4/r3-um-following-actual-code-primary')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def diff_paths(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(a.keys()|b.keys()):
   if k not in a or k not in b:out.append(path+'/'+k)
   else:out+=diff_paths(a[k],b[k],path+'/'+k)
  return out
 return [] if a==b else [path]
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute() and '..' not in rel.parts
  t=root/rel;return t if t.is_file() else fallback/rel
 def load(rel):return json.loads(resolve(rel).read_text())
 groups=[load(ER/name)['sources'] for name in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,1,10];items={x['id']:x for g in groups for x in g};assert len(items)==16;byte_checks=[]
 for sid,row in items.items():
  raw=resolve(row['preserved_repo_path']).read_bytes();assert len(raw)==row['source_size'] and sha(raw)==row['source_sha256'];assert row['full_file_reviewed'] and row['read_scope']!='pending';byte_checks.append(dict(id=sid,size=len(raw),sha256=sha(raw),passed=True))
 claim=load(ER/'claim-confirmation.json');resolution=load(ER/'sync-resolution.json');preserve=load(ER/'sync-preservation-verification.json')
 assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='needs-attention';assert set(claim['ids'])=={x['id'] for x in groups[0]}
 assert resolution['status']=='resolved-and-verified' and resolution['claim_tip']==resolution['current_HEAD']==claim['remote_tip'];assert resolution['all_five_claims_Boss4_in_progress'] and not resolution['missing'] and not resolution['different'] and not resolution['unmerged'];assert preserve['untracked_count']==5 and all(x['same'] for x in preserve['tracked']) and not preserve['missing'] and not preserve['different'] and not preserve['unmerged']
 executions=load(ER/'runs/execution-manifest.json')['executions'];assert len(executions)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in executions);assert {r['source_sha256'] for r in executions}=={r['source_sha256'] for r in groups[0]}
 for r in executions:assert resolve(r['stdout']).is_file() and resolve(r['stderr']).read_bytes()==b''
 art=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(art)==19
 for row in art:
  raw=resolve(row['repo_path']).read_bytes();assert len(raw)==row['size'] and sha(raw)==row['sha256']
 hist=load(ER/'historical-comparison-and-version-scope.json')['comparisons'];assert len(hist)==7
 for r,expected in zip(hist[:2],[['/evidence_scope','/run_command'],['/expanded/LST_elapsed_seconds','/expanded/actual_peer_GHMR/elapsed_seconds','/run_command']]):
  assert diff_paths(load(r['current']),load(r['historical']))==expected
  assert [x['path'] for x in r['differences']]==expected
 for r in hist[2:4]:assert r['byte_equal'] and r['structurally_equal'] and resolve(r['current']).read_bytes()==resolve(r['historical']).read_bytes()
 assert hist[4]['new_stdout_equal_both_old_stdout'] and hist[5]['new_stdout_equal_old_stdout'];assert hist[6]['new_fixture_matches_old_inventory_SHA'];assert [d['path'] for d in hist[6]['differences_from_old_source_enumeration']]==['/actual_fixture_file','/actual_fixture_sha256']
 scope=load(ER/'mathematical-execution-scope.json');assert (scope['primary_CLI_executions_this_batch'],scope['supplemental_mathematical_executions_this_batch'],scope['total_mathematical_process_executions_this_batch'])==(5,0,5)
 raw=load(ER/'runs/raw-k2.payload.json');row=load(ER/'runs/row-degree.payload.json');sink=load(ER/'runs/sink-all-k4.stdout');esc=load(ER/'runs/escape-full.stdout');group=load(ER/'runs/distorted-independent.stdout')
 assert (raw['dimension'],raw['enumerated_weighted_states'],raw['B_config_count'],len(raw['exact_LDL_positive_pivots']))==(50,121,10,50);assert raw['exact_LDL_replay'] and raw['B_config_first_and_pair_match']
 assert [c['checked_all_squarefree_row_monomials_through_degree_d'] for c in row['cases']]==[11,42,163,1471];assert all(c['pure_home_marginal_exactly_equal'] and c['matched'] for c in row['cases'])
 assert [r['lst_probes_checked'] for r in sink['results']]==[14,74,4562] and sink['results'][0]['exhaustive_assignments']==128
 ex=esc['expanded'];assert (ex['machines'],ex['jobs'],ex['eligible_edges'],ex['only_mandatory_job'])==(427,521,4914,0);assert (ex['independent_GHMR_big_edge_certificates'],ex['all_star_matching_certificates'])==(4394,4914);assert ex['actual_peer_GHMR']['accepted'] and ex['actual_peer_GHMR']['rounds']==1 and ex['actual_peer_GHMR']['deleted_edges']==0;assert [r['k'] for r in esc['compressed_formula_checks']]==list(range(4,65))
 assert (group['fixtures'],group['original_assignments'],group['T_feasible_fixtures'],group['source_schedules_used'])==(1248,1192421,1087,3720);assert group['explicit_blocked_conservation']['demand']=='1/2'
 fixture=resolve(ER/'runs/distorted-group.fixtures.json');assert len(fixture.read_bytes())==76603 and sha(fixture.read_bytes())==group['actual_fixture_sha256']==hist[6]['old_fixture_inventory_sha256'];assert len(load(ER/'runs/distorted-group.fixtures.json')['cases'])==16
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}=={x['id'] for x in groups[0]}
 for x in rec:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']);assert x['disposition'] in {'retained','integrated','duplicate','retired'} and all(resolve(t).is_file() for t in x['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==4 and not rel['formal_hypergraph_written'];formal_checks=[]
 for x in rel['formal_comparison_snapshots']:
  raw=resolve(x['repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256'];formal_checks.append(dict(repo_path=x['repo_path'],passed=True))
 links=[]
 for doc in [Path(x) for x in rel['new_computation_objects']]+[ER/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for name in listed:assert not Path(name).is_absolute() and '..' not in Path(name).parts and (root/name).is_file()
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:
  mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root)) for x in root.rglob('*') if x.is_file())
 report=dict(check_kind='saved bytes and result consistency only, no mathematical program execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=1,comparison_source_count=10,source_byte_checks=byte_checks,runtime_artifact_hash_count=len(art),historical_comparison_count=len(hist),formal_comparison_hash_checks=formal_checks,receipt_count=len(rec),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_CLI_executions_observed=5,supplemental_mathematical_executions_observed=0,total_mathematical_process_executions_this_batch=5,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False,original_claim_local_sync_not_rewritten=True,separate_sync_resolution_checked=True)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_mathematical_process_executions_this_batch']},ensure_ascii=False))

if __name__=='__main__':main()
