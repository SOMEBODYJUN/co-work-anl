"""Verify saved bytes/complete JSON/links only. Never import mathematical sources."""
from pathlib import Path
import argparse,hashlib,json,re,random,difflib
ER=Path('archives/unrelated-machines/tools/evidence/um-locally-cached-four-audits-primary');WS=Path('cleanup/workspaces/Boss4/r3-um-locally-cached-four-audits-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 def resolve(rel):
  rel=Path(rel);assert not rel.is_absolute() and '..' not in rel.parts;x=root/rel;return x if x.is_file()else fallback/rel
 def raw(rel):return resolve(rel).read_bytes()
 def load(rel):return json.loads(raw(rel))
 groups=[load(ER/n)['sources']for n in ['source-manifest.json','dependency-manifest.json','comparison-manifest.json']];assert list(map(len,groups))==[4,3,13];items={x['id']:x for g in groups for x in g};assert len(items)==20;checks=[]
 for sid,x in items.items():
  b=raw(x['preserved_repo_path']);assert len(b)==x['source_size'] and sha(b)==x['source_sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['source_git_blob'] and x['full_file_reviewed'] and 'pending'not in x['read_scope'];checks.append(dict(id=sid,size=len(b),sha256=sha(b),Git_blob_sha1=x['source_git_blob'],passed=True))
 ids={x['id']for x in groups[0]};claim=load(ER/'claim-confirmation.json');assert claim['actor']=='Boss4' and claim['status']=='pushed' and claim['local_sync']['status']=='synced' and set(claim['ids'])==ids
 owners=load(ER/'actual-owner-verification.json');assert len(owners)==4 and {x['id']for x in owners}==ids and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==items[x['id']]['source_sha256']for x in owners)
 original=load(ER/'root-local-input-manifest.json');assert len(original)==4 and {x['id']for x in original}==ids and all(x['network_requests']==0 and x['sha256']==items[x['id']]['source_sha256'] and x['blob']==items[x['id']]['source_git_blob']for x in original)
 execution=load(ER/'runs/execution-manifest.json');runs=execution['executions'];assert len(runs)==4 and {x['source_sha256']for x in runs}=={x['source_sha256']for x in groups[0]}
 for x in runs:
  assert x['exit_code']==0 and not x['timed_out'] and x['mathematical_program_execution'] and raw(x['stderr'])==b'' and resolve(x['stdout']).is_file() and load(ER/('runs/'+x['name']+'.execution.json'))==x
 countfields=['primary_source_CLI_executions_this_batch','primary_mathematical_audit_body_executions_this_batch','additional_source_CLI_invocations','supplemental_mathematical_audit_executions_this_batch','imported_unguarded_mathematical_audit_bodies','top_level_primary_audit_body_executions','guarded_primary_audit_body_executions','helper_mains_executed'];assert [execution[k]for k in countfields]==[4,4,0,0,0,1,3,0]
 artifacts=load(ER/'artifact-manifest.json')['runtime_artifacts'];assert len(artifacts)==13
 for x in artifacts:
  b=raw(x['repo_path']);assert len(b)==x['size'] and sha(b)==x['sha256']
 history=load(ER/'historical-comparison-and-version-scope.json');assert len(history['comparisons'])==5
 for x in history['comparisons']:
  ajson=load(x['current']);bjson=load(x['historical'])
  for k in x['historical_keys']:bjson=bjson[k]
  diff=sorted(k for k in set(ajson)|set(bjson)if ajson.get(k)!=bjson.get(k));assert diff==x['difference_keys'] and (ajson==bjson)==x['all_fields_equal']
  assert diff==(['source_sha256']if x['name']=='symmetric-reset-old-source'else[]) and x['all_mathematical_fields_equal']
  if x['byte_equal']:assert raw(x['current'])==raw(x['historical'])
 lines=raw(items['00d731603b0001b80486']['preserved_repo_path']).splitlines(keepends=True);lines[309]=lines[309][:-1]+b' \n';assert sha(b''.join(lines))==history['symmetric_reset_old_source_reconstructed_by_one_ASCII_space_before_line310_LF']=='32488435252174b6d7302af66c7976518b6b2f0cf77ac07fccc3788254dc7735'
 old=load(ER/'comparison/evidence/runs/unrelated_machines/joint_matching_completion_audit.json');rng=random.Random(20261016);u=[(a,b,c)for a in range(3)for b in range(3)for c in range(3)];samples=[[list(t)for t in rng.sample(u,rng.randint(1,12))]for _ in range(50)];assert samples==old['actual_q3_sampled_tripartite_inputs'] and history['all50_unique_small_q3_inputs_equal_frozen_seed_recipe']
 scope=load(ER/'mathematical-execution-scope.json');assert [scope[k]for k in countfields]==[4,4,0,0,0,1,3,0] and not scope['source_bytes_modified'] and scope['network_calls_for_materialization_or_runs']==0 and scope['new_blind_reviews']==0
 reset=load(ER/'runs/symmetric-reset.stdout');tree=load(ER/'runs/tree-markov.stdout');small=load(ER/'runs/two-small-flow.stdout');unique=load(ER/'runs/unique-small.stdout')
 assert sum(x['count_vectors']for x in reset['lower_count_vector_audits'])==27591 and sum(x['count_vectors']for x in reset['upper_count_vector_audits'])==41 and sum(x['literal_machine_checks']for x in reset['upper_count_vector_audits'])==4385 and reset['scalar_checks']==10584 and sum(x['assignments_enumerated']for x in reset['direct_pushforward_audits'])==7564
 assert [x['decomposition_states']for x in reset['same_base_recoupling_audits']]==[4,6] and [x['recoupled_joint_entries']for x in reset['same_base_recoupling_audits']]==[324,5625] and [x['recoupled_true_and_false_literal_checks']for x in reset['same_base_recoupling_audits']]==[108,750]
 assert tree['complete_orientations_enumerated']==32 and tree['exact_OPT']=='1' and len(tree['markov_outputs'])==4 and [x['weight']for x in tree['markov_outputs']]==['1/4']*4 and sorted(x['completion_optimum']for x in tree['markov_outputs'])==['1','1','1','2']
 assert [small[k]for k in ['local_membership_checks','random_matrices','threshold_checks','q2_3dm_all_subsets']]==[16128,300,7997,256] and small['status']=='PASS'
 assert [unique[k]for k in ['instances','yes_instances','scheduling_backtracking_nodes','sampled_q3_instances']]==[309,194,2438807,50] and unique['every_job_exactly_one_small'] and unique['N_empty'] and unique['helper_sha256']==items['30bcde3e1f48ab5c0e63']['source_sha256'] and unique['baseline_sha256']==items['e57947bc795251d373c3']['source_sha256']
 assert unique['block_cuts']['single_block_k4_feasible_assignments_counted_per_threshold']==558 and len(unique['block_cuts']['family_parameter_checks'])==61 and unique['block_cuts']['family_parameter_checks'][-1]['h']==221 and unique['block_cuts']['delta_one_third_counterexample']
 rec=load(WS/'semantic-receipts.json');assert len(rec)==4 and {x['id']for x in rec}==ids
 for x in rec:assert all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(isinstance(x[k],str)and x[k].strip()for k in ['read_note','comparison_note','decision_note']) and x['disposition']=='retained' and x['targets'] and all(resolve(t).is_file()for t in x['targets'])
 rel=load(ER/'relation-review.json');assert len(rel['new_computation_objects'])==4 and not rel['formal_hypergraph_written'];formal=[]
 for x in rel['formal_comparison_snapshots']:
  b=raw(x['preserved_snapshot_path']);assert len(b)==x['size'] and sha(b)==x['sha256'] and x['not_modified'];formal.append(dict(repo_path=x['repo_path'],preserved_snapshot_path=x['preserved_snapshot_path'],passed=True))
 assert len(formal)==6;err=load(ER/'errata/manifest.json');before=raw(err['original_snapshot']);after=raw(err['proposed_path']);assert sha(before)==err['before_sha256'] and sha(after)==err['proposed_sha256'] and not err['source_code_modified'] and not err['old_done_modified'] and not err['new_mathematical_counterexample_claimed']
 patch=''.join(difflib.unified_diff(before.decode().splitlines(keepends=True),after.decode().splitlines(keepends=True),fromfile='a/'+err['target'],tofile='b/'+err['target']));assert raw(err['patch_path']).decode()==patch
 links=[]
 for doc in [Path(x)for x in rel['new_computation_objects']]+[ER/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(doc).read_text()):
   if '://'in url or url.startswith('#'):continue
   dest=(root/doc.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file()or(root/dest).resolve()==a.output.resolve(),(doc,url);links.append(dict(source=str(doc),target=str(dest),passed=True))
 listed=load(WS/'copy-files.json');assert isinstance(listed,list)and listed==sorted(set(listed))
 for f in listed:assert not Path(f).is_absolute()and '..'not in Path(f).parts and(root/f).is_file()
 if(root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(x.relative_to(root))for x in root.rglob('*')if x.is_file())
 out=dict(check_kind='saved source bytes with SHA256/Git blob SHA1, complete JSON, byte-version/seed-input recipe, concrete errata and links only; no mathematical source execution',all_checks_passed=True,primary_source_count=4,dependency_source_count=3,comparison_source_count=13,source_byte_checks=checks,runtime_artifact_hash_count=13,historical_comparison_count=5,formal_comparison_snapshot_hash_checks=formal,receipt_count=4,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,copy_list_file_count=len(listed),primary_source_CLI_executions_observed=4,mathematical_audit_body_executions_observed=4,additional_source_CLI_invocations=0,supplemental_mathematical_audit_executions=0,imported_unguarded_mathematical_audit_bodies=0,top_level_primary_audit_body_executions=1,helper_mains_executed=0,mathematical_programs_executed_by_verifier=0,network_requests_by_verifier=0,source_bytes_modified=False,other_Boss_formal_pages_modified=False,errata_is_proposal_only=True,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['all_checks_passed','primary_source_count','dependency_source_count','comparison_source_count','runtime_artifact_hash_count','historical_comparison_count','receipt_count','markdown_link_count','copy_list_check_mode','copy_list_file_count']},ensure_ascii=False))
if __name__=='__main__':main()
