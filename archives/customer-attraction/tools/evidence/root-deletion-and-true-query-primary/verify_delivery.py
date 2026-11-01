"""Saved-byte/metadata/link checks; never import math program or local exporter."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/root-deletion-and-true-query-primary');WS=Path('cleanup/workspaces/Boss4/r3-root-deletion-and-true-query-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and '..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');src=m['sources'];cmp=load(ER/'comparison-manifest.json')['sources'];ids={x['id']for x in src};assert len(src)==m['primary_count']==5 and sum(x['source_size']for x in src)==m['primary_bytes']==21476 and ids=={'a5531f818789a46412ff','6457a807149fc79ffc4f','b74d950f076f1a38e71e','569d1326872515d2699d','812faf2f217d20e631b5'}and len(cmp)==2;items={x['id']:x for x in src+cmp};checks=[]
 for x in src+cmp:
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size']and sha(b)==x['source_sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob']and x['full_file_reviewed']and x['read_scope'].strip();checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and set(claim['ids'])==ids and claim['remote_tip']=='30f756f40f68d43fe43bd3aa4061ab3cc06311fd'
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==5 and{x['id']for x in owners}==ids and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 fresh=load(ER/'safe-local-export-manifest.json');reuse=load(ER/'same-SHA-prior-export-reuse.json');assert len(fresh['rows'])==5 and len(fresh['missing'])==0 and reuse['source']['id']=='812faf2f217d20e631b5'and reuse['current_whole_Markdown_reread']and reuse['prior_helper_invocations_not_newly_counted_in_DV']==1 and reuse['prior_read_only_cat_file_calls_not_newly_counted_in_DV']==7
 for x in fresh['rows']+[reuse['source']]:
  y=items[x['id']];assert[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 old=load(ER/'already-integrated-comparison-owner.json');assert old['id']=='eefb6c57b13b59a4bb2b'and old['owner']=='Boss2'and old['disposition']=='integrated'and old['source_sha256']==items[old['id']]['source_sha256']
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==5 and scope['primary_bytes']==21476 and scope['primary_types']==['Markdown']*5 and scope['operational_safe_export_helper_invocations_for_new_pre_read']==1 and scope['read_only_Git_cat_file_calls_for_new_pre_read']==5 and scope['new_blob_exports_succeeded']==5 and scope['new_blob_exports_missing']==0 and scope['primary_new_exports']==4 and scope['comparison_new_exports']==1 and scope['primary_same_SHA_prior_export_reused']==1
 for k in ['original_primary_source_CLI_executions','comparison_source_CLI_executions','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions','audit_import_or_compile_count','new_blind_reviews','network_requests','shared_Git_mutations','own_claim_done_checkpoint_invocations','stage_materialization_Git_invocations']:assert scope[k]==0
 assert not scope['full_primary_source_bytes_modified']and scope['all_final_receipts_after_actual_pushed_synced_and_owner_verification']
 helper=raw(ER/'local-export-helper-snapshot.py');assert sha(helper)==scope['safe_helper_sha256']
 for x in [b"GIT_NO_LAZY_FETCH='1'",b'protocol.allow=never',b'remote.origin.promisor=false',b'/nonexistent-codex-local-object-only']:assert x in helper
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and{x['id']for x in rec}==ids
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==3 and len(rel['relations'])==7 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified'];formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==11 and formal==rel['formal_comparison_snapshots'];fc=[]
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
 out=dict(all_checks_passed=True,check_kind='saved bytes/metadata, receipts and Markdown links only; no mathematical truth oracle or program rerun',primary_count=5,primary_bytes=21476,comparison_source_count=2,source_byte_checks=checks,new_mathematical_object_count=3,receipt_count=5,formal_comparison_snapshot_count=11,formal_snapshot_checks=fc,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),new_operational_safe_helper_invocations_observed=1,new_read_only_Git_cat_file_calls_observed=5,same_SHA_prior_primary_export_reused=1,mathematical_source_CLI_executions_this_batch=0,supplemental_mathematical_program_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,operational_helpers_executed_by_verifier=0,network_requests_by_verifier=0,shared_Git_mutations_by_verifier=0)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_count','primary_bytes','new_mathematical_object_count','receipt_count','formal_comparison_snapshot_count','markdown_link_count','copy_list_check_mode','copy_list_file_count']},ensure_ascii=False))
if __name__=='__main__':main()
