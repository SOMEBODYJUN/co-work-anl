"""Final read-only evidence/contract/link/manifest checks; executes no original or complement program."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,hashlib,json,re
S=Path(__file__).resolve().parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/mixed-pi-and-uniform-tree-tax-primary';W=Path(__file__).resolve().parent
checks=[]
def ck(n,v):
 if not v:raise AssertionError(n)
 checks.append(n)
def J(p):return json.loads(p.read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
M=J(E/'source-manifest.json');D=J(E/'dependency-manifest.json');T=J(W/'target-paths.json');auth=J(W/'primary-authorization-check.json');claim=J(W/'claim-evidence.json')
ck('exact-five-primary-versions',set(x['id']for x in M)=={'44d4846cdced71831d39','7a790f8a0eac4c54cd9a','606a70388180ef3ff633','fb207f64371ab9ed8442','722e666a191091b6fe33'})
ck('primary54824B',sum(x['size']for x in M)==54824)
for x in M:
 p=E/'original'/x['path'];b=p.read_bytes();ck('original-sha256-size-blob-'+x['id'],sha(p)==x['sha256']and len(b)==x['size']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('actual-five-claim-pushed-synced',len(claim['ids'])==5 and claim['status']=='pushed'and claim['actor']=='Boss4'and claim['local_sync']['status']=='synced')
ck('exact-gated-five-intersection',set(auth['expected_ids'])==set(auth['expected_actual_intersection'])==set(claim['ids'])==set(x['id']for x in M)and auth['actual_claim_ids_count']==5)
ck('actual-a81-tip',auth['remote_tip']==claim['remote_tip']==claim['local_sync']['remote_tip']=='a81c6ef91c1baaf279713e3698fdf52a0db460c9')
ck('full-claim-bytes-unmodified',Path(auth['original_capture']).read_bytes()==(W/'claim-evidence.json').read_bytes()and sha(W/'claim-evidence.json')==auth['original_capture_sha256'])
ck('all-five-Boss4-owner-gate',len(auth['owners_at_primary_start'])==5 and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==next(y['sha256']for y in M if y['id']==x['id'])for x in auth['owners_at_primary_start']))
local=J(W/'local-source-export-manifest.json');ck('safe-local-export-five-no-missing',len(local['rows'])==5 and local['missing']==[]and all(sha(Path(x['local_path']))==x['sha256']for x in local['rows']))
ck('preclaim-note-preserved-as-history',(W/'pre-claim-read-scope.md').exists()and not(W/'pre-read-scope.md').exists()and '当前不是等待claim'in(W/'STATUS.md').read_text())
ck('pre-execution-no-old-success',J(W/'pre-execution-same-sha-search.json')['matching_execution_records']==[])
ck('three-true-dependencies43752',len(D)==3 and sum(x['size']for x in D)==43752)
for x in D:ck('dependency-byte-'+x['id'],sha(S/x['copied_path'])==x['sha256']and(S/x['copied_path']).stat().st_size==x['size'])
related=J(E/'related-source-manifest.json');ck('two-unexecuted-related1935',len(related)==2 and sum(x['size']for x in related)==1935 and all(x['used_by']=='neither original'for x in related))
for x in related:ck('related-raw-'+x['id'],sha(S/x['copied_path'])==x['sha256']and(S/x['copied_path']).stat().st_size==x['size'])
for mode,sourceid in [('pi-review','44d4846cdced71831d39'),('tree-tax','fb207f64371ab9ed8442')]:
 state=J(E/'replay'/mode/'execution.json');src=next(x for x in M if x['id']==sourceid);code=(E/'original'/src['path']).read_text();asttree=ast.parse(code)
 ck('source-entry-guard-'+mode,any(isinstance(n,ast.If)and '__main__'in ast.unparse(n.test)for n in ast.walk(asttree))==(mode=='pi-review'))
 ck('entry-once-exit0-'+mode,state['source_invocations']==1 and state['returncode']==0 and state['optimize']==0 and state['extra_original_function_calls']==0)
 ck('unchanged-source-mirror-'+mode,sha(E/'replay'/mode/'source-root'/src['path'])==state['source_sha256']==src['sha256'])
 ck('only-standard-imports-'+mode,state['local_program_imports']==state['third_party_libraries']==[])
 for x in state['true_file_inputs']:ck('actual-mirrored-input-'+mode+'-'+x['id'],sha(E/'replay'/mode/'source-root'/x['path'])==x['sha256'])
 report=E/state['output_path'];frozen=E/'original'/next(x['path']for x in M if x['path'].endswith('/'+report.name))
 ck('new-report-frozen-byte-identical-'+mode,report.read_bytes()==frozen.read_bytes()and sha(report)==state['output_sha256']and report.stat().st_size==state['output_bytes'])
 ck('stderr-empty-'+mode,(E/'replay'/mode/'stderr.txt').stat().st_size==0)
pi=J(E/'replay/pi-review/passive-observation.json');ps=J(E/'replay/pi-review/execution.json');px=J(E/ps['output_path']);tax=J(E/'replay/tree-tax/passive-observation.json');ts=J(E/'replay/tree-tax/execution.json');tx=J(E/ts['output_path']);c=J(E/'root-complement-and-scope-check.json');scope=J(E/'version-and-execution-scope.json')
ck('PI-main-exactly-one',pi['main_calls']==1)
ck('PI-two-semantic-packet-fields-whole6437',pi['source_packet_subscript_fields']==['instance','strategy']and len(ps['true_file_inputs'])==1 and ps['true_file_inputs'][0]['id']=='73bc0f6d20fe90dbd39c'and next(x['size']for x in D if x['used_by']=='pi-review')==6437)
ck('PI-no-other-packet-access-static-AST',{n.slice.value for n in ast.walk(ast.parse((E/'original'/next(x['path']for x in M if x['id']=='44d4846cdced71831d39')).read_text()))if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='packet'and isinstance(n.slice,ast.Constant)}=={'instance','strategy'})
ck('PI-full43-histories',set(map(tuple,pi['histories']))=={h for d in range(3)for h in product(range(6),repeat=d)})
ck('PI258-unit-IC-gaps',len(pi['exact_IC_gaps'])==258 and min(map(F,pi['exact_IC_gaps']))==0 and pi['unit_customers']==430)
ck('PI-182-static-records',pi['table_sizes']=={'3':56,'4':126}and len(px['potential_tables']['3'])==56 and len(px['potential_tables']['4'])==126)
for slots in ['3','4']:
 rows=px['potential_tables'][slots];ck('complete-unique-profile-list-'+slots,len({tuple(x['counts'])for x in rows})==len(rows)and all(sum(x['counts'])==int(slots)for x in rows))
 ck('correct-potential-max-and-maximizers-'+slots,max(F(x['potential'])for x in rows)==F(px['P'+slots])and[x['counts']for x in rows if F(x['potential'])==F(px['P'+slots])]==px['P'+slots+'_maximizers'])
ck('PI-positive33over2-and-half206',F(px['P4'])-F(px['P3'])-F(px['actual_payoffs'][0])==F(33,2)and px['half_slack']==206 and px['actual_welfare']==265 and px['optimum_3']==324)
ck('PI-root6-all91-and-Pr3',len(px['root_branches'])==6 and all(x['root_payoff']=='91'and x['potential']=='329'for x in px['root_branches']))
ck('PI-K36-max90-and-actual-column80',len(px['complete_root_insertion_matrix'])==6 and all(len(row)==6 for row in px['complete_root_insertion_matrix'])and max(F(v)for row in px['complete_root_insertion_matrix']for v in row)==90 and max(map(F,px['actual_terminal_extra_query_caps']))==80)
ck('PI-36550-complete-vs-4132-summary',ps['output_bytes']==36550 and ps['stdout_bytes']==4132 and ps['stdout_equals_output_bytes']is False and (E/'replay/pi-review/stdout.txt').read_bytes()==(json.dumps({k:v for k,v in px.items()if k!='potential_tables'},ensure_ascii=False,indent=2)+'\n').encode())
ck('PI-passive-report-object-identical',pi['main_original_report']==px)
ck('PI-original-no-repeat-arithmetic',c['pi_original_scope']['static_profile_rows']==182 and len(c['pi_original_scope']['coverage_potential_orbits'])==26)
for n,total in [(3,56),(4,126)]:ck('PI-orbit-count-'+str(n),sum(x['profiles']for x in c['pi_original_scope']['coverage_potential_orbits']if x['slots']==n)==total)
ck('original-tax-two-inputs53-and400',len(ts['true_file_inputs'])==2 and {x['id']for x in ts['true_file_inputs']}=={'0ebc828733fab492d2a5','2cd505cd05ed8ab77f21'}and tax['base_unit_count']==53)
ck('original-tax-empty-root-zero',tax['empty_root_IC_assertions_executed']==scope['tax_input']['empty_root_IC_in_original']==0)
ck('original-tax-six-parameter-rows',len(tx['rows'])==6 and {(x['core'],x['lambda'])for x in tx['rows']}=={(core,lam)for core in [0,7]for lam in ['1/2','3/4','84796/85443']})
ck('original-tax399-nonempty2793-per-row',all(x['tail_decision_histories']==399 and x['deviations_including_self']==2793 and x['fixed_first_action_subgames']==7 for x in tx['rows'])and sum(x['deviations_including_self']for x in tx['rows'])==16758)
ck('original-tax-exact-passive-unique-event-counts',tax['raw_observed_line_events']=={'nodes':2394,'paths':2394,'root_leaves':42}and len(tax['unique_node_records'])==len(tax['unique_prescribed_path_records'])==2394 and len(tax['forced_root_leaves'])==42)
ck('original-tax-output-object-identical',tax['source_original_report']==tx)
ck('2075B-tax-stdout-full-byte-identical',ts['output_bytes']==ts['stdout_bytes']==2075 and ts['stdout_equals_output_bytes']is True and (E/'replay/tree-tax/stdout.txt').read_bytes()==(E/ts['output_path']).read_bytes())
ck('recorded-tax-all-node-and-path-domains',len({(x['core'],x['lambda'],tuple(x['history']))for x in tax['unique_node_records']})==2394 and all(1<=len(x['history'])<=3 and x['history'][0]in range(7)for x in tax['unique_node_records']))
for row in c['tax_original_scope']['parameter_rows']:
 old=next(x for x in tx['rows']if x['core']==row['core']and x['lambda']==row['lambda']);ck('min-max-source-contract-'+str(row['core'])+'-'+row['lambda'],row['max_local_regret']==old['maximum_local_regret']and row['max_refund_minus_path_regret']==old['maximum_refund_minus_prescribed_path_regret']and F(row['min_noncore_future_tax_minus_path_regret'])==0 and F(row['min_refund_minus_path_regret'])>=0 and row['original_tail_nodes']==399)
ck('core0-min0-separate-from-max',all(F(x['min_refund_minus_path_regret'])==0 for x in c['tax_original_scope']['parameter_rows']if x['core']==0))
for core in c['core_credit_check']:
 k=F(7)*(1-F(core['lambda']))/(4*(1+3*F(core['lambda'])));ck('core-shift-checked-'+core['lambda'],F(core['tail_core_tax_per_role'])==k and F(core['full_refund_increase'])==3*k and core['regret_vectors_identical_at_all399_nodes']and core['source_count_of_nonzero_core_scenario_nodes']==399)
root=c['root_complement'];ck('separate-data-root7-not-original',root['comparison_count_including_self']==7 and root['new_full_tree_scan']is False and root['was_not_checked_by_original_tax_entry']is True and root['source_complete_key_count']==400)
ck('root-unit-19-versus-six29over3',root['root_action']==6 and root['root_payoffs']==['29/3']*6+['19']and all(F(v)>=0 for v in root['root_IC_gaps']))
ck('actual53-and60-coverage-witness',root['actual']==[6,0,3,4]and root['actual_unit_payoffs']==['19','29/3','67/6','67/6']and root['actual_W53']==51 and root['OPT53']==53 and root['OPT53_coverage_witness']==[2,4,5,6]and root['actual_W60']==58 and root['OPT60']==60)
ck('extra-data-only-zero-original-LP-oracle',c['new_original_calls']==c['new_LP_calls']==c['new_solver_calls']==0 and scope['additional_data_check']['calls']==1 and root['constructor_not_executed']is True)
ck('lambda-provenance-only-not-static-certification',c['endogenous_lambda_provenance']['static_security_optimality_not_reverified']is True and c['endogenous_lambda_provenance']['security_file_not_read_by_original_tax']is True and F(29,3)/F(c['endogenous_lambda_provenance']['reported_static_t'])==F(84796,85443))
ck('two-original-entries-no-failures',scope['original_entry_calls']=={'pi_review':1,'tree_tax':1,'total':2}and scope['original_failures']==scope['original_retries']==0)
for x in J(E/'comparison-manifest.json'):ck('comparison-raw-'+Path(x['path']).stem,sha(S/x['copied_path'])==x['sha256']and(S/x['copied_path']).stat().st_size==x['bytes'])
r=J(W/'semantic-receipts.json');ck('five-primary-semantic-receipts',len(r)==5 and set(x['id']for x in r)==set(x['id']for x in M))
for x in r:ck('complete-receipt-'+x['id'],all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>40 for k in ['read_note','comparison_note','decision_note'])and all(t in T and(S/t).exists()for t in x['targets']))
ck('44-manual-math-checks',len(re.findall(r'^\d+\. ',(W/'mathematical-self-review.md').read_text(),re.M))==44)
ck('11-reviewed-relations',len(J(W/'relation-review.json')['relations'])==11)
n=J(W/'next-candidates.json')['candidates'];ck('five-actual-local-next-no-false-history',len(n)==5 and all(x['availability_readonly']['progress_file_exists']is False and x['availability_readonly']['history_checked']is False for x in n))
links=[];ids=[]
for rel in T:
 p=S/rel;s=p.read_text();front=s.split('---',2)[1];ck('MATEK-flat-'+p.name,all(re.search(r'^'+k+r':',front,re.M)for k in ['id','kind','type_tag','title','status','summary','source_refs']));ids.append(re.search(r'^id: (.+)$',front,re.M).group(1));ck('no-template-left-'+p.name,not any(x in s for x in ['SOURCE_','BUCKET_TABLE','TAX_ROWS']))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
  if dest.startswith(('http:','https:','#','source:')):continue
  q=(p.parent/dest.split('#')[0]).resolve();rr=q.relative_to(S);ck('formal-link-'+str(len(links)),q.exists()or(R/rr).exists());links.append({'from':rel,'to':str(rr)})
ck('three-unique-stable-objects',len(T)==len(set(ids))==3)
actual=sorted(str(p.relative_to(S))for p in S.rglob('*')if p.is_file());manifest=J(W/'copy-files.json');ck('exact-whitelist-sorted-self-inclusive',manifest==actual and len(manifest)==len(set(manifest))and str((W/'copy-files.json').relative_to(S))in manifest)
ck('safe-relative-manifest-paths',all(not Path(x).is_absolute()and '..'not in Path(x).parts for x in manifest))
for p in S.rglob('*.json'):J(p)
ck('strict-finite-JSON-everywhere',True)
out={'status':'pass','scope':'read-only full bytes/contracts/observed-summary/links/whitelist; no original or complement program execution','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'original_entry_calls_in_batch':2,'original_entry_calls_in_selfcheck':0,'additional_data_check_calls_in_batch':1,'additional_data_check_calls_in_selfcheck':0,'empty_root_comparisons_in_original_tax':0,'additional_root_comparisons':7,'original_PI_IC_comparisons':258,'original_PI_static_rows':182,'original_tax_six_parameter_tail_comparisons':16758,'human_math_items':44,'human_relations':11}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['checks','formal_links']},ensure_ascii=False))
