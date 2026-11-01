#!/usr/bin/env python3
"""Read-only frozen/raw/AST/already-generated exact algebra/links/C0 checks."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,ast
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/minimal-support-and-uniform-time-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['bc7f3e7e454cb4c97de9','da6e19798dcb465f7e3c','cc8c02480db3aa8e6872','d90777ff1eddafbef008','d8802c3a9881694f5a77'];m=read(E/'source-manifest.json');by={a['id']:a for a in m['rows']};ck(m['source_count']==5 and m['source_bytes']==21913 and set(by)==set(ids),'exact-five-primary21913')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-size-SHA256-blob-'+id)
 ck(all(v['path']==a['source_path'] for v in a['sources']),'frozen-source-path-'+id)
cap=read(W/'claim-evidence.json');g=read(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced','actual-pushed-synced-Boss4')
ck(cap['remote_tip']==g['remote_tip']=='d6ca36aa9a014d374a00a91b8ba06a5f8bff6311','actuald6ca36-tip')
ck(set(cap['ids'])==set(g['actual_intersection'])==set(ids) and g['status']=='pass' and g['actual_expected_intersection_count']==5,'actual-exact-five-owner-gate')
ck((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-fk-claim.json').read_bytes() and g['capture_sha256']==sha(W/'claim-evidence.json'),'full-original-capture-not-projection')
for a in g['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'owner-source-'+a['id'])
ck(not read(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_found'],'no-prior-sameSHA-success')
d=read(E/'dependency-manifest.json');a=d['rows'][0];p=S/a['path'];b=p.read_bytes();ck(d['true_runtime_file_inputs']==1 and d['total_bytes']==7417 and len(b)==7417 and sha(p)==a['sha256']=='d60b843f01893bf24f11141342918760a9c3f25b44e43e1ddf8e4aefe09303d9' and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'true7417-runtime-input-exact')
ck(d['consumed_packet_fields']==['instance','certificate.actions','K'] and len(d['unused_packet_fields_preserved'])==9,'input-consumed-versus-unused-fields')
packet=read(p);ck(packet['instance']['players']==3 and len(packet['instance']['topics'])==6 and sum(a['multiplicity'] for a in packet['instance']['customers'])==348 and len(packet['instance']['customers'])==18,'348-unit18types-six3-schema')
keys=[tuple(a['history']) for a in packet['certificate']['actions']];ck(len(keys)==len(set(keys))==43 and [sum(len(a)==i for a in keys) for i in range(3)]==[1,6,36],'full43-literal-ordered-actions')
source=S/by[ids[1]]['path'];tr=ast.parse(source.read_text());imports=[a.module for a in ast.walk(tr) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tr) if isinstance(a,ast.Import) for n in a.names]
ck(set(imports)=={'fractions','itertools','pathlib','json'},'pure-stdlib-imports')
ck(any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tr.body),'original-main-guard')
ck('REPO = HERE.parents[5]' in ast.unparse(tr),'real-parents5-root-contract')
run=read(E/'replay/execution.json');ob=read(E/'replay/passive-observation.json');ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'single-original-success-assertions-on')
ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==sha(source)==run['source_sha256'],'raw-relocated-original-SHA')
ck(run['input_bytes_unchanged'] and len(run['true_runtime_file_inputs'])==1 and sha(S/run['true_runtime_file_inputs'][0]['runtime_path'])==a['sha256'],'runtime-input-byte-identical')
f=ob['final_original_values'];entry=S/run['runtime_entry'];ck(Path(f['REPO'])==entry.parent.parents[5] and Path(f['SOURCE'])==S/run['true_runtime_file_inputs'][0]['runtime_path'],'actual-REPO-and-SOURCE-resolution')
out=S/run['output']['path'];frozen=S/by[ids[2]]['path'];ck(run['output']['frozen_byte_equal'] and out.read_bytes()==frozen.read_bytes() and out.stat().st_size==3197,'whole3197-output-byte-equal')
ck(sha(out)==run['output']['sha256']==by[ids[2]]['sha256']=='3365ee3fff361a00a3d9c0d139783afee3273006ce2eabc47590133981d7d239','actual-output-SHA')
ck(run['stdout_bytes']==(E/'replay/stdout.txt').stat().st_size==993 and run['stderr_bytes']==(E/'replay/stderr.txt').stat().st_size==0,'stdout993-stderr0')
stdout=read(E/'replay/stdout.txt');ck(not any(k.startswith('abstract') for k in stdout) and stdout['ordered_histories']==43 and stdout['deviation_comparisons']==258,'stdout-single-summary-excludes-abstract-fields')
for k,v in {'<module>':1,'main':1,'follow':308,'utility':308,'pair_extremum':4}.items():ck(ob['function_calls'][k]==v,'actual-call-'+k+'-'+str(v))
ck(ob['observer_extra_original_calls']==0 and run['optimizer_SPE_solver_project_verifier_calls']==run['network_or_shared_repo_writes']==0,'no-extra-source-or-project-network-calls')
r=read(frozen);ck(r['players']==3 and r['topics']==6 and r['unit_customers']==348 and r['ordered_histories']==43 and r['deviation_comparisons']==258 and r['query_matrix_entries']==36,'original-finite348-43-258-36')
ck(r['actual']==f['actual']==[0,3,4] and r['root_utility']==f['u']=='147/2' and f['d']==['147/2']*6,'original-actual-and-six-root-profits')
ck(f['K']==packet['K'] and r['diagonal_insertion_taxes']==f['taxes']==['53/2','125/4','181/6']*2,'full36-K-and-six-taxes-match')
K=[[F(v) for v in row] for row in f['K']];u=F(r['root_utility']);ck(all(K[i][i]==u-F(r['diagonal_insertion_taxes'][i]) for i in range(6)),'six-diagonal-tax-identities')
ck(max(K[i][0] for i in range(6))==max(K[i][3] for i in range(6))==69<u,'old348-has-safe-pure-columns')
for j,z in enumerate([r['existing_high_cycle_pair'],*r['abstract_pair_formula_checks']]):
 alpha,beta,s,uu,x,maximum,gap,det=[F(z[k]) for k in ['alpha','beta','cross_average','root_utility','probability_A','maximum','maximum_minus_root','gap_matrix_determinant']];den=2*s-alpha-beta
 ck(alpha<uu and beta<uu and den>0 and 0<x<1 and x==(s-beta)/den,'pair-domain-and-vertex-'+str(j))
 ck(maximum==(s*s-alpha*beta)/den==alpha*x*x+2*s*x*(1-x)+beta*(1-x)*(1-x),'pair-exact-max-'+str(j))
 ck(gap==maximum-uu==-det/den and det==(uu-alpha)*(uu-beta)-(uu-s)**2 and z['unsafe_pair']==(s>uu and (s-uu)**2>(uu-alpha)*(uu-beta)),'pair-exact-threshold-'+str(j))
ck(r['existing_high_cycle_pair']['unsafe_pair'] is False and r['existing_high_cycle_pair']['maximum_minus_root']=='-145/12','old348-high-cycle-not-unsafe')
ck([a['support'] for a in r['abstract_matrix_identity_checks']]==list(range(2,9)),'abstract-only-k2-through8')
for a in r['abstract_matrix_identity_checks']:
 k=a['support'];ck(F(a['gap'])==F(1,2*k) and a['inverse_times_one']==[-2]*k and F(a['proper_face_minimum'])==F(1,2*(k-1)),'abstract-inverse-gap-face-'+str(k))
context=read(E/'time-context-manifest.json');ck(len(context['rows'])==1 and context['rows'][0]['id']=='92a40e62e2ec52cab29c','7002-global-time-context-not-primary')
for a in context['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'context-raw-exact')
comp=read(E/'comparison-manifest.json');ck(len(comp['rows'])==3,'three-full-related-formal-pages')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-raw-'+Path(a['path']).name)
bank=read(E/'bank-two-query-exact.json');base=next(a for a in comp['rows'] if '笛卡尔银行' in a['repo_path']);ck(base['size']==11233 and base['sha256']==bank['proof_source_sha256']=='e66e762af835f21575d7799a16937aee608e87706f75bebb3994cec1427562b0','already-pushed-bank-proof-exact-SHA')
ck(bank['new_analytic_expansion_calls']==1 and bank['case_parameters']==[4,6] and bank['original_frozen_program_calls']==bank['bank_controller_or_SPE_calls']==bank['optimizer_or_Nash_solver_calls']==0,'one-bank-formula-expansion-no-controller-or-SPE')
for a in bank['cases']:
 m=a['players'];topics=a['topics'];cp=F(a['C_p']);fixed=F(a['min_all_root_columns_fixed_p']);uu=F(a['root_u']);alpha=F(1,m)+F(2,3);rows=[[F(v) for v in z] for z in a['two_query_rows_all_root_columns']];cost=list(map(F,a['fixed_p_cost_all_root_columns']))
 ck(len(topics)==m*(m-1) and len(rows)==2 and all(len(z)==len(topics) for z in rows),'bank-two-rows-all-columns-shape-'+str(m))
 ck(cost==[(x+y)/2 for x,y in zip(*rows)] and min(cost)==fixed==cp==F(4,3)+F(1,2*m),'bank-Cp-fixed-all-column-min-'+str(m))
 ck(a['attaining_root_columns']==[[1,0],[1,1],[2,0],[2,1]] and [A for A,v in zip(topics,cost) if v==fixed]==a['attaining_root_columns'],'bank-exact-four-attainment-columns-'+str(m))
 ck(all(F(v)==alpha<uu for v in a['all_singleton_query_values']) and F(a['singleton_slack'])==uu-alpha==F(1,3)+F(1,m*(m-1)),'bank-all-singletons-strict-tax-safe-'+str(m))
 ck(F(a['fixed_p_strict_gap'])==cp-uu==F((2*m+1)*(m-3),6*m*(m-1))>0,'bank-fixed-p-strict-general-gap-'+str(m))
 ck(a['p_is_symmetric_NE'] is False and F(a['profitable_meta_query_value'])==2>cp and a['profitable_meta_query']==[3,2],'bank-two-query-p-not-NE-'+str(m))
 det=F(a['pair_gap_matrix_determinant']);ck(det==(uu-alpha)**2-(uu-2)**2<0 and -det/(4-2*alpha)==cp-uu,'bank-pair-negative-determinant-'+str(m))
 z=a['full_menu_matching_laws'];V=F(z['exact_full_menu_minimax']);lower=list(map(F,z['row_law_cost_all_columns']));upper=list(map(F,z['column_law_value_all_queries']))
 ck(len(z['support'])==(m-1)**2 and F(z['each_probability'])==F(1,(m-1)**2) and min(lower)==max(upper)==V==F(2)-F(1,m)-F(1,3*(m-1))>cp,'bank-matching-full-menu-independent-laws-'+str(m))
 for A,v in zip(topics,lower):
  eco=F(1)-F(1,2*(m-1)) if A[0]==0 else F(1)-F(1,m);ck(v==eco+1-F(1,3*(m-1)),'bank-same-row-law-all-columns-'+str(m)+'-'+str(A))
 for T,v in zip(topics,upper):
  eco=F(1,2) if T[0]==0 else F(1)-F(1,m);ck(v==eco+1-F(1,3*(m-1)),'bank-independent-column-law-all-pure-queries-'+str(m)+'-'+str(T))
 ck(V-uu==F((3*m-1)*(m-3),3*m*(m-1)) and V-cp==F((4*m-3)*(m-3),6*m*(m-1)),'bank-full-menu-versus-root-versus-fixed-p-'+str(m))
 ck(a['actual_W']==2*m and a['OPT']==3*m-2 and a['half_slack']==m+2,'bank-not-half-counterexample-'+str(m))
ck([(a['C_p'],a['root_u'],a['fixed_p_strict_gap'],a['full_menu_matching_laws']['exact_full_menu_minimax']) for a in bank['cases']]==[('35/24','4/3','1/8','59/36'),('17/12','6/5','13/60','53/30')],'requested-m4-m6-exact-values')
bd=read(E/'bank-boundary-domains.json');ck(bd['m2']['distinct_nonzero_economic_and_distinct_bank_p2_exists'] is False and bd['m2']['root_u']=='2' and F(bd['m2']['all_K_entries'])==F(1,2)+F(2,3)==F(bd['m2']['exact_Mfull'])==F(7,6),'m2-direct-degenerate-boundary')
ck(bd['m3']['C_p2']==bd['m3']['fixed_p2_min_all_columns']==bd['m3']['exact_Mfull']==bd['m3']['root_u']=='3/2' and bd['m3']['pair_strict_gap']==bd['m3']['pair_gap_matrix_determinant']=='0' and bd['m3']['p2_can_be_symmetric_NE'],'m3-equality-not-strict-unsafe')
legacy=read(W/'legacy-status-review.json');ck(legacy['replacement_proposals']==[] and legacy['raw_frozen_sources_not_edited'] and all('不凭名字' in z['text'] for a in legacy['matches'] for z in a['exact_segments']),'legacy-no-false-currentOPEN-replacement')
rec=read(W/'semantic-receipts.json');targets=read(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids),'five-complete-primary-receipts')
for a in rec:ck(all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>100 and set(a['targets'])<=set(targets),'complete-semantic-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==67 and len(read(W/'relation-review.json')['relations'])==9,'67-math-items-9-relations')
n=read(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==15606 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'five-next-local-only-availability-and791-unverified')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);ck((S/rel).is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
ck(len(stable)==len(set(stable))==4,'four-distinct-stable-objects')
scope=read(E/'scope.json');ck(scope['new_original_entry_calls']==1 and scope['new_bank_analytic_expansion_calls']==1 and scope['original_failures']==scope['original_retries']==scope['bank_controller_or_SPE_calls']==scope['new_optimizer_or_Nash_calls']==scope['new_old_VAR_waterfill_or_extra348_calls']==0 and scope['new_U_truth_decision'] is False,'one-original-one-bank-algebra-no-old-reruns-no-U-decision')
manifest=read(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist')
ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-actual-staged-bytes-C0-excluding-only-LF-TAB-CR')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-files')
v={'status':'pass','scope':'read-only raw/AST/existing rational/column formula certificates/linear identities/links/C0/whitelist; no original calls','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':4,'primary_receipts':5,'human_math_items':67,'human_relations':9,'new_original_entry_calls':1,'new_bank_analytic_expansion_calls':1,'bank_controller_or_SPE_calls':0,'original_failures':0,'old_VAR_waterfill_or_extra348_calls':0,'original_or_expansion_calls_in_selfcheck':0,'C0_scope':'all actual staged bytes excluding only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
