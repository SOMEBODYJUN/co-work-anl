"""Saved bytes/metadata/JSON/link structure only; never import or rerun math/helper."""
from pathlib import Path
import argparse,json,hashlib,re
ER=Path('archives/customer-attraction/tools/evidence/six-optimal-query-decorrelation-primary');WS=Path('cleanup/workspaces/Boss4/r3-six-optimal-query-decorrelation-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute()and '..'not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 m=load(ER/'source-manifest.json');src=m['sources'];cmp=load(ER/'comparison-manifest.json')['sources'];ids={x['id']for x in src};assert len(src)==m['primary_count']==3 and sum(x['source_size']for x in src)==m['primary_bytes']==11904 and ids=={'9ed8e721eb65b29560a8','2c22116da98969895119','8330c50084f72a0d7ded'}and len(cmp)==2
 checks=[]
 for x in src+cmp:
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size']and sha(b)==x['source_sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob']and x['full_file_reviewed'];checks.append(dict(id=x['id'],size=len(b),sha256=sha(b),passed=True))
 claim=load(ER/'claim-confirmation.json');assert claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and set(claim['ids'])==ids and claim['remote_tip']=='3892c6641708d3a353c2ecf850acd614b7569fe2'
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==3 and{x['id']for x in owners}==ids
 for x in owners:assert x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==next(y['source_sha256']for y in src if y['id']==x['id'])
 initial=load(ER/'initial-safe-export-manifest.json');related=load(ER/'related-safe-export-manifest.json');assert len(initial['rows'])==3 and len(initial['missing'])==0 and len(related['rows'])==1 and len(related['missing'])==6
 for x in initial['rows']:
  y=next(y for y in src if y['id']==x['id']);assert[x[k]for k in ['path','size','sha256','blob','sources']]==[y[k]for k in ['source_path','source_size','source_sha256','source_git_blob','frozen_sources']]
 missing=load(ER/'missing-original-audits-boundary.json');assert len(missing['missing'])==missing['actual_missing_count']==6
 for x in missing['missing']:assert all(x[k]is False for k in ['available_local_blob','whole_file_read','claimed_in_DP','network_fallback_attempted'])and x['original_source_CLI_executions']==0
 scope=load(ER/'mathematical-review-and-execution-scope.json');assert scope['primary_count']==3 and scope['primary_bytes']==11904 and scope['operational_safe_helper_invocations']==2 and scope['read_only_Git_cat_file_calls']==10 and scope['local_blob_exports_succeeded']==4 and scope['local_blob_exports_missing']==6
 for k in ['original_primary_source_CLI_executions','comparison_original_source_CLI_executions','new_blind_reviews','network_requests','shared_Git_mutations','own_claim_done_checkpoint_invocations','stage_materialization_Git_invocations']:assert scope[k]==0
 assert scope['new_supplemental_audit_process_invocations']==2 and scope['new_supplemental_syntax_failure_processes']==1 and scope['new_supplemental_mathematical_body_executions']==1 and scope['new_supplemental_fixture_checks']==2 and not scope['full_primary_source_bytes_modified']
 helper=raw(ER/'local-export-helper-snapshot.py');assert sha(helper)==scope['safe_helper_sha256']
 for t in [b"GIT_NO_LAZY_FETCH='1'",b'protocol.allow=never',b'remote.origin.promisor=false',b'/nonexistent-codex-local-object-only']:assert t in helper
 arts=load(ER/'new-audit-artifact-manifest.json');artifactchecks=[]
 for x in arts['files']:
  b=raw(x['path']);assert len(b)==x['size']and sha(b)==x['sha256'];artifactchecks.append(dict(path=x['path'],passed=True))
 NEW=ER/'new-independent-audit';failed=load(NEW/'attempt-01-syntax-failure/execution.json');success=load(NEW/'execution.json');assert failed['exit_code']==1 and b'SyntaxError'in raw(NEW/'attempt-01-syntax-failure/independent-audit.stderr')and success['exit_code']==0 and raw(NEW/'independent-audit.stderr')==b''
 assert sha(raw(NEW/'attempt-01-syntax-failure/independent_six_decorrelation.py'))==failed['source_sha256']and sha(raw(NEW/'independent_six_decorrelation.py'))==success['source_sha256']=='5d596fd1b87bae2652e92b01223f5dbc0e8ecc55f97cfbc1f11c75b914d4f375'
 payload=load(NEW/'outputs/independent-audit.payload.json');assert payload['status']=='all exact definition-level checks passed'and payload['own_source_sha256']==success['source_sha256']and payload['input_sha256']==success['input_sha256']=='bc5202502faa778fae402da4d74a4da8971ffa30bd712423147555b6e15a437a'and payload['total_full_decision_histories']==86038 and payload['total_nonself_deviations']==649088
 for x,n,d,k in zip(payload['cases'],[19608,66430],[117648,531440],[7,9]):
  assert x['full_decision_histories']==n and x['nonself_deviations']==d and x['all_action_comparisons_including_self']==n*k and x['strictly_losing_deviations']+x['tied_deviations']==d
  b=raw(NEW/'outputs'/x['full_policy_file']);assert sha(b)==x['full_policy_sha256']and len(b)==x['full_policy_bytes'];policy=json.loads(b);assert len(policy)==n
  for history,action in policy.items():
   h=tuple(map(int,history.split(',')))if history else();assert len(h)<6 and all(0<=a<k for a in h)and isinstance(action,int)and 0<=action<k
 old,new=payload['cases'];assert not old['prefix_is_on_actual_path']and new['prefix_is_on_actual_path']and old['optimal_benchmark_budget']==3 and old['optimal_benchmark_multisets_enumerated']==84 and new['optimal_benchmark_budget']==6 and new['optimal_benchmark_multisets_enumerated']==3003 and len(new['all_optimal_multisets'])==4
 assert[x['Delta']for x in old['queries']]==['-3/8','0']+['-5/18']*4 and[x['Delta']for x in new['queries']]==['-11/72','-11/72','-1/9','-1/9']
 rec=load(WS/'semantic-receipts.json');assert len(rec)==3 and{x['id']for x in rec}==ids
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='retained'and x['targets']and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');docs=rel['new_mathematical_objects'];assert len(docs)==2 and not rel['formal_hypergraph_written']and not rel['source_bytes_modified']and not rel['other_Boss_formal_pages_modified']
 formal=load(ER/'formal-comparison-manifest.json')['snapshots'];assert len(formal)==5 and formal==rel['formal_comparison_snapshots'];fc=[]
 for x in formal:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size']and sha(b)==x['sha256']and x['full_file_reviewed']and x['not_modified'];fc.append(dict(path=x['repo_path'],passed=True))
 links=[]
 for d in [Path(x)for x in docs]+[ER/'README.md']:
  txt=resolve(d).read_text()
  if str(d)in docs:assert txt.startswith('---\n')and 'source_ids:'in txt and 'source_refs:'in txt and len(txt)>2500
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',txt):
   if '://'in url or url.startswith('#'):continue
   dest=(root/d.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file(),(d,url);links.append(dict(source=str(d),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list)and listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute()and '..'not in Path(f).parts and(root/f).is_file()
 if(root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root))for x in root.rglob('*')if x.is_file())
 out=dict(all_checks_passed=True,check_kind='saved bytes and metadata, JSON/policy table structure and links only; no mathematical truth oracle or rerun',primary_count=3,primary_bytes=11904,comparison_source_count=2,source_byte_checks=checks,formal_snapshot_count=5,formal_snapshot_checks=fc,new_mathematical_objects=2,receipt_count=3,artifact_hash_checks=artifactchecks,markdown_link_checks=links,markdown_link_count=len(links),copy_list_check_mode=mode,copy_list_file_count=len(listed),original_source_CLI_executions_this_batch=0,new_supplemental_process_invocations_this_batch=2,new_supplemental_syntax_failure_processes_this_batch=1,new_supplemental_mathematical_body_executions_this_batch=1,new_supplemental_fixture_checks_this_batch=2,mathematical_programs_executed_by_verifier=0,operational_helpers_executed_by_verifier=0,network_requests_by_verifier=0,shared_Git_mutations_by_verifier=0)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_count','primary_bytes','new_mathematical_objects','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count']},ensure_ascii=False))
if __name__=='__main__':main()
