#!/usr/bin/env python3
"""Read-only raw/AST/existing exact certificate/linear identity/links/C0 verification."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,ast
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/variational-independent-review-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['1e80c518f470fecf53a4','a54a82388483bb30dd79','04add1c7f2f20ff28945','4e1fdd322c7dd4fdbe69','3094f003ec031946e864'];m=read(E/'source-manifest.json');by={a['id']:a for a in m['rows']};ck(m['source_count']==5 and m['source_bytes']==35222 and set(by)==set(ids),'exact-five-primary35222')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-size-SHA256-blob-'+id)
 ck(all(v['path']==a['source_path'] for v in a['sources']),'frozen-source-path-'+id)
cap=read(W/'claim-evidence.json');gate=read(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced','authentic-pushed-Boss4-synced')
ck(cap['remote_tip']==gate['remote_tip']=='eb737324b0995c218421f7e3f1c626a8d253e19a','actualeb7373-tip')
ck(set(ids)==set(cap['ids'])==set(gate['actual_intersection']) and gate['status']=='pass' and gate['actual_expected_intersection_count']==5,'actual-exact-five-owner-gate')
ck((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-fd-claim.json').read_bytes() and gate['capture_sha256']==sha(W/'claim-evidence.json'),'full-original-capture-not-projection')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'owner-source-'+a['id'])
bind=read(E/'review-target-version-binding.json');ck('no explicit SHA' in bind['binding_method'] and bind['original_final_review_sha256']==by[ids[2]]['sha256'],'historical-final-no-SHA-current-binding')
expected=['9f9fd9b8f35b5c2ba2b5ff2e534ccd4f065866934420ac25b6560c73bd0a8013','a0c0a2e4851ad9953f8d25e340c0bfe1e22582cc3bfc6475a60b7dda2cc9bb13']
for a,h in zip(bind['targets'],expected):
 p=S/a['path'];b=p.read_bytes();ck(sha(p)==a['sha256']==h and len(b)==a['size'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'exact-target-SHA-'+a['id'])
ck(not re.search(r'[a-f0-9]{64}',(S/by[ids[2]]['path']).read_text()),'original4600-has-no-target-SHA-literal')
ck(not read(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_found'],'no-prior-sameSHA-success')
ck(read(E/'dependency-manifest.json')['true_runtime_file_inputs']==0,'zero-file-input-contract')
source=S/by[ids[0]]['path'];tr=ast.parse(source.read_text());imports=[a.module for a in ast.walk(tr) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tr) if isinstance(a,ast.Import) for n in a.names]
ck(set(imports)=={'fractions','pathlib','json'},'only-three-stdlib-imports')
ck(not any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tr.body),'original-top-level-no-main-guard')
ck(not any(isinstance(a,ast.Attribute) and a.attr in ('read_text','read_bytes','open') for a in ast.walk(tr)),'original-no-runtime-file-reads')
ck(not any(isinstance(a,ast.FunctionDef) and a.name in ('Q','query') for a in tr.body) and 'combinations' not in source.read_text(),'original-no-query-subset-enumerator')
run=read(E/'replay/execution.json');ob=read(E/'replay/passive-observation.json');ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'one-original-success-assertions-on')
ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==sha(source)==run['source_sha256'],'raw-relocated-entry-SHA')
ck(run['true_runtime_file_inputs']==[] and run['optimizer_SPE_project_calls']==run['network_or_shared_repo_writes']==0,'zero-input-optimizer-SPE-network')
out=S/run['output']['path'];frozen=S/by[ids[3]]['path'];ck(run['output']['frozen_byte_equal'] and out.read_bytes()==frozen.read_bytes() and out.stat().st_size==16641,'complete16641-byte-equal')
ck(sha(out)==run['output']['sha256']==by[ids[3]]['sha256']=='b63ccdfb0506aea7eb3a819a122b5ac00092e84a7d687dde5923dd9885e50827','actual-output-SHA')
ck(run['stdout_bytes']==(E/'replay/stdout.txt').stat().st_size==97 and run['stderr_bytes']==(E/'replay/stderr.txt').stat().st_size==0,'stdout97-stderr0')
stdout=read(E/'replay/stdout.txt');ck(stdout=={'KKT_cases':14,'all_exact_checks':True,'root_credit_derivative':'-159964/8445449'},'actual-stdout-summary')
ck(ob['function_calls']['<module>']==1 and ob['function_calls']['audit_case']==14 and ob['function_calls']['log_bounds']==18 and ob['function_calls']['solve']==1 and ob['observer_extra_original_calls']==0,'actual-original-call-counts')
ck(len(ob['log_bounds_arguments'])==18 and all(a['N']==100 for a in ob['log_bounds_arguments']) and sum(a['q']=='1' for a in ob['log_bounds_arguments'])==6,'six-q1-shortcuts-twelve100-series')
report=read(frozen);cases=report['KKT_cases'];fixtures=ob['embedded_original_fixture_arguments'];returns=ob['case_return_locals'];ck(len(cases)==len(fixtures)==len(returns)==14,'fourteen-small-KKT-cases')
ck([a['N'] for a in returns]==[0]+[1]*11+[3,4] and max(a['N'] for a in returns)==4,'exact-small-universe-domain-not208')
for a,b,r in zip(cases,fixtures,returns):
 name=a['name'];n=len(b['S']);N=len(b['b']);t=F(a['t']);w=list(map(F,a['weights']));M=F(a['M']);D=F(a['D']);H=F(a['H']);G=F(a['G']);credit=F(a['credit_sum']);lo,hi=map(F,a['energy_interval'])
 ck(len(a)==10 and name==b['name']==r['name'] and t==F(b['t'])>0 and w==list(map(F,b['w'])) and r['N']==N and r['n']==n,'case10fields-input-identity-'+name)
 ck(all(0<=v<=1 for v in w) and M==sum(w,F()) and len(a['load_signature'])==N,'case-mass-and-load-shape-'+name)
 ck(0<=H<=credit<=D and 0<=lo<=hi<=D and max(H,G)+hi+t*M<=t*n,'case-common-credit-and-max-JOINT-'+name)
 ck(F(r['V1'])-F(r['V'])==G and F(r['V'])>=t*M and G==F(r['R'])-F(r['R1'])+F(r['B'])-F(r['B1']),'case-joint-root-background-conservation-'+name)
 ck(F(r['seat'])==F(r['ratios'])<=t*(n-M),'case-stretch-'+name)
 # Validate only the supplied small rational point; never run a source function or search weights.
 bg=list(map(F,b['b']));A=set(b['A']);tails=list(map(set,b['S']));L1=[bg[x]+int(x in A)+sum(x in s for s in tails) for x in range(N)];L=[bg[x]+int(x in A)+sum((w[j] for j,s in enumerate(tails) if x in s),F()) for x in range(N)]
 u=[sum((1/L1[x] for x in s),F()) for s in tails];U=[sum((1/L[x] for x in s),F()) for s in tails]
 ck(all((U[j]<=t if v==0 else U[j]>=t if v==1 else U[j]==t) for j,v in enumerate(w)) and all(w[j]==1 for j,v in enumerate(u) if v>=t),'case-fixed-rational-KKT-'+name)
 ck(D==sum((max(F(),t-v) for v in u),F()) and credit==sum((U[j]-u[j] for j,v in enumerate(w) if v<1),F()),'case-D-and-reduced-credit-'+name)
 ck([str(sum((w[j] for j,s in enumerate(tails) if x in s),F())) for x in range(N)]==a['load_signature'],'case-stored-load-signature-'+name)
ck(report['duplicate_weights_have_same_load_and_mass'] and report['H_plus_free_energy_can_exceed_D'],'two-reported-interface-booleans')
for key in ['H','G','M','load_signature','energy_interval']:ck(cases[8][key]==cases[9][key],'two-decompositions-same-'+key)
ck(cases[8]['credit_sum']=='1/3' and cases[9]['credit_sum']=='1/6','decomposition-credit-upperbound-not-unique')
ck(F(cases[4]['H'])+F(cases[4]['energy_interval'][0])>F(cases[4]['D']),'actual-H-plus-FE-lower-exceeds-D')
ck(F(cases[7]['G'])==100*F(cases[7]['D']) and F(cases[7]['H'])<=F(cases[7]['D']),'G-is-not-root-only-or-D-capped')
l,h=map(F,report['greedy_zero_reentry_interval']);t=F(16,15);ck(0<l<h<F(1,2) and h-l==F(1,2**90),'greedy90-width-positive-below-half')
ck(1/(1+l)+1/(3+l)>=t>=1/(1+h)+1/(3+h) and 1/(1+h)+F(1,2)>t,'greedy-bracket-and-entire-interval-reentry')
final=ob['final_original_globals'];ck([str(l),str(h)]==[final['lo'],final['hi']] and final['t']=='16/15','actual-original-bisection-globals')
M=[[F(v) for v in row] for row in final['M']];wp=list(map(F,final['wp']));gradient=list(map(F,final['gradient']));ck(len(M)==3 and all(len(row)==3 for row in M) and all(sum((a*b for a,b in zip(row,wp)),F())==-1 for row in M),'independent-Gram-linear-solution-certificate')
ck(M==[[F(40409,80802),F(1,4),F(1,4)],[F(1,4),F(20303,80802),F(205,161604)],[F(1,4),F(205,161604),F(20303,80802)]],'all-nine-Gram-entries')
ck(gradient==[F(-4,40401),F(),F()] and sum((a*b for a,b in zip(gradient,wp)),F())==F(final['derivative'])==F(-159964,8445449),'independent-root-gradient-dot-derivative')
ck(report['root_credit_nonmonotonicity']['customers']==208 and report['root_credit_nonmonotonicity']['weight_derivative']==final['wp'] and report['root_credit_nonmonotonicity']['root_credit_derivative']==final['derivative'] and final['U']==['203/201']*3,'separate208-point-report-not-KKT-list')
# Small exact constants support the new domain note and scalar analytic obstruction; no game scan.
ck(F(11,3)<4 and F(2*4,3)+1==F(11,3),'README-s2-exact-static-value-note')
ck(sum((F(1,n*n) for n in range(2,8)),F())>F(1,2),'harmonic-derivative-at-zero-positive-finite-witness')
ck(F(2,3)+F(2,5)==F(16,15) and F(2,3)+F(1,3)<F(16,15),'canonical-greedy-reentry-two-KKT-densities')
comp=read(E/'comparison-manifest.json');ck(len(comp['rows'])==5,'five-full-related-formal-pages')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-raw-'+Path(a['path']).name)
rec=read(W/'semantic-receipts.json');targets=read(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids),'five-complete-primary-receipts')
for a in rec:ck(all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>100 and set(a['targets'])<=set(targets),'complete-semantic-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==62 and len(read(W/'relation-review.json')['relations'])==8,'62-human-math-8-relations')
n=read(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==21913 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'five-next-local-only-availability')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);ck((S/rel).is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
ck(len(stable)==len(set(stable))==3,'three-distinct-stable-objects')
scope=read(E/'scope.json');ck(scope['new_original_entry_calls']==1 and scope['original_failures']==scope['original_retries']==scope['new_EU5191_calls']==scope['new_optimizer_SPE_or_project_calls']==scope['new_data_supplement_calls']==0,'one-new-entry-no-failures-or-old-reruns')
ck(scope['historical_final_review_has_explicit_target_SHA'] is False and scope['current_same_frozen_commit_target_SHA_binding'] is True,'original-vs-current-SHA-identity')
manifest=read(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist')
ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-actual-staged-bytes-C0-excluding-only-LF-TAB-CR')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-files')
v={'status':'pass','scope':'raw/AST/already-supplied rational certificate and linear identities/constants/links/actual C0/whitelist; no original source calls','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':62,'human_relations':8,'new_original_entry_calls':1,'original_failures':0,'new_optimizer_SPE_or_old_EU_calls':0,'new_data_supplement_calls':0,'original_calls_in_selfcheck':0,'C0_scope':'all actual staged file bytes; exclude only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
