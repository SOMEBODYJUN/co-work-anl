#!/usr/bin/env python3
"""Read-only raw/AST/observed finite identity/report scalars/links/C0 checks."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,ast
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/two-query-recursion-and-uniform-debt-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['f0257bb0ec1b1cc5f477','6645edc912eedf7f62e9','2b9bf76a9ad9513eef87','8ca6264fd88ed658527e','d45d167d722d23f87286'];sm=read(E/'source-manifest.json');by={a['id']:a for a in sm['rows']};ck(sm['source_count']==5 and sm['source_bytes']==15606 and set(by)==set(ids),'exact-five-primary15606')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-size-SHA256-blob-'+id)
 ck(all(v['path']==a['source_path'] for v in a['sources']),'frozen-source-path-'+id)
cap=read(W/'claim-evidence.json');gate=read(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced','authentic-pushed-synced-Boss4')
ck(cap['remote_tip']==gate['remote_tip']=='c632ea1a749734d4ddea832932839c6e78b16497','actualc632-tip')
ck(set(cap['ids'])==set(gate['actual_intersection'])==set(ids) and gate['status']=='pass' and gate['actual_expected_intersection_count']==5,'actual-exact-five-owner-gate')
ck((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-fz-claim.json').read_bytes() and gate['capture_sha256']==sha(W/'claim-evidence.json'),'full-original-capture-not-projection')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'owner-and-source-'+a['id'])
ck(read(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_records']==[],'no-prior-success-on-either-sourceSHA')
d=read(E/'dependency-manifest.json');a=d['two_query']['available'][0];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size']==7417 and sha(p)==a['sha256']=='d60b843f01893bf24f11141342918760a9c3f25b44e43e1ddf8e4aefe09303d9' and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'available348-only-input-exactSHA')
ck(d['two_query']['true_runtime_file_inputs']==1 and d['two_query']['consumed_fields']==['instance.customers','certificate.actions'],'two-query-real-consumed-fields')
missing=d['uniform_debt'];mi=missing['missing_inventory_record'];ck(missing['true_runtime_file_inputs']==1 and missing['available'] is False and mi['id']=='04c0c02f34f0dc225b7f' and mi['size']==48798,'791-input-missing-identity')
ck(mi['sha256']==missing['needed_sha256']=='098bd6a2278aa8ae28b18ba07fe585bffcbad1571f04a835bd5d70794e401135' and mi['blob']=='649baca7fcda68f7fe3fe4c860d86e494a9e420a','missing-input-SHA-blob-not-invented')
local=read(W/'local-dependency-export-manifest.json');ck([a['id'] for a in local['rows']]==['23b69044426c185f1653'] and [a['id'] for a in local['missing']]==[mi['id']] and 'no network attempted' in local['missing'][0]['reason'],'original-no-network-helper-missing-receipt')
blocked=read(E/'uniform-debt-blocked-execution.json');ck(blocked['status']=='not-run-missing-local-input' and blocked['original_entry_calls']==0 and blocked['source_sha256']==by[ids[3]]['sha256'],'uniform3862-actual-zero-entry-blocked')
ck(blocked['network_attempts']==0 and blocked['reconstruction_or_frozen_report_substitution_attempted'] is False and blocked['predictable_FileNotFound_original_call_avoided'] and blocked['frozen1617_output_is_not_a_current_success_receipt'],'no-fake-input-or-failure-or-success')
ck(not any(p.name=='phi_rise_exact.json' for p in S.rglob('*')) and not (E/'replay-uniform-debt').exists(),'no-staged791-substitution-or-original-replay')
for id,hasguard in [(ids[1],True),(ids[3],True)]:
 source=S/by[id]['path'];tr=ast.parse(source.read_text());imports=[a.module for a in ast.walk(tr) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tr) if isinstance(a,ast.Import) for n in a.names]
 ck(set(imports)<= {'fractions','itertools','pathlib','json'} and 'fractions' in imports,'only-stdlib-imports-'+id)
 ck(any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tr.body)==hasguard,'real-main-guard-'+id)
run=read(E/'replay-two-query/execution.json');ob=read(E/'replay-two-query/passive-observation.json');ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'3378-one-success-assertions-on')
ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==run['source_sha256']==by[ids[1]]['sha256'],'3378-relocated-raw-source')
ck(run['input_bytes_unchanged'],'input-unchanged-flag')
ri=run['true_runtime_file_inputs'][0];ck(len(run['true_runtime_file_inputs'])==1 and ri['size']==7417 and sha(S/ri['runtime_path'])==ri['sha256']==d['two_query']['available'][0]['sha256'],'actual-mirrored348-input')
f=ob['final_original_values'];entry=S/run['runtime_entry'];ck(Path(f['REPO'])==entry.parent.parents[5] and Path(f['SOURCE'])==S/ri['runtime_path'],'real-HEREparents5-source-resolution')
output=S/run['output']['path'];frozen=S/by[ids[2]]['path'];ck(run['output']['frozen_byte_equal'] and output.read_bytes()==frozen.read_bytes() and output.stat().st_size==1085 and sha(output)==run['output']['sha256']==by[ids[2]]['sha256'],'whole1085-output-byte-equal')
ck(run['stdout_bytes']==(E/'replay-two-query/stdout.txt').stat().st_size==1086 and (E/'replay-two-query/stdout.txt').read_bytes()==output.read_bytes()+b'\n' and run['stderr_bytes']==(E/'replay-two-query/stderr.txt').stat().st_size==0,'print-text-extra-LF1086-and-stderr0')
for k,v in {'<module>':1,'main':1,'follow':4,'phi':12,'pay':6,'insertion':2}.items():ck(ob['function_calls'][k]==v,'actual-3378-calls-'+k+'-'+str(v))
ck(ob['observer_extra_original_calls']==ob['new_all43_SPE_audits']==ob['new_258_full_IC_scans']==ob['new_all36_K_scans']==0,'no-extra-source-or-full-audits')
ck(run['involved_child_IC_comparisons']==2 and run['involved_terminal_BR_comparisons']==2 and run['uniform_debt3862_calls']==run['optimizer_SPE_solver_or_project_calls']==run['network_or_shared_repo_writes']==0,'two-child-two-terminal-only-791zero')
r=read(frozen);ck(r['root_pair']==[2,5] and r['real_first_child_actions']==[3,0] and r['root_branches']==[[2,3,4],[5,0,1]] and r['cross_child_branches']==[[2,0,1],[5,3,4]],'all-four-real-paths-and-child-actions')
for key,expected in [('joint_regrets',['12','12']),('deep_terminal_regrets',['0','0']),('deletion_potential_drifts',['12','12']),('child_ic_slacks',['0','0']),('diagonal_root_payoffs',['147/2','147/2']),('cross_insertions',['159/2','159/2']),('cross_intersection_taxes',['6','6'])]:ck(r[key]==expected,'twoquery-frozen-field-'+key)
for j in range(2):ck(F(r['joint_regrets'][j])==F(r['deep_terminal_regrets'][j])+F(r['deletion_potential_drifts'][j])-F(r['child_ic_slacks'][j]),'each-R-identity-'+str(j))
ck(sum(map(F,r['cross_insertions']))==sum(map(F,r['diagonal_root_payoffs']))+sum(map(F,r['joint_regrets']))-sum(map(F,r['cross_intersection_taxes'])) and r['R_identity_residual']==r['K_identity_residual']=='0','exact-symmetric-K-and-two-residuals')
ck([f[k] for k in ('RAB','RBA','FA','FB')]==['12']*4 and [f[k] for k in ('gammaA','gammaB','deepA','deepB')]==['0']*4,'actual-source-final-values-not-only-frozen-report')
u=read(S/by[ids[4]]['path']);scalar=read(E/'frozen-uniform-scalar-check.json');ck(scalar['status']=='pass-report-internal-scalars-only' and scalar['entry_calls']==1 and scalar['source_program3862_calls']==scalar['source_functions_or_solver_calls']==scalar['full_SPE_checks']==0,'separate-report-only-scalar-check-once')
ck(scalar['input_size']==1617 and scalar['input_sha256']==sha(S/by[ids[4]]['path'])==by[ids[4]]['sha256'] and scalar['791_unit_model_reconstructed'] is False and scalar['missing48798_input_replaced_or_rebuilt'] is False,'report-only-input1617-not791')
ck(u['players']==3 and u['topics']==7 and u['unit_customers']==791 and u['decision_histories']==57 and u['deviation_comparisons']==399,'frozen-reported-sample-metadata-not-current-proof')
query=list(map(F,u['query']));ck(len(query)==7 and all(x>=0 for x in query) and sum(query)==1 and query==[F(w,42) for w in (1,2,3,5,7,11,13)],'frozen-fixed-query-normalization')
sums={k:F() for k in ['psi','C','D','actual_utility','root_slack','free_column_gain','covariance','insertion_tax']}
for a,b in zip(u['positions'],scalar['position_results']):
 z={k:F(a[k]) for k in sums};ck(a['index']==b['index'] and F(a['identity_residual'])==0,'report-row-identity-field-'+str(a['index']))
 ck(z['root_slack']==z['actual_utility']-z['D']>=0 and z['free_column_gain']==z['C']-z['psi']>=0,'report-e-and-L-'+str(a['index']))
 ck(z['D']-z['C']==z['covariance']+z['insertion_tax'] and z['psi']-z['actual_utility']==z['C']-z['D']-z['root_slack']-z['free_column_gain'],'report-Cov-and-debt-identity-'+str(a['index']))
 ck(b['covariance_identity_residual']==b['debt_identity_residual']=='0','scalar-check-row-residual-'+str(a['index']))
 if a['index']>=2:ck(z['psi']<=z['actual_utility'] and b['reported_last_two_scalar_bound_checked'],'report-last-two-scalar-bound-'+str(a['index']))
 for k in sums:sums[k]+=z[k]
ck({k:str(v) for k,v in sums.items()}==scalar['report_scalar_sums'] and sums['actual_utility']==F(u['welfare'])==597,'all-eight-frozen-report-scalar-totals')
ck(sums['psi']-597==sums['C']-sums['D']-sums['root_slack']-sums['free_column_gain']==F(-26407,84) and scalar['report_sum_psi_minus_report_W']=='-26407/84' and scalar['aggregate_scalar_residual']=='0','aggregate-only-reported-scalar-identity')
ck(F(5,2)-F(1423,605)==F(179,1210)>0,'old13reported-pair-gap-arithmetic-not-new-SPE-check')
comp=read(E/'comparison-manifest.json');ck(len(comp['rows'])==5,'five-related-full-formal-snapshots')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-raw-'+Path(a['path']).name)
rec=read(W/'semantic-receipts.json');targets=read(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids),'five-complete-primary-receipts-with-blocked-boundary')
for a in rec:ck(all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>100 and set(a['targets'])<=set(targets),'complete-semantic-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==58 and len(read(W/'relation-review.json')['relations'])==7,'58-human-math-7-relations')
n=read(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==42943 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'next-GI-five-local-only-availability')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);ck((S/rel).is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
ck(len(stable)==len(set(stable))==3,'three-distinct-stable-objects')
scope=read(E/'scope.json');ck(scope['two_query3378_original_entry_calls']==scope['uniform_frozen_report_scalar_check_calls']==1 and scope['uniform_debt3862_original_entry_calls']==scope['scalar_check_source_functions_or_SPE_calls']==scope['new_all43_SPE_audits']==scope['new_258_full_IC_scans']==scope['new_all36_K_scans']==scope['network_attempts']==0 and scope['report_claims_791_57_399_not_current_verified'],'one-original-one-scalar-check-one-blocked-no-fake-SPE')
manifest=read(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist')
ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-actual-staged-bytes-C0-excluding-only-LF-TAB-CR')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-files')
v={'status':'pass','scope':'read-only raw/AST/already-observed four-path and frozen-scalar certificates/links/C0/whitelist; no source or checker calls','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':58,'human_relations':7,'two_query3378_original_entry_calls':1,'uniform_debt3862_original_entry_calls':0,'uniform_debt_status':'not-run-missing48798B-input','frozen_uniform_scalar_check_calls':1,'original_or_scalar_checker_calls_in_selfcheck':0,'new_all43_SPE_or_258_or_36K_scans':0,'C0_scope':'actual bytes of every staged file; exclude only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
