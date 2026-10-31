"""Verify saved source bytes/provenance/receipts/links; not a mathematics oracle or source-program run."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/credible-prefix-followup-and-free-root-primary');WS=Path('cleanup/workspaces/Boss4/r3-credible-prefix-followup-and-free-root-primary')
IDS={'35d47386e0da22f6debd','ab1c4da1e715eb5ba7b8','6bd482e74c37a62e2c92','08a7d90a546f08ba6dd5','e4a5aeb65de06c7e6db8'}
CMP=set()
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and'..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');cm=load(ER/'comparison-manifest.json');src=m['sources'];cmp=cm['sources'];assert len(src)==m['primary_count']==5 and{x['id']for x in src}==IDS and sum(x['source_size']for x in src)==m['primary_bytes']==12059;assert len(cmp)==cm['comparison_count']==0 and{x['id']for x in cmp}==CMP and sum(x['source_size']for x in cmp)==cm['comparison_bytes']==0;items={x['id']:x for x in src+cmp};checks=[]
 for x in src+cmp:
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size']and sha(b)==x['source_sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob']and x['full_file_reviewed']and x['read_scope'].strip();checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),passed=True))
 claim=load(ER/'claim-confirmation-full-ids.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and IDS<=set(claim['ids'])and len(claim['ids'])==len(set(claim['ids']))>=5 and len(claim['remote_tip'])==40
 cl=load(ER/'claim-subset-scope.json');assert cl['actual_claim_id_count']==len(claim['ids'])and cl['actual_claim_all_ids']==claim['ids']and set(cl['primary_subset_ids'])==IDS and set(cl['other_claim_ids'])==set(claim['ids'])-IDS and cl['original_capture_sha256']==sha(raw(ER/'claim-confirmation-full-ids.json'))and not cl['original_capture_modified']and not cl['claim_called_by_this_subagent']and cl['this_package_receipts_only_primary_subset']
 owners=load(ER/'actual-owner-verification-five.json');assert len(owners)==5 and{x['id']for x in owners}==IDS and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 for name,expected in [('primary-safe-local-export-manifest.json',IDS)]:
  e=load(ER/name);assert len(e['rows'])==len(expected)and not e['missing']and{x['id']for x in e['rows']}==expected
  for x in e['rows']:
   y=items[x['id']];assert[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 ptr=load(ER/'historical-run-and-pointer-scope.json');got={x['path']for x in ptr['inventory_rows']};missing=set(ptr['missing_inventory_paths']);assert len(ptr['expected_paths'])==11 and got|missing==set(ptr['expected_paths'])and not got&missing and ptr['current_program_source_reads']==ptr['current_JSON_report_reads']==ptr['current_program_executions']==0
 for x in ptr['inventory_rows']:assert x['full_file_reviewed']is False and x['CLI_executions_this_batch']==0 and len(x['sha256'])==64 and len(x['blob'])==40 and x['sources']
 h=ptr['historical_MD_reports'];assert h['bank_m_range']==[2,7]and [h[k]for k in ['bank_states','bank_action_IC','product_players','product_prefix_j','product_customers','product_themes','product_ordered_decision_nodes','product_joint_action_IC','product_W','product_OPT','threshold_random_inputs']]==[10713,19470,3,2,25,6,43,258,25,25,300]and h['product_actual_payoffs']==[7,7,11]and [x['value']for x in h['suffix_cones']]==['7/4','2','149/103','5/4']and h['suffix_only_reported_strict_primal_dual_matching']and not h['pair_dual_optimality_certificate']and not h['pair_positive_target_found']and h['threshold_zero_customer_ratio']=='1'and not h['threshold_nonzero_minimum_claim']
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==5 and scope['primary_bytes']==12059 and scope['comparison_raw_source_count']==0 and scope['comparison_raw_source_bytes']==0 and scope['primary_types']==['Markdown']*5 and scope['operational_safe_export_helper_invocations']==1 and scope['read_only_Git_cat_file_calls']==5 and scope['local_blob_exports_succeeded']==5 and scope['local_blob_exports_missing']==0 and scope['actual_claim_id_count']==len(claim['ids'])and scope['primary_subset_processed']==5 and not scope['other_claim_sources_processed_by_this_package']and not scope['comparison_done_repeated']and not scope['original_program_successes_repeated']
 for k in ['original_primary_source_CLI_executions','pointed_program_source_reads','pointed_mathematical_JSON_report_reads','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions','audit_import_or_compile_count','new_blind_reviews','new_scans','new_finite_SPE_examples','network_requests','shared_Git_mutations','own_claim_done_checkpoint_invocations','stage_materialization_Git_invocations']:assert scope[k]==0
 assert not scope['full_primary_source_bytes_modified']and scope['all_final_receipts_after_actual_pushed_synced_and_subset_owner_verification'];helper=raw(ER/'safe-local-export-helper-snapshot.py');assert sha(helper)==scope['safe_helper_sha256']
 for x in [b"GIT_NO_LAZY_FETCH='1'",b'protocol.allow=never',b'remote.origin.promisor=false',b'/nonexistent-codex-local-object-only']:assert x in helper
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and{x['id']for x in rec}==IDS
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==3 and len(rel['relations'])==10 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified'];formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==9 and formal==rel['formal_comparison_snapshots'];fc=[]
 for x in formal:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size']and sha(b)==x['sha256']and x['full_file_reviewed']and x['not_modified'];fc.append(dict(path=x['repo_path'],size=len(b),sha256=sha(b),passed=True))
 links=[]
 for d in [Path(x)for x in docs]+[ER/'README.md']:
  txt=resolve(d).read_text()
  if str(d)in docs:assert txt.startswith('---\n')and'source_ids:'in txt and'source_refs:'in txt and len(txt)>2000
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',txt):
   if '://'in url or url.startswith('#'):continue
   dest=(root/d.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file(),(d,url);links.append(dict(source=str(d),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute()and'..'not in Path(f).parts and(root/f).is_file()
 if(root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root))for x in root.rglob('*')if x.is_file())
 out=dict(all_checks_passed=True,check_kind='saved source/provenance/receipts/links only; no mathematical truth oracle or program rerun',primary_count=5,primary_bytes=12059,comparison_source_count=0,comparison_bytes=0,actual_claim_id_count=len(claim['ids']),processed_primary_subset_count=5,source_byte_checks=checks,new_mathematical_object_count=3,receipt_count=5,formal_comparison_snapshot_count=9,formal_snapshot_checks=fc,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),safe_helper_invocations_this_batch=1,read_only_Git_cat_file_calls_this_batch=5,mathematical_source_CLI_executions_this_batch=0,supplemental_mathematical_program_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,operational_helpers_executed_by_verifier=0,network_requests_by_verifier=0,shared_Git_mutations_by_verifier=0)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_count','primary_bytes','comparison_source_count','actual_claim_id_count','processed_primary_subset_count','new_mathematical_object_count','receipt_count','formal_comparison_snapshot_count','markdown_link_count','copy_list_check_mode','copy_list_file_count']},ensure_ascii=False))
if __name__=='__main__':main()
