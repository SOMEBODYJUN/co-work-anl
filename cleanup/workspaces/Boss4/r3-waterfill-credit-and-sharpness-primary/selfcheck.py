#!/usr/bin/env python3
"""Final immutable data/source/link checks, never executes original or data supplement."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,ast
W=Path(__file__).resolve().parent;S=W.parents[3]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/waterfill-credit-and-sharpness-primary'
checks=[]
def check(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ids=['79c287548a2a767d9927','441ffbbdc0918f92fa81','153ebdf5b7f4ecf49f64','32346300107fbae30c54','7cf743807d3dabbf4c6f']
m=read(E/'source-manifest.json');check(m['source_count']==5 and m['source_bytes']==36721,'exact-five-primary36721')
byid={a['id']:a for a in m['rows']};check(set(byid)==set(ids),'exact-primary-IDs')
for id in ids:
 a=byid[id];p=S/a['path'];b=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 check(len(b)==a['size'] and sha(p)==a['sha256'] and blob==a['blob'],'raw-byte-size-SHA256-blob-'+id)
 check(all(c['path']==a['source_path'] for c in a['sources']),'frozen-path-identity-'+id)
cap=read(W/'claim-evidence.json');gate=read(W/'primary-authorization-check.json')
check(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced','authentic-pushed-Boss4-synced')
check(cap['remote_tip']=='86239392f353628df95534d325c3ec115645d5ca','actual86239392-tip')
check(set(cap['ids'])==set(ids)==set(gate['actual_intersection']),'actual-exact-five-intersection')
check((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-ea-claim.json').read_bytes(),'full-original-capture-not-projection')
check(gate['status']=='pass' and gate['actual_expected_intersection_count']==5 and gate['capture_sha256']==sha(W/'claim-evidence.json'),'gate-pass-hash')
for row in gate['ownership_records']:
 check(row['record']['owner']=='Boss4' and row['record']['disposition']=='in-progress' and row['record']['source_sha256']==byid[row['id']]['sha256'],'owner-and-source-'+row['id'])
pre=read(W/'preflight-corrections.json')
check(pre['wrapper_preflight_attempts_before_authorization_file']==1 and pre['original_entry_calls_in_these_failures']==0 and pre['source_functions_called_in_these_failures']==0,'preflight-failure-before-original-preserved')
check('KeyError' in (W/'preflight-failure-output.txt').read_text() and 'FileNotFoundError' in (W/'preflight-failure-output.txt').read_text(),'preflight-output-retained')
check(read(W/'pre-execution-same-sha-search.json')['success_record_found'] is False,'no-prior-same-source-success-record')
d=read(E/'dependency-manifest.json');check(d['true_original_runtime_file_inputs']==2 and d['total_bytes']==37315,'true-two-inputs37315')
for a in d['rows']:check((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'raw-dependency-'+a['runtime_relative_to_entry'])
source=S/byid['441ffbbdc0918f92fa81']['path'];tree=ast.parse(source.read_text())
imports=[a.module for a in ast.walk(tree) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tree) if isinstance(a,ast.Import) for n in a.names]
check(set(imports)=={'fractions','functools','itertools','pathlib','json'},'pure-stdlib-original-imports')
check(not any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tree.body),'original-top-level-no-main-guard')
code=source.read_text();check('endogenous_53_security.json' not in code and 'endogenous_53_instance.json' in code and 'endogenous_53_strategy.json' in code,'source-hardcoded-pQ-no-security-input')
run=read(E/'replay/execution.json');obs=read(E/'replay/passive-observation.json')
check(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'single-original-success-assertions-on')
check(run['new_empty_replay'] and run['source_absolute_path_is_relocated'],'new-empty-relocated-entry')
check(run['source_sha256']==byid['441ffbbdc0918f92fa81']['sha256']==sha(S/run['runtime_entry']),'original-entry-raw-SHA')
check(run['input_bytes_unchanged'] and run['original_bytes_unchanged'],'runtime-inputs-source-unchanged')
check(len(run['true_file_inputs'])==2,'runtime-exact-two-inputs')
for a in run['true_file_inputs']:check((S/a['runtime_path']).stat().st_size==a['size'] and sha(S/a['runtime_path'])==a['sha256'],'mirrored-input-'+Path(a['runtime_path']).name)
frozen=S/byid['153ebdf5b7f4ecf49f64']['path'];generated=S/run['output']['path']
check(run['output']['frozen_byte_equal'] and generated.read_bytes()==frozen.read_bytes() and generated.stat().st_size==4775,'report4775-byte-equal')
check(sha(generated)==run['output']['sha256']=='46abde1969843921d8dbf508f8f6e1ff575f26668eeb987b50ee704319d16145','actual-output-SHA')
check(run['stdout_bytes']==(E/'replay/stdout.txt').stat().st_size==1233 and run['stderr_bytes']==(E/'replay/stderr.txt').stat().st_size==0,'stdout1233-stderr0')
s=(E/'replay/stdout.txt').read_text();dec=json.JSONDecoder();docs=[]
while s.strip():s=s.lstrip();v,n=dec.raw_decode(s);docs.append(v);s=s[n:]
check(len(docs)==6 and 'cases' not in docs[0] and [a['core'] for a in docs[1:]]==[0,1,10,1000,1000000],'stdout-six-JSON-documents-not-full-report')
calls=obs['original_function_calls'];check(calls['<module>']==1 and calls['payoff']==3204 and calls['query']==637,'passive-module1-payoff3204-query637')
check(calls['case']==5 and calls['low_unit']==425 and calls['root_unit']==10 and obs['no_extra_original_import_or_calls'],'passive-case5-low425-root10-no-added-calls')
report=read(frozen)
for key,value in [('complete_ordered_histories',400),('checked_SPE_comparisons_including_self',2800),('static_backgrounds_checked',84),('finite_difference_checks',142),('unit_customers_base',53),('players',4),('topics',7)]:check(report[key]==value,'original-report-'+key)
check(report['actual_path']==[6,0,3,4] and report['actual_payoffs']==['19','29/3','67/6','67/6'] and report['minimum_SPE_slack']=='0','actual53-leaf-and-minimum-slack')
check(report['true_v4']==report['primal_minimum']=='28481/2924' and report['dual_all_queries']==['28481/2924']*7,'true-v4-primal-dual-match')
for key,value in [('comparisons','2800'),('finite_checks','142'),('D','647/8772'),('m','4'),('p','7')]:check(obs['final_original_globals'][key]==value,'passive-final-global-'+key)
check(obs['final_original_globals']['expected_histories']==400 and obs['final_original_globals']['backgrounds']==84,'passive-node-and-static-counts')
ins=read(S/d['rows'][0]['path']);cert=read(S/d['rows'][1]['path']);rows=cert['actions']
check(ins['players']==4 and len(ins['topics'])==7 and sum(a['multiplicity'] for a in ins['customers'])==53,'53-unit-raw-schema')
keys=[tuple(a['history']) for a in rows];check(len(rows)==len(set(keys))==400 and {len(h):sum(len(x)==len(h) for x in keys) for h in keys}=={0:1,1:7,2:49,3:343},'literal400-no-duplicate-depths')
check(all(0<=a['action']<7 and all(0<=v<7 for v in a['history']) for a in rows),'all-literal-actions-legal')
sup=read(E/'zero-pool-and-brackets-exact.json');check(sup['status']=='pass' and sup['entry_calls']==1 and sup['original_source_calls']==0 and sup['new_full_SPE_scans']==0 and sup['VAR_optimization_calls']==sup['LP_or_solver_calls']==0,'data-supplement-once-no-original-fullSPE-VAR-LP')
for a in sup['inputs']:check((E/a['path']).stat().st_size==a['size'] and sha(E/a['path'])==a['sha256'],'supplement-input-'+Path(a['path']).name)
z=sup['zero_pool'];check(z['stored_actions']==43 and len(z['forced_root_leaves'])==6 and z['full43_IC_nodes_checked']==z['full258_IC_comparisons_checked']==0,'only-six-old-root-leaves-not-full258')
for a in z['forced_root_leaves']:check(F(a['payoffs'][0])==F(29,3) and min(map(F,a['payoffs'][1:]))>F(2411,246),'six-old-real-tail-high-'+str(a['root']))
check(len(z['static_backgrounds'])==21 and len(z['static_payoff_matrix'])==6 and all(len(a)==21 for a in z['static_payoff_matrix']),'old34-static6by21')
vals=list(map(F,z['all21_primal_values']));check(min(vals)==F(2411,246) and z['dual6_caps']==['2411/246']*6,'old34-true-v3-match')
for i,a in enumerate(vals):check(a>=F(2411,246),'old34-primal-column-'+str(i))
check(z['X0_original_load_spectrum']=={'2':12,'3':11} and z['threshold_minus_endpoint_density']=='1342711/14637246' and z['integral_lower_bound']=='1342711/1463724600','zero-pool-spectrum-and-exact-positive-integral')
check(z['W']=='32' and z['W_minus3v3']=='213/82' and z['OPT3']==34 and z['half_slack']==30,'zero-pool-keeps-aggregate-half-slack')
check(len(report['cases'])==len(sup['all_five_saved80_step_cases'])==5,'all-five-case-versions')
for a,b in zip(report['cases'],sup['all_five_saved80_step_cases']):
 c=a['common_core'];lo,hi=map(F,a['water_weight_interval']);check(len(a)==10 and c==b['common_core'] and F(0)<lo<hi<F(1) and hi-lo==F(1,2**80),'all-ten-fields-and80-width-'+str(c))
 check(F(b['F_lower_endpoint'])>=0>=F(b['F_upper_endpoint']) and a['root_gain_interval']==b['gamma_interval'] and a['root_gain_over_deficit_interval']==b['ratio_interval'],'case-bracket-direction-and-return-'+str(c))
 check(F(a['linear_shortfall'])>0 and F(a['deficit'])==F(647,8772),'case-linear-failure-and-fixed-deficit-'+str(c))
 if c:check(F(c,c+94)<F(b['ratio_interval'][0])<=F(b['ratio_interval'][1])<F(9*c,9*c+608),'case-strict-analytic-ratio-bound-'+str(c))
for mf in ['context-manifest.json','comparison-manifest.json']:
 for a in read(E/mf)['rows']:check((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],mf+'-'+Path(a['path']).name)
check(len(read(E/'context-manifest.json')['rows'])==4,'two-VAR-context-plus34-input-certificate-not-primary')
check(len(read(E/'comparison-manifest.json')['rows'])==7,'seven-complete-related-formal-pages')
rec=read(W/'semantic-receipts.json');targets=read(W/'target-paths.json');check(len(rec)==5 and {a['id'] for a in rec}==set(ids),'five-complete-primary-receipts')
for a in rec:check(all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>90 and set(a['targets'])<=set(targets),'complete-semantic-'+a['id'])
check((W/'mathematical-self-review.md').read_text().count('[x]')==62,'62-human-math-items')
check(len(read(W/'relation-review.json')['relations'])==13,'13-explained-relations')
nexts=read(W/'next-candidates.json');check(nexts['count']==5 and nexts['total_bytes']==33862 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in nexts['rows']),'five-local-next-not-remote-availability')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);check(len(parts)==3,'flat-frontmatter-'+p.name);meta=parts[1]
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:check(re.search('^'+k+':',meta,re.M) is not None,'MATEK-'+k+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',meta,re.M).group(1))
 check(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholders-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  clean=raw.split('#')[0];resolved=(p.parent/clean).resolve();rel=resolved.relative_to(S);q=S/rel
  check(q.is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
check(len(stable)==len(set(stable))==4,'four-distinct-object-identities')
# Primitive arithmetic verifies analytical constants without re-running any source/checker.
check(F(19)-F(28481,2924)==F(27075,2924) and F(67,6)-F(28481,2924)==F(12511,8772),'sharp-root-positive-and-unique-low-gap')
check(F(51)-4*F(28481,2924)==F(8800,731) and 2*51-53==49,'53-keeps-aggregate-half-slack')
check(4*4*(F(6,2)+F(11,9))==F(608,9) and 4*3*(F(6)+F(11,6))==94,'H-endpoints608over9-and94')
scope=read(E/'execution-and-evidence-scope.json');check(scope['original_entry_calls']==1 and scope['original_entry_failures']==0 and scope['wrapper_preflight_failures_before_source_calls']==1 and scope['new_independent_full2800_scans']==scope['new_old258_SPE_scans']==scope['new_VAR_optimization_calls']==0,'scope-runs-and-preflight-separated')
manifest=read(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());check(manifest==sorted(manifest)==actual and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist')
check(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
check(True,'strict-finite-JSON-all-files')
result={'status':'pass','scope':'read-only hashes/AST/certificate carrier and rational constants/links/whitelist; no original or supplement execution','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':4,'primary_receipts':5,'human_math_items':62,'human_relations':13,'original_entry_calls':1,'original_entry_failures':0,'wrapper_preflight_failures_before_original':1,'preflight_original_calls':0,'new_data_supplement_calls':1,'new_old258_scans':0,'new_independent2800_scans':0,'new_VAR_or_LP_calls':0,'original_or_supplement_calls_in_selfcheck':0}
(W/'selfcheck.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','formal_links')},ensure_ascii=False))
