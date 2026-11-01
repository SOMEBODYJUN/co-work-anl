"""Saved-byte/metadata/receipt/link integrity; no mathematical source execution."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/product-representation-primary');WS=Path('cleanup/workspaces/Boss4/r3-product-representation-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and '..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');src=m['sources'];assert len(src)==3 and sum(x['source_size']for x in src)==m['primary_bytes']==8419;ids={x['id']for x in src};assert ids=={'8109059e0334d5b42cdb','0943e0f6ba3a4918ed64','6d15161b9994536d67a7'};items={x['id']:x for x in src};checks=[]
 for x in src:
  b=raw(x['preserved_repo_path']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert len(b)==x['source_size']and sha(b)==x['source_sha256']and blob==x['source_git_blob']and x['full_file_reviewed']and 'pre-read' in x['read_scope']and Path(x['source_path']).suffix=='.md';checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),Git_blob_sha1=blob,passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and set(claim['ids'])==ids and claim['remote_tip']=='f0d5cc661e5d0a90adb72254fb8a6effc350fa5c'
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==3 and {x['id']for x in owners}==ids and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 supplied=load(ER/'root-local-input-manifest.json');assert len(supplied['rows'])==3 and {x['id']for x in supplied['rows']}==ids
 for x in supplied['rows']:
  y=items[x['id']];assert x['group']=='query_da'and[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 missing=load(ER/'missing-audit-local-input-boundary.json');assert len(missing['sources'])==2 and {x['id']for x in missing['sources']}=={'0eaeeb1d33eb9d593585','054b7383360547d9fe14'}and not(ids&{x['id']for x in missing['sources']})and missing['same_SHA_file_matches']==[]and missing['no_network_or_Git_retry']and missing['original_source_CLI_executions']==0 and missing['math_program_executions']==0 and missing['counts_verified_by_reading_actual_audit_program_or_result']is False
 assert missing['sources']==supplied['missing_query_da']
 for x in missing['sources']:assert all(x[k]is False for k in ['local_source_bytes_available','whole_source_read','executed','claimed_in_DA'])
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==3 and scope['primary_bytes']==8419 and scope['primary_types']==['Markdown']*3 and all(scope[k]==0 for k in ['source_CLI_executions_this_batch','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions_this_batch','audit_py_or_JSON_whole_read_count','new_blind_reviews','network_requests_for_materialization_or_review','Git_clean_show_or_lazy_fetch_invocations'])and scope['primary_pre_read_before_claim_was_explicitly_authorized_by_Root']and scope['no_successful_receipt_written_before_actual_claim']and scope['all_three_owner_and_source_hashes_rechecked_after_claim']and scope['missing_two_historical_audit_inputs_block_only_finite_replay_not_analytic_primary_completion']and not scope['source_bytes_modified']
 rec=load(WS/'semantic-receipts.json');assert len(rec)==3 and{x['id']for x in rec}==ids
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==2 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified']and rel['mathematical_program_executions']==0
 for d in docs:
  txt=resolve(d).read_text();assert txt.startswith('---\n')and 'source_refs:'in txt and 'source_ids:'in txt and len(txt)>2000
 formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==7 and formal==rel['formal_comparison_snapshots'];formalchecks=[]
 for x in formal:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size']and sha(b)==x['sha256']and x['full_file_reviewed']and x['not_modified'];formalchecks.append(dict(repo_path=x['repo_path'],preserved_snapshot_path=x['preserved_snapshot_path'],passed=True))
 links=[]
 for doc in [Path(x)for x in docs]+[ER/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://'in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file()or(root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list)and listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute()and '..'not in Path(f).parts and(root/f).is_file()
 if(root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root))for x in root.rglob('*')if x.is_file())
 out=dict(check_kind='saved SHA256/Git blob SHA1, metadata, missing-input scope, receipt completeness and links only; no mathematical truth oracle or source execution',all_checks_passed=True,primary_source_count=3,primary_source_bytes=8419,source_byte_checks=checks,formal_comparison_snapshot_count=7,formal_comparison_snapshot_hash_checks=formalchecks,new_mathematical_object_count=2,receipt_count=3,missing_historical_audit_source_count=2,missing_source_read_or_run_count=0,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),source_CLI_executions_this_batch=0,mathematical_audit_body_executions_this_batch=0,supplemental_mathematical_program_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,network_requests_by_verifier=0,source_bytes_modified=False,other_Boss_formal_pages_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_source_count','primary_source_bytes','formal_comparison_snapshot_count','new_mathematical_object_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','missing_source_read_or_run_count']},ensure_ascii=False))
if __name__=='__main__':main()
