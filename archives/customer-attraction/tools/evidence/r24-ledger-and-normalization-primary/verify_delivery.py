"""Saved bytes/metadata/JSON/link integrity only. Never import audit or export helper."""
from pathlib import Path
import argparse,hashlib,json,re
ER=Path('archives/customer-attraction/tools/evidence/r24-ledger-and-normalization-primary');WS=Path('cleanup/workspaces/Boss4/r3-r24-ledger-and-normalization-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and '..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');src=m['sources'];cmp=load(ER/'comparison-manifest.json')['sources'];assert len(src)==4 and sum(x['source_size']for x in src)==m['primary_bytes']==8917 and len(cmp)==2;ids={x['id']for x in src};assert ids=={'4c8ff8832a9f52272cf8','a191339abd31925817cc','79111673eabd6dc6c95f','6820e075353da53af9df'};items={x['id']:x for x in src+cmp};assert len(items)==6;checks=[]
 for x in src+cmp:
  b=raw(x['preserved_repo_path']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert len(b)==x['source_size']and sha(b)==x['source_sha256']and blob==x['source_git_blob']and x['full_file_reviewed']and x['read_scope'].strip()!='pending';checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),Git_blob_sha1=blob,passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and ids<=set(claim['ids'])and len(claim['ids'])==10 and claim['remote_tip']=='1591bf9946b573b39e542805b4342fad396bd2c5'
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==4 and{x['id']for x in owners}==ids and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 supplied=load(ER/'root-local-input-manifest.json')['rows'];initial=load(ER/'initial-safe-export-manifest.json');assert len(supplied)==len(initial['rows'])==4 and{x['id']for x in supplied}=={x['id']for x in initial['rows']}==ids
 for rows in [supplied,initial['rows']]:
  for x in rows:
   y=items[x['id']];assert[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 missing=load(ER/'missing-induction-source-boundary.json');assert missing['source']['id']=='767dede40a59e83985bd'and all(missing[k]is False for k in ['available_local_blob','claimed_in_DI','source_whole_read','source_executed'])and missing['current_source_CLI_executions']==missing['mathematical_program_executions']==0 and len(initial['missing'])==1 and initial['missing'][0]['id']=='767dede40a59e83985bd'
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==4 and scope['primary_bytes']==8917 and scope['primary_types']==['Markdown']*4 and all(scope[k]==0 for k in ['original_primary_source_CLI_executions','comparison_mathematical_source_CLI_executions','mathematical_audit_body_executions_this_batch','supplemental_mathematical_program_executions','comparison_audit_import_or_compile_count','new_blind_reviews','network_requests','shared_Git_mutations','own_claim_done_checkpoint_invocations','stage_materialization_Git_invocations'])and scope['initial_operational_safe_helper_invocations']==1 and scope['initial_read_only_Git_cat_file_calls']==5 and scope['initial_local_blob_exports_succeeded']==4 and scope['initial_local_blob_exports_missing']==1 and scope['failed_refill15_not_used_as_success']and scope['successful_receipts_only_after_actual_refill10_pushed_synced_and_four_owners']and not scope['source_bytes_modified']
 helper=raw(ER/'local-export-helper-snapshot.py');assert sha(helper)==scope['safe_helper_sha256']
 for t in [b"GIT_NO_LAZY_FETCH='1'",b'protocol.allow=never',b'remote.origin.promisor=false',b'/nonexistent-codex-local-object-only']:assert t in helper
 report=load(items['79196feb0c2101b7b789']['preserved_repo_path']);assert [report[k]for k in ['customers','menu_size','players','last_prefixes','ordered_SPE_outcomes','ordered_tail_min_SPE_outcomes','minimum_SPE_welfare','minimum_tail_min_SPE_welfare','exact_relocation_gap']]==[36,6,3,36,48,12,34,36,2]
 assert [x['nodes']for x in report['strategies']]==[43,43]and[x['comparisons_with_self']for x in report['strategies']]==[258,258]and[x['comparisons_nonself']for x in report['strategies']]==[215,215]and sum(report['terminal_patterns'].values())==216 and report['theta']=='12'
 rec=load(WS/'semantic-receipts.json');assert len(rec)==4 and{x['id']for x in rec}==ids
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
 out=dict(check_kind='saved sourceSHA256/Git blobSHA1, claim/owner and export metadata, saved historicalJSON/receipts/links only; no mathematical truth oracle',all_checks_passed=True,primary_source_count=4,primary_source_bytes=8917,comparison_source_count=2,source_byte_checks=checks,formal_comparison_snapshot_count=7,formal_comparison_snapshot_hash_checks=formalchecks,new_mathematical_object_count=2,receipt_count=4,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),initial_operational_helper_invocations_observed=1,initial_read_only_local_Git_calls_observed=5,mathematical_source_CLI_executions_this_batch=0,mathematical_audit_body_executions_this_batch=0,mathematical_programs_executed_by_verifier=0,operational_helpers_executed_by_verifier=0,network_requests_by_verifier=0,source_bytes_modified=False,other_Boss_formal_pages_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_source_count','primary_source_bytes','comparison_source_count','formal_comparison_snapshot_count','new_mathematical_object_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count','mathematical_audit_body_executions_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
