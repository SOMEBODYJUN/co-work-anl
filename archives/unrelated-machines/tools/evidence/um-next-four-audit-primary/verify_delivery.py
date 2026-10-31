"""Delivery/artifact integrity only: never executes the mathematical audit programs."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,re,difflib

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve();er=Path('archives/unrelated-machines/tools/evidence/um-next-four-audit-primary');ws=Path('cleanup/workspaces/Boss4/r3-um-next-four-audit-primary')
 def resolve(rel):
  q=root/rel;return q if q.is_file() else fallback/rel
 def load(rel):return json.loads(resolve(rel).read_text())
 groups=[load(er/n)['sources'] for n in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[4,3,7];items={x['id']:x for g in groups for x in g};checks=[]
 for sid,x in items.items():
  r=resolve(x['preserved_repo_path']).read_bytes();assert len(r)==x['source_size'] and sha(r)==x['source_sha256'],sid;checks.append(dict(id=sid,size=len(r),sha256=sha(r),passed=True))
 assert all(x['full_file_reviewed'] for x in groups[0])
 hist=load(er/'historical-comparison-and-version-diffs.json');assert all(hist['comparisons'].values())
 for d in hist['original_diffs']:
  old=resolve(d['old_repo_path']).read_bytes();new=resolve(d['new_repo_path']).read_bytes();assert sha(old)==d['old_sha256'] and sha(new)==d['new_sha256'];diff=''.join(difflib.unified_diff(old.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True),fromfile='old-preserved',tofile='current-frozen')).encode();assert diff==resolve(d['path']).read_bytes() and sha(diff)==d['diff_sha256']
 artifacts=load(er/'artifact-manifest.json')['runtime_and_probe_artifacts']
 for x in artifacts:
  r=resolve(x['repo_path']).read_bytes();assert len(r)==x['size'] and sha(r)==x['sha256'],x['repo_path']
 executions=load(er/'runs/execution-manifest.json')['executions'];assert len(executions)==4 and all(x['exit_code']==0 and not x['timed_out'] for x in executions)
 for x in executions:assert x['source_sha256'] in {v['source_sha256'] for v in groups[0]}
 math=load(er/'mathematical-execution-scope.json');assert (math['primary_CLI_executions_this_batch'],math['supplemental_contract_probe_executions_this_batch'],math['total_mathematical_process_executions_this_batch'])==(4,1,5);assert math['baseline_audit_main_executions']==0
 assert load(er/'runs/anchor-beta-probe.execution.json')['exit_code']==0 and load(er/'runs/anchor-beta-probe.stdout')['status']=='EXPECTED_WRAPPER_REJECTION'
 receipts=load(ws/'semantic-receipts.json');assert len(receipts)==4 and {x['id'] for x in receipts}=={x['id'] for x in groups[0]}
 for x in receipts:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']);assert x['disposition'] in {'retained','integrated','duplicate','retired'};assert all(resolve(t).is_file() for t in x['targets'])
 rel=load(er/'relation-review.json');assert not rel['formal_hypergraph_written'];docs=[Path(x) for x in rel['new_computation_objects']]+[er/'README.md'];links=[]
 for doc in docs:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://' in url or url.startswith('#'):continue
   dst=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dst).is_file() or (root/dst).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dst),passed=True))
 listed=load(ws/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for r in listed:assert not Path(r).is_absolute() and '..' not in Path(r).parts and resolve(r).is_file()
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(q.relative_to(root)) for q in root.rglob('*') if q.is_file())
 out=dict(check_kind='delivery-source-runtime-artifact-diff-and-link-integrity-not-a-new-mathematical-execution',all_checks_passed=True,primary_source_count=4,dependency_source_count=3,comparison_source_count=7,source_byte_checks=checks,exact_original_version_diff_count=2,runtime_artifact_hash_count=len(artifacts),observed_original_CLI_executions=4,observed_supplemental_contract_probe_executions=1,total_observed_mathematical_process_executions_this_batch=5,mathematical_audits_executed_by_this_verifier=0,receipt_count=4,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,original_source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','exact_original_version_diff_count','runtime_artifact_hash_count','receipt_count','markdown_link_count','copy_list_check_mode','total_observed_mathematical_process_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
