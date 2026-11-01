"""Evidence/manifest/contract validation only; does not run original or fixed-data checker."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,hashlib,json,re
S=Path(__file__).resolve().parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/pi-and-potential-diagnostics-primary';W=Path(__file__).resolve().parent
checks=[]
def ck(n,v):
 if not v:raise AssertionError(n)
 checks.append(n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def J(p):return json.loads(p.read_text(),parse_constant=lambda z:(_ for _ in ()).throw(ValueError(z)))
M=J(E/'source-manifest.json');T=J(W/'target-paths.json');D=J(E/'dependency-manifest.json');auth=J(W/'primary-authorization-check.json');claim=J(W/'claim-evidence.json')
ck('exact-five-primary',set(x['id']for x in M)=={'631acdc8cafa7861cec6','1bd769d92e6bcbdc563a','99b5fe51e039efd9f405','f690378df805d692ebb2','7778aef9866288463707'})
ck('five-source-bytes78133',sum(x['size']for x in M)==78133)
for x in M:
 p=E/'original'/x['path'];b=p.read_bytes();ck('primary-raw-sha1-SHA256-'+x['id'],len(b)==x['size']and sha(p)==x['sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('full-original24-claim-pushed-synced',claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced'and len(claim['ids'])==24)
ck('expected-five-intersection-not-projection',set(auth['expected_ids'])==set(x['id']for x in M)and set(auth['expected_actual_intersection'])==set(auth['expected_ids'])and set(auth['expected_ids'])<=set(claim['ids'])and auth['actual_claim_ids_count']==24)
ck('original-capture-byte-preserved',Path(auth['original_capture']).read_bytes()==(W/'claim-evidence.json').read_bytes()and sha(W/'claim-evidence.json')==auth['original_capture_sha256'])
ck('claim-tip5a8e',auth['remote_tip']==claim['remote_tip']==claim['local_sync']['remote_tip']=='5a8e6e6069abd3fcefd8086a69f5a27eb61da8e2')
ck('five-Boss4-owner-gate',len(auth['owners_at_primary_start'])==5 and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==next(y['sha256']for y in M if y['id']==x['id'])for x in auth['owners_at_primary_start']))
local=J(W/'local-source-cache-manifest.json');ck('five-real-local-cached-sources',len(local['rows'])==5 and all(x['group']=='submarkov_cv'for x in local['rows']))
for x in local['rows']:ck('local-cache-raw-'+x['id'],sha(Path(x['local_path']))==x['sha256'])
ck('no-previous-success-necessitated-original-runs',J(W/'pre-execution-same-sha-search.json')['matching_execution_records']==[])
ck('nine-true-dependencies35470',len(D)==9 and sum(x['size']for x in D)==35470)
for x in D:ck('true-dependency-'+x['id'],(S/x['copied_path']).stat().st_size==x['size']and sha(S/x['copied_path'])==x['sha256'])
for x in M:
 if x['path'].endswith('.py'):
  code=(E/'original'/x['path']).read_text();tree=ast.parse(code)
  ck('no-main-guard-'+x['id'],not any(isinstance(n,ast.If)and '__main__'in ast.unparse(n.test)for n in ast.walk(tree)))
  ck('original-write-text-side-effects-'+x['id'],'write_text'in code and 'argparse'not in code)
fixed=J(E/'replay/fixed-cone/execution.json');known=J(E/'replay/known-cases/execution.json');fx=J(E/'replay/fixed-cone/passive-observation.json');kn=J(E/'replay/known-cases/passive-observation.json');scope=J(E/'version-and-execution-scope.json');check=J(E/'stored-certificates-check.json')
for mode,state in [('fixed-cone',fixed),('known-cases',known)]:
 ck('original-once-success-'+mode,state['source_invocations']==1 and state['returncode']==0 and state['optimize']==0 and state['trace_extra_original_calls']==0)
 src=next(x for x in M if x['id']==state['source_id']);q=E/'replay'/mode/'source-root'/src['path']
 ck('unchanged-original-'+mode,q.stat().st_size==src['size']and sha(q)==src['sha256']==state['source_sha256'])
 ck('source-root-contract-'+mode,q.parent.parents[5]==E/'replay'/mode/'source-root'and state['cwd']==state['original_ROOT']==str(q.parent.parents[5]))
 ck('stderr-empty-'+mode,(E/'replay'/mode/'stderr.txt').stat().st_size==0)
 for x in state['true_file_dependencies']:
  ck('real-mirrored-input-'+mode+'-'+x['id'],sha(E/'replay'/mode/'source-root'/x['path'])==x['sha256'])
 for x in state['outputs']:ck('generated-output-bytes-'+mode+'-'+Path(x['path']).name,(E/x['path']).stat().st_size==x['bytes']and sha(E/x['path'])==x['sha256'])
ck('exact-two-original-entries',scope['original_invocations']=={'fixed_cone':1,'known_cases':1,'total':2}and scope['original_failures']==scope['original_retries']==0)
ck('fixed-only-one-strategy-file-input',len(fixed['true_file_dependencies'])==1 and fixed['true_file_dependencies'][0]['id']=='4617d18c9d098ce255c9'and fixed['imported_local_modules']==[])
ck('fixed-numeric-runtime-exactly-recorded',fixed['third_party_versions']=={'numpy':'2.3.5','scipy':'1.17.0'})
ck('known-actual-four-local-modules',len(known['true_file_dependencies'])==8 and len(known['imported_local_modules'])==4 and known['third_party_versions']=={})
for module in known['imported_local_modules']:ck('imported-module-SHA-'+module['module'],sha(Path(module['path']))==module['sha256'])
ck('fixed-all47-LPs-success',len(fx['LP_calls'])==47 and all(x['success']and x['status']==0 for x in fx['LP_calls']))
ck('fixed-full-43-ordered-node-keyset',set(map(tuple,fx['histories']))=={h for d in range(3)for h in product(range(6),repeat=d)})
ck('fixed-63-types-64-variable-271-row-matrix',len(fx['types'])==63 and len(fx['exact_root_equality'])==64 and fx['ic_count']==215 and len(fx['exact_constraint_rows'])==271 and all(len(row)==64 for row in fx['exact_constraint_rows']))
ck('all56-and126-static-counts',len(fx['all_r'])==56 and len(fx['all_r1'])==126)
source_report=next(x for x in M if x['id']=='99b5fe51e039efd9f405');old=J(E/'original'/source_report['path']);fixedreport=E/next(x['path']for x in fixed['outputs']if x['path'].endswith('pi_fixed_cone_diagnostic.json'))
ck('frozen57116-byte-reproduction',fixedreport.read_bytes()==(E/'original'/source_report['path']).read_bytes())
ck('actual47-of126-stop',old['candidate_r1_counts_total']==126 and old['candidate_r1_counts_tested']==47 and [list(x)for x in fx['all_r1'][:47]]==[x['q']for x in old['candidate_results']]==[x['q']for x in fx['LP_calls']])
ck('exact46-duals-last-positive-not-failure',len(old['exact_dual_certificates'])==46 and all(x['exact_nonpositive_dual_certificate']for x in old['candidate_results'][:-1])and old['candidate_results'][-1]['exact_nonpositive_dual_certificate']is False and old['all_tested_nonpositive_certified_exactly']is False)
ck('positive47-q-and-normalized-gap',old['numeric_best_q']==[0,1,1,0,1,1]and F(fx['last_exact_gap_normalized'])==F(33,182)and F(fx['last_exact_min_IC_slack'])==0)
ck('positive-root-normalization',sum(F(x)*F(y)for x,y in zip(fx['last_reconstructed_weights'],fx['exact_root_equality'][:-1]))==1 and min(map(F,fx['last_reconstructed_weights']))>=0)
candidate=fx['candidate_if_generated'];ck('generated430-unit-model',sum(x['multiplicity']for x in candidate['instance']['customers'])==430 and len(candidate['instance']['customers'])==17 and candidate['exact_root_payoff']=='91'and candidate['P_r']=='329'and candidate['P_r1']=='873/2'and candidate['delta_minus_root']=='33/2')
ck('generated-6437-not-an-input',scope['generated_PI6437']['byte_equal_prior']is True and scope['generated_PI6437']['not_actual_input_to_either_original']is True and sha(S/scope['generated_PI6437']['new_output_path'])==scope['generated_PI6437']['sha256']=='a1269d86beeb6d5aaacd530a501bec7afafb3e0a7c864f1b81073cac537fd944')
ck('exact-independent-matrix-rebuilt',check['matrix']['equals_passive_original_matrix']is True and check['matrix']['total_rows']==271 and check['matrix']['residual_coordinates_checked']==2944)
ck('46-old-certificate-carriers-checked',check['old_report']['exact_nonpositive_duals_checked']==46 and check['old_report']['zero_equality_multiplier_certificates']==7)
for i,x in enumerate(check['old_report']['dual_certificates']):ck('stored-exact-dual-'+str(i+1),x['q']==old['exact_dual_certificates'][i]['q']and F(x['equality_multiplier'])>=0 and F(x['minimum_residual'])==0 and x['residual_coordinates']==64)
ck('P1P2-27-profile-extra',check['primary_MD_extra_values']['P1']=='144'and check['primary_MD_extra_values']['P2']=='246'and check['primary_MD_extra_values']['arithmetic_profiles_checked']==27 and check['primary_MD_extra_values']['increments']==['144','102','83','215/2'])
ck('checker-had-zero-LP-original-calls',check['new_original_calls_in_this_checker']==check['new_LP_calls_in_this_checker']==0)
source_known=next(x for x in M if x['id']=='7778aef9866288463707');oldknown=J(E/'original'/source_known['path']);knownreport=E/known['outputs'][0]['path'];ck('frozen6338-byte-reproduction',knownreport.read_bytes()==(E/'original'/source_known['path']).read_bytes())
ck('known14-exact-threshold-returns',len(kn['threshold_returns'])==14 and len(oldknown)==14 and [x['floor']for x in kn['threshold_returns']]==[x['root_floor_all_SPE']for x in oldknown])
ck('known-verifier-certificate-unexecuted',kn['verify_certificate_calls']==kn['solver_certificate_calls']==0 and scope['known_cases']['counterexample_export_branch_executed']is False and not(knownreport.parent/'potential_increment_counterexample.json').exists())
ck('known-four-original-unit-sizes',sorted(set(x['customer_count']for x in kn['threshold_returns']))==[17,22,34,113])
ck('known14-nonnegative-onezero',all(F(x['margin'])>=0 for x in oldknown)and sum(F(x['margin'])==0 for x in oldknown)==1)
for i,x in enumerate(oldknown):ck('known-row-arithmetic-'+str(i+1),F(x['P_r1'])-F(x['P_r'])==F(x['delta'])and F(x['root_floor_all_SPE'])-F(x['delta'])==F(x['margin'])and x['remaining']==x['m']-sum(x['prefix'])and all(sum(q)==int(n)for n,q in x['maximizers'].items()))
ck('known-comps-domain2145',sum(__import__('math').comb(x['remaining']+len(x['prefix'])-1,len(x['prefix'])-1)+__import__('math').comb(x['remaining']+1+len(x['prefix'])-1,len(x['prefix'])-1)for x in oldknown)==2145)
ck('known-stdout14-JSON-lines',[json.loads(x)for x in(E/'replay/known-cases/stdout.txt').read_text().splitlines()]==oldknown and (E/'replay/known-cases/stdout.txt').stat().st_size==3489 and (E/'replay/known-cases/stdout.txt').read_bytes()!=knownreport.read_bytes())
log=(E/'replay/fixed-cone/stdout.txt').read_text();line,rest=log.split('\n',1);ck('fixed-stdout-candidate-and-summary',line.startswith('EXACT_PI_COUNTEREXAMPLE ')and json.loads(line.split(' ',1)[1])==candidate and json.loads(rest)=={k:v for k,v in old.items()if k not in ['candidate_results','exact_dual_certificates']}and len(log.encode())==3346)
for x in J(E/'comparison-manifest.json'):ck('comparison-byte-'+Path(x['path']).stem,sha(S/x['copied_path'])==x['sha256']and(S/x['copied_path']).stat().st_size==x['bytes'])
base=J(W/'replacement-base.json');ck('PI-update-base-SHA-safe',sha(R/base['path'])==base['base_sha256']=='bbcc756282df9f23d739fb2c97037f4964efa2ee5cccbce70cd14ad7918cc635')
body=(S/base['path']).read_text();ck('PI-preserves-strategy-tables-and-current-truth',all(x in body for x in ['五类','第二位','873/2','all-p WP严格成立','20个','half','P_1=144,P_2=246','49/2']))
ck('PI-updates-primary-and-history',all(x in body for x in ['首轮CI5','本次CV5正式认领','215个非self','重新运行该原程序0次'])and '它**不是本批五主源之一'not in body)
receipts=J(W/'semantic-receipts.json');ck('exact-five-integrated-receipts',len(receipts)==5 and set(x['id']for x in receipts)==set(x['id']for x in M))
for x in receipts:ck('full-semantic-receipt-'+x['id'],all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>40 for k in ['read_note','comparison_note','decision_note'])and all(p in T and(S/p).exists()for p in x['targets']))
ck('40-human-math-items',len(re.findall(r'^\d+\. ',(W/'mathematical-self-review.md').read_text(),re.M))==40)
ck('11-human-relations',len(J(W/'relation-review.json')['relations'])==11)
nexts=J(W/'next-candidates.json')['candidates'];ck('five-local-next-no-false-history',len(nexts)==5 and all(not x['availability_readonly']['progress_file_exists']and x['availability_readonly']['history_checked']is False for x in nexts))
links=[];ids=[]
for rel in T:
 p=S/rel;s=p.read_text();front=s.split('---',2)[1];ck('flat-MATEK-'+p.name,all(re.search(r'^'+k+r':',front,re.M)for k in ['id','kind','type_tag','title','status','summary','source_refs']));ids.append(re.search(r'^id: (.+)$',front,re.M).group(1));ck('no-source-template-placeholder-'+p.name,not any(x in s for x in ['SOURCE_','RESULT_TABLE','KNOWN_TABLE','INPUT_TABLE','.py_REPORT']))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
  if dest.startswith(('https:','http:','#','source:')):continue
  q=(p.parent/dest.split('#')[0]).resolve();r=q.relative_to(S);ck('formal-link-'+str(len(links)),q.exists()or(R/r).exists());links.append({'from':rel,'to':str(r)})
ck('three-distinct-stable-formal-IDs',len(ids)==len(set(ids))==3)
ck('algorithm-complete47-table',re.findall(r'^\|(\d+)\|',(S/T[0]).read_text(),re.M)==list(map(str,range(1,48))))
actual=sorted(str(p.relative_to(S))for p in S.rglob('*')if p.is_file());manifest=J(W/'copy-files.json');ck('manifest-exact-sorted-self-inclusive',manifest==actual and len(set(manifest))==len(manifest)and str((W/'copy-files.json').relative_to(S))in manifest)
ck('manifest-safe-relative-paths',all(not Path(x).is_absolute()and '..'not in Path(x).parts for x in manifest))
for p in S.rglob('*.json'):J(p)
ck('strict-finite-JSON-every-file',True)
result={'status':'pass','scope':'read-only final evidence/contract/version/links/manifest validation, no original or data-checker program execution','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'new_objects':2,'existing_object_replacement':1,'primary_receipts':5,'original_program_calls_in_batch':2,'original_program_calls_in_selfcheck':0,'data_checker_calls_in_batch':1,'data_checker_calls_in_selfcheck':0,'LP_calls_in_original_only':47,'known_threshold_calls':14,'known_solver_certificate_calls':0,'known_verify_certificate_calls':0,'human_math_items':40,'human_relations':11}
(W/'selfcheck.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','formal_links']},ensure_ascii=False))
