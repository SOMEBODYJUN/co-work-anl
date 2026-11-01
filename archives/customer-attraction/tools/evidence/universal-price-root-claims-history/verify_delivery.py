"""Verify saved bytes/metadata/JSON/links; never import math or safe-export helper."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/universal-price-root-claims-history');WS=Path('cleanup/workspaces/Boss4/r3-universal-price-root-claims-history')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and '..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');cm=load(ER/'comparison-manifest.json');src=m['sources'];cmp=cm['sources'];ids={x['id']for x in src};assert len(src)==m['primary_count']==5 and sum(x['source_size']for x in src)==m['primary_bytes']==22583 and ids=={'71343219a912de03f30b','996cfbe04d2e153d5094','660dac4b87243547590f','3872de1c995b0372b0c2','6f74496aabf2d52b703e'}and len(cmp)==1 and sum(x['source_size']for x in cmp)==cm['comparison_bytes']==1324
 items={x['id']:x for x in src+cmp};assert len(items)==6;checks=[]
 for x in src+cmp:
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size']and sha(b)==x['source_sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob']and x['full_file_reviewed']and x['read_scope'].strip();checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and set(claim['ids'])==ids and claim['remote_tip']=='2a105b4a33e6865b6f77692a0c84f40d779a934f'
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==5 and{x['id']for x in owners}==ids and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 for name,expected in [('primary-safe-local-export-manifest.json',ids),('comparison-safe-local-export-manifest.json',{'f29d2df5059a9091bd25'})]:
  exported=load(ER/name);assert len(exported['rows'])==len(expected) and not exported['missing']and{x['id']for x in exported['rows']}==expected
  for x in exported['rows']:
   y=items[x['id']];assert[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 pointed=load(ER/'pointed-audit-resource-index.json');assert len(pointed['expected_paths'])==len(pointed['inventory_rows'])==10 and{r['path']for r in pointed['inventory_rows']}==set(pointed['expected_paths'])and pointed['current_program_reads']==pointed['current_program_executions']==0
 for row in pointed['inventory_rows']:assert row['full_file_reviewed']is False and row['source_CLI_executions']==0 and len(row['sha256'])==64 and len(row['blob'])==40 and row['sources']
 assert '57' in pointed['historical_count_statement']and '57' in raw(items['71343219a912de03f30b']['preserved_repo_path']).decode()
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==5 and scope['primary_bytes']==22583 and scope['comparison_count']==1 and scope['comparison_bytes']==1324 and scope['primary_types']==['Markdown']*5 and scope['operational_safe_export_helper_invocations']==2 and scope['read_only_Git_cat_file_calls']==6 and scope['local_blob_exports_succeeded']==6 and scope['local_blob_exports_missing']==0
 for k in ['original_primary_source_CLI_executions','comparison_source_CLI_executions','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions','audit_import_or_compile_count','new_blind_reviews','network_requests','shared_Git_mutations','own_claim_done_checkpoint_invocations','stage_materialization_Git_invocations']:assert scope[k]==0
 assert not scope['full_primary_source_bytes_modified']and scope['all_final_receipts_after_actual_pushed_synced_and_owner_verification'];helper=raw(ER/'local-export-helper-snapshot.py');assert sha(helper)==scope['safe_helper_sha256']
 for x in [b"GIT_NO_LAZY_FETCH='1'",b'protocol.allow=never',b'remote.origin.promisor=false',b'/nonexistent-codex-local-object-only']:assert x in helper
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and{x['id']for x in rec}==ids
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==2 and len(rel['relations'])==7 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified'];formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==12 and formal==rel['formal_comparison_snapshots'];fc=[]
 for x in formal:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size']and sha(b)==x['sha256']and x['full_file_reviewed']and x['not_modified'];fc.append(dict(path=x['repo_path'],size=len(b),sha256=sha(b),passed=True))
 links=[]
 for d in [Path(x)for x in docs]+[ER/'README.md']:
  txt=resolve(d).read_text()
  if str(d)in docs:assert txt.startswith('---\n')and 'source_ids:'in txt and 'source_refs:'in txt and len(txt)>3000
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',txt):
   if '://'in url or url.startswith('#'):continue
   dest=(root/d.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file(),(d,url);links.append(dict(source=str(d),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute()and '..'not in Path(f).parts and(root/f).is_file()
 if(root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root))for x in root.rglob('*')if x.is_file())
 out=dict(all_checks_passed=True,check_kind='saved bytes/metadata, receipts and links only; no mathematical truth oracle or program rerun',primary_count=5,primary_bytes=22583,comparison_source_count=1,comparison_bytes=1324,source_byte_checks=checks,new_mathematical_object_count=2,receipt_count=5,formal_comparison_snapshot_count=12,formal_snapshot_checks=fc,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),operational_safe_helper_invocations_observed=2,read_only_Git_cat_file_calls_observed=6,mathematical_source_CLI_executions_this_batch=0,supplemental_mathematical_program_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,operational_helpers_executed_by_verifier=0,network_requests_by_verifier=0,shared_Git_mutations_by_verifier=0)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_count','primary_bytes','comparison_source_count','new_mathematical_object_count','receipt_count','formal_comparison_snapshot_count','markdown_link_count','copy_list_check_mode','copy_list_file_count']},ensure_ascii=False))
if __name__=='__main__':main()
