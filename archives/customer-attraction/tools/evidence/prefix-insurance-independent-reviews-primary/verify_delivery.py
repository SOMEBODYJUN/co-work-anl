"""Verify saved source bytes, metadata, receipts and links. Never import/run mathematics or export helper."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/prefix-insurance-independent-reviews-primary');WS=Path('cleanup/workspaces/Boss4/r3-prefix-insurance-independent-reviews-primary')
IDS={'5f2b15e32f8224374479','3d136ccc67ecc8606454','2ccbc43549f3e6a57e9a','6e6acd2f6a7665c1fe1a','f2ac90af97571aa19364'}
CMP={'943eafea92a7250ef615','eb41d97e7ff1ccc8d9ce','8441f5cfceed95828f7d'}
TIP='79926f95bbefa0f7f9439a60cffc77c7eca1ff9f'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and'..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');cm=load(ER/'comparison-manifest.json');src=m['sources'];cmp=cm['sources'];assert len(src)==m['primary_count']==5 and{x['id']for x in src}==IDS and sum(x['source_size']for x in src)==m['primary_bytes']==29565;assert len(cmp)==cm['comparison_count']==3 and{x['id']for x in cmp}==CMP and sum(x['source_size']for x in cmp)==cm['comparison_bytes']==35006
 items={x['id']:x for x in src+cmp};assert len(items)==8;checks=[]
 for x in src+cmp:
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size']and sha(b)==x['source_sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob']and x['full_file_reviewed']and x['read_scope'].strip();checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='needs-attention'and set(claim['ids'])==IDS and claim['remote_tip']==TIP
 preserved=load(ER/'original-sync-preservation.json');resolution=load(ER/'sync-resolution-confirmation.json');assert preserved['receipt']=='boss4-r3-next-fv-claim'and preserved['stash']=='e488ce3decc7dbdce750fe89831385b7e078a80d'and preserved['stash']in claim['local_sync']['detail']and preserved['untracked_count']==2 and not preserved['missing']and not preserved['different']and not preserved['unmerged']and len(preserved['tracked'])==2 and all(x['same']for x in preserved['tracked'])and preserved['stash_kept'];assert resolution['actual_claim_pushed']==TIP and resolution['original_capture_local_sync_status']=='needs-attention'and resolution['original_capture_sha256']==sha(raw(ER/'claim-confirmation.json'))and resolution['preservation_sha256']==sha(raw(ER/'original-sync-preservation.json'))and resolution['current_primary_owners_verified']==5 and resolution['current_source_SHA256_matches']and not resolution['original_capture_modified']and not resolution['claim_retried']and not resolution['root_recovery_tool_executed_by_this_subagent']
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==5 and{x['id']for x in owners}==IDS and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 for name,expected in [('primary-cache-reuse-manifest.json',IDS),('comparison-cache-reuse-manifest.json',CMP)]:
  reused=load(ER/name);assert len(reused['rows'])==len(expected)and not reused['missing']and{x['id']for x in reused['rows']}==expected and'same-SHA'in reused['method']
  for x in reused['rows']:
   y=items[x['id']];assert[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 for name,expected in [('prior-FS-primary-export-snapshot.json',5),('prior-FS-comparison-export-snapshot.json',7)]:
  prior=load(ER/name);assert len(prior['rows'])==expected and not prior['missing']
  for x in prior['rows']:
   if x['id']in items:assert x['sha256']==items[x['id']]['source_sha256']
 pointer=load(ER/'unread-third-proof-pointer.json');assert not pointer['full_file_reviewed']and pointer['inventory']['id']=='bec0d97ae608cc661bc4'and pointer['inventory']['size']==7590 and pointer['new_helper_invocations']==pointer['new_source_reads']==pointer['new_mathematical_runs']==0
 analytic=load(ER/'analytic-myopic-expansion.json');assert len(analytic['rows'])==7 and analytic['source_id']=='5f2b15e32f8224374479'and analytic['kind'].startswith('new informed analytical expansion')and analytic['root_IC_gap']=='-1/2'and analytic['W']==analytic['OPT_3']==5 and analytic['mathematical_program_executions']==0
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==5 and scope['primary_bytes']==29565 and scope['comparison_count']==3 and scope['comparison_bytes']==35006 and scope['primary_types']==['Markdown']*5 and scope['same_SHA_cached_primary_files_reused']==5 and scope['same_SHA_cached_comparison_files_reused']==3
 for k in ['original_primary_source_CLI_executions','comparison_source_CLI_executions','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions','audit_import_or_compile_count','new_blind_reviews','new_scans','network_requests','shared_Git_mutations','own_claim_done_checkpoint_invocations','stage_materialization_Git_invocations','operational_safe_export_helper_invocations','read_only_Git_cat_file_calls','local_blob_exports_succeeded_this_batch','local_blob_exports_missing_this_batch']:assert scope[k]==0
 assert scope['prior_FS_export_provenance']==dict(helper_invocations=2,read_only_cat_file_calls=12,exports_succeeded=12,missing=0,not_counted_as_FV_run=True)and scope['new_informed_analytical_expansions']==1 and scope['full_reads_first_completed_in_prior_FS_comparison']and not scope['full_primary_source_bytes_modified']and scope['all_final_receipts_after_actual_pushed_preservation_verified_and_owner_verification']and not scope['safe_helper_snapshot_executed_this_batch'];helper=raw(ER/'unused-safe-local-export-helper-snapshot.py');assert sha(helper)==scope['safe_helper_snapshot_sha256']
 for x in [b"GIT_NO_LAZY_FETCH='1'",b'protocol.allow=never',b'remote.origin.promisor=false',b'/nonexistent-codex-local-object-only']:assert x in helper
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and{x['id']for x in rec}==IDS
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==3 and len(rel['relations'])==7 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified'];formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==7 and formal==rel['formal_comparison_snapshots'];fc=[]
 for x in formal:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size']and sha(b)==x['sha256']and x['full_file_reviewed']and x['not_modified'];fc.append(dict(path=x['repo_path'],size=len(b),sha256=sha(b),passed=True))
 links=[]
 for d in [Path(x)for x in docs]+[ER/'README.md']:
  txt=resolve(d).read_text()
  if str(d)in docs:assert txt.startswith('---\n')and'source_ids:'in txt and'source_refs:'in txt and len(txt)>1500
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',txt):
   if '://'in url or url.startswith('#'):continue
   dest=(root/d.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file(),(d,url);links.append(dict(source=str(d),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute()and'..'not in Path(f).parts and(root/f).is_file()
 if(root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root))for x in root.rglob('*')if x.is_file())
 out=dict(all_checks_passed=True,check_kind='saved bytes/metadata/receipts/links only; analytical table retained as prose-derived record, not computed or judged by verifier',primary_count=5,primary_bytes=29565,comparison_source_count=3,comparison_bytes=35006,source_byte_checks=checks,new_mathematical_object_count=3,receipt_count=5,formal_comparison_snapshot_count=7,formal_snapshot_checks=fc,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),safe_helper_invocations_this_batch=0,read_only_Git_cat_file_calls_this_batch=0,same_SHA_source_files_reused=8,new_informed_analytical_expansions_retained=1,mathematical_source_CLI_executions_this_batch=0,supplemental_mathematical_program_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,operational_helpers_executed_by_verifier=0,network_requests_by_verifier=0,shared_Git_mutations_by_verifier=0)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_count','primary_bytes','comparison_source_count','new_mathematical_object_count','receipt_count','formal_comparison_snapshot_count','markdown_link_count','copy_list_check_mode','copy_list_file_count']},ensure_ascii=False))
if __name__=='__main__':main()
