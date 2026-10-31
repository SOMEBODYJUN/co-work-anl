#!/usr/bin/env python3
"""Read-only records/raw bytes and closed-form arithmetic; no math entry imported or rerun."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib,re,posixpath,ast
ROOT=Path('/workspace/scratch/37f0f9248cfc');R=ROOT/'boss4-research';S=ROOT/'boss4-next-cache/r3-random-retention-common-pool-and-reset-primary';ER='archives/customer-attraction/tools/evidence/random-retention-common-pool-and-reset-primary';WR='cleanup/workspaces/Boss4/r3-random-retention-common-pool-and-reset-primary';E=S/ER;W=S/WR
j=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(x,n):
 if not x:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(b<32 and b not in (9,10,13) for b in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];inv={a['id']:a for a in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())};lm=j(W/'local-source-export-manifest.json');ck(len(rows)==5 and sum(a['size'] for a in rows)==23752 and not lm['missing'],'five-full-MD-primary23752')
for a in rows:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256']==inv[a['id']]['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-source-sizeSHAblob-'+a['id']);ck(a['full_primary_read'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md'),'full-primary-MD-no-original-entry-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['remote_tip']=='1c77a5e55c2a8939e7b4689c0e10ac1ad62df288','real-KC-pushed-synced1c77a5')
ck(sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-kc-claim.json')==g['original_capture_unmodified_sha256'],'exact-whole-original-capture-bytes');ck(len(c['ids'])==g['whole_capture_size']==19 and c['ids']==g['whole_capture_ids'] and set(a['id'] for a in rows)<=set(c['ids']) and g['claim_subset_not_projected'],'own-five-intersect-original19-not-projected')
for o in g['current_owners']:ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'actual-owner-sourceSHA-'+o['id'])
ctx=j(E/'context-manifest.json');ck(len(ctx['rows'])==3 and sum(a['size'] for a in ctx['rows'])==23342 and ctx['context_primary_done_added']==ctx['source_function_calls']==0,'three-full-context23342-no-extra-done')
for a in ctx['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'] and a['full_context_read'] and not a['additional_primary_done'],'raw-full-context-'+a['id'])
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==5,'five-current-comparisons')
for a in comp:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'] and a['full_related_read'] and a['publication_not_inferred_from_local_presence'],'full-raw-current-comparison-'+a['name'])
initial=j(E/'initial-missing-dependency-export.json');ck(not initial['rows'] and len(initial['missing'])==5 and 'no network/lazy fetch' in initial['method'],'initial-five-local-missing-preserved')
dm=j(E/'dependency-manifest.json');dep=dm['rows'][0];p=S/dep['path'];raw=p.read_bytes();ck(dep['id']=='4990c154aeab44fc616a' and dep['size']==len(raw)==10115 and sha(p)==dep['sha256']=='2b8fc76f799bee83b5e8588f94f7c8dfa6f91a634ffe624ede820cc909af541c' and hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()==dep['blob'],'later-real-original31-input-sizeSHAblob')
ck(dep['full_original_input_and_85_actions_read'] and not dep['additional_primary_done'] and not dm['supplement_not_executed_yet'] and dm['independent_definition_level_supplement_entry_calls']==2,'later-read-no-extra-JSON-done-and-real-two-entries')
show=j(E/'original-certificate-show-capture.json');ck(show['source']['id']==dep['id'] and show['source']['sha256']==dep['sha256'] and show['source']['size']==10115,'raw-normal-show-capture-exact-source-identity')
reuse=j(E/'reuse-search.json');ck(not reuse['existing_successful_exact_input_run_found'] and reuse['matches_are_only_frozen_inventory_or_path_indexes'] and len(reuse['whole_repository_matches'])==5,'whole-repo-old-exactSHA-success-search')
first=j(E/'supplement/actual-invocation.json');second=j(E/'supplement/actual-invocation-corrected.json');ck(first['status']=='failed' and first['exit_code']==1 and first['own_supplement_entry_calls']==1 and first['stdout_bytes']==0,'first-actual-failed-entry-retained-not-PASS');ck(second['status']=='completed' and second['exit_code']==0 and second['own_supplement_entry_calls_total']==2 and second['own_supplement_entry_calls_this_attempt']==1 and second['previous_failed_attempts']==1 and second['stderr_bytes']==0,'one-corrective-success-total-two-entries')
ck(first['input_sha256']==second['input_sha256']==dep['sha256'] and first['claim_remote_tip']==second['claim_remote_tip']==c['remote_tip'] and first['original_entry_calls']==second['original_entry_calls']==0,'same-original-input-and-authorized-claim-not-original-CLI')
ck(first['claim_capture_sha256']==second['claim_capture_sha256']==sha(W/'claim-evidence.json'),'both-actual-runs-after-same-real-claim')
for fn in ['actual-invocation.json','stdout.txt','stderr.txt']:ck((E/'supplement'/fn).read_bytes()==(E/'supplement/failed-attempt-1'/fn).read_bytes(),'unchanged-first-failure-'+fn)
fc=E/'supplement/failed-attempt-1/check_original_31_policy_and_true_three_floor.py';cc=E/'supplement/check_original_31_policy_and_true_three_floor.py';ck(sha(fc)==first['implementation_sha256']=='80a27240dae968bd1b44c7328b26746639c4d1abd614e9414bc3433f6bd363bf' and sha(cc)==second['implementation_sha256']=='85dfbc7714bd8b8f95390fb5bfa388fa869280dbc6383aa6c029090755190d5c','both-exact-implementation-versions-retained')
ck('zreset in rootleaves and set(welfare' in fc.read_text() and 'zreset not in rootleaves and set(welfare' in cc.read_text(),'narrow-own-overstrong-postcondition-fix')
allowed={'pathlib','fractions','functools','itertools','hashlib','json','sys'}
for p in [fc,cc]:
 tree=ast.parse(p.read_text());mods=set()
 for a in ast.walk(tree):
  if isinstance(a,ast.Import):mods.update(x.name.split('.')[0] for x in a.names)
  elif isinstance(a,ast.ImportFrom):mods.add(a.module.split('.')[0])
 ck(mods<=allowed,'own-definition-code-stdlib-only-no-canonical-import-'+p.parent.name)
r=j(E/'supplement/corrected-replay/summary.json');ck(r['status']=='pass' and r['input_sha256']==dep['sha256'] and r['input_bytes']==10115 and r['expanded_unit_customers']==31,'successful-one-input-summary-identity')
ck(r['original_complete_strategy_nodes']==85 and r['original_real_IC_comparisons_including_self']==340 and F(r['minimum_IC_slack'])==0,'recorded-original-complete-policy85-340')
ic=j(E/'supplement/corrected-replay/all-original-340-IC.json');ck(len(ic)==340 and min(F(x['slack']) for x in ic)==0 and all(F(x['slack'])>=0 for x in ic),'saved-full340-records-not-reexecuted')
bi=j(E/'supplement/corrected-replay/all-true-three-BI.json');ck(len(bi)==r['true_three_decision_nodes']==21 and r['true_three_ordered_states']==85 and r['true_three_forced_children']==84 and all(len(x['children'])==4 for x in bi),'saved-all-ordered-three-BI21-84-85')
ck(r['true_three_SPE_terminal_count']==1 and r['true_three_SPE_welfare_set']==[31] and r['true_three_OPT']==31,'exact-fixed-three-domain-not-general-parameter-result')
ck(r['floors']==['12','12','10'] and r['target_profits']==['8','15/2','15/2'] and r['positive_deficits']==['4','9/2','5/2'] and r['sum_deficits']=='11' and r['budget']=='28/3' and r['budget_failure']=='5/3','recorded-true-floor-counterexample11-vs28over3')
ck(not r['deleted_target_is_SPE_outcome'] and not r['BR_reset_target_is_root_SPE_outcome'] and r['BR_reset_sum_deficits']=='3' and r['BR_reset_profits']==['9','12','10'],'BR-reset-target-not-root-SPE-but-different-budget-not-refuted')
ck(json.loads((E/'supplement/stdout-corrected.txt').read_text())==r and not (E/'supplement/stderr-corrected.txt').read_bytes(),'actual-success-stdout-summary-and-zero-stderr')
scope=j(E/'scope.json');ck(scope['primary_sources']==5 and scope['primary_source_bytes']==23752 and scope['formal_objects']==3 and scope['human_math_items']==64 and scope['explained_relations']==8,'scope-source-math-items-relations')
for k in ['original_entry_calls','original_source_function_calls','canonical_solver_or_import_calls','new_LP_or_parameter_scans','network_or_shared_git_writes','context_primary_done_added']:ck(scope[k]==0,'actual-zero-'+k)
ck(scope['independent_definition_level_supplement_entry_calls']==scope['original_policy_IC_audits']==scope['true_three_BI_root_calls']==2 and scope['independent_supplement_failed_attempts']==scope['independent_supplement_successful_attempts']==1,'actual-two-computations-one-failed-one-success-not-unique-PASS')
for k in ['same_original_r_tree_not_physical_n_SPE','fixed_external_background_and_rn','qdev_and_Gamma_and_row_mass_preserved','fixed_parameters_in_deleted_slot_potential','individual_loss_pool_not_second_potential_wallet','signed_flow_not_positive_parts','floor_failure_includes_last_not_BR_reset','BR_reset_different_contract_not_refuted','fresh_and_signed_read_orders_preserved','historical_kernel_runs_not_repeated','six_provider_coefficients_analytic_not_original_kernel_run','initial_missing_record_retained','supplement_after_true_actual_claim','no_new_blind_or_external_review','first_failure_own_overstrong_postcondition_not_source_failure']:ck(scope[k],'precise-quantifier-domain-'+k)
recs=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(recs)==5 and len(targets)==len(set(targets))==3 and {a['id'] for a in recs}=={a['id'] for a in rows},'five-final-primary-receipts-three-objects')
for a in recs:
 sr=next(x for x in rows if x['id']==a['id']);ck(a['owner']=='Boss4' and a['disposition']=='integrated' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-integrated-'+a['id']);ck(a['source_sha256']==sr['sha256'] and a['source_size']==sr['size'] and a['source_path']==sr['source_path'] and a['raw_evidence']==sr['path'],'receipt-exact-raw-identity-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'substantive-specific-receipt-'+a['id']);ck('external stage only' in a['publication_status'] and 'not body-pushed' in a['delivery_status'],'semantic-integrated-versus-body-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==64,'sixty-four-human-source-math-obligations');rels=j(W/'relation-review.json')['relations'];ck(len(rels)==8 and all(len(x['explanation'])>40 for x in rels),'eight-explained-relations')
ids=[];links=[]
for rel in targets:
 p=S/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>7000 and not c0(p) and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'full-object-actual-C0-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));p2=S/q if (S/q).is_file() else R/q;ck(p2.is_file(),'resolve-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(p2)})
ck(len(set(ids))==3,'three-stable-object-ids')
a,b,d=[(S/t).read_text() for t in targets]
for s,label in [('全部r身份仍在原有序树中作决定','auxiliary-not-physical'),('同一个J','same-client-sampling-coupling'),('偏离叶q_i(z_A)','negative-dev-credit'),('L_i=Σ_Aλ_(i,A)≤1','same-identity-row-capacity'),('b0,t1须用分段值','singular-background-endpoint'),('r6的直接解析代入','six-coefficients-not-kernel-run')]:ck(s in a,'pool-unit-'+label)
for s,label in [('仍按原r,n的ψ核','fixed-r-n-under-slot-deletion'),('第一份整势差由FLOW共付','flow-vs-unpaid-reset'),('源总质量为M','source-mass-not-free'),('个人总损失池','not-second-wallet')]:ck(s in b,'potential-unit-'+label)
for s,label in [('两次实际调用','actual-two-entry-count'),('根收益9<12','failed-own-overstrong-assertion-explained'),('末位BR-reset','contract-last-reset-boundary'),('保存§1–8后','fresh-read-order'),('没有把同计数','ordered-context')]:
 if label=='ordered-context':ck('强绑同计数动作' in d,'finite-unit-'+label)
 else:ck(s in d,'finite-unit-'+label)
# Scalar substitutions only: no source functions/retention enumeration/SPE solver reexecuted.
ck(sum([6,3,2,1,5,2,6,2,4])==31 and F(4)+F(9,2)+F(5,2)==11 and F(11)-F(28,3)==F(5,3) and F(28,3)-8==F(4,3),'31-contract-scalar-bookkeeping')
ck(F(9)<12 and F(12)-9==3<F(28,3),'reset-root-not-SPE-exact-scalar')
q6={n:[F(6,n)*F(comb(6-t,n),comb(6,n)) for t in range(1,7-n)] for n in range(1,6)};ck(q6=={1:[F(5),F(4),F(3),F(2),F(1)],2:[F(2),F(6,5),F(3,5),F(1,5)],3:[F(1),F(2,5),F(1,10)],4:[F(1,2),F(1,10)],5:[F(1,5)]},'six-load-coefficient-closed-form-substitution-not-kernel-scan')
h=lambda r:sum((F(1,k) for k in range(1,r+1)),F(0));ck([h(5)-h(n) for n in [4,3,2,1]]==[F(1,5),F(9,20),F(47,60),F(77,60)] and [h(6)-h(n) for n in [5,4,3,2,1]]==[F(1,6),F(11,30),F(37,60),F(19,20),F(29,20)],'five-six-harmonic-scalar-substitutions-not-original-run')
n=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(n['rows'])==len(nm['rows'])==5 and not nm['missing'] and n['source_bytes']==sum(x['size'] for x in n['rows'])==30833,'next-actual-five30833-context-not-done')
for x in n['rows']:
 p=Path(x['local_path']);ck(p.stat().st_size==x['size'] and sha(p)==x['sha256'] and x['actual_local_complete'] and x['not_primary_done_here'],'next-raw-identity-not-done-'+x['id'])
files=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file());ck(files==j(W/'copy-files.json') and WR+'/copy-files.json' in files,'exact-sorted-self-inclusive-copy-manifest');ck(all(not p.startswith('/') and '..' not in Path(p).parts for p in files),'safe-relative-copy-whitelist');ck(not any(c0(S/p) for p in files),'all-actual-C0-bytes-except-LF-TAB-CR');ck(not any(any(line.endswith((' ','\t')) for line in (S/p).read_text().splitlines()) for p in files),'no-trailing-whitespace-all-files')
for p in files:
 if p.endswith('.json'):json.loads((S/p).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'read-only raw/provenance/receipts/success-failure records/metadata/links/C0 and closed-form scalar bookkeeping; no math code reexecuted','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'primary_bytes':23752,'objects':3,'integrated_receipts':5,'human_math_items':64,'explained_relations':8,'original_entry_calls':0,'original_source_or_canonical_imports':0,'LP_or_parameter_scans':0,'independent_supplement_entries':2,'supplement_failed_attempts':1,'supplement_successful_attempts':1,'unique_input_customers':31,'per_attempt_original_policy_nodes':85,'per_attempt_original_IC_comparisons':340,'per_attempt_true_three_ordered_states':85,'per_attempt_true_three_forced_children':84,'same_input_no_parameter_expansion':True,'initial_missing_later_acquisition_failure_and_success_preserved':True,'next_actual_local_bytes':30833,'C0_scope':'actual bytes except only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
