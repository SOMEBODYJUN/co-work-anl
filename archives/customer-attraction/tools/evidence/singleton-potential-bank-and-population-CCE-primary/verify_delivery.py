"""Saved bytes/metadata/JSON/receipts/links only; never import mathematical sources or helper."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/singleton-potential-bank-and-population-CCE-primary');WS=Path('cleanup/workspaces/Boss4/r3-singleton-potential-bank-and-population-CCE-primary')
IDS={'bec0d97ae608cc661bc4','009790e77d5822411b8f','bfd0c75d429ab0038cfa','d441e8ce67f731332784','44d55cdf20962ae5ff02'}
TIP='005aef3c9ed2e09d7fd6c1cc60a54bf7c3ad6490'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and'..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');src=m['sources'];assert len(src)==m['primary_count']==5 and{x['id']for x in src}==IDS and sum(x['source_size']for x in src)==m['primary_bytes']==19248;items={x['id']:x for x in src};checks=[]
 for x in src:
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size']and sha(b)==x['source_sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob']and x['full_file_reviewed']and x['read_scope'].strip();checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),passed=True))
 claim=load(ER/'claim-confirmation-full-22-ids.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and IDS<=set(claim['ids'])and len(claim['ids'])==22 and claim['remote_tip']==TIP
 scopeclaim=load(ER/'claim-subset-scope.json');assert scopeclaim['actual_claim_id_count']==22 and scopeclaim['actual_claim_all_ids']==claim['ids']and set(scopeclaim['primary_subset_ids'])==IDS and set(scopeclaim['other_claim_ids'])==set(claim['ids'])-IDS and len(scopeclaim['other_claim_ids'])==17 and scopeclaim['original_capture_sha256']==sha(raw(ER/'claim-confirmation-full-22-ids.json'))and not scopeclaim['original_capture_modified']and not scopeclaim['claim_called_by_this_subagent']and scopeclaim['this_package_receipts_only_primary_subset']
 owners=load(ER/'actual-owner-verification-five.json');assert len(owners)==5 and{x['id']for x in owners}==IDS and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 exported=load(ER/'safe-local-export-manifest.json');assert len(exported['rows'])==5 and not exported['missing']and{x['id']for x in exported['rows']}==IDS
 for x in exported['rows']:
  y=items[x['id']];assert[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 pointer=load(ER/'pointed-program-resource-index.json');assert len(pointer['expected_paths'])==len(pointer['inventory_rows'])==6 and{r['path']for r in pointer['inventory_rows']}==set(pointer['expected_paths'])and pointer['current_program_reads']==pointer['current_program_executions']==0 and pointer['historical_bank_report']==dict(m_range=[2,7],forced_children=322,remembered_target_DAG_states=27061,action_IC_comparisons=92788)
 for x in pointer['inventory_rows']:assert x['full_file_reviewed']is False and x['source_CLI_executions_this_batch']==0 and len(x['sha256'])==64 and len(x['blob'])==40 and x['sources']
 analytic=load(ER/'analytic-global-count-calibration.json');assert len(analytic['potential_by_A_count'])==4 and analytic['global_max_count']==[2,1]and analytic['max_final_profit_action']=='B'and analytic['implemented_order']==['B','A','A']and analytic['mathematical_program_executions']==0 and analytic['kind'].startswith('new informed analytical calibration')
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==5 and scope['primary_bytes']==19248 and scope['comparison_raw_source_count']==0 and scope['primary_types']==['Markdown']*5 and scope['operational_safe_export_helper_invocations']==1 and scope['read_only_Git_cat_file_calls']==5 and scope['local_blob_exports_succeeded']==5 and scope['local_blob_exports_missing']==0 and scope['new_informed_analytical_expansions']==1 and scope['actual_claim_id_count']==22 and scope['primary_subset_processed']==5 and not scope['other17_processed_by_this_package']
 for k in ['original_primary_source_CLI_executions','pointed_program_source_reads','pointed_mathematical_JSON_report_reads','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions','audit_import_or_compile_count','new_blind_reviews','new_scans','network_requests','shared_Git_mutations','own_claim_done_checkpoint_invocations','stage_materialization_Git_invocations']:assert scope[k]==0
 assert not scope['full_primary_source_bytes_modified']and scope['all_final_receipts_after_actual_pushed_synced_and_subset_owner_verification'];helper=raw(ER/'safe-local-export-helper-snapshot.py');assert sha(helper)==scope['safe_helper_sha256']
 for x in [b"GIT_NO_LAZY_FETCH='1'",b'protocol.allow=never',b'remote.origin.promisor=false',b'/nonexistent-codex-local-object-only']:assert x in helper
 rec=load(WS/'semantic-receipts.json');assert len(rec)==5 and{x['id']for x in rec}==IDS
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==4 and len(rel['relations'])==8 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified'];formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==15 and formal==rel['formal_comparison_snapshots'];fc=[]
 for x in formal:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size']and sha(b)==x['sha256']and x['full_file_reviewed']and x['not_modified'];fc.append(dict(path=x['repo_path'],size=len(b),sha256=sha(b),passed=True))
 links=[]
 for d in [Path(x)for x in docs]+[ER/'README.md']:
  txt=resolve(d).read_text()
  if str(d)in docs:assert txt.startswith('---\n')and'source_ids:'in txt and'source_refs:'in txt and len(txt)>2000 and'本稿私有预备阶段不声称'not in txt
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',txt):
   if '://'in url or url.startswith('#'):continue
   dest=(root/d.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file(),(d,url);links.append(dict(source=str(d),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute()and'..'not in Path(f).parts and(root/f).is_file()
 if(root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root))for x in root.rglob('*')if x.is_file())
 out=dict(all_checks_passed=True,check_kind='saved bytes/metadata/receipts/links only; no mathematical truth oracle, analytical calibration not recomputed by checker',primary_count=5,primary_bytes=19248,actual_claim_id_count=22,processed_primary_subset_count=5,source_byte_checks=checks,new_mathematical_object_count=4,receipt_count=5,formal_comparison_snapshot_count=15,formal_snapshot_checks=fc,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),safe_helper_invocations_this_batch=1,read_only_Git_cat_file_calls_this_batch=5,new_informed_analytical_expansions_retained=1,mathematical_source_CLI_executions_this_batch=0,supplemental_mathematical_program_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,operational_helpers_executed_by_verifier=0,network_requests_by_verifier=0,shared_Git_mutations_by_verifier=0)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_count','primary_bytes','actual_claim_id_count','processed_primary_subset_count','new_mathematical_object_count','receipt_count','formal_comparison_snapshot_count','markdown_link_count','copy_list_check_mode','copy_list_file_count']},ensure_ascii=False))
if __name__=='__main__':main()
