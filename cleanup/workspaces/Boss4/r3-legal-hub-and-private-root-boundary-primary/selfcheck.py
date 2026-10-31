#!/usr/bin/env python3
"""Read-only raw/AST/observed hub report and small type/data identities; no original calls.
Writes only the selfcheck and the explicitly data-only certificate, never runs IC/OPT scans.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,ast,re
W=Path(__file__).resolve().parent;S=W.parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/legal-hub-and-private-root-boundary-primary';checks=[]
def ck(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bad(p):return [(i,b) for i,b in enumerate(p.read_bytes()) if b<32 and b not in (9,10,13)]
ids=['67654e634d4590492795','07d70be3c03ed289eb7b','6297dd1198e26059e5c8','12a6ad47fe898772312f','87885d84446f6f6a7100'];sm=j(E/'source-manifest.json');by={a['id']:a for a in sm['rows']};ck(sm['source_count']==5 and sm['source_bytes']==23399 and set(by)==set(ids),'five-full-primary23399')
for id in ids:
 a=by[id];p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'raw-sizeSHA256blob-'+id);ck(all(x['path']==a['source_path'] for x in a['sources']),'exact-frozen-source-path-'+id)
cap=j(W/'claim-evidence.json');gate=j(W/'primary-authorization-check.json');ck(cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced' and cap['remote_tip']==gate['remote_tip']=='87e9a6366207a3f5ece007adc436eb91b51aa021','actual-pushed-synced-87e9a6')
ck(set(cap['ids'])==set(gate['actual_intersection'])==set(ids) and gate['actual_claim_count']==gate['source_count']==5 and gate['status']=='pass','exact-five-owner-gate')
ck((W/'claim-evidence.json').read_bytes()==(R.parent/'boss4-r3-next-gz-claim.json').read_bytes() and sha(W/'claim-evidence.json')==gate['capture_sha256'],'original-full-capture-unaltered')
for a in gate['ownership_records']:ck(a['record']['owner']=='Boss4' and a['record']['disposition']=='in-progress' and a['record']['source_sha256']==by[a['id']]['sha256'],'actual-ownerSHA-'+a['id'])
ck(j(W/'pre-execution-same-sha-search.json')['successful_same_sha_execution_records']==[],'no-prior-success-on-exact-hub-sourceSHA')
d=j(E/'dependency-manifest.json');ck(d['claimed_hub2381']['runtime_file_inputs']==0 and d['claimed_hub2381']['pivot_checked']=='future[-1] only' and d['root6484_primary_is_manuscript_only']['related6714_code_read_full_but_not_executed'],'claimed-zero-file-inputs-last-pivot-and-related-root-only-reading')
tr=ast.parse((S/by[ids[2]]['path']).read_text());mods=[a.module for a in ast.walk(tr) if isinstance(a,ast.ImportFrom)]+[n.name for a in ast.walk(tr) if isinstance(a,ast.Import) for n in a.names];ck(set(mods)=={'fractions','itertools','json','pathlib'},'only-stdlib-no-SPE-or-author-import')
ck(any(isinstance(a,ast.If) and '__name__' in ast.unparse(a.test) for a in tr.body),'hub-main-guard')
run=j(E/'replay-hub/execution.json');ob=j(E/'replay-hub/passive-observation.json');ck(run['status']=='success' and run['exit_code']==0 and run['original_entry_calls']==1 and run['optimize']==0,'one-original-hub-success-assertions-on')
ck(run['new_empty_replay'] and run['source_absolute_path_is_relocated'] and run['source_bytes_unchanged'] and sha(S/run['runtime_entry'])==run['source_sha256']==by[ids[2]]['sha256'],'original-raw-source-relocated')
ck(run['true_runtime_file_inputs']==[] and run['observer_extra_original_calls']==run['root_regret6714_original_entry_calls']==run['SPE_BI_or_optimizer_calls']==run['other_original_replays']==run['network_or_shared_repo_writes']==0,'zero-inputs-no-other-source-or-SPE-calls')
output=S/run['output']['path'];ck(run['output']['frozen_byte_equal'] and output.read_bytes()==(S/by[ids[3]]['path']).read_bytes() and output.stat().st_size==run['output']['size']==359 and sha(output)==run['output']['sha256']==by[ids[3]]['sha256'],'359-entire-output-frozen-byte-equal')
ck(run['stdout_bytes']==(E/'replay-hub/stdout.txt').stat().st_size==360 and (E/'replay-hub/stdout.txt').read_bytes()==output.read_bytes()+b'\n' and run['stderr_bytes']==(E/'replay-hub/stderr.txt').stat().st_size==0,'stdout360-print-payload-extra-LF-and-stderr0')
ck(ob['function_calls']['<module>']==ob['function_calls']['main']==1 and ob['observer_extra_original_calls']==0,'actual-module-main-one-no-observer-extra-calls')
report=j(output);final=ob['final_original_values'];ck(final['report']==report and final['total']==report['identity_checks']==8*8*(8+64+512)==37376 and final['hub_hypotheses']==report['hub_protection_checks']==8791 and final['unanimous']==report['unanimous_tail_checks']==945,'actual-observed37376-8791-945-exact-finite-domain')
ck(0<945<=8791<=37376 and 'No general existence' in report['limitations'] and 'no SPE counterexample' in report['limitations'],'finite-report-limits-not-existence-or-equilibrium')
ck(len([a for a in ob['observed_local_opens'] if a['mode']=='x'])==1 and all(Path(a['path']).name in ['audit_hub_relay.py','hub_relay_audit.json'] for a in ob['observed_local_opens']),'observed-source-and-one-exclusive-output-no-input-file')
cm=j(E/'context-manifest.json');ctx={a['id']:a for a in cm['rows']};ck(len(ctx)==5 and cm['context_only_not_primary_done'] and cm['root_regret6714_original_entry_calls']==0 and cm['root4803_frozen_report_not_current_execution'],'five-related-context-raw-not-done-or-executed')
for a in ctx.values():
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['blob'],'context-sizeSHAblob-'+a['id'])
I=j(S/ctx['0ebc828733fab492d2a5']['path']);P=j(S/ctx['2cd505cd05ed8ab77f21']['path']);old=j(S/ctx['464a4071ed64844f3709']['path']);policy={tuple(a['history']):a['action'] for a in P['actions']};types=[frozenset(a['topics']) for a in I['customers']];multiplicities=[a['multiplicity'] for a in I['customers']];alltypes=types+[frozenset(range(7))];N=sum(multiplicities);ck(N==53 and len(types)==14 and len(policy)==400,'context-original53-14types-400keys-no-IC-scan')
expected=((0,6,3,4),(1,6,3,4),(2,6,3,4),(3,6,0,1),(4,6,0,1),(5,6,0,1),(6,0,3,4));paths=[]
for root in range(7):
 h=(root,)
 while len(h)<4:h=h+(policy[h],)
 paths.append(h)
ck(tuple(paths)==expected,'seven-true-source-paths-by-only-data-lookups-not-BI')
ck(all(any(t in c for t in (0,2,5,6)) for c in alltypes),'fixed-four-support-covers-all15types-no210-search')
expected_missing=[{4,32},{4,32},{32},{4,32},{4,32},{4},{4,32}];records=[];typechecks=0
for root,z in enumerate(paths):
 absent=[];coverlist=[]
 for c in alltypes:
  mask=sum(1<<t for t in c);covered=any(t in c for t in z);coverlist.append({'mask':mask,'covered':covered});typechecks+=1
  if not covered:ck(c in [frozenset([2]),frozenset([5])],'only-global-private-omitted-type-root'+str(root)+'-mask'+str(mask));absent.append(mask)
 ck(set(absent)==expected_missing[root],'all-multiplicity-coverage-identity-root'+str(root))
 utility=[sum((F(mult,sum(a in c for a in z)) for c,mult in zip(types,multiplicities) if z[who] in c),F()) for who in range(4)];welfare=sum(mult for c,mult in zip(types,multiplicities) if any(a in c for a in z));ck(sum(utility)==welfare,'root-point-share-sum-is-coverage-'+str(root))
 oldrow=old['root_plans'][root];ck(oldrow['actual_path']==list(z) and oldrow['actual_payoffs']==list(map(str,utility)) and oldrow['welfare']==welfare and set(oldrow['omitted_interest_masks'])==set(absent),'related-frozen-report-data-scalar-match-root'+str(root))
 records.append({'root':root,'path':list(z),'type_coverage':coverlist,'omitted_masks':absent,'point_utilities':list(map(str,utility)),'point_welfare':welfare})
ck(typechecks==105 and old['targeted_typewise_root_checks_including_added_core_type']==105 and old['positive_depth_complete_histories']==399 and old['positive_depth_action_comparisons']==2793 and old['optimal_multisets_checked_at_source_point']==210,'105-new-type-identities-old3992793210-only-historical-coverage')
rootvalues=[F(a['point_utilities'][0]) for a in records];ck(rootvalues==[F(29,3)]*6+[F(19)],'point-forced-root-values-no-root-IC-certification')
for a in records:
 i=a['root'];us=list(map(F,a['point_utilities']));Wpoint=a['point_welfare'];delta=max(rootvalues)-us[0];margin=N-2*Wpoint-3*delta;D=N-Wpoint;oldrow=old['root_plans'][i];ck(str(delta)==oldrow['root_regret'] and str(margin)==oldrow['OPT_minus_2W_minus_3regret'] and D==oldrow['private_omissions'],'point-Delta-margin-omission-scalars-'+str(i))
 ck(D<=us[2]+us[3] and N<=2*Wpoint-us[0]-us[1] and margin<=-us[0]-us[1]-3*delta,'point-specialized-private-budget-not-general-SPE-test-'+str(i));a['point_Delta']=str(delta);a['point_margin']=str(margin)
ck([a['point_welfare'] for a in records]==[51,51,52,51,51,52,51] and [a['point_margin'] for a in records]==['-77','-77','-79','-77','-77','-79','-49'],'all-seven-concrete-welfare-and-margins')
certificate={'status':'pass-small-data-only-type-identities-and-point-scalars','source_original_entry_calls':0,'root_regret6714_original_entry_calls':0,'SPE_IC_scans':0,'OPT_multiset_searches':0,'fixed_support_cover_proves_source_point_OPT_equals53':True,'type_identity_count':105,'input_hashes':{Path(ctx[id]['source_path']).name:ctx[id]['sha256'] for id in ['0ebc828733fab492d2a5','2cd505cd05ed8ab77f21','464a4071ed64844f3709']},'type_basis_directions_not_asserted_SPE_feasible':True,'all_multiplicity_theorem_depends_on_positive_depth_SPE_and_private_spectrum_proof':True,'records':records};(E/'data-type-and-root-scalar-check.json').write_text(json.dumps(certificate,ensure_ascii=False,indent=2)+'\n')
comp=j(E/'comparison-manifest.json');ck(len(comp['rows'])==7,'seven-current-related-formal-snapshots')
for a in comp['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'],'related-formal-raw-'+Path(a['path']).name)
rec=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(rec)==5 and {a['id'] for a in rec}==set(ids) and all(a['disposition']=='integrated' for a in rec),'five-final-semantic-integrated-receipts')
for a in rec:ck(a['source_sha256']==by[a['id']]['sha256'] and all(a[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and min(len(a[k]) for k in ['read_note','comparison_note','decision_note'])>=100 and set(a['targets'])<=set(targets) and a['publication_status'].startswith('external stage only'),'full-read-related-unique-decision-publication-separate-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('[x]')==79 and len(j(W/'relation-review.json')['relations'])==9,'79-math9-semantic-relations')
n=j(W/'next-candidates.json');ck(n['count']==5 and n['total_bytes']==40285 and all(not a['local_progress_exists'] and 'Root' in a['availability_scope'] for a in n['rows']),'next-five40285-local-only-no-owner-promise')
links=[];stable=[]
for f in targets:
 p=S/f;text=p.read_text();parts=text.split('---',2);ck(len(parts)==3,'flat-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search('^'+key+':',parts[1],re.M) is not None,'MATEK-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not bad(p),'actual-canonical-C0-'+p.name);ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'no-placeholder-'+p.name)
 for raw in re.findall(r'\]\(([^)]+)\)',text):
  if raw.startswith(('http','source:','#')):continue
  rel=(p.parent/raw.split('#')[0]).resolve().relative_to(S);ck((S/rel).is_file() or (R/rel).is_file(),'formal-link-'+str(len(links)));links.append({'from':f,'to':str(rel)})
ck(len(stable)==len(set(stable))==3,'three-distinct-stable-objects')
scope=j(E/'scope.json');ck(scope['hub2381_original_entry_calls']==1 and scope['root_regret6714_original_entry_calls']==scope['restricted_graph2920_original_entry_calls']==scope['old_original_replays']==scope['source_functions_added_by_observer']==scope['network_or_shared_git_writes']==0 and scope['new_selfcheck_type_identities']==105 and scope['new_selfcheck_SPE_or_OPT_scans']==0 and scope['general_shared_omission_payment_proved'] is False,'one-local-original-zero-related-or-old-replays-no-fake-general-budget')
manifest=j(W/'copy-files.json');actual=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());ck(manifest==actual==sorted(manifest) and len(manifest)==len(set(manifest)),'exact-sorted-self-inclusive-copy-whitelist');ck(all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in manifest),'safe-relative-copy-paths');ck(all(not bad(S/f) for f in manifest),'all-staged-actual-C0-bytes-except-only-LF-TAB-CR')
ck(all(not any(line.rstrip(b' \t')!=line for line in (S/f).read_bytes().split(b'\n')) for f in manifest if f.endswith(('.py','.md','.json'))),'all-text-no-trailing-space-tab')
for f in manifest:
 if f.endswith('.json'):json.loads((S/f).read_text(),parse_constant=lambda z:(_ for _ in ()).throw(ValueError(z)))
ck(True,'strict-finite-JSON-all-staged')
v={'status':'pass','scope':'raw/AST/already-observed local hub report and small type105/root7 data scalar checks/links/C0; no source execution or IC/OPT scans','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'human_math_items':79,'human_relations':9,'hub_original_entry_calls':1,'related_root6714_or_graph2920_calls':0,'original_source_functions_in_selfcheck':0,'data_type_identity_checks':105,'data_root_point_rows':7,'SPE_IC_or_OPT_multiset_scans_in_selfcheck':0,'C0_scope':'actual bytes of all staged files excluding only LF/TAB/CR'};(W/'selfcheck.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x for k,x in v.items() if k not in ['checks','formal_links']},ensure_ascii=False))
