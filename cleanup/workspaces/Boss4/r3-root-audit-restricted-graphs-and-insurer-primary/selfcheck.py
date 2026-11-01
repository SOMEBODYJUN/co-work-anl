#!/usr/bin/env python3
"""Read-only raw/AST/observed reports/calls/finite scalar and input reconstruction/links/C0.
Never imports canonical/original code or performs a new SPE/OPT scan.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb,isfinite
import json,hashlib,re,ast
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');GZ=R.parent/'boss4-next-cache/r3-legal-hub-and-private-root-boundary-primary';E=S/'archives/customer-attraction/tools/evidence/root-audit-restricted-graphs-and-insurer-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['ac4741967772eab01138','464a4071ed64844f3709','bd6f652e751100092fec','0e6368273fd36eb86b5a','8c3c0850f65a2812d079'];sm=j(E/'source-manifest.json');by={a['id']:a for a in sm['rows']};ck(sm['source_count']==5 and sm['source_bytes']==40285 and set(by)==set(ids),'five-full-primary40285')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+id);ck(all(x['path']==a['source_path'] for x in a['sources']),'full-frozen-source-path-'+id)
cap=j(W/'claim-evidence.json');gate=j(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced' and cap['remote_tip']==gate['remote_tip']=='f2c7edbda53bae2b977de6042aa4f4cbf598742c','actual-pushed-synced-f2c7ed')
ck(len(cap['ids'])==gate['actual_claim_count']==30 and set(ids)<=set(cap['ids']) and set(gate['actual_intersection'])==set(ids) and gate['status']=='pass','five-actual-subset-of-whole30')
ck((W/'claim-evidence.json').read_bytes()==(R.parent/'boss4-r3-next-hi-claim.json').read_bytes() and sha(W/'claim-evidence.json')==gate['capture_sha256'],'full-original30-capture-unchanged')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'current-owner-sourceSHA-'+a['id'])
ck(j(W/'pre-execution-search.json')['successful_same_sha_execution_records']==[] and j(W/'pre-execution-search.json')['GZ_original_root_entry_calls']==0,'no-old-exact-source-success-GZ-context-not-run')
d=j(E/'dependency-manifest.json');deps={a['source_path']:a for a in d['rows']};ck(len(deps)==6 and sum(a['size'] for a in deps.values())==62790,'six-real-dependencies62790')
for a in deps.values():
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'dependency-raw-'+a['id'])
ck(d['root6714']['file_data_bytes']==37315 and d['graph2920']['package_bytes']==25475 and d['graph2920']['external_data_files']==0 and d['graph2920']['certificate_and_verifier_imported_but_not_called'],'distinct-data-and-import-closures')
rs={};ob={};rep={};expected={'root':(ids[0],ids[1],2,37315,772),'graph':(ids[2],ids[3],4,25475,7212)}
for kind,(codeid,outid,num,total,std) in expected.items():
 code=S/by[codeid]['path'];tree=ast.parse(code.read_text());ck(any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tree.body),'actual-main-guard-'+kind)
 imports=[a.module for a in ast.walk(tree) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tree) if isinstance(a,ast.Import) for n in a.names]
 if kind=='root':ck(set(imports)<={'fractions','functools','itertools','pathlib','hashlib','json'} and 'fractions' in imports,'root-stdlib-no-canonical-import')
 else:ck('customer_attraction' in imports and 'sys' in imports,'graph-real-canonical-import-not-independent-verifier')
 run=j(E/('replay-'+kind)/'execution.json');obs=j(E/('replay-'+kind)/'passive-observation.json');rs[kind]=run;ob[kind]=obs;ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'one-original-success-assertions-on-'+kind)
 ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==run['source_sha256']==by[codeid]['sha256'],'original-source-bytes-and-relocated-path-'+kind)
 ck(len(run['runtime_dependencies'])==num and sum(a['size'] for a in run['runtime_dependencies'])==total and run['dependency_bytes_unchanged'],'actual-runtime-closure-countbytes-'+kind)
 for a in run['runtime_dependencies']:ck((S/a['runtime_path']).stat().st_size==a['size'] and sha(S/a['runtime_path'])==a['sha256']==deps[a['source_path']]['sha256'],'runtime-dependency-hash-'+kind+'-'+Path(a['source_path']).name)
 ck(run['external_file_data_inputs']==(2 if kind=='root' else 0) and run['imported_custom_package_files']==(0 if kind=='root' else 4),'data-inputs-versus-imported-code-'+kind)
 out=S/run['output']['path'];ck(out.stat().st_size==run['output']['size']==by[outid]['size'] and sha(out)==run['output']['sha256'] and run['output']['frozen_sha256']==by[outid]['sha256'],'new-report-sizehash-and-frozenidentity-'+kind);rep[kind]=j(out)
 ck(run['stdout_bytes']==(E/('replay-'+kind)/'stdout.txt').stat().st_size==std and run['stderr_bytes']==(E/('replay-'+kind)/'stderr.txt').stat().st_size==0,'stdout-stderr-real-'+kind)
 ck(obs['source_main_calls']==obs['source_module_calls']==1 and obs['observer_extra_original_calls']==run['observer_extra_original_calls']==run['other_original_entries']==run['padded_insurer_audit_or_blind_audit_entries']==run['network_or_shared_repo_writes']==0,'module-main-one-no-observer-or-other-entries-'+kind)
 writes=[a for a in obs['observed_local_opens'] if a['mode']=='x'];ck(len(writes)==1 and Path(writes[0]['path'])==out.resolve(),'one-exclusive-output-write-'+kind)
root=rep['root'];graph=rep['graph'];oldgraph=j(S/by[ids[3]]['path']);oldroot=S/by[ids[1]]['path'];ck(rs['root']['output']['frozen_byte_equal'] and (S/rs['root']['output']['path']).read_bytes()==oldroot.read_bytes() and rs['root']['output']['json_differences']==[],'root4803-whole-frozen-byteequal')
ck(sha(S/rs['root']['output']['path'])=='7ee08d927069d3a97dc3aefe30c50513a805a22d761291e80455bc2f209f2c4a' and ob['root']['final_original_values']['report']==root,'actual-root-report-and-source-final-frame')
for name,num in {'finish':2800,'payoff':3227,'coverage':218,'mask':12}.items():ck(ob['root']['function_calls']['entry:'+name]==num,'actual-root-function-'+name+'-'+str(num))
ck(ob['root']['loaded_package_module_paths']=={} and ob['root']['final_original_values']['count']==2793 and ob['root']['final_original_values']['type_checks']==105,'root-no-canonical-import-actual2793and105')
ck(root['source_unit_customers']==53 and root['original_interest_types']==14 and root['positive_depth_complete_histories']==399 and root['positive_depth_action_comparisons']==399*7==2793 and root['targeted_typewise_root_checks_including_added_core_type']==105 and root['optimal_multisets_checked_at_source_point']==comb(10,4)==210,'root53-fixed-sample-scope')
ck(root['source_hashes']=={Path(a['source_path']).name:a['sha256'] for a in rs['root']['runtime_dependencies']},'root-source-data-hashes-actual')
ck(root['fixed_optimal_support_covers_all_allowed_interest_types']==[0,2,5,6] and len(root['root_plans'])==7,'root-fixed-support-and-seven-records')
values=[F(a['actual_payoffs'][0]) for a in root['root_plans']];ck(values==[F(29,3)]*6+[F(19)],'root-true-values-six29over3-plus19')
for a in root['root_plans']:
 i=a['root'];us=list(map(F,a['actual_payoffs']));Wpoint=a['welfare'];D=53-Wpoint;delta=max(values)-us[0];margin=53-2*Wpoint-3*delta;ck(sum(us)==Wpoint and a['optimal_coverage']==53 and a['private_omissions']==D,'root-point-share-coverage-row'+str(i))
 ck(F(a['root_regret'])==delta and F(a['OPT_minus_2W_minus_3regret'])==margin and F(a['last_two_real_profit_budget'])==us[2]+us[3] and F(a['first_two_profit_saving'])==us[0]+us[1],'root-point-Delta-margin-and-profit-budgets-row'+str(i))
 ck(D<=us[2]+us[3] and 53<=2*Wpoint-us[0]-us[1] and margin<=-us[0]-us[1]-3*delta,'root-private-bound-specialization-not-general-cone-row'+str(i))
ck([a['welfare'] for a in root['root_plans']]==[51,51,52,51,51,52,51] and [a['OPT_minus_2W_minus_3regret'] for a in root['root_plans']]==['-77','-77','-79','-77','-77','-79','-49'],'all-seven-root-W-and-margins')
ck('conditional on' in root['all_multiplicity_scope'] and 'not claimed feasible SPE' in root['all_multiplicity_scope'],'source-reported-all-multiplicities-is-conditional-type-basis-not-feasibility')
# Exact math-data comparison discards only the independently preserved elapsed field.
def without_times(g):return {**g,'reports':[{k:v for k,v in a.items() if k!='elapsed_seconds'} for a in g['reports']]}
ck(rs['graph']['output']['frozen_byte_equal'] is False and rs['graph']['output']['math_fields_equal_ignoring_only_per_case_elapsed_seconds'] and without_times(graph)==without_times(oldgraph),'graph-only-timing-math-normalization-complete-equality')
diff=rs['graph']['output']['json_differences'];ck(len(diff)==18 and {a['json_pointer'] for a in diff}=={'/reports/'+str(i)+'/elapsed_seconds' for i in range(18)},'exact18-actual-timing-fields-differ-no-other-fields')
for a in diff:
 idx=int(a['json_pointer'].split('/')[2]);ck(a['frozen']==oldgraph['reports'][idx]['elapsed_seconds'] and a['new']==graph['reports'][idx]['elapsed_seconds'] and isfinite(a['new']) and a['new']>=0,'actual-not-zeroed-timing-preserved-case'+str(idx))
ck(sha(S/rs['graph']['output']['path'])=='7586473b307d1d950d41e88d5b7ee8550d9a819c091aad8c302f3ef0f6bc4299','actual-new18240-graphSHA-not-frozen')
ck(ob['graph']['final_original_values']['reports']==graph['reports'] and len(graph['reports'])==18,'all18-actual-original-frame-reports')
stdout=[json.loads(a) for a in (E/'replay-graph/stdout.txt').read_text().splitlines()];ck(stdout==graph['reports'],'18-stdout-rows-equal-actual-new-report-including-times')
mods=ob['graph']['loaded_package_module_paths'];ck(set(mods)=={'customer_attraction','customer_attraction.model','customer_attraction.exact','customer_attraction.certificate'},'four-real-loaded-package-modules')
base=(S/rs['graph']['runtime_entry']).parents[6]
for module,file in [('customer_attraction','__init__.py'),('customer_attraction.model','model.py'),('customer_attraction.exact','exact.py'),('customer_attraction.certificate','certificate.py')]:ck(Path(mods[module])==base/'customer_attraction'/file,'module-actually-loaded-relocated-frozen-'+file)
calls=ob['graph']['function_calls'];ck(calls['entry:instance']==calls['customer_attraction/exact.py:__init__']==calls['customer_attraction/exact.py:outcomes']==calls['customer_attraction/exact.py:stats']==calls['customer_attraction/model.py:optimal_welfare']==18,'exact18-real-instance-solver-outcomes-stats-OPT-calls')
for f in ['certificate','worst_certificate','ordered_outcomes']:ck(calls.get('customer_attraction/exact.py:'+f,0)==0,'unused-canonical-function-zero-'+f)
ck(calls.get('customer_attraction/certificate.py:verify_certificate',0)==0 and calls.get('customer_attraction/certificate.py:__post_init__',0)==0,'import-certificate-class-suite-not-verification-or-certificate-construction')
case_order=[(kind,k,p) for kind in ['cycle','band'] for k in [3,4,5] for p in ['uniform','bank4','staircase']];ck([(a['kind'],a['k'],a['pattern']) for a in graph['reports']]==case_order,'eighteen-fixed-case-order-no-new-sweep')
roots=states=terminal=retained=0;ratios=[];solve_expected=18
for idx,a in enumerate(graph['reports']):
 k=a['k'];kind=a['kind'];pattern=a['pattern'];edges=[(i,k+z) for i in range(k) for z in (i,(i+1)%k)] if kind=='cycle' else [(i,k+z) for i in range(k) for z in range(k) if abs(i-z)<=1];weights=[1]*(2*k) if pattern=='uniform' else [1]*k+[4]*k if pattern=='bank4' else [1<<(i%3) for i in range(k)]+[1<<((i+1)%3) for i in range(k)];q=len(edges);cnt=a['worst_counts'];ck(a['edges']==[list(e) for e in edges] and a['resource_weights']==weights and a['players']==k and a['topics']==q==(2*k if kind=='cycle' else 3*k-2),'case-exact-legal-edges-weights-model-'+str(idx))
 ck(len(cnt)==q and all(type(x) is int and x>=0 for x in cnt) and sum(cnt)==k,'case-valid-returned-terminal-count-'+str(idx))
 covered={v for count,e in zip(cnt,edges) if count for v in e};welfare=sum(weights[v] for v in covered);ck(a['welfare']==welfare and all((i,k+i) in edges for i in range(k)) and a['optimum']==sum(weights) and F(a['ratio'])==F(sum(weights),welfare),'case-coverage-and-fixed-diagonal-OPT-identity-not-new-solver-'+str(idx))
 cstates=comb(q+k,k);tstates=comb(q+k-1,k);ck(a['count_states']==cstates and 0<a['full_spe_terminal_counts']<=tstates and a['retained_outcomes']>=cstates,'case-state-statistics-not-ordered-history-count-'+str(idx));roots+=a['full_spe_terminal_counts'];states+=cstates;terminal+=tstates;retained+=a['retained_outcomes'];solve_expected+=q*(cstates-tstates);ratios.append(F(a['ratio']))
ck(roots==307 and states==39813 and terminal==28125 and calls['entry:<lambda>']==roots and calls['customer_attraction/model.py:topic_payoffs']==terminal,'307-root-counts39813-states28125-terminal-payoffs-calls')
ck(solve_expected==calls['customer_attraction/exact.py:_solve']==136668 and solve_expected>states,'actual136668-solve-calls-include-cache-hits-not-new-states')
ck(max(ratios)==F(17,12) and [(a['kind'],a['k'],a['pattern']) for a,v in zip(graph['reports'],ratios) if v==max(ratios)]==[('cycle',4,'staircase')],'finite17over12-only-cycle4staircase-not-general-half')
cm=j(E/'context-manifest.json');ck(len(cm['rows'])==6 and cm['context_only_not_additional_primary_done'] and cm['insurer_audit_entry_calls_here']==cm['blind_audit_entry_calls_here']==0 and cm['blind_scope_excludes_sunflower_dilution_sharpness'] and cm['later_sharpness_review_read_full'],'six-full-context-not-primarydone-firstblind-excludes-latersharp')
for a in cm['rows']:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'all-context-raw-sizeSHAblob-'+a['id'])
# Scalar identities supplement the full human proof, not a new insurer audit.
for m in [2,3,6]:
 s=F(3,2);C=(2*m-1)*s;WH=(m+1)*s;O=C;high=2*s;low=s;ck(2*WH-O==3*s==3*(high-low) and C>=(m+1)*s and C-(m+1)*s==(m-2)*s,'three-distinct-insurer-costs-and-equality-scalar-m'+str(m))
comp=j(E/'comparison-manifest.json');ck(len(comp['rows'])==4,'four-full-related-canonical-or-mature-comparisons')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'formal-comparison-bytehash-'+Path(a['path']).name)
rec=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids) and all(a['disposition']=='integrated' for a in rec),'five-final-semantic-integrated-receipts')
for a in rec:ck(a['source_sha256']==by[a['id']]['sha256'] and all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>=100 and set(a['targets'])<=set(targets) and a['publication_status'].startswith('external stage only'),'complete-read-related-unique-decision-publication-separate-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==81 and len(j(W/'relation-review.json')['relations'])==9,'81-human-math9-semantic-relations')
n=j(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==34889 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'HQ-next-five34889-only-local-availability')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);roots_ok=[x for x in [S,R,GZ] if (x/rel).is_file()];ck(bool(roots_ok),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel),'resolved_at':str(roots_ok[0]),'mature-only-no-publication-inferred':not (S/rel).is_file() and not (R/rel).is_file()})
ck(len(stable)==len(set(stable))==3,'three-distinct-stable-mathematical-objects')
scope=j(E/'scope.json');ck(scope['root6714_original_entry_calls']==scope['graph2920_original_entry_calls']==1 and scope['graph_actual_json_timing_differences']==18 and scope['graph_frozen_bytes_equal'] is False and scope['root_frozen_bytes_equal'] and scope['padded_or_blind_or_sharp_audit_entry_calls']==scope['old_original_replays']==scope['source_functions_added_by_observer']==scope['network_or_shared_git_writes']==0 and scope['original_blind_review_excluded_sharpness'] and scope['later_sharpness_context_read_full'] and scope['sharpness_common_core_is_all_legal_topics_intersection'],'actual-two-distinct-originals-and-exact-sharp-review-scope')
manifest=j(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist');ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-actual-staged-C0-bytes-except-LF-TAB-CR')
ck(all(not any(line.rstrip(b' \t')!=line for line in (S/f).read_bytes().split(b'\n')) for f in manifest if f.endswith(('.py','.md','.json'))),'all-text-no-trailing-space-tab')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda z:(_ for _ in ()).throw(ValueError(z)))
ck(True,'strict-finite-JSON-all-staged')
v={'status':'pass','scope':'read-only raw/AST/observed root and graph certificates/scalar-input reconstruction/links/C0; no original or canonical code imported/executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':81,'human_relations':9,'root_original_entry_calls':1,'graph_original_entry_calls':1,'padded_blind_sharp_audit_entry_calls':0,'source_or_canonical_calls_in_selfcheck':0,'graph_changed_fields':'18 /reports/i/elapsed_seconds only','root_frozen_bytes_equal':True,'graph_canonical_certificate_verifier_ordered_path_calls':0,'next_primary_context_already_read_not_done':True,'C0_scope':'actual bytes of all staged files excluding only LF/TAB/CR'};(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
