#!/usr/bin/env python3
"""Read-only bytes/AST/already-observed finite certificates/links/C0; no source calls."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib,re
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');BASE=R.parent/'boss4-next-cache';GI=BASE/'r3-waterfill-credibility-and-uniform-contraction-primary';GR=BASE/'r3-uniform-contraction-and-credibility-relay-primary';E=S/'archives/customer-attraction/tools/evidence/general-contraction-review-and-vertical-br-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['9c9fa33a34f4f7cb19ca','91582e274236e69c5c53','22b55891724b6ab6ce39','d92f11639c1df0e88da1','3164d9a2699689c8c3c2'];sm=j(E/'source-manifest.json');by={a['id']:a for a in sm['rows']};ck(sm['source_count']==5 and sm['source_bytes']==22433 and set(by)==set(ids),'five-full-primary22433')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-sizeSHA256blob-'+id);ck(all(x['path']==a['source_path'] for x in a['sources']),'full-source-frozen-path-'+id)
cap=j(W/'claim-evidence.json');gate=j(W/'primary-authorization-check.json');recovery=j(W/'claim-sync-preservation.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['remote_tip']==gate['remote_tip']=='7891451cbd07d36981ec193061e5107a20dbddd8','actual-pushed-7891451')
ck(cap['local_sync']['status']==gate['original_capture_local_sync_status']=='needs-attention' and gate['status']=='pass' and 'separately verified' in gate['authorization_basis'],'unchanged-needs-attention-plus-independent-Root-recovery')
ck(len(cap['ids'])==gate['actual_claim_count']==23 and set(ids)<=set(cap['ids']) and set(gate['actual_intersection'])==set(ids),'five-subset-full23-capture')
ck((W/'claim-evidence.json').read_bytes()==(R.parent/'boss4-r3-next-gv-claim.json').read_bytes() and sha(W/'claim-evidence.json')==gate['capture_sha256'],'full-original23-capture-unaltered')
ck((W/'claim-sync-preservation.json').read_bytes()==(BASE/'boss4-r3-next-gu-to-gy-atomic-claim-sync-preservation.json').read_bytes() and sha(W/'claim-sync-preservation.json')==gate['recovery_sha256'],'independent-preservation-report-unaltered')
ck(recovery['stash']=='aad9b887a8a70fc30fb8cb633bc074f76de9d437' and recovery['untracked_count']==2 and recovery['missing']==recovery['different']==[] and recovery['unmerged']=='' and len(recovery['tracked'])==2 and all(a['same'] for a in recovery['tracked']),'Root-2untracked2tracked-all-same0missing0different0unmerged')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'owner-and-sourceSHA-'+a['id'])
stop=j(W/'initial-claim-gate-stop.json');ck(stop['status']=='stopped-before-original-entry' and stop['exception']=='AssertionError' and stop['original_source_entry_calls']==stop['original_source_functions']==0 and (S/stop['initial_gate_script']).is_file(),'initial-strict-synced-gate-stop-zero-source-calls-preserved')
search=j(W/'pre-execution-search.json');ck(search['successful_same_sha_execution_records']==[] and search['historical_target_bytes_materialized'] is False and search['no_network_or_reconstruction'],'no-prior-sameSHA-success-no-missing-old-target-reconstruction')
d=j(E/'dependency-manifest.json');dep=d['uniform5155'];ck(dep['real_runtime_file_inputs']==1 and dep['input_bytes']==14339 and d['vertical919']['real_runtime_file_inputs']==0,'real-one-MD14339-versus-zero-inputs')
a=dep['rows'][0];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size']==14339 and sha(p)==a['sha256']==dep['available_current_target_sha256']=='f0a1235e3aad55acb1eb020cf0989198c36dc37a2e0588ee227814d9eef24a7d' and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'current-author-target-exact14339f0a-bytes')
old='1d150d7dff2d832d90591c9079f01ea8f986163f07fd817f6d794870247785d5';ck(dep['frozen_report_historical_target_sha256']==old and dep['historical_target_bytes_found'] is False and dep['historical_target_not_reconstructed'],'missing-historical1d150-identity-not-pretended-current')
context=j(E/'context-manifest.json');ck(len(context['rows'])==2 and context['primary_dispositions_not_claimed_for_context'],'two-context-read-only-not-primary-done')
for a in context['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'context-byte-hash-'+a['id'])
rs={};obs={};reports={}
for kind,codeid,outid,ninputs,nbytes,stdbytes in [('uniform',ids[1],ids[2],1,14339,232),('vertical',ids[3],ids[4],0,0,526)]:
 code=S/by[codeid]['path'];tr=ast.parse(code.read_text());mods=[x.module for x in ast.walk(tr) if isinstance(x,ast.ImportFrom)]+[n.name for x in ast.walk(tr) if isinstance(x,ast.Import) for n in x.names];ck(set(mods)<={'fractions','itertools','pathlib','json','hashlib'} and 'fractions' in mods,'stdlib-only-no-original-import-'+kind)
 ck(not any(isinstance(x,ast.If) and '__name__' in ast.unparse(x.test) for x in tr.body),'no-main-guard-all-top-level-'+kind)
 if kind=='uniform':ck(len([x for x in ast.walk(tr) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='read_bytes'])==1,'single-author-text-read_bytes-for-final-hash-only')
 run=j(E/('replay-'+kind)/'execution.json');ob=j(E/('replay-'+kind)/'passive-observation.json');rs[kind]=run;obs[kind]=ob;ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'one-raw-original-success-assertions-on-'+kind)
 ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==run['source_sha256']==by[codeid]['sha256'],'raw-source-bytes-relocated-'+kind)
 ck(run['input_bytes_unchanged'] and len(run['true_runtime_file_inputs'])==ninputs and sum(a['size'] for a in run['true_runtime_file_inputs'])==nbytes,'actual-input-countbytes-'+kind)
 for a in run['true_runtime_file_inputs']:ck((S/a['runtime_path']).stat().st_size==a['size'] and sha(S/a['runtime_path'])==a['sha256'],'runtime-dependency-bytes-'+kind)
 out=S/run['output']['path'];ck(out.stat().st_size==run['output']['size']==by[outid]['size'] and sha(out)==run['output']['sha256'] and run['output']['frozen_sha256']==by[outid]['sha256'],'new-output-size-SHA-original-frozenSHA-'+kind);reports[kind]=j(out)
 ck(run['stdout_bytes']==(E/('replay-'+kind)/'stdout.txt').stat().st_size==stdbytes and run['stderr_bytes']==(E/('replay-'+kind)/'stderr.txt').stat().st_size==0,'real-stdout-stderr-'+kind)
 ck(ob['original_module_calls']==1 and ob['original_main_calls']==0 and ob['observer_extra_original_calls']==run['observer_extra_original_calls']==run['other_original_entry_calls']==run['network_or_shared_repo_writes']==0,'module1-main0-no-extra-original-calls-'+kind)
 ck(ob['final_original_values']['out']==reports[kind],'actual-final-original-out-versus-generated-report-'+kind)
 writes=[x for x in ob['observed_local_opens'] if x['mode']=='w'];ck(len(writes)==1 and Path(writes[0]['path'])==out.resolve(),'only-one-new-write_text-output-'+kind)
for k,n in {'check_family':7,'pay':2493,'K':1464,'density':812,'pool':63}.items():ck(obs['uniform']['function_calls'][k]==n,'observed-uniform-source-calls-'+k+'-'+str(n))
ck(obs['vertical']['function_calls']['payoff']==12,'observed-vertical-payoff12-local-only')
u=reports['uniform'];v=reports['vertical'];frozen=j(S/by[ids[2]]['path']);ck(rs['uniform']['output']['frozen_byte_equal'] is False and u['source_sha256']==dep['available_current_target_sha256'] and frozen['source_sha256']==old,'new-report-not-frozen-byte-equal-distinct-targets')
ck(rs['uniform']['output']['json_differences']==[{'json_pointer':'/source_sha256','frozen':old,'new':dep['available_current_target_sha256']}] and {k:x for k,x in u.items() if k!='source_sha256'}=={k:x for k,x in frozen.items() if k!='source_sha256'},'exact-one-field-target-hash-diff-all-numeric-data-identical')
ck(sha(S/rs['uniform']['output']['path'])=='dfa6ac1d63f2e178fd5d5535e802d6cd42777cb817321775fa3c17b662e55fba','actual-new5403-dfa6ac-not-oldb72')
ri=rs['uniform']['true_runtime_file_inputs'][0];ck(sum(a['path']==str((S/ri['runtime_path']).resolve()) and a['mode']=='r' for a in obs['uniform']['observed_local_opens'])==1,'author-MD-open-exactly-once-at-final-hash')
ck(rs['vertical']['output']['frozen_byte_equal'] and not rs['vertical']['output']['json_differences'] and (S/rs['vertical']['output']['path']).read_bytes()==(S/by[ids[4]]['path']).read_bytes(),'vertical526-whole-frozen-byte-identical')
ck(u['local_identity_checks']==27 and len(u['cases'])==7 and len(u['zero_fresh_boundary'])==3,'seven-families-three-zero-fresh27-parameter-combinations')
sumcomparisons=0;sumhist=0
for index,a in enumerate(u['cases']):
 n=a['n'];b=list(map(F,a['core_background']));lo,hi=F(a['water_lambda_lower']),F(a['water_lambda_upper']);hist=2**n-1;count=hist*3*2;sumhist+=hist;sumcomparisons+=count
 ck(a['a_star']=='1' and F(a['S'])==F(n*n,(n+1)**2)<1 and a['all_history_comparisons']==count,'family-count-S-astar-'+str(index))
 ck(0<lo<=hi<=1 and hi-lo==F(1,2**110),'family110step-positive-no-zero-eval-'+str(index))
 def K(w):return sum((1/(x+n*w) for x in b),F())
 target=1+K(F(1))+F(1,3);glo=1/lo+K(lo);ghi=1/hi+K(hi);pool=n*(1/(1+n*lo)-F(1,n+1))+K(lo)-K(F(1))
 ck(glo>=target>=ghi and F(a['H_upper'])==pool<F(1,3)==F(a['minimum_deficit'])<=F(a['total_deficit'])==F(n,3),'family-bracket-conservative-H-and-deficits-'+str(index))
 ck(pool<=F(a['S'])*(1/lo-1)+K(lo)-K(F(1)),'family-common-pool-spectral-chain-'+str(index))
 for weight in [F(1),F(3,4),lo,hi]:
  Gamma=K(weight)-K(F(1));oldreturn=sum(((x-1)*(1/(x+n*weight)-1/(x+n)) for x in b),F());V=n+n*weight*K(weight);V1=n+n*K(F(1));ck(Gamma+oldreturn+V==V1 and V-n*weight*target==n*weight*(1/weight+K(weight)-target),'family-fourpoint-once-budget-signed-residual-'+str(index)+'-'+str(weight))
 if not b:ck(hi==F(3,4) and lo<F(3,4) and F(n*n,(n+1)*(3*n+4))<F(1,3) and pool>=F(n*n,(n+1)*(3*n+4)),'no-core-exact-threequarter-versus-conservative-lo-'+str(index))
 if index<6:ck(b in [[],[F(1),F(1)]] and a['scope']=='legal original CAG prefix','six-legal-empty-old-prefix-core1-'+str(index))
 else:ck(n==3 and b==[F(1),F(3),F(7)] and 'not a same-catalog' in a['scope'],'heterogeneous-core-1-3-7-frozen-not-legal')
ck(sumcomparisons==1662 and sumhist==277 and [a['all_history_comparisons'] for a in u['cases']]==[6,6,42,42,762,762,42],'1662-exact277-histories-times6')
ck(obs['uniform']['function_calls']['pay']==sumhist*3*3,'pay2493-three-requests-per-history-not1662-ICs')
for i,a in enumerate(u['zero_fresh_boundary']):
 n=a['n'];b=list(map(F,a['b']));K0=sum((1/x for x in b),F());K1=sum((1/(x+n) for x in b),F());target=(K0+K1)/2;lo,hi=F(a['lambda_lower']),F(a['lambda_upper']);ck(F(a['K0'])==K0>F(a['K1'])==K1 and F(a['interior_target'])==target and 0<lo<hi<1 and hi-lo==F(1,2**110),'zero-fresh-three-interior110bit-'+str(i))
 ck(sum((1/(x+n*lo) for x in b),F())>=target>=sum((1/(x+n*hi) for x in b),F()) and target-K1<=n*(target-K1),'zero-fresh-root-credit-'+str(i))
ck([(a['n'],a['b'],a['interior_target']) for a in u['zero_fresh_boundary']]==[(1,['1'],'3/4'),(3,['1'],'5/8'),(3,['1','3'],'7/8')],'three-distinct-pure-core-boundaries')
ck('lambda=1 for t=0' in u['empty_core_zero_fresh'] and 'no positive-mass guarantee for t>0' in u['empty_core_zero_fresh'],'empty-core-no-fresh-trivial-threshold-only')
for a in v:
 m=a['M'];ck(a['current']==[str(m),str(m)] and a['ancestor']==[str(m),str(2*m)] and a['current_difference']=='0' and a['ancestor_difference']==str(m),'vertical-four-exact-values-M'+str(m))
 ck(F(2*m,2)==F(m) and F(m,1)==F(m) and F(2*m,1)==2*m and m>0,'vertical-all-M-counting-current-tie-ancestor-positive-'+str(m))
 ck(F(2*m,3*m)==F(2,3)>F(1,2) and F(3*m,3*m)==1,'two-analytic-full-SPE-coverages-not-half-counterexample-M'+str(m))
ck([a['M'] for a in v]==[1,2,7] and len(v)==3,'only-three-finite-M-in-source-not-all-M-run')
comp=j(E/'comparison-manifest.json');ck(len(comp['rows'])==5,'five-full-related-proof-snapshots')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'comparison-raw-'+Path(a['path']).name)
rec=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids) and all(a['disposition']=='integrated' for a in rec),'five-final-semantic-integrated-receipts')
for a in rec:ck(a['source_sha256']==by[a['id']]['sha256'] and all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>=100 and set(a['targets'])<=set(targets) and a['publication_status'].startswith('external stage only'),'full-read-comparison-unique-decision-publication-separate-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==74 and len(j(W/'relation-review.json')['relations'])==7,'74-math7-semantic-relations')
n=j(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==23399 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'next-five23399-local-only-root-remote-recheck')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);roots=[root for root in [S,R,GI,GR] if (root/rel).is_file()];ck(bool(roots),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel),'resolved_at':str(roots[0]),'mature-package-only-not-publication-claim':not (S/rel).is_file() and not (R/rel).is_file()})
ck(len(stable)==len(set(stable))==3,'three-distinct-stable-objects')
scope=j(E/'scope.json');ck(scope['uniform5155_original_entry_calls']==scope['vertical919_original_entry_calls']==1 and scope['old_original_replays']==scope['source_functions_added_by_observer']==scope['network_or_shared_git_writes']==0 and scope['uniform_new_vs_frozen_changed_fields']==['/source_sha256'] and scope['vertical_source_root_SPE_checks']==0 and scope['vertical_full_two_player_SPE_extension_is_analytic_not_original_run'],'actual-one-each-with-exact-different-target-and-analytic-root-extension')
manifest=j(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-whitelist');ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-actual-staged-C0-bytes-excluding-only-LF-TAB-CR')
ck(all(not any(line.rstrip(b' \t')!=line for line in (S/f).read_bytes().split(b'\n')) for f in manifest if f.endswith(('.py','.md','.json'))),'all-text-no-trailing-whitespace')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda z:(_ for _ in ()).throw(ValueError(z)))
ck(True,'strict-finite-JSON-all-staged')
v={'status':'pass','scope':'read-only raw/AST/already-observed seven family/three boundary/three local-M reports and scalar arithmetic/links/C0; no original execution','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':74,'human_relations':7,'uniform_original_entry_calls':1,'vertical_original_entry_calls':1,'original_source_functions_in_selfcheck':0,'preflight_strict_gate_source_entry_calls':0,'original_claim_sync':'needs-attention unchanged','Root_independent_recovery_preserved':True,'general_report_exact_changed_fields':['/source_sha256'],'vertical_frozen_bytes_equal':True,'C0_scope':'actual bytes of all staged files excluding only LF/TAB/CR'};(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
