"""Saved-file integrity and historical result comparisons; never import source audits."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/unrelated-machines/tools/evidence/um-following-actual-source-primary');WS=Path('cleanup/workspaces/Boss4/r3-um-following-actual-source-primary')
def sha(r):return hashlib.sha256(r).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(r):
  r=Path(r);assert not r.is_absolute() and '..' not in r.parts
  f=root/r;return f if f.is_file() else fallback/r
 def load(r):return json.loads(resolve(r).read_text())
 groups=[load(ER/n)['sources'] for n in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,1,6];items={x['id']:x for g in groups for x in g};assert len(items)==12;checks=[]
 for sid,x in items.items():
  raw=resolve(x['preserved_repo_path']).read_bytes();assert len(raw)==x['source_size'] and sha(raw)==x['source_sha256'];assert x['full_file_reviewed'] and x['read_scope']!='pending';checks.append(dict(id=sid,size=len(raw),sha256=sha(raw),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])=={x['id'] for x in groups[0]}
 prior=load(ER/'prior-comparison-snapshots.json')['prior_snapshots'];assert len(prior)==3
 for x in prior:
  raw=resolve(x['preserved_repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256'] and x['executed_this_batch'] is False
 records=load(ER/'runs/execution-manifest.json');runs=records['executions'];assert len(runs)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in runs);assert {x['source_sha256'] for x in runs}=={x['source_sha256'] for x in groups[0]};assert records['downward_top_level_audit_evaluations']==2 and records['downward_evaluations_from_runpy_import_in_crosscheck']==1
 for x in runs:assert resolve(x['stdout']).is_file() and resolve(x['stderr']).read_bytes()==b''
 art=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(art)==16
 for x in art:
  raw=resolve(x['repo_path']).read_bytes();assert len(raw)==x['size'] and sha(raw)==x['sha256']
 hist=load(ER/'historical-comparison-and-version-scope.json')['comparisons'];assert len(hist)==5
 for x in hist[:4]:assert x['structurally_equal'] and load(x['current'])==load(x['historical'])
 x=hist[4];assert x['byte_equal'] and resolve(x['current']).read_bytes()==resolve(x['historical']).read_bytes()
 scope=load(ER/'mathematical-execution-scope.json');assert (scope['primary_CLI_executions_this_batch'],scope['supplemental_mathematical_process_executions_this_batch'],scope['total_mathematical_process_executions_this_batch'],scope['downward_top_level_audit_evaluations'])==(5,0,5,2)
 d=load(ER/'runs/forest-downward.stdout');u=load(ER/'runs/forest-upward.stdout');c=load(ER/'runs/forest-crosscheck.stdout');f=load(ER/'runs/forest-family.stdout')
 assert (d['random_trials'],d['nested_composition_trials'],d['deep_chain_vertices'])==(2500,100,300) and d['outcomes']==dict(exact_False_returned_False=970,exact_False_returned_True=34,exact_True_returned_True=1496)
 assert (u['cases'],u['returned'],u['correct_rejections'],u['large_denominator_bits'])==(500,350,150,1001);assert [x['moved_small'] for x in u['stress']]==[4,8,12,36,182]
 assert c['cross_comparison']==dict(cases=600,exact_feasible=382,down_returned=387,up_returned=414,different_success_status=27,different_root_load=20,disconnected_support_cases=323)
 assert len(f['classical'])==5 and len(f['private_sink_B_fixed'])==4 and f['classical'][3]['root_b']=='2' and f['classical'][3]['root_b_at_most_T'] is False
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
 out=dict(check_kind='saved bytes and result comparisons only, not a mathematical program execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=1,comparison_source_count=6,source_byte_checks=checks,prior_maintained_hash_count=len(prior),runtime_artifact_hash_count=len(art),historical_comparison_count=len(hist),formal_comparison_hash_checks=formal,receipt_count=len(rec),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_CLI_executions_observed=5,supplemental_mathematical_process_executions_observed=0,total_mathematical_process_executions_this_batch=5,downward_top_level_audit_evaluations=2,extra_downward_top_level_evaluation_via_crosscheck_runpy=1,downward_unique_random_case_count=2500,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','prior_maintained_hash_count','runtime_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_mathematical_process_executions_this_batch','downward_top_level_audit_evaluations']},ensure_ascii=False))
if __name__=='__main__':main()
