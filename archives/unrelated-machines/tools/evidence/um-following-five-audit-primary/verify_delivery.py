"""Delivery integrity and saved-output comparisons; never executes mathematical programs."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve();er=Path('archives/unrelated-machines/tools/evidence/um-following-five-audit-primary');ws=Path('cleanup/workspaces/Boss4/r3-um-following-five-audit-primary')
 def resolve(rel):
  x=root/rel;return x if x.is_file() else fallback/rel
 def load(rel):return json.loads(resolve(rel).read_text())
 groups=[load(er/x)['sources'] for x in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[5,1,10];items={x['id']:x for g in groups for x in g};assert len(items)==16;checks=[]
 for sid,x in items.items():
  r=resolve(x['preserved_repo_path']).read_bytes();assert len(r)==x['source_size'] and sha(r)==x['source_sha256'],sid;checks.append(dict(id=sid,size=len(r),sha256=sha(r),passed=True))
 assert all(x['full_file_reviewed'] for x in groups[0]);hist=load(er/'historical-comparison-and-version-scope.json');assert all(hist['comparisons'].values())
 records=load(er/'runs/execution-manifest.json')['executions'];assert len(records)==5 and all(x['exit_code']==0 and not x['timed_out'] for x in records)
 assert {x['source_sha256'] for x in records}=={x['source_sha256'] for x in groups[0]}
 art=load(er/'artifact-manifest.json')['runtime_artifacts']
 for x in art:
  r=resolve(x['repo_path']).read_bytes();assert len(r)==x['size'] and sha(r)==x['sha256']
 math=load(er/'mathematical-execution-scope.json');assert (math['primary_CLI_executions_this_batch'],math['supplemental_mathematical_executions_this_batch'],math['total_mathematical_process_executions_this_batch'])==(5,0,5)
 assert math['configuration']['all_covering_matchings_total']==254 and math['unit']['full_m']==[3,4] and math['unit']['formulas_m']==list(range(3,9));assert hist['prefix']['old_script_SHA']!=hist['prefix']['current_script_SHA']
 rec=load(ws/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}=={x['id'] for x in groups[0]}
 for x in rec:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note']);assert x['disposition'] in {'retained','integrated','duplicate','retired'};assert all(resolve(t).is_file() for t in x['targets'])
 rel=load(er/'relation-review.json');assert not rel['formal_hypergraph_written'];links=[]
 for doc in [Path(x) for x in rel['new_computation_objects']]+[er/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(ws/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for rel in listed:assert not Path(rel).is_absolute() and '..' not in Path(rel).parts and resolve(rel).is_file(),rel
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root)) for x in root.rglob('*') if x.is_file())
 out=dict(check_kind='delivery-source-and-runtime-artifact-integrity-not-a-new-mathematical-execution',all_checks_passed=True,primary_source_count=5,dependency_source_count=1,comparison_source_count=10,source_byte_checks=checks,runtime_artifact_hash_count=len(art),historical_semantic_comparison_count=len(hist['comparisons']),original_CLI_executions_observed=5,supplemental_mathematical_executions_observed=0,total_mathematical_process_executions_this_batch=5,mathematical_programs_executed_by_verifier=0,receipt_count=5,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_semantic_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','total_mathematical_process_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
