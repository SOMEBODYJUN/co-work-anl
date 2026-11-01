#!/usr/bin/env python3
"""Final raw/source/parsed-certificate/links/C0 checks. Never invokes the original."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,ast
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/variational-waterfill-and-switch-debt-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['df7320852ee065441b3c','5655dad77a49cb1cde6f','20e3bbc8751afdd386f5','c7d14f818e6b386ae07b','26b6fb4e568d63e19162'];m=read(E/'source-manifest.json');by={a['id']:a for a in m['rows']};ck(m['source_count']==5 and m['source_bytes']==40688 and set(by)==set(ids),'exact-five-primary40688')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-size-SHA256-blob-'+id)
 ck(all(v['path']==a['source_path'] for v in a['sources']),'frozen-version-path-'+id)
cap=read(W/'claim-evidence.json');g=read(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced','actual-pushed-Boss4-synced')
ck(cap['remote_tip']==g['remote_tip']=='93d728888d63d74d6ad5247e223ac09feae1dcbf','actual93d72888-tip')
ck(set(cap['ids'])==set(g['actual_intersection'])==set(ids) and g['status']=='pass' and g['actual_expected_intersection_count']==5,'exact-five-owner-gate')
ck((W/'claim-evidence.json').read_bytes()==Path('/workspace/scratch/37f0f9248cfc/boss4-r3-next-eu-claim.json').read_bytes() and g['capture_sha256']==sha(W/'claim-evidence.json'),'full-original-capture-bytes')
for a in g['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'source-owner-'+a['id'])
ck(not read(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_found'],'targeted-no-prior-success-record')
ck(read(E/'dependency-manifest.json')['true_runtime_file_inputs']==0,'zero-runtime-file-inputs')
source=S/by[ids[2]]['path'];tr=ast.parse(source.read_text());imports=[a.module for a in ast.walk(tr) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tr) if isinstance(a,ast.Import) for n in a.names]
ck(set(imports)=={'fractions','itertools','pathlib','functools','json'},'pure-stdlib-imports')
ck(not any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tr.body),'original-top-level-no-main-guard')
ck(not any(isinstance(a,ast.Attribute) and a.attr in ('read_text','read_bytes','open') for a in ast.walk(tr)),'no-runtime-file-reads-in-original')
run=read(E/'replay/execution.json');ob=read(E/'replay/passive-observation.json');ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'single-original-success-assertions-on')
ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==sha(source)==run['source_sha256'],'actual-new-relocated-source-SHA')
ck(run['true_runtime_file_inputs']==[] and run['optimizer_project_solver_payoff_verifier_calls']==0 and run['shared_repo_writes_or_network']==0,'zero-input-optimizer-project-network')
out=S/run['output']['path'];frozen=S/by[ids[3]]['path'];ck(run['output']['frozen_byte_equal'] and out.read_bytes()==frozen.read_bytes() and out.stat().st_size==20153,'full20153-output-byte-equal')
ck(sha(out)==run['output']['sha256']==by[ids[3]]['sha256']=='9154b0b5a6910c2b418f9c94d9341ed2a05a21d32b7091b818f59a893ef44217','actual-output-SHA')
ck(run['stdout_bytes']==(E/'replay/stdout.txt').stat().st_size==165 and run['stderr_bytes']==(E/'replay/stderr.txt').stat().st_size==0,'stdout165-stderr0')
stdout=json.loads((E/'replay/stdout.txt').read_text());ck(stdout['KKT_certificates']==14 and stdout['largest_unit_instance']==208,'stdout-summary14-208')
for k,v in {'<module>':1,'certificate':14,'L':4658,'c':9055,'U':38,'Q':526,'R':28,'B':28,'V':73,'log_bounds':8}.items():ck(ob['function_calls'][k]==v,'actual-function-'+k+'-'+str(v))
ck(ob['observer_extra_original_calls']==0,'observer-no-extra-source-calls')
ck(ob['log_bounds_actual_uncached_q']==['2','4/3','1','3/2','8/7','101/100','202/201','403/402'],'eight-uncached-q-values')
ck(ob['conditional_V_initial_ge_tn_executed_names']==['initial_equal_high_preserved','aggregate_high_low_joint','no_tails'],'actual-three-conditional-profit-assertions')
node=next(a for a in ast.walk(tr) if isinstance(a,ast.If) and 'V(one)' in ast.unparse(a.test));ck(node.body[0].lineno==ob['conditional_V_initial_ge_tn_assertion_line']==73,'actual-original-conditional-line73')
logfun=next(a for a in tr.body if isinstance(a,ast.FunctionDef) and a.name=='log_bounds');ck('terms = 80' in ast.unparse(logfun) and 'remainder' in ast.unparse(logfun),'80-term-original-log-bound')
report=read(frozen);cases=report['cases'];fixtures=ob['embedded_original_fixture_arguments'];returns=ob['certificate_returns'];ck(report['status']=='pass' and len(cases)==len(fixtures)==len(returns)==14,'all-fourteen-original-certificates')
ck(sum(a['query_count'] for a in cases[:13])==35 and sum(a['query_count'] for a in cases)==249,'small35-total249-query-list-entries')
ck(cases[-1]['unit_customers']==returns[-1]['N']==208 and returns[-1]['query_entries']==214 and returns[-1]['distinct_query_sets']==213,'large208-list214-distinct213')
ck(all(a['query_entries']==a['distinct_query_sets']==2**a['N'] for a in returns[:13]),'small-thirteen-full-subset-lists')
conditional=[]
for a,b,r in zip(cases,fixtures,returns):
 name=a['name'];t=F(a['t']);w=list(map(F,a['w']));ui=list(map(F,a['u_initial']));uf=list(map(F,a['u_final']));n=len(w);M=F(a['mass']);loss=F(a['mass_loss']);D=F(a['D']);delta=F(a['sum_reduced_unit_increase']);H=F(a['H']);gamma=F(a['root_gain']);db=F(a['background_gain']);stretch=F(a['stretch']);lo=F(a['free_energy_lower']);hi=F(a['free_energy_upper']);V0=sum(ui,F());V1=sum((x*y for x,y in zip(w,uf)),F())
 ck(len(a)==18 and name==b['name']==r['name'] and a['unit_customers']==len(b['N'])==r['N'] and t==F(b['t'])>0,'case-version-and18fields-'+name)
 ck(all(0<=v<=1 for v in w) and all((uf[j]<=t if v==0 else uf[j]>=t if v==1 else uf[j]==t) for j,v in enumerate(w)),'case-full-KKT-'+name)
 ck(all(w[j]==1 for j,u in enumerate(ui) if u>=t),'case-initial-high-retained-'+name)
 ck(D==sum((max(F(),t-u) for u in ui),F()) and delta==sum((uf[j]-ui[j] for j,v in enumerate(w) if v<1),F()) and 0<=H<=delta<=D,'case-common-credit-'+name)
 ck(M==sum(w,F()) and loss==n-M and stretch==sum(((1-v)*uf[j] for j,v in enumerate(w)),F())<=t*loss==F(a['t_mass_loss']),'case-stretch-and-mass-'+name)
 ck(gamma>=0 and db>=0 and gamma+db+V1==V0 and gamma+db+t*M<=V0,'case-original-mass-profit-budget-'+name)
 ck(0<=lo<=hi<=D and max(H,gamma+db)+hi+t*M<=t*n,'case-FE-and-max-JOINT-'+name)
 if V0>=t*n:
  conditional.append(name);ck(max(H,gamma+db)+hi+t*M<=V0,'case-conditional-original-profit-'+name)
ck(conditional==ob['conditional_V_initial_ge_tn_executed_names'],'parsed-conditional-domain-matches-real-line-events')
dup=cases[7:10];ck([a['w'] for a in dup]==[['1/2','1/2'],['1','0'],['0','1']],'three-duplicate-weight-decompositions')
for k in ['H','mass','mass_loss','stretch','free_energy_lower','free_energy_upper','root_gain','background_gain']:ck(len({a[k] for a in dup})==1,'duplicate-same-canonical-'+k)
ck([a['sum_reduced_unit_increase'] for a in dup]==['1/3','1/6','1/6'],'duplicate-reduced-increase-not-unique')
empty=next(a for a in cases if a['name']=='empty_tail');ck(empty['unit_customers']==0 and empty['H']=='0' and empty['free_energy_lower']==empty['free_energy_upper']=='1','emptyN-positive-FE-no-free-original-profit')
non=cases[-1];ck(non['u_initial']==['205/303','1018/1209','1018/1209'] and non['u_final']==['203/201']*3 and non['D']=='5475310/8181303' and non['H']=='5497019/32725212' and non['root_gain']=='1/20301' and non['background_gain']=='13836701/16362606','nonmonotone-exact-fixed-state')
dx=F(1,4);dy=F(205,402**2);du=F(4,201**2);det=(2*dx+du)*(dx+2*dy)-2*dx*dx;ap=(dx-2*dy)/det;bp=-(dx+du)/det;rp=-du*ap;mp=ap+2*bp
ck(det==F(8445449,6528963204)>0 and ap==F(1615676391,8445449)>0 and bp==F(-1632887217,8445449)<0,'exact-positive-Jacobian-and-weight-derivatives')
ck(rp==F(-159964,8445449)<0 and mp==F(-1650098043,8445449)<0,'exact-negative-root-and-mass-derivatives')
rd=report['nonmonotone_derivatives'];ck(rd=={'determinant':str(det),'w1_prime':str(ap),'w2_prime':str(bp),'root_credit_prime':str(rp),'mass_prime':str(mp)},'all-five-report-derivatives')
ck(ob['nonmonotone_original_globals']['root_prime']==str(rp) and ob['nonmonotone_original_globals']['mass_prime']==str(mp),'real-original-derivative-globals')
comp=read(E/'comparison-manifest.json');ck(len(comp['rows'])==4,'four-full-related-formal-pages')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-raw-'+Path(a['path']).name)
rec=read(W/'semantic-receipts.json');targets=read(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids),'five-complete-primary-receipts')
for a in rec:ck(all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>100 and set(a['targets'])<=set(targets),'complete-semantic-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==65 and len(read(W/'relation-review.json')['relations'])==9,'65-human-math-9-relations')
n=read(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==35222 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'five-next-local-only-availability')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+k+':',parts[1],re.M) is not None,'MATEK-'+k+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);ck((S/rel).is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
ck(len(stable)==len(set(stable))==4,'four-distinct-stable-objects')
scope=read(E/'scope.json');ck(scope['new_original_entry_calls']==1 and scope['original_failures']==scope['original_retries']==scope['new_optimizer_or_SPE_or_project_calls']==scope['new_old_waterfill_34_53_audit_calls']==scope['new_data_supplement_calls']==0,'one-new-entry-no-extra-original-or-solver')
manifest=read(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist')
ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-actual-staged-bytes-C0-exclude-only-LF-TAB-CR')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-files')
v={'status':'pass','scope':'read-only raw/AST/existing rational certificate fields/derivative algebra/links/actual C0/whitelist; no original function calls','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':4,'primary_receipts':5,'human_math_items':65,'human_relations':9,'new_original_entry_calls':1,'original_failures':0,'new_optimizer_SPE_or_old_audit_calls':0,'new_data_supplement_calls':0,'original_calls_in_selfcheck':0,'C0_scope':'actual bytes of every staged file; exclude only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
