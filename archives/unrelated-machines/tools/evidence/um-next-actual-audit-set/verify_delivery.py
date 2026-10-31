"""Check preserved bytes and saved results; do not execute mathematical programs."""
from pathlib import Path
import argparse,hashlib,json,re

ER=Path('archives/unrelated-machines/tools/evidence/um-next-actual-audit-set')
WS=Path('cleanup/workspaces/Boss4/r3-um-next-actual-audit-set')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute() and '..' not in rel.parts
  x=root/rel;return x if x.is_file() else fallback/rel
 def load(rel):return json.loads(resolve(rel).read_text())
 groups=[load(ER/name)['sources'] for name in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,1,9]
 items={r['id']:r for g in groups for r in g};assert len(items)==15;byte_checks=[]
 for sid,row in items.items():
  raw=resolve(row['preserved_repo_path']).read_bytes();assert len(raw)==row['source_size'] and sha(raw)==row['source_sha256'],sid
  assert row['full_file_reviewed'] and row['read_scope']!='pending';byte_checks.append(dict(id=sid,size=len(raw),sha256=sha(raw),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced';assert set(claim['ids'])=={r['id'] for r in groups[0]}
 records=load(ER/'runs/execution-manifest.json')['executions'];assert len(records)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in records);assert {r['source_sha256'] for r in records}=={r['source_sha256'] for r in groups[0]}
 for r in records:
  assert resolve(r['stdout']).is_file() and resolve(r['stderr']).read_bytes()==b''
 helper=load(ER/'runs/witness-export.execution.json');assert helper['exit_code']==0 and helper['supplemental_witness_export_execution_count']==1 and helper['original_audit_not_repeated'];assert sha(resolve(ER/'helpers/export-provided-cover-witness.py').read_bytes())==helper['helper_sha256']
 exported=load(ER/'runs/witness-export.stdout');assert exported['full_audit_called'] is False and exported['q']==6 and exported['job_copies']==42 and exported['machine_copies']==24
 assert resolve(ER/'runs/witness-export.stderr').read_bytes()==b''
 art=load(ER/'artifact-manifest.json')['runtime_and_helper_artifacts'];assert len(art)==22
 for row in art:
  raw=resolve(row['repo_path']).read_bytes();assert len(raw)==row['size'] and sha(raw)==row['sha256'],row['repo_path']
 hist=load(ER/'historical-comparison-and-version-scope.json')['comparisons'];assert len(hist)==9
 expected_diffs=[[],[],['base_commit','certificate_sha256','input_sha256','replay_command'],['base_commit','certificate_sha256','input_sha256','replay_command','source_sha256'],['canonical_sha256','platform'],['platform']]
 for row,expected in zip(hist[:6],expected_diffs):
  now=load(row['current']);old=load(row['historical']);diffs=sorted(k for k in now.keys()|old.keys() if now.get(k)!=old.get(k));assert diffs==row['different_top_level_fields']==expected
  assert row['all_shared_fields_equal_except_declared_version_environment'] is True and all(now[k]==old[k] for k in now.keys()&old.keys() if k not in {'canonical_sha256','platform'})
 for row in hist[6:8]:
  assert row['structurally_equal'] and row['byte_equal'];assert resolve(row['current']).read_bytes()==resolve(row['historical']).read_bytes()
 row=hist[8];now=load(row['current']);old=load(row['historical']);assert sorted(k for k in now if now[k]!=old[k])==['canonical_sha256'];assert row['all_fields_equal_except_canonical_sha256']
 scope=load(ER/'mathematical-execution-scope.json');assert (scope['primary_CLI_executions_this_batch'],scope['supplemental_mathematical_executions_this_batch'],scope['total_mathematical_process_executions_this_batch'])==(5,1,6)
 one=load(ER/'runs/activation-single.stdout');two=load(ER/'runs/activation-two-sign.stdout');cov=load(ER/'runs/finite-cover.stdout');ind=load(ER/'runs/finite-cover-independent.stdout');cyc=load(ER/'runs/single-cycle.stdout')
 assert (one['original_full_assignments_enumerated'],one['explicit_optimal_atoms_checked'],one['maximal_pivot_step'],one['endpoint_exact_completion_OPT'])==(128,14,'3/4','5/4')
 assert (two['rank'],two['nullity'],two['two_copy_optimal_atoms'],two['original_assignments_enumerated'])==(30,28,10,128)
 assert (cov['base_schedules'],cov['random_true_mixtures'],cov['boundary_cases'],cov['invalid_cases'])==(128,160,3,7)
 assert ind['high_girth_partial_permutation_words_checked']==570 and ind['cover']['all_base_schedule_lifts_checked']==128
 assert cyc['canonical_sha256']==groups[1][0]['source_sha256'];runs=cyc['runs'];assert [r['D'] for r in runs]==[3,5,7] and [r['exact_matrix_rank_if_run'] for r in runs]==[59,139,None]
 assert [sum(r[k] for r in runs) for k in ['true_optimal_atoms','explicit_configurations_checked','selected_label_hard_matching_checks']]==[113,6740,336]
 receipts=load(WS/'semantic-receipts.json');assert len(receipts)==5 and {r['id'] for r in receipts}=={r['id'] for r in groups[0]}
 for row in receipts:
  assert all(row.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(isinstance(row.get(k),str) and row[k].strip() for k in ['read_note','comparison_note','decision_note']);assert row['disposition'] in {'retained','integrated','duplicate','retired'} and all(resolve(t).is_file() for t in row['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==3 and not rel['formal_hypergraph_written'] and not rel['full_raw_single_cycle_review_read'];formal_checks=[]
 for row in rel['formal_comparison_snapshots']:
  raw=resolve(row['repo_path']).read_bytes();assert len(raw)==row['size'] and sha(raw)==row['sha256'];formal_checks.append(dict(repo_path=row['repo_path'],passed=True))
 links=[]
 for doc in [Path(x) for x in rel['new_computation_objects']]+[ER/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for path in listed:assert not Path(path).is_absolute() and '..' not in Path(path).parts and (root/path).is_file(),path
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:
  mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root)) for x in root.rglob('*') if x.is_file())
 report=dict(check_kind='delivery bytes and saved-output consistency, not a mathematical execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=1,comparison_source_count=9,source_byte_checks=byte_checks,runtime_and_helper_artifact_hash_count=len(art),historical_comparison_count=len(hist),formal_comparison_hash_checks=formal_checks,receipt_count=len(receipts),markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_CLI_executions_observed=5,supplemental_mathematical_executions_observed=1,total_mathematical_process_executions_this_batch=6,mathematical_programs_executed_by_verifier=0,source_bytes_modified=False,formal_hypergraph_written=False,other_Boss_formal_page_modified=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['all_checks_passed','source_byte_checks','runtime_and_helper_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','total_mathematical_process_executions_this_batch']},ensure_ascii=False))

if __name__=='__main__':main()
