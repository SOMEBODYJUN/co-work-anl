"""Saved-byte/metadata/receipt/link integrity only; executes no mathematical source."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/symmetric-image-and-orbit-price-primary');WS=Path('cleanup/workspaces/Boss4/r3-symmetric-image-and-orbit-price-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and '..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 manifest=load(ER/'source-manifest.json');sources=manifest['sources'];assert len(sources)==7 and sum(x['source_size']for x in sources)==manifest['primary_bytes']==31698;ids={x['id']for x in sources};assert len(ids)==7 and set(manifest['owned_primary_ids'])==ids
 expected={'50a7b2fad535f570e034','525d18a03450a0d4bf32','105bac24c53f6fab48d8','7c822c33cd5b7f09f8aa','d1fa9750d89675d91ee8','b5c534e4fad278a1f847','3b98167255f2d3f641bf'};assert ids==expected;items={x['id']:x for x in sources};checks=[]
 for x in sources:
  b=raw(x['preserved_repo_path']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert len(b)==x['source_size']and sha(b)==x['source_sha256']and blob==x['source_git_blob']and x['full_file_reviewed']and 'pending'not in x['read_scope']and Path(x['source_path']).suffix=='.md';checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),Git_blob_sha1=blob,passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['actor']=='Boss4'and claim['status']=='pushed'and claim['local_sync']['status']=='synced'and ids<=set(claim['ids'])and len(claim['ids'])==24 and claim['remote_tip']=='5a8e6e6069abd3fcefd8086a69f5a27eb61da8e2'
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==7 and{x['id']for x in owners}==ids and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 supplied=load(ER/'root-local-input-manifest.json')['rows'];assert len(supplied)==7 and {x['id']for x in supplied}==ids
 for x in supplied:
  y=items[x['id']];assert x['group']=='query_cu'and [x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['source_count']==7 and scope['source_types']==['Markdown']*7 and all(scope[k]==0 for k in ['source_programs_supplied_in_primary','original_source_CLI_executions_this_batch','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions_this_batch','new_blind_reviews','external_reviews_or_novelty_certifications','network_requests_for_materialization_and_review','Git_or_clean_show_invocations_for_materialization'])and not scope['source_bytes_modified']
 assert scope['boundaries']['image_support_threshold']=='d>=min(k,m)' and scope['boundaries']['all_history_pure_SPE_and_ties_preserved_for_tail_application']and scope['boundaries']['m10_counterexample_is_not_six_provider_counterexample']and scope['boundaries']['price_example_B_is_lower_bound_not_exact_optimum']and scope['boundaries']['general_six_provider_half_not_closed']
 assert scope['unexecuted_historical_scratch_reference']['not_needed_for_any_analytic_proof']and scope['source_text_precision_note']['source_id']=='105bac24c53f6fab48d8'and scope['source_text_precision_note']['no_source_or_shared_page_edit']
 rec=load(WS/'semantic-receipts.json');assert len(rec)==7 and {x['id']for x in rec}==ids
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==3 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified']and rel['mathematical_program_executions']==0
 for d in docs:
  txt=resolve(d).read_text();assert txt.startswith('---\n')and 'source_refs:'in txt and 'source_ids:'in txt and len(txt)>2000
 formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==6 and formal==rel['formal_comparison_snapshots'];formalchecks=[]
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
 out=dict(check_kind='saved source SHA256/Git blob SHA1, supplied metadata, receipt completeness, explicit scope and links only; not a mathematical truth oracle',all_checks_passed=True,primary_source_count=7,primary_source_bytes=31698,source_byte_checks=checks,formal_comparison_snapshot_count=6,formal_comparison_snapshot_hash_checks=formalchecks,new_mathematical_object_count=3,receipt_count=7,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),original_source_CLI_executions_this_batch=0,mathematical_audit_body_executions_this_batch=0,supplemental_mathematical_program_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,network_requests_by_verifier=0,claim24_only_seven_owned_primary_receipts=True,source_bytes_modified=False,other_Boss_formal_pages_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_source_count','primary_source_bytes','formal_comparison_snapshot_count','new_mathematical_object_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','mathematical_audit_body_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
