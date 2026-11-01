#!/usr/bin/env python3
"""Read-only hashes/AST/previously observed certificates/links/actual C0 bytes.
Does not import or execute either original or the separate leaf checker.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,ast,re
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/waterfill-credibility-and-uniform-contraction-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['035523def9872dfc4097','984d8cc1858eba449ca2','1ba0af014409270eba80','aba1c5ad7f8545bac193','d3d862c542db6a80d84e'];sm=j(E/'source-manifest.json');by={a['id']:a for a in sm['rows']};ck(sm['source_count']==5 and sm['source_bytes']==42943 and set(by)==set(ids),'exact-five42943-primary')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-sizeSHA256blob-'+id)
 ck(all(x['path']==a['source_path'] for x in a['sources']),'frozen-source-full-path-'+id)
cap=j(W/'claim-evidence.json');gate=j(W/'primary-authorization-check.json');recovery=j(W/'claim-sync-preservation.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['remote_tip']==gate['remote_tip']=='652cea58f65a262962978718b2dd10ce2e9bba45','actual14-source-pushed-652cea')
ck(cap['local_sync']['status']==gate['original_capture_local_sync_status']=='needs-attention' and gate['status']=='pass-with-independent-sync-recovery','original-needs-attention-not-rewritten-synced')
ck(len(cap['ids'])==gate['actual_claim_count']==14 and set(ids)<=set(cap['ids']) and set(gate['actual_intersection'])==set(ids),'actual-five-subset-not-demand-entire14-equals5')
ck((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-gi-claim.json').read_bytes() and sha(W/'claim-evidence.json')==gate['capture_sha256'],'full-original14-capture-unaltered')
ck((W/'claim-sync-preservation.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/boss4-r3-next-gh-to-gj-atomic-claim-sync-preservation.json').read_bytes() and sha(W/'claim-sync-preservation.json')==gate['recovery_sha256'],'independent-Root-recovery-unaltered')
ck(recovery['stash']=='31ff0b3b4ae9fabf162f431dddad7847a735f463' and recovery['untracked_count']==2 and recovery['missing']==recovery['different']==[] and recovery['unmerged']=='' and len(recovery['tracked'])==2 and all(a['same'] for a in recovery['tracked']),'Root-2untracked2tracked0missing0different0conflict')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'current-five-ownerSHA-'+a['id'])
ck(j(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_records']==[],'no-prior-success-exact8522SHA')
d=j(E/'dependency-manifest.json');ck(d['true_runtime_file_inputs']==2 and d['true_runtime_input_bytes']==37315 and sum(a['size'] for a in d['rows'])==37315,'real-two-inputs37315')
for a in d['rows']:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'dependency-raw-'+a['id'])
ck(d['consumed_fields']=={'instance':['customers[].topics','customers[].multiplicity'],'strategy':['actions[].history','actions[].action']} and d['hardcoded_topics']==7 and d['hardcoded_players']==4 and d['module_top_level_reads'],'actual-true-fields-and-top-level-input-side-effect')
tr=ast.parse((S/by[ids[1]]['path']).read_text());mods=[x.module for x in ast.walk(tr) if isinstance(x,ast.ImportFrom)]+[n.name for x in ast.walk(tr) if isinstance(x,ast.Import) for n in x.names];ck(set(mods)=={'fractions','functools','itertools','pathlib','hashlib','json'},'only-stdlib-no-model-author-solver-import')
ck(any(isinstance(x,ast.If) and '__name__' in ast.unparse(x.test) for x in tr.body),'main-guard-after-top-level-reads')
run=j(E/'replay/execution.json');ob=j(E/'replay/passive-observation.json');ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'only-one-original8522-success-assertions-on')
ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==run['source_sha256']==by[ids[1]]['sha256'],'relocated-unchanged-original-source')
ck(run['input_bytes_unchanged'] and len(run['true_runtime_file_inputs'])==2,'actual-two-inputs-unchanged')
for a in run['true_runtime_file_inputs']:ck((S/a['runtime_path']).stat().st_size==a['size'] and sha(S/a['runtime_path'])==a['sha256'],'runtime-input-hash-'+Path(a['path']).name)
output=S/run['output']['path'];frozen=S/by[ids[2]]['path'];ck(run['output']['frozen_byte_equal'] and output.read_bytes()==frozen.read_bytes() and output.stat().st_size==run['output']['size']==6997 and sha(output)==run['output']['sha256']==by[ids[2]]['sha256'],'whole6997-frozen-byte-equal')
ck(run['stdout_bytes']==(E/'replay/stdout.txt').stat().st_size==1075 and run['stderr_bytes']==(E/'replay/stderr.txt').stat().st_size==0,'actualstdout1075-stderr0')
for k,v in {'<module>':1,'main':1,'finish':2801,'density':5608,'query':637,'difference':16,'symbolic':32,'bernstein_certificate':12,'weighted_query':42,'small_u':8}.items():ck(ob['function_calls'][k]==v,'actual-source-calls-'+k+'-'+str(v))
ck(ob['entry_calls']==1 and ob['observer_extra_original_calls']==0 and run['observer_extra_original_calls']==run['other_original_entries']==run['uniform_contraction_entry_calls']==run['network_or_shared_repo_writes']==0,'no-extra-source-or-other-original-calls')
inputs={str((S/a['runtime_path']).resolve()) for a in run['true_runtime_file_inputs']};reads=[a for a in ob['observed_local_opens'] if a['path'] in inputs];ck(len(reads)==4 and all(sum(a['path']==p for a in reads)==2 for p in inputs),'two-distinct-inputs-open-twice-parse-and-hash-not-two-main')
writes=[a for a in ob['observed_local_opens'] if a['mode']=='x'];ck(len(writes)==1 and Path(writes[0]['path'])==output.resolve(),'one-exclusive-new-output-write')
r=j(output);final=ob['final_original_values'];ck(final['report']==r and final['comparisons']==r['original_action_comparisons_including_self']==2800 and final['minimum']==r['original_minimum_slack']=='0','actual-main-report2800min0')
ck(r['original_unit_customers']==53 and r['original_histories']==400 and r['matching_static_backgrounds']==84 and r['true_v4']==final['t']=='28481/2924' and r['deficit']==final['D']=='647/8772','observed53-400-84-truev4-D')
ck(r['source_packet_hashes']=={Path(a['path']).name:a['sha256'] for a in d['rows']},'report-real-inputSHA-match')
cert=r['last_BR_polynomial_certificates'];ck(len(cert)==12,'12-nonself-certificates-from14-rows')
for i,a in enumerate(cert):
 lower,upper=map(F,a['open_interval']);p0,p1,p2=map(F,a['power_coefficients']);scale=1-lower;q0=p0+p1*lower+p2*lower*lower;q1=scale*(p1+2*p2*lower);q2=scale*scale*p2;bern=(q0,q0+q1/2,q0+q1+q2);ck(upper==1 and tuple(map(F,a['bernstein_coefficients']))==bern and min(bern)>=0 and max(bern)>0,'exact-Bernstein-nonnegative-open-strict-'+str(i))
 if a['history']==[6,0,3]:ck(a['chosen']==4 and a['alternative']!=4 and lower==0,'left-last-BR-interval-'+str(i))
 else:ck(a['history']==[6,0,1] and a['chosen']==2 and a['alternative']!=2 and lower==F(2,11),'right-last-BR-interval-'+str(i))
ck({a['alternative'] for a in cert if a['history']==[6,0,3]}==set(range(7))-{4} and {a['alternative'] for a in cert if a['history']==[6,0,1]}==set(range(7))-{2},'both-all-six-nonself-BR-columns')
ck(F(r['zero_mass_query_excess'])==F(35,12)>F(r['deficit']) and F(r['rho_at_most_2_over_11_query_excess'])==F(309,140)>F(r['deficit']),'rhozero-and2over11-necessary-credit-exclusions')
ck([a['common_core'] for a in r['waterfill_core_cases']]==[0,1,1000],'exact-three-finite-core-parameters')
for a in r['waterfill_core_cases']:
 c=a['common_core'];lo,hi=map(F,a['rho_interval']);t=F(28481,2924)+F(c,4);ck(F(2,11)<lo<hi<1 and hi-lo==F(1,2**80),'one80step-open-root-interval-c'+str(c))
 ck(F(12,1+lo)+F(11,2+lo)+F(c,3+lo)>t>F(12,1+hi)+F(11,2+hi)+F(c,3+hi),'root-bracket-strict-densities-c'+str(c))
 ck(F(a['strict_root_profit_improvement_lower'])==2*(1-hi)/(hi+2)>0 and F(a['strict_third_profit_improvement_lower'])==3*(1-hi)/((hi+1)*(hi+2))>0,'both-positive-improvement-lower-c'+str(c))
 ck(0<=F(a['all_query_credit_max_upper'])<=F(647,8772),'observed-seven-query-max-bound-c'+str(c))
ck(r['small_free_threshold_example']=={'unit_customers':3,'players':2,'topics':2,'threshold':'4/3','unique_admissible_weight':'1/2','strict_tail_profit_improvement':'1/3'},'exact-small3-free-not-endogenous-threshold')
ck('No common waterfill weights' in r['scope'] and 'different leaf' in r['scope'] and 'fixed high' not in r['scope'].lower(),'original-frozen-scope-unmodified-needs-narrow-contract')
leaf=j(E/'uniform-leaf-arithmetic-check.json');ck(leaf['status']=='pass-separate-data-only-actual-leaf-and-one-terminal-symbolic-comparison' and leaf['entry_calls']==1 and leaf['original_source_function_calls']==leaf['new_full400_SPE_scans']==leaf['new_2800_comparisons']==leaf['uniform_contraction_original_entry_calls']==0,'separate-leaf-check-one-entry-no-SPE-or-original-functions')
ck(leaf['input_hashes']==r['source_packet_hashes'] and leaf['actual_tail']==[0,3,4] and leaf['actual_spectrum']=={'0':21,'1':6,'2':15,'3':11},'same-input-actual-leaf-spectrum21-6-15-11')
ck(list(map(F,leaf['original_fresh_utilities']))==[F(29,3),F(67,6),F(67,6)] and F(leaf['S'])==F(6,4)+F(30,9)+F(33,16)==F(331,48) and F(leaf['a_star_minus_S'])==F(133,48),'fresh-a-and-spectral-algebra')
lam=F(leaf['lambda0']);t=F(leaf['true_t0_from_source_matching_certificate']);D=F(leaf['D']);ck(lam==F(84796,85443) and F(29,3)/lam==t and t-F(29,3)==D==F(647,8772),'true-t-lambda0-deficit-exact')
ck(F(leaf['all_customer_H0'])==sum((n*(1/(1+lam*k)-F(1,1+k)) for k,n in [(1,6),(2,15),(3,11)]),F())==F(206474219394865,3934509249981684)<D,'full-actual-spectral-H0-exact-below-D')
ck(F(leaf['max_seven_queries'])==max(map(F,leaf['seven_query_credits']))==F(187117307516351,4918136562477105)<=F(leaf['all_customer_H0']),'sevenquerymax-distinct-from-common-H0')
ck(F(leaf['all_customer_H0'])<=D-F(133,48)*(1/lam-1) and F(leaf['Vminus3lambda_t'])==sum(map(F,leaf['original_fresh_utilities']))-3*lam*t==3,'spectral-slack-and-three-profit-budget')
ck(leaf['P_child_decision_rows_inspected_without_IC']==57 and leaf['P_child_all_prescribed_actions_avoid_P'],'57-ordered-P-child-prescribed-action-inspection-no-IC')
ck(leaf['two_terminal_leaves']==[[0,0,6,1],[0,0,6,2]] and {(a['background_first_root_covered'],a['three_tail_coverage']):a['signed_customers'] for a in leaf['signed_terminal_buckets']}=={(1,2):3,(0,1):-1},'two-terminal-packet-buckets-plus3-minus1')
ck(3*lam/(1+2*lam)-1==(lam-1)/(1+2*lam)==F(leaf['terminal_profit_gap_at_lambda0'])==F(-647,255035)<0,'offpath-analytic-IC-flip-at-lambda0')
ck(leaf['claimed36_other_tree_flips_not_recomputed'] and leaf['root_seven_IC_not_recomputed'],'36-and-root7-not-counted-as-new-checks')
comp=j(E/'comparison-manifest.json');ck(len(comp['rows'])==4,'four-full-related-formal-snapshots')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-current-bytes-'+Path(a['path']).name)
ck(comp['rows'][0]['size']==8599 and comp['rows'][0]['sha256']=='b8016751cd4d68e9236fa25dbf3b3a26c28a35b46e3205dee13190cfd86c6501' and comp['frozen_older_EA_package_unchanged'],'corrected8599b801-base-no-old-frozen-edit')
rec=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids),'five-primary-semantic-receipts')
for a in rec:ck(a['source_sha256']==by[a['id']]['sha256'] and all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>100 and set(a['targets'])<=set(targets),'complete-read-comparison-decision-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==74 and len(j(W/'relation-review.json')['relations'])==10,'74-math-and10-meaningful-relations')
n=j(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==56410 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'next-five56410-local-only-no-progress')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-metadata-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);ck((S/rel).is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
ck(len(stable)==len(set(stable))==3,'three-distinct-stable-objects')
scope=j(E/'scope.json');ck(scope['original8522_entry_calls']==scope['separate_data_only_actual_leaf_checker_calls']==1 and scope['data_only_original_function_calls']==scope['data_only_new_full_SPE_scans']==scope['uniform_contraction13247_entry_calls']==scope['old_waterfill_VAR_tax_constructor_entry_calls']==scope['network_or_shared_git_writes']==0,'actual-one-original-one-leaf-zero-other-entries')
manifest=j(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist')
ck(all(not Path(x).is_absolute() and '..' not in Path(x).parts for x in manifest),'safe-copy-relative-paths')
ck(all(not bad(S/x) for x in manifest),'all-staged-actual-C0-bytes-except-LF-TAB-CR')
ck(all(not any(line.rstrip(b' \t')!=line for line in (S/x).read_bytes().split(b'\n')) for x in manifest if x.endswith(('.py','.md','.json'))),'all-text-no-trailing-space-tab')
for x in manifest:
 if x.endswith('.json'):json.loads((S/x).read_text(),parse_constant=lambda z:(_ for _ in ()).throw(ValueError(z)))
ck(True,'strict-finite-JSON-all-files')
v={'status':'pass','scope':'read-only source/input/raw/AST/already-observed finite certificates/limited leaf arithmetic/links/whitelist/C0; no original or leaf checker execution','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':74,'human_relations':10,'original8522_entry_calls':1,'separate_leaf_checker_entry_calls':1,'uniform_contraction13247_entry_calls':0,'original_or_leaf_checker_calls_in_selfcheck':0,'claim_original_sync_status':'needs-attention','independent_Root_recovery_record_preserved':True,'C0_scope':'actual bytes of every staged file; exclude only LF/TAB/CR'};(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
