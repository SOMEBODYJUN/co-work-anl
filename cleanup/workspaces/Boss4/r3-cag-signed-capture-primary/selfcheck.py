"""Read-only evidence/contract validation; never runs original or arithmetic programs."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,copy,hashlib,json,re
S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/cag-signed-capture-primary'
W=Path(__file__).resolve().parent
checks=[]
def ck(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def J(p):return json.loads(p.read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
M=J(E/'source-manifest.json');T=J(W/'target-paths.json');receipts=J(W/'semantic-receipts.json')
ck('exact-five-primary-IDs',set(x['id']for x in M)=={'0965f4715c4dcd4ddd0f','82ce376f47bfd342d6bd','9dd03a30c822afa37b71','9cf5ddaabdb97f5530ee','73bc0f6d20fe90dbd39c'})
ck('five-primary-bytes34846',sum(x['size']for x in M)==34846)
for x in M:
 p=E/'original'/x['path'];ck('primary-raw-'+x['id'],p.stat().st_size==x['size']and sha(p)==x['sha256'])
ck('primary-manifest-equals-requested',M==J(W/'requested-sources.json'))
auth=J(W/'primary-authorization-check.json');claim=J(W/'claim-evidence.json')
ck('claim-pushed-Boss4-synced',claim['status']=='pushed'and claim['actor']=='Boss4'and claim['operation']=='claim'and claim['local_sync']['status']=='synced')
ck('original-full25-not-projected',len(claim['ids'])==25 and set(auth['expected_ids'])==set(x['id']for x in M)and set(auth['expected_ids']).issubset(set(claim['ids'])))
ck('full-original-capture-hash',sha(W/'claim-evidence.json')==auth['original_capture_sha256'])
ck('full-original-capture-bytes',Path(auth['original_capture']).read_bytes()==(W/'claim-evidence.json').read_bytes())
ck('claim-tip-identical',auth['remote_tip']==claim['remote_tip']==claim['local_sync']['remote_tip']=='9bff88d715e258bf152edf97073591b1652307e2')
ck('all-five-owner-gate',len(auth['source_owners_at_primary_start'])==5 and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==next(y['sha256']for y in M if y['id']==x['id'])for x in auth['source_owners_at_primary_start']))
ck('five-complete-semantic-receipts',len(receipts)==5 and set(x['id']for x in receipts)==set(x['id']for x in M))
for x in receipts:
 ck('semantic-receipt-'+x['id'],all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and all(len(x[k])>40 for k in ['read_note','comparison_note','decision_note'])and x['disposition']=='integrated'and all(t in T and (S/t).exists()for t in x['targets']))
ck('related-proof-not-sixth-primary','631acdc8cafa7861cec6'not in [x['id']for x in receipts])
code=(E/'original'/M[0]['path']).read_text();tree=ast.parse(code)
ck('original-no-main-guard',not any(isinstance(n,ast.If)and '__main__'in ast.unparse(n.test)for n in ast.walk(tree)))
ck('original-path-output-top-level-contract','ROOT=HERE.parents[5]'in code and "destination.open('x')"in code and 'destination.parent==HERE.resolve()'in code and code.index("read_case('individual_security_failure')")<code.index('parser=argparse.ArgumentParser()'))
imports={n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)}|{x.name for n in ast.walk(tree)if isinstance(n,ast.Import)for x in n.names}
ck('only-six-standard-library-imports',imports=={'collections','fractions','itertools','pathlib','json','argparse'})
state=J(E/'replay/execution-state.json');trace=J(E/'replay/original-input-guards-and-flow.json');docs=J(E/'replay/stdout-documents.json')
ck('one-original-run-exit0-assertions-on',state['original_program_calls']==state['execution_count']==1 and state['exit_code']==0 and state['optimize']==0)
ck('original-code-SHA-path-mirror',state['program_sha256']==M[0]['sha256']and sha(E/'replay/source-root'/M[0]['path'])==M[0]['sha256'])
ck('original-report-path-new-direct-HERE',state['argv'][-2:]==['--output','current-signed-capture-output.json']and Path(state['argv'][0]).parent/ state['argv'][-1] == E/'replay/source-root'/Path(M[0]['path']).parent/'current-signed-capture-output.json')
ck('original-standard-only',state['local_program_imports']==[]and state['third_party_libraries']==[])
D=J(E/'dependency-manifest.json');ck('four-true-inputs7851B',len(D)==4 and sum(x['size']for x in D)==7851 and set(x['path']for x in D)==set(state['external_file_inputs']))
for x in D:
 p=S/x['copied_path'];mirror=E/'replay/source-root'/x['path'];ck('true-dependency-'+x['id'],p.stat().st_size==x['size']and sha(p)==x['sha256']==sha(mirror))
ck('PI6437-not-this-program-input',not any('pi_fixed_cone' in x for x in state['external_file_inputs']))
for c in trace['cases']:
 hset={tuple(x['history'])for x in c['policy']};expected={h for d in range(c['m'])for h in product(range(c['q']),repeat=d)}
 ck('true-keyset-complete-'+c['name'],hset==expected and len(c['customer_likes'])==c['expanded_units'])
 ck('actual-IC-count-'+c['name'],len(hset)*c['q']==c['actual_original_IC_checks'])
ck('original34-86-expanded',[(x['expanded_units'],x['actual_original_IC_checks'])for x in trace['cases']]==[(34,258),(86,30)])
ck('exact-loop-counts',(trace['joint_checks'],trace['edge_checks'],trace['path_checks'])==(84,504,432))
ck('joint-domain-all84',len(trace['joint_cases'])==84 and {(x['lambda'],x['depth'],tuple(x['history']),x['action'])for x in trace['joint_cases']}=={(lam,d,h,a)for lam in ['1/2','3/4']for d in [0,1]for h in product(range(6),repeat=d)for a in range(6)})
t=F(trace['threshold_t']);ck('literal-threshold-not-new-LP',t==F(2411,246))
for j,c in enumerate(trace['joint_cases']):
 lam=F(c['lambda']);n=c['n'];gam=F(c['gamma']);db=F(c['delta_B']);v=F(c['V']);vn=F(c['V_new']);eta=F(c['eta']);fac=F(c['factor'])
 ck('recorded-joint84-arithmetic-'+str(j),vn-lam*n*t-gam==eta+n*(1-lam)*t-2*gam-db and eta==v-n*t and fac==n*(1-lam)/(1+n*lam)and 2*gam+db<=fac*(2*F(c['root_old'])+F(c['old_B'])))
ck('observed-PAY12-not-merely-present',state['conditional_PAY_assertion_hits']==trace['conditional_PAY_assertion_hits_count']==12 and len(trace['conditional_PAY_assertion_hits'])==12)
ck('PAY-only-depth0-domain',{(x['lambda'],tuple(x['history']),x['action'])for x in trace['conditional_PAY_assertion_hits']}=={(lam,(),a)for lam in ['1/2','3/4']for a in range(6)}and all(x['n']*F(x['lambda'])>=1 and F(x['d'])<=F(x['t'])and F(x['V'])>=x['n']*F(x['t'])for x in trace['conditional_PAY_assertion_hits']))
report=J(E/'replay/source-root'/Path(M[0]['path']).parent/'current-signed-capture-output.json');frozenold=next(x for x in M if x['id']=='82ce376f47bfd342d6bd');frozennew=next(x for x in M if x['id']=='9dd03a30c822afa37b71')
newpath=E/'replay/source-root'/Path(M[0]['path']).parent/'current-signed-capture-output.json'
ck('1739-new-report-byte-equality',newpath.stat().st_size==1739 and newpath.read_bytes()==(E/'original'/frozennew['path']).read_bytes()and sha(newpath)==state['report_sha256'])
ck('stdout1598-two-documents-not-report',(E/'replay/original.stdout.txt').stat().st_size==1598 and len(docs)==2 and state['stdout_json_document_count']==2 and (E/'replay/original.stdout.txt').read_bytes()!=newpath.read_bytes())
ck('stdout-documents-reconstruct',report=={**docs[0],'capture_flow':docs[1]}and state['stdout_documents_reconstruct_report'])
ck('stderr-empty',(E/'replay/original.stderr.txt').stat().st_size==0)
projection=copy.deepcopy(report);fields=['formal_marginal','owner_error_R','owner_error_I','scalarization_covariance','covariance_upper']
for row in projection['capture_flow']['states']:
 for k in fields:row.pop(k)
projection['capture_flow'].pop('high_weight_nonpositive_covariance_nodes')
ck('owner-fields-project-exact-old',projection==J(E/'original'/frozenold['path']))
ck('version-scope-old-not-run',J(E/'version-and-scope.json')['old_report_reexecuted']is False and J(E/'version-and-scope.json')['old_semantic_projection_equal']is True)
f=report['capture_flow'];ck('86-fixed-uncancelled-inventories',(f['W'],f['R'],f['G'],f['actual'],f['optimal'])==(44,42,41,[4,0],[1,3]))
ck('42-customers-each-absorbed1',len(trace['absorption_by_customer'])==42 and all(F(x['amount'])==1 for x in trace['absorption_by_customer'])and F(f['absorbed_total'])==42)
ck('three-positive-states-and-rows',len(f['states'])==3 and f['row_loads']==['35/38','49/44'])
ck('weighted-IC-tax-sign-and-cost',F(f['paid_cost'])==F(1701,38)==42+F(f['weighted_original_IC_slack'])and F(f['weighted_original_IC_slack'])==F(105,38)and F(f['paid_cost'])-44==F(29,38)>0)
ck('86-original-only-W-plus-G-test','assert cost<=len(C)+len(G)'in code and F(f['paid_cost'])<=f['W']+f['G'])
ck('two-high-nonpositive-and-low-equality',f['high_weight_nonpositive_covariance_nodes']==2 and [x['scalarization_covariance']for x in f['states']]==['0','35/44','0']and f['states'][1]['covariance_upper']=='35/44')
ck('passive-snapshot-original-output',trace['original_output_object']==report)
ck('no-Hall-gamma-NET-original-entry','maxflow'not in code and 'NET?'not in code and 'rho'not in code)
reuse=J(E/'reused-validation-manifest.json');ck('reuse-zero-new-old-program-calls',reuse['new_old_program_invocations']==0 and reuse['input_primary_id']=='73bc0f6d20fe90dbd39c'and len(reuse['files'])==7)
for x in reuse['files']:ck('reuse-byte-'+Path(x['copied_path']).name,(S/x['copied_path']).stat().st_size==x['bytes']and sha(S/x['copied_path'])==x['sha256'])
ex=J(E/'reused-pi-sanity-validation/execution.json');prev=J(E/'reused-pi-sanity-validation/execution-state.json');prior=prev['completed_original_report'];pirow=next(x for x in M if x['id']=='73bc0f6d20fe90dbd39c')
ck('successful-same-input-SHA-validation',ex['returncode']==0 and ex['source_invocations']==1 and ex['source_argv_suffix']==['--prefer-I']and ex['true_external_inputs'][0]['sha256']==reuse['input_sha256']==pirow['sha256'])
ck('reused-full-SPE-OPT-exact',prior['ordered_histories']==43 and prior['IC_comparisons']==258 and prior['OPT']==324 and prior['W']==265 and prior['actual_u']==['91','91','83'])
a=J(E/'pi-certificate-arithmetic.json');ck('separate-fixed-arithmetic-no-fullSPE-or-original-rerun',a['new_original_program_calls']==0 and a['new_full_SPE_checks']==0 and a['input_sha256']==pirow['sha256'])
ck('PI182-profile26bucket-domain',a['harmonic']['3']['multiset_profiles']==56 and a['harmonic']['4']['multiset_profiles']==126 and len(a['symmetry_buckets'])==26 and len([x for x in a['symmetry_buckets']if x['slots']==3])==9)
for r,total,best in [(3,56,'329'),(4,126,'873/2')]:ck('PI-complete-orbit-sum-'+str(r),sum(x['orbit_profiles']for x in a['symmetry_buckets']if x['slots']==r)==total and max(F(x['potential'])for x in a['symmetry_buckets']if x['slots']==r)==F(best))
ck('PI-next-increment-root-gap',F(a['harmonic']['4']['maximum_potential'])-F(a['harmonic']['3']['maximum_potential'])==F(a['next_increment'])==F(215,2)and F(a['next_increment'])-F(a['root_u'])==F(a['PI_gap'])==F(33,2))
ck('PI-all20-triples-and-unique-four',len(a['harmonic']['3']['maximizers_as_sorted_topics'])==20 and a['harmonic']['4']['maximizers_as_sorted_topics']==[[1,2,4,5]])
ck('PI-half-positive-margin',2*a['W']-a['OPT3']==206)
ck('PI-full-root-K36-WP-strict',len(a['full_root_K'])==6 and all(len(row)==6 for row in a['full_root_K'])and max(F(v)for row in a['full_root_K']for v in row)==90<91)
ck('PI-pure-background-upper-only',a['pure_background']==[0,0,3]and a['pure_background_query_values']==['41','315/4','315/4','51','315/4','315/4']and 'not a new scan' in a['pure_background_scope'])
ck('PI-necessary-arithmetic-code-no-source-import',all(w not in (E/'check-pi-certificate-arithmetic.py').read_text()for w in ['runpy.run_path','importlib','subprocess']))
for n in ['comparison-manifest.json','related-source-manifest.json']:
 for x in J(E/n):
  p=S/x['copied_path'];ck('comparison-related-raw-'+p.name,p.stat().st_size==x.get('bytes',x.get('size'))and sha(p)==x['sha256'])
ck('43-human-math-reviews',len(re.findall(r'^\d+\. ',(W/'mathematical-self-review.md').read_text(),re.M))==43)
ck('13-semantic-relations',len(J(W/'relation-review.json')['relations'])==13)
ck('five-real-next-candidates',len(J(W/'next-candidates.json')['candidates'])==5 and all(not x['availability_readonly']['progress_file_exists']and not x['availability_readonly']['all_ref_progress_path_history']for x in J(W/'next-candidates.json')['candidates']))
links=[];formal_ids=[]
for p in map(lambda t:S/t,T):
 s=p.read_text();front=s.split('---',2)[1]
 ck('MATEK-flat-fields-'+p.name,all(re.search(r'^'+k+r':',front,re.M)for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 formal_ids.append(re.search(r'^id: (.*)$',front,re.M).group(1))
 ck('no-placeholder-'+p.name,all(x not in s for x in ['SOURCE_MAIN','SOURCE_PI','SOURCE_CODE','POTENTIAL_TABLE','K_TABLE']))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
  if dest.startswith(('http:','https:','source:','#')):continue
  dest=dest.split('#')[0];target=(p.parent/dest).resolve();rel=target.relative_to(S)
  ck('formal-link-'+p.stem+'-'+str(len(links)),target.exists()or (R/rel).exists());links.append({'from':str(p.relative_to(S)),'to':str(rel)})
ck('three-unique-formal-IDs',len(set(formal_ids))==len(T)==3)
allfiles=sorted(str(p.relative_to(S))for p in S.rglob('*')if p.is_file());manifest=J(W/'copy-files.json')
ck('exact-sorted-white-list-including-itself',manifest==allfiles and len(manifest)==len(set(manifest))and str((W/'copy-files.json').relative_to(S))in manifest)
ck('all-white-list-paths-safe',all(not Path(x).is_absolute()and '..'not in Path(x).parts for x in manifest))
for p in S.rglob('*.json'):J(p)
ck('all-JSON-strict-finite-and-valid',True)
# Avoid claiming current mutable progress is itself part of frozen evidence; start owner records suffice.
result={'status':'pass','scope':'read-only raw/hash/contract/version/recorded-arithmetic/link/manifest checks; original and arithmetic program calls0 in selfcheck','checks_count':len(checks),'checks':checks,'formal_link_count':len(links),'formal_links':links,'formal_objects':len(T),'primary_receipts':len(receipts),'original_program_calls_in_this_batch':1,'original_program_calls_in_this_selfcheck':0,'new_full_SPE_scans_for_PI430_in_this_batch':0,'original_program_full_IC_cases34_86':2,'original_program_full_IC_checks34_86':288,'new_old_rankwise_calls':0,'fixed_PI_arithmetic_invocations_in_this_batch':1,'human_math_items':43,'reviewed_relations':13}
(W/'selfcheck.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','formal_links']},ensure_ascii=False))
