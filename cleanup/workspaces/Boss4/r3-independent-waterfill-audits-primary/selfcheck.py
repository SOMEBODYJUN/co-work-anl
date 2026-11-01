#!/usr/bin/env python3
"""Pure data/AST/hash/link/C0 check. Never imports or invokes either original."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,ast
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/independent-waterfill-audits-primary'
checks=[]
def ck(ok,name):
 if not ok:raise AssertionError(name)
 checks.append(name)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def c0(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['6561b4cc09f8443753c9','334a24486e2ad0ba92b5','9a6a5ef841dfef2ed15a','bd043a0028b9611c57fb','4705f54e019a04df1f10'];m=read(E/'source-manifest.json');by={a['id']:a for a in m['rows']}
ck(m['source_count']==5 and m['source_bytes']==33862 and set(by)==set(ids),'exact-five-primary33862')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();ck(len(b)==a['size'] and sha(p)==a['sha256'] and blob==a['blob'],'raw-size-SHA256-blob-'+id)
 ck(all(v['path']==a['source_path'] for v in a['sources']),'frozen-source-path-'+id)
cap=read(W/'claim-evidence.json');gate=read(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced','authentic-pushed-synced-Boss4')
ck(set(cap['ids'])==set(ids)==set(gate['actual_intersection']) and gate['status']=='pass' and gate['actual_expected_intersection_count']==5,'actual-exact-five-owner-gate')
ck(cap['remote_tip']=='86da7daedd094584a07333413ced759c57c23345','actual86da7da-tip')
ck((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-em-claim.json').read_bytes() and gate['capture_sha256']==sha(W/'claim-evidence.json'),'full-original-capture-not-projection')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'owner-and-source-'+a['id'])
ck(read(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_records']==[],'no-prior-same-SHA-success')
d=read(E/'dependency-manifest.json');ck(d['mixed']['true_file_inputs']==3 and d['mixed']['total_bytes']==42090 and d['shared']['true_file_inputs']==0,'runtime-three42090-versus-zero')
for a in d['mixed']['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'true-input-'+Path(a['path']).name)
reports={};observations={}
for label,sid,rid,outsize,outbytes,ninputs,guard in [('mixed',ids[0],ids[1],4257,1597,3,True),('shared',ids[3],ids[4],9866,164,0,False)]:
 source=S/by[sid]['path'];tr=ast.parse(source.read_text());imports=[a.module for a in ast.walk(tr) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tr) if isinstance(a,ast.Import) for n in a.names]
 ck(set(imports)<= {'collections','fractions','itertools','pathlib','json'} and 'pathlib' in imports,'only-stdlib-imports-'+label)
 hasguard=any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tr.body);ck(hasguard==guard,'real-main-guard-contract-'+label)
 run=read(E/'replay'/label/'execution.json');ob=read(E/'replay'/label/'passive-observation.json');observations[label]=ob
 ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'one-original-success-assertions-on-'+label)
 ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['original_bytes_unchanged'] and sha(S/run['runtime_entry'])==sha(source)==run['source_sha256'],'raw-original-relocation-'+label)
 ck(len(run['true_file_inputs'])==ninputs and run['inputs_unchanged'],'true-runtime-input-count-'+label)
 for a in run['true_file_inputs']:ck((S/a['runtime_path']).stat().st_size==a['size'] and sha(S/a['runtime_path'])==a['sha256'],'actual-input-SHA-'+label+'-'+Path(a['runtime_path']).name)
 q=S/run['output']['path'];frozen=S/by[rid]['path'];ck(run['output']['frozen_byte_equal'] and q.read_bytes()==frozen.read_bytes() and q.stat().st_size==outsize and sha(q)==by[rid]['sha256']==run['output']['sha256'],'complete-generated-byte-equal-'+label)
 ck(run['stdout_bytes']==(E/'replay'/label/'stdout.txt').stat().st_size==outbytes and run['stderr_bytes']==(E/'replay'/label/'stderr.txt').stat().st_size==0,'actual-stdout-stderr-'+label)
 ck(run['project_solver_payoff_verifier_imports']==0 and ob['no_extra_source_calls'],'no-project-or-observer-source-calls-'+label)
 text=(E/'replay'/label/'stdout.txt').read_text();dec=json.JSONDecoder();docs=[]
 while text.strip():text=text.lstrip();v,n=dec.raw_decode(text);docs.append(v);text=text[n:]
 ck(len(docs)==(2 if label=='mixed' else 1),'stdout-document-count-'+label)
 if label=='mixed':ck('new_exact_intervals' not in docs[0] and len(docs[1])==5,'mixed-stdout-summary-not-report')
 else:ck(docs[0]['rational_cases']==14 and docs[0]['queries_checked']==43,'shared-stdout14-43-summary')
 reports[label]=read(frozen)
mo=observations['mixed'];so=observations['shared'];mc=mo['function_calls'];sc=so['function_calls']
for k,v in {'<module>':1,'main':1,'follow':3201,'pay':16804,'insertion':637,'equation':510,'gamma':20,'bisect':5,'compact_interval':5}.items():ck(mc[k]==v,'mixed-passive-'+k+'-'+str(v))
for k,v in {'<module>':1,'audit':14,'unit':86,'load':381,'c':730,'support':42,'query':128,'R':42,'B':28,'V':98,'mixed_u':102}.items():ck(sc[k]==v,'shared-passive-'+k+'-'+str(v))
ck(mo['final_original_values']['comparisons']==2800 and mo['final_original_values']['core_translation_checks']==5600 and mo['final_original_values']['minimum']=='0','mixed-final2800-5600-min0')
ck(so['final_original_values']['rational_cases']==14 and so['final_original_values']['queries_checked']==43,'shared-final14-43')
mr=reports['mixed'];sr=reports['shared'];ck(mr['ordered_histories']==400 and mr['spe_comparisons']==2800 and mr['core_translation_checks']==5600 and mr['minimum_spe_slack']=='0','mixed-finite-scope-report')
ck(mr['actual']==[6,0,3,4] and mr['utilities']==['19','29/3','67/6','67/6'] and mr['welfare']=='51','mixed-actual53-leaf')
ck(mr['true_v4']==mr['primal_minimum']=='28481/2924' and mr['static_backgrounds']==84 and mr['dual_caps']==['28481/2924']*7,'mixed-true-v4-84-seven-caps')
ck(mr['low_tail_positions']==[1] and mr['deficit']=='647/8772' and mr['X0_original_load_spectrum']=={'3':11,'2':12},'mixed-roleposition-and-spectrum')
ck(mr['frozen_intervals_independently_checked']==mo['final_original_values']['frozen_checks']==[0,1,10,1000,1000000],'mixed-old80-c10-parameters')
ck([a['core'] for a in mr['new_exact_intervals']]==[0,1,37,1000,1000000],'mixed-new96-c37-parameters')
D=F(647,8772);T=F(28481,2924)
for row in mr['new_exact_intervals']:
 c=row['core'];l,h=map(F,row['water_weight_interval']);gl,gh=map(F,row['gamma_interval']);rl,rh=map(F,row['gamma_over_deficit_interval']);cl,ch=map(F,row['compact_ratio_interval'])
 ck(0<l<h<1 and h-l==F(1,2**96),'mixed96-width-'+str(c))
 fl=12/(1+l)+11/(2+l)+c/(3+l)-T-F(c,4);fh=12/(1+h)+11/(2+h)+c/(3+h)-T-F(c,4)
 ck(fl>0>fh,'mixed96-equation-sign-'+str(c))
 ck(gl==c/(3+h)-F(c,4) and gh==c/(3+l)-F(c,4) and 0<=gl<=gh<D and (rl,rh)==(gl/D,gh/D),'mixed-gamma-reverse-endpoints-'+str(c))
 ck(cl<=rl<=rh<=ch and cl==F((rl.numerator*10**12)//rl.denominator,10**12) and ch==F((rh.numerator*10**12+rh.denominator-1)//rh.denominator,10**12),'mixed-compact-outward-grid-'+str(c))
 if c:ck(F(c,c+94)<rl<=rh<F(9*c,9*c+608),'mixed-strict-analytic-bounds-'+str(c))
ck(mr['new_exact_intervals'][-1]['compact_ratio_interval']==['999932448991/1000000000000','31247889031/31250000000'],'million-core-compact-version')
inputdata=read(S/d['mixed']['rows'][0]['path']);packet=read(S/d['mixed']['rows'][1]['path']);author=read(S/d['mixed']['rows'][2]['path'])
ck(sum(a['multiplicity'] for a in inputdata['customers'])==53 and inputdata['players']==4 and len(inputdata['topics'])==7,'true53-model-schema')
keys=[tuple(a['history']) for a in packet['actions']];ck(len(keys)==len(set(keys))==400 and [sum(len(a)==i for a in keys) for i in range(4)]==[1,7,49,343],'actual400-literal-keys-no-duplicate')
ck([a['common_core'] for a in author['cases']]==mr['frozen_intervals_independently_checked'],'actual-author-report-data-version')
fixtures=so['fixture_arguments'];cases=sr['rational_cases'];ck(len(fixtures)==len(cases)==14,'fourteen-real-embedded-fixtures')
ck(sum(a['queries_checked'] for a in cases)==43 and sum(len(a['steps']) for a in cases)==14,'43-subset-queries-14-drop-events')
for a,b in zip(cases,fixtures):
 t=F(b['threshold']);weights=list(map(F,a['weights']));initial=list(map(F,a['initial_unit']));dd=F(a['D']);ee=F(a['E']);hh=F(a['common_full_universe_gain']);gamma=F(a['gamma_root']);db=F(a['background_gain']);v0=F(a['V_initial']);v1=F(a['V_final']);mass=F(a['positive_mass'])
 ck(a['name']==b['name'] and t>0 and a['queries_checked']==2**len(b['universe']),'fixture-input-and-query-count-'+a['name'])
 ck(dd==sum((max(F(0),t-u) for u in initial),F()) and 0<=gamma<=hh<=ee<=dd and db>=0,'fixture-common-pool-budget-'+a['name'])
 ck(mass==sum(weights,F()) and v1==v0-gamma-db and v1>=t*mass,'fixture-mass-profit-conservation-'+a['name'])
 ck(all(weights[i]==1 for i,u in enumerate(initial) if u>=t) and all(F(a['final_positive_unit'][i])>=t for i,w in enumerate(weights) if w>0),'fixture-retained-high-and-final-density-'+a['name'])
 ck(sum((F(s['own_increment']) for s in a['steps']),F())==ee and all(F(s['unit_after'])-F(s['unit_before'])==F(s['own_increment']) for s in a['steps']),'fixture-event-increments-'+a['name'])
for k in [1,2,7,100]:
 a=next(a for a in cases if a['name']=='old_background_return_k_'+str(k));ck(F(a['background_gain'])==k*F(a['D']),'old-background-return-ratio-'+str(k))
ck(next(a for a in cases if a['name']=='empty_tail_removed')['queries_checked']==1 and next(a for a in cases if a['name']=='no_tails')['queries_checked']==4,'empty-universe-and-no-tail-separate')
ck(next(a for a in cases if a['name']=='repeated_tail_partial')['positive_mass']=='3/2','repeated-tail-positive-mass')
a=sr['irrational_case'];l,h=F(a['rho_lower']),F(a['rho_upper']);ck(0<l<h<1 and h-l==F(a['width'])==F(1,2**100),'irrational100-width')
ck(l*l<F(1,2)<h*h and 1/(1+l)+1/l>2>1/(1+h)+1/h,'irrational-square-and-unit-equation-bracket')
ck(0<2/(1+h)-1<2/(1+l)-1==F(a['common_gain_upper'])<F(a['D'])==F(1,2),'irrational-whole-bracket-common-pool')
ck(all(1/(1+v)+v/(1+v)+1==2 for v in (l,h)),'irrational-mass-conservation-endpoints')
comp=read(E/'comparison-manifest.json');ck(len(comp['rows'])==6,'six-related-formal-pages')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-raw-'+Path(a['path']).name)
fixed=next(a for a in comp['rows'] if '水位事件的共同信用' in a['repo_path']);ck(fixed['size']==8599 and fixed['sha256']=='b8016751cd4d68e9236fa25dbf3b3a26c28a35b46e3205dee13190cfd86c6501' and fixed['canonical_formula_correction']['root_confirmed_body_push']=='2fcf53ecdf9e447798b6b8459a16d6588fe6c3ce','root-fixed-canonical-snapshot-and-provenance')
ck(not c0(R/fixed['repo_path']),'actual-current-canonical-C0-scan')
receipts=read(W/'semantic-receipts.json');targets=read(W/'target-paths.json');ck(len(receipts)==5 and {a['id'] for a in receipts}==set(ids),'five-complete-primary-receipts')
for a in receipts:ck(all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>100 and set(a['targets'])<=set(targets),'complete-semantic-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==60 and len(read(W/'relation-review.json')['relations'])==10,'60-math-items-10-relations')
n=read(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==40688 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'five-local-next-not-remoteclaim-inference')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+k+':',parts[1],re.M) is not None,'MATEK-'+k+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not c0(p),'actual-new-canonical-byte-C0-'+p.name)
 ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);ck((S/rel).is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
ck(len(set(stable))==len(stable)==3,'three-distinct-stable-objects')
scope=read(E/'scope.json');ck(scope['new_original_entry_calls']=={'mixed':1,'shared':1} and scope['original_failures']==scope['original_retries']==scope['new_author5640_calls']==scope['extra_independent2800_scans']==scope['new_data_supplement_calls']==0,'two-new-entry-runs-no-extra-old-runs')
manifest=read(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist')
ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths')
ck(all(not c0(S/f) for f in manifest),'all-staged-actual-bytes-no-nonLF-TAB-CR-C0')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-files')
out={'status':'pass','scope':'read-only data/AST/hashes/rational certificate fields/links and actual raw-byte C0 scans; no original calls','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':60,'human_relations':10,'new_original_entry_calls':{'mixed':1,'shared':1},'original_failures':0,'original_retries':0,'new_author5640_calls':0,'new_data_supplement_calls':0,'new_extra2800_scans':0,'original_calls_in_selfcheck':0,'C0_check':'all actual staged file bytes, and actual current corrected canonical; exclude only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','formal_links')},ensure_ascii=False))
