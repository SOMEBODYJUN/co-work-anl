#!/usr/bin/env python3
"""Read-only byte/AST/observed-report/finite certificate/links/C0 selfcheck.
No original program import, execution, or added source-function calls.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,ast,re
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');GI=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-waterfill-credibility-and-uniform-contraction-primary');E=S/'archives/customer-attraction/tools/evidence/uniform-contraction-and-credibility-relay-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['db227274fac376624980','b799d7f35245d89e4f69','9148fc370cca9d7b1038','4d500d3dc5c58bcf5f45','18771c888f536e75a6cf'];sm=j(E/'source-manifest.json');by={a['id']:a for a in sm['rows']};ck(sm['source_count']==5 and sm['source_bytes']==56410 and set(by)==set(ids),'five-full-primary56410')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-sizeSHA256blob-'+id);ck(all(x['path']==a['source_path'] for x in a['sources']),'full-frozen-path-'+id)
cap=j(W/'claim-evidence.json');gate=j(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced' and cap['remote_tip']==gate['remote_tip']=='b9c55b203d9c6136a175dad21ae6162a809ed01f','authentic-pushed-synced-b9c55')
ck(len(cap['ids'])==gate['actual_claim_count']==11 and set(ids)<=set(cap['ids']) and set(gate['actual_intersection'])==set(ids) and gate['status']=='pass','actual-five-subset-of-full11')
ck((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-gr-claim.json').read_bytes() and sha(W/'claim-evidence.json')==gate['capture_sha256'],'full-original11-capture-unaltered')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'ownerSHA-'+a['id'])
ck(j(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_records']==[],'no-old-success-either-exact-sourceSHA')
d=j(E/'dependency-manifest.json');ck(sum(a['size'] for a in d['rows'])==38061 and d['shared_instance_and_strategy_bytes']==37315 and d['security_bytes']==746,'two37315-versus-three38061-input-closures')
for a in d['rows']:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'dependency-sizeSHAblob-'+a['id'])
ck(len(d['uniform13247']['real_file_inputs'])==2 and len(d['relay11754']['real_file_inputs'])==3 and d['uniform13247']['minimax_certificate_hardcoded'] and d['relay11754']['top_level_reads_and_full_entry_on_import'],'true-fields-and-certificate-origin-differ')
rs={};obs={};reports={}
for kind,codeid,outid,ninputs,nbytes,guard,stdbytes in [('uniform',ids[0],ids[1],2,37315,True,805),('relay',ids[3],ids[4],3,38061,False,671)]:
 code=S/by[codeid]['path'];tree=ast.parse(code.read_text());mods=[x.module for x in ast.walk(tree) if isinstance(x,ast.ImportFrom)]+[n.name for x in ast.walk(tree) if isinstance(x,ast.Import) for n in x.names];ck(set(mods)<={'collections','fractions','functools','itertools','pathlib','hashlib','json'} and 'fractions' in mods,'stdlib-only-no-author-solver-import-'+kind)
 ck(any(isinstance(x,ast.If) and '__name__' in ast.unparse(x.test) for x in tree.body)==guard,'actual-main-guard-'+kind)
 run=j(E/('replay-'+kind)/'execution.json');ob=j(E/('replay-'+kind)/'passive-observation.json');rs[kind]=run;obs[kind]=ob;ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'one-original-success-assertions-on-'+kind)
 ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==run['source_sha256']==by[codeid]['sha256'],'raw-source-relocated-'+kind)
 ck(len(run['true_runtime_file_inputs'])==ninputs and sum(a['size'] for a in run['true_runtime_file_inputs'])==nbytes and run['input_bytes_unchanged'],'real-input-countbytes-'+kind)
 for a in run['true_runtime_file_inputs']:ck((S/a['runtime_path']).stat().st_size==a['size'] and sha(S/a['runtime_path'])==a['sha256'],'runtime-input-hash-'+kind+'-'+Path(a['path']).name)
 out=S/run['output']['path'];frozen=S/by[outid]['path'];ck(run['output']['frozen_byte_equal'] and out.read_bytes()==frozen.read_bytes() and out.stat().st_size==run['output']['size']==by[outid]['size'] and sha(out)==run['output']['sha256']==by[outid]['sha256'],'whole-report-frozen-byte-equal-'+kind);reports[kind]=j(out)
 ck(run['stdout_bytes']==(E/('replay-'+kind)/'stdout.txt').stat().st_size==stdbytes and run['stderr_bytes']==(E/('replay-'+kind)/'stderr.txt').stat().st_size==0,'real-stdout-stderr-'+kind)
 ck(ob['original_module_calls']==1 and ob['original_main_calls']==(1 if guard else 0) and ob['observer_extra_original_calls']==run['observer_extra_original_calls']==run['other_original_entry_calls']==run['network_or_shared_repo_writes']==0,'one-module-main-structure-no-extra-original-calls-'+kind)
 inputs={str((S/a['runtime_path']).resolve()) for a in run['true_runtime_file_inputs']};ck(all(sum(a['path']==p and a['mode']=='r' for a in ob['observed_local_opens'])==2 for p in inputs),'parse-and-report-hash-two-reads-not-two-entry-'+kind)
 writes=[a for a in ob['observed_local_opens'] if a['mode'] in ['x','w']];ck(len(writes)==1 and Path(writes[0]['path'])==out.resolve() and writes[0]['mode']==('x' if guard else 'w'),'one-real-exclusive-or-write-output-'+kind)
for kind,expect in {'uniform':{'main':1,'finish':2801,'profit':8809,'static_query':637,'query':84,'heterogeneous_frozen_background':1,'terminal':234,'player_profit':237,'positive_part':1},'relay':{'finish':2801,'profits':3660,'unit':15442,'last_coeff':14,'difference':14,'numerator':14,'bernstein2':11,'qX0':22,'tail_query':14,'density':500,'pool':15}}.items():
 for f,n in expect.items():ck(obs[kind]['function_calls'][f]==n,'observed-source-function-'+kind+'-'+f+'-'+str(n))
u=reports['uniform'];r=reports['relay'];ck(obs['uniform']['final_original_values']['report']==u and obs['relay']['final_original_values']['out']==r,'whole-actual-final-report-versus-observed-original-frame')
ck(u['source_unit_customers']==r['customers']==53 and u['source_complete_histories']==r['nodes']==400 and r['comparisons']==2800 and r['minimum_unit_SPE_slack']=='0','actual-unit-full400-SPE-only-relay2800')
ck(len(obs['relay']['final_original_values']['slacks'])==2800 and len(obs['relay']['final_original_values']['uniform_slacks'])==399,'observed-real-2800-and399-not-inferred-from-status')
ck(u['P_child_complete_histories']==57 and u['P_child_prescribed_P_actions']==0 and len(u['complete_child_finite_replays'])==4,'uniform57-child-four-masses')
ck([a['mass'] for a in u['complete_child_finite_replays']]==['1','84796/85443','1/3','2/7'] and all(a['action_comparisons']==399 and a['minimum_slack']=='0' for a in u['complete_child_finite_replays']) and sum(a['action_comparisons'] for a in u['complete_child_finite_replays'])==1596,'exact-four-masses1596')
failed=u['other_root_children_failed_comparisons'];hist={tuple(a['history']) for a in failed};rootcounts=Counter(a['history'][0] for a in failed);slackcounts=Counter(a['profit_slack'] for a in failed);ck(len(failed)==36 and len(hist)==26 and all(len(a['history'])==3 and a['history'][0]!=6 and F(a['profit_slack'])<0 for a in failed),'lambda0-fulltree36negative26terminal-histories-not-SPE-certification')
ck([rootcounts[i] for i in range(7)]==[8,8,2,8,8,2,0] and slackcounts=={'-647/255035':24,'-1941/340478':8,'-715312201/86833806730':4},'complete36-root-distribution-and-three-slack-counts')
root=list(map(F,u['original_root_row_c0_slacks']));ck(root==[F(36675150748,3946991215),F(36675150748,3946991215),F(403646947494,43416903365),F(36675150748,3946991215),F(36675150748,3946991215),F(403646947494,43416903365),F()] and min(root[:6])>0,'separate-root-seven-preserved-does-not-preserve-other-children')
ck(r['actual']==[6,0,3,4] and r['deviation']==[6,2,3,4] and r['actual_payoffs']==['19','29/3','67/6','67/6'] and r['deviation_payoffs']==['19','29/3','35/3','35/3'],'true-same-original-branches-and-payoffs')
ck(r['buckets']=={'0':[0,12,11],'2':[1,12,8]} and r['critical_interval']=='2/11 < rho < 1','root-buckets-and-necessary-feasible-open-interval')
ck(u['noncore_actual_load_counts']=={'0':21,'1':6,'2':15,'3':11} and u['fresh_utilities']==['29/3','67/6','67/6'] and u['a_star']=='29/3' and u['S']=='331/48' and u['a_star_minus_S']=='133/48','same-source-spectral-parameters')
lam=F(u['lambda0']);t=F(u['true_original_v4']);D=F(u['original_low_tail_deficit']);repair=r['broader_uniform_repair'];ck(lam==F(84796,85443)==F(repair['lambda_value']) and t==F(r['security_value'])==F(28481,2924) and D==F(r['deficit'])==t-F(29,3)==F(647,8772),'same-lambda-true-static-t-and-deficit')
ck(u['matching_static_opponent_multisets']==r['static_backgrounds']==84 and u['source_sha256']=={k:v for k,v in r['sources'].items() if not k.endswith('security.json')},'same-two-dataSHA-distinct-third-input')
ck(u['c0_common_query_pool']==repair['global_customer_query_pool']=='206474219394865/3934509249981684' and u['c0_max_legal_query_credit']==repair['maximum_query_refund']=='187117307516351/4918136562477105' and F(u['c0_max_legal_query_credit'])<=F(u['c0_common_query_pool'])<D,'same-H0-sevenquerymax-distinct-below-D')
ck(repair['child_comparisons']==399 and repair['minimum_slack']=='0' and min(map(F,repair['tail_unit_densities']))==t and repair['tail_unit_densities']==['28481/2924','1908227/169592','1908227/169592'],'relay-exact-lambda0-tail-densities-399')
core0=1-lam
for a,b in zip(u['all_core_cases'],repair['core_repairs']):
 c=a['core_unit_customers'];ck(c==b['c'],'same-core-parameter-'+str(c));lo,hi=map(F,a['lambda_interval']);low,high=F(b['lambda_lower']),F(b['lambda_upper']);target=t+F(c,4)
 def density(w):return F(29,3)/w+F(c,1+3*w)
 def pool(w):return sum((n*(1/(1+k*w)-F(1,1+k)) for k,n in [(1,6),(2,15),(3,11)]),F())+F(c,1+3*w)-F(c,4)
 ck(lam<=lo<=low<=high<=hi<=1 and density(lo)>=target>=density(hi) and density(low)>=target>=density(high),'80-120-intervals-nested-same-root-c'+str(c))
 ck(hi-lo==(F() if c==0 else core0/2**80) and high-low==(F() if c==0 else core0/2**120),'c0-no-bisection-positive-c80-versus120-c'+str(c))
 ck(F(a['minimum_density_lower'])==density(hi) and a['rational_lower_endpoint_is_feasible_witness'] and density(lo)>=target,'field-minimum-density-lower-is-hi-lo-is-feasible-c'+str(c))
 ck(F(a['common_query_pool_upper'])==pool(lo)<D and F(b['H_upper'])==pool(low)<D and F(a['legal_query_credit_upper'])<=pool(lo),'both-conservative-pool-upper-below-D-c'+str(c))
 V=F(32)+3*lo*F(c,1+3*lo);ck(F(a['tail_profit_above_threshold_mass_at_rational_witness'])==V-target*3*lo>=3 and V-target*3*lo-3==3*lo*(density(lo)-target),'lo-budget-is-at-least3-exact-root-equality-only-c'+str(c))
ck([a['core_unit_customers'] for a in u['all_core_cases']]==[0,1,10,1000,1000000],'five-core-cases-only-four-positive-loops')
polys=r['last_gap_numerators_const_rho_rho2'];coefs=r['last_utility_coefficients_C_A_B'];bernst=0
for third,winner in [('3',4),('1',2)]:
 vals=[tuple(map(F,a)) for a in coefs[third]];ck(len(vals)==len(polys[third])==7,'all-seven-raw-last-utility-coefficients-'+third)
 for a in range(7):
  C,A,B=[x-y for x,y in zip(vals[winner],vals[a])];poly=(2*C+2*A+B,3*C+A+B,C);ck(poly==tuple(map(F,polys[third][a])),'exact-last-gap-numerator-'+third+'-'+str(a))
  if a==winner:ck(poly==(F(),F(),F()),'two-self-zero-polynomials-'+third)
  elif third=='1' and a==0:ck(poly==(F(-1),F(9,2),F(11,2)),'special-X0-factor-critical2over11-not-Bernstein0to1')
  else:
   c0,c1,c2=poly;bern=(c0,c0+c1/2,c0+c1+c2);ck(min(bern)>=0 and max(bern)>0,'eleven-unshifted-positive-Bernstein-'+third+'-'+str(a));bernst+=1
ck(bernst==11,'eleven-not-earlier-twelve-shifted-certificates')
for rho,key in [(F(),'rho=0'),(F(2,11),'rho=2/11'),(F(1),'rho=1')]:
 for third,name in [('3','after_P_X0_Y0'),('1','after_P_X0_X1')]:
  values=[F(C)+F(A)/(rho+1)+F(B)/(rho+2) for C,A,B in coefs[third]];actual=[a for a,v in enumerate(values) if v==max(values)];ck(actual==r['boundary_BR'][key][name],'complete-weak-BR-endpoint-'+key+'-'+third)
ck(r['boundary_BR']['rho=1']['after_P_X0_Y0']==[1,2,4,5] and r['boundary_BR']['rho=2/11']['after_P_X0_X1']==[0,2],'no-extending-unique-BR-to-endpoint-ties')
ck([a['rho'] for a in r['rho_checks']]==['1','9/10','3/4','1/2','2/11','1/10'],'six-positive-rho-formula-tests-not-all-waterfill-feasible')
for a in r['rho_checks']:
 rho=F(a['rho']);rd=2*(rho-1)/(rho*(rho+2));td=3*(rho-1)/((rho+1)*(rho+2));ck(F(a['root_unit_delta'])==rd and F(a['root_profit_delta'])==rho*rd and F(a['third_delta'])==td,'sample-formula-root-mass-third-'+a['rho'])
ck(F(r['query_refund_at_zero'])==F(35,12)>D and F(r['query_refund_at_2_over_11'])==F(309,140)>D,'zero-and-low-rho-query-credit-excluded-no-zero-times-infinity')
flip=r['whole_tree_flip'];ck(flip['history']==[0,0,6] and flip['prescribed']==1 and flip['deviation']==2 and {(a['root_load'],a['tail_load']):a['coefficient'] for a in flip['buckets']}=={(0,1):-1,(1,2):3} and F(flip['at_lambda0'])==3*lam/(1+2*lam)-1==F(-647,255035),'all-lambda-analytic-flip-same-packet-two-buckets')
h=u['heterogeneous_background_and_boundary_audit'];ck(h['decision_histories']==13 and h['finite_action_replays']==117 and h['core_initial_background']==[1,3] and 'not a legal' in h['scope'],'heterogeneous-frozen14clients117-not-general1662')
ck(F(h['threshold'])==F(298,45) and F(h['original_minimum'])==F(41,12) and F(h['spectrum'])==F(27,16) and F(h['common_query_pool'])==F(14,9),'heterogeneous-t-min-S-H')
ck(F(h['core_refund'])==F(28,45)-F(5,12)==F(37,180) and F(h['old_background_refund'])==F(1,9),'heterogeneous-core-and-old-refunds-distinct')
ck(F(h['original_tail_profit'])==F(41,4) and F(h['retained_tail_profit'])==F(149,15)==F(3,2)*F(298,45) and F(h['core_refund'])+F(h['old_background_refund'])+F(h['retained_tail_profit'])==F(h['original_tail_profit']),'heterogeneous-once-budget-exact')
ck(F(14,9)<=F(27,16)+F(37,180)==F(1363,720)<=F(298,45)-F(41,12)==F(577,180),'heterogeneous-spectrum-credit-chain')
ck(F(h['pure_core_zero_fresh_case']['threshold'])==F(28,45) and F(h['pure_core_zero_fresh_case']['common_pool'])==F(37,180) and F(5,12)<F(28,45)<F(4,3),'purecore-zero-fresh-interior-boundary-not-new-SPE-scan')
comp=j(E/'comparison-manifest.json');ck(len(comp['rows'])==5,'five-full-related-snapshots-three-prior-mature-two-repo')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-byte-hash-'+Path(a['path']).name)
rec=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids),'five-complete-primary-receipts')
ck(all(a['disposition']=='integrated' and a['publication_status']=='external stage only; no body-pushed/done inferred' for a in rec),'final-semantic-integrated-publication-ready-separate')
for a in rec:ck(a['source_sha256']==by[a['id']]['sha256'] and all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>100 and set(a['targets'])<=set(targets),'full-read-comparison-unique-decision-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==75 and len(j(W/'relation-review.json')['relations'])==9,'75-math9-semantic-relations')
n=j(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==22433 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'five-actual-next22433-local-only-not-remote-claim')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);roots=[root for root in [S,R,GI] if (root/rel).is_file()];ck(bool(roots),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel),'resolved_at':str(roots[0]),'previous_mature_package_only_if_not_yet_in_repo':not (S/rel).is_file() and not (R/rel).is_file()})
ck(len(stable)==len(set(stable))==3,'three-distinct-stable-formal-objects')
scope=j(E/'scope.json');ck(scope['uniform13247_original_entry_calls']==scope['relay11754_original_entry_calls']==1 and scope['original_source_functions_added_by_observer']==scope['GI8522_or_old_waterfill_VAR_tax_constructor_replays']==scope['network_or_shared_git_writes']==0 and scope['uniform_unit_full400_SPE_certification'] is False and scope['three_customer_free_threshold_example_reviewed_here'] is False and scope['general_n_review1662_run_here'] is False,'two-distinct-real-originals-each-one-no-other-entries-or-borrowed-scopes')
manifest=j(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-copy-whitelist');ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-staged-actual-C0-bytes-except-LF-TAB-CR')
ck(all(not any(line.rstrip(b' \t')!=line for line in (S/f).read_bytes().split(b'\n')) for f in manifest if f.endswith(('.py','.md','.json'))),'all-text-no-trailing-space-tab')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda z:(_ for _ in ()).throw(ValueError(z)))
ck(True,'strict-finite-JSON-all-staged')
v={'status':'pass','scope':'read-only raw/AST/observed finite reports and arithmetic/links/whitelist/actual C0; no original program calls','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':75,'human_relations':9,'uniform_original_entry_calls':1,'relay_original_entry_calls':1,'old_original_replays':0,'source_function_calls_in_selfcheck':0,'lambda0_negative_deviations':36,'lambda0_distinct_negative_terminal_histories':26,'relay_unshifted_Bernstein_checks':11,'uniform_other_heterogeneous_action_replays':117,'C0_scope':'all actual bytes excluding only LF/TAB/CR'};(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
