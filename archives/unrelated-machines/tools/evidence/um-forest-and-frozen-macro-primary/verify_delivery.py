"""Saved source/result integrity only; no mathematical source imports or execution."""
from pathlib import Path
import argparse,ast,hashlib,json,re
ER=Path('archives/unrelated-machines/tools/evidence/um-forest-and-frozen-macro-primary');WS=Path('cleanup/workspaces/Boss4/r3-um-forest-and-frozen-macro-primary')
def sha(r):return hashlib.sha256(r).hexdigest()
def differences(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(a.keys()|b.keys()):out.extend([p+'/'+k] if k not in a or k not in b else differences(a[k],b[k],p+'/'+k))
  return out
 return [] if a==b else [p]
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(r):
  r=Path(r);assert not r.is_absolute() and '..' not in r.parts
  x=root/r;return x if x.is_file() else fallback/r
 def load(r):return json.loads(resolve(r).read_text())
 groups=[load(ER/x)['sources'] for x in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,1,10];items={x['id']:x for g in groups for x in g};assert len(items)==16;checks=[]
 for sid,x in items.items():
  raw=resolve(x['preserved_repo_path']).read_bytes();assert len(raw)==x['source_size'] and sha(raw)==x['source_sha256'];assert x['full_file_reviewed'] and x['read_scope']!='pending';checks.append(dict(id=sid,size=len(raw),sha256=sha(raw),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])=={x['id'] for x in groups[0]}
 runs=load(ER/'runs/execution-manifest.json')['executions'];assert len(runs)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in runs) and {x['source_sha256'] for x in runs}=={x['source_sha256'] for x in groups[0]}
 for x in runs:assert resolve(x['stdout']).is_file() and resolve(x['stderr']).read_bytes()==b''
 art=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(art)==17
 for x in art:
  raw=resolve(x['repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256']
 hist=load(ER/'historical-comparison-and-version-scope.json')['comparisons'];assert len(hist)==4
 x=hist[0];now=load(x['current']);old=load(x['historical']);assert x['all_current_fields_equal_old'] and all(now[k]==old[k] for k in now);assert x['old_only_fields']==sorted(old.keys()-now.keys()) and len(x['old_only_fields'])==8
 x=hist[1];now=load(x['current']);old=load(x['historical']);assert x['complete_458_instance_rows_equal'] and len(now['instances'])==458 and now['instances']==old['instances'];assert differences(now,old)==['/author_comparison/source','/proof_target/path']
 for x in hist[2:]:assert x['structurally_equal'] and load(x['current'])==load(x['historical'])
 scope=load(ER/'mathematical-execution-scope.json');assert (scope['primary_CLI_executions_this_batch'],scope['supplemental_mathematical_process_executions_this_batch'],scope['total_mathematical_process_executions_this_batch'])==(5,0,5)
 independent=load(ER/'runs/forest-independent.payload.json');menu=load(ER/'runs/forest-menu.stdout');frozen=load(ER/'runs/frozen-reoptimization.stdout');fi=load(ER/'runs/frozen-independent.stdout');atoms=ast.literal_eval(resolve(ER/'runs/full-moment-saddle.stdout').read_text())
 assert independent['totals']['actual_menu_witnesses']==541 and independent['totals']['covered_strong_domain_schedules']==1211 and independent['totals']['references_with_a_above_T']==411;assert independent['author_comparison']['totals']['actual_menu_witnesses']==542 and not independent['author_comparison']['failures'];assert independent['proof_target']['source_sha256']==groups[1][0]['source_sha256']
 assert [menu[k] for k in ['random_cases','original_feasible_cases','empty_menu_certificates','covered_original_schedules','zero_b_original_schedules']]==[500,288,201,1465,612]
 assert [x['r'] for x in frozen['construction_checks']]==list(range(1,9));assert [x['raw_oracle']['assignments'] for x in frozen['construction_checks'][:2]]==[4,36864]
 assert [x['count_vectors'] for x in fi['frozen_count_enumerations']]==[3,49,2197,194481] and [x['count_vectors'] for x in fi['sharp_frontier_enumerations']]==[3,49,2197,194481];assert fi['slot_injections'][-1]['jobs']==8420
 assert atoms['status']=='ok' and atoms['full_moment_atoms']==(4,2) and [x['g'] for x in atoms['saddle_cycle'].values()]==scope['saddle']['matrices']
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}=={x['id'] for x in groups[0]}
 for x in rec:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']);assert x['disposition'] in {'retained','integrated','duplicate','retired'} and all(resolve(t).is_file() for t in x['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==3 and not rel['formal_hypergraph_written'];formal=[]
 for x in rel['formal_comparison_snapshots']:
  raw=resolve(x['repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256'];formal.append(dict(repo_path=x['repo_path'],passed=True))
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
 out=dict(check_kind='saved bytes and result consistency only, not another mathematical execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=1,comparison_source_count=10,source_byte_checks=checks,runtime_artifact_hash_count=len(art),historical_comparison_count=len(hist),complete_forest_instance_rows_compared=458,formal_comparison_hash_checks=formal,receipt_count=len(rec),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_CLI_executions_observed=5,supplemental_mathematical_process_executions_observed=0,total_mathematical_process_executions_this_batch=5,optional_author_api_comparison_cases=458,author_main_reexecuted_by_import=False,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_mathematical_process_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
