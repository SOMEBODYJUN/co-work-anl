#!/usr/bin/env python3
"""Read-only provenance/receipt/byte checks and recorded-input scalar arithmetic; no math entry rerun."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');R=ROOT/'boss4-research';S=ROOT/'boss4-next-cache/r3-retention-semigroup-and-signed-seed-reviews-primary';ER='archives/customer-attraction/tools/evidence/retention-semigroup-and-signed-seed-reviews-primary';WR='cleanup/workspaces/Boss4/r3-retention-semigroup-and-signed-seed-reviews-primary';E=S/ER;W=S/WR;j=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(b<32 and b not in (9,10,13) for b in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json');inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())};ck(len(rows)==5 and sum(x['size'] for x in rows)==30833 and not lm['missing'],'five-primary-MD30833')
for a in rows:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256']==inv[a['id']]['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+a['id']);ck(a['full_primary_read'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md'),'full-source-primary-not-old-context-summary-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['remote_tip']=='4fc30aa7dea20fd5e04e8f2c68e3cb1057736835','actual-KP-pushed-synced4fc30aa')
ck(sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-kp-claim.json')==g['original_capture_unmodified_sha256'],'whole-real-unprojected-capture-bytes');ck(len(c['ids'])==g['whole_capture_size']==17 and c['ids']==g['whole_capture_ids'] and set(x['id'] for x in rows)<=set(c['ids']) and g['claim_subset_not_projected'],'own-five-subset-original17-not-projection')
for a in g['current_owners']:ck(a['owner']=='Boss4' and a['disposition']=='in-progress' and a['source_sha256']==next(x['sha256'] for x in rows if x['id']==a['id']),'actual-own-sourceSHA-'+a['id'])
ctx=j(E/'context-manifest.json');ck(len(ctx['rows'])==1 and ctx['rows'][0]['id']=='c3d703c76d4e966b6509' and ctx['context_primary_done_added']==0,'one-SCREEN-context-not-extra-primary-done')
for a in ctx['rows']:ck((S/a['path']).stat().st_size==a['size']==3251 and sha(S/a['path'])==a['sha256'] and a['full_context_read'] and not a['additional_primary_done'],'full-original-SCREEN-context-sizeSHA')
comps=j(E/'comparison-manifest.json')['rows'];ck(len(comps)==6,'six-related-whole-current-objects')
for a in comps:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256']==sha(R/a['canonical_path']) and a['full_related_read'] and a['publication_not_inferred_from_local_presence'],'whole-related-comparison-current-sameSHA-'+a['name'])
reuse=j(E/'prior-success-reuse.json');ck(reuse['prior_supplement_entry_attempts']==2 and reuse['prior_failed_attempts']==reuse['prior_successful_attempts']==1 and reuse['current_batch_new_math_entries']==reuse['original_author_or_canonical_entry_calls']==0,'exact-old-KC-two-attempts-reused-zero-new')
ck(reuse['prior_input_sha256']=='2b8fc76f799bee83b5e8588f94f7c8dfa6f91a634ffe624ede820cc909af541c' and reuse['prior_success_code_sha256']=='85dfbc7714bd8b8f95390fb5bfa388fa869280dbc6383aa6c029090755190d5c','reused-exact-input-and-success-code-SHA')
ck(not reuse['prior_second_independent_original_strategy_replayed_here'] and 'explicit parent' in reuse['publication_evidence_basis'] and reuse['parent_reported_KC_body_tip']=='102fa8667074c3a3bd131dc7207b8e1ab116236e' and reuse['parent_reported_KC_done_tip']=='cef30d260173527efeee34610b07eb34adae6ded','prior-actual-publication-distinct-second-strategy-not-replayed')
for a in reuse['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256']==sha(R/a['prior_relative_path']),'old-KC-record-byte-exact-no-run-'+a['prior_relative_path'])
f=j(E/'reused-KC-records/supplement/actual-invocation.json');s=j(E/'reused-KC-records/supplement/actual-invocation-corrected.json');rr=j(E/'reused-KC-records/supplement/corrected-replay/summary.json');ck(f['status']=='failed' and f['exit_code']==1 and s['status']=='completed' and s['exit_code']==0 and s['own_supplement_entry_calls_total']==2 and rr['status']=='pass','first-failure-and-corrective-success-not-one-PASS')
ck(rr['original_real_IC_comparisons_including_self']==340 and rr['true_three_ordered_states']==85 and rr['true_three_decision_nodes']==21 and rr['true_three_forced_children']==84 and not rr['BR_reset_target_is_root_SPE_outcome'],'old-success-exact-finite-domain-not-new-enumeration')
scope=j(E/'scope.json');ck(scope['primary_sources']==5 and scope['primary_source_bytes']==30833 and scope['formal_objects']==3 and scope['human_math_items']==66 and scope['explained_relations']==8,'primary-scope-math-review-identity')
for k in ['original_entry_calls','source_function_calls','canonical_solver_imports_or_calls','LP_or_parameter_scans','new_independent_math_entries','context_primary_done_added','network_or_shared_git_writes']:ck(scope[k]==0,'zero-new-'+k)
for k in ['SG_without_concavity_assumption','concavity_requires_monotone_concave_f','role_cocycle_same_identity_query_context','fixed_rn_background_not_physical_deletion','loss_current_slot_reset_unpaid','nonBR_last_defect_alpha_dm_preserved','MP_last_BR_normalization_not_other_price_contracts','floor_counterexample_includes_unreset_last','BR_reset_target_not_root_SPE','signed_screen_necessary_not_sufficient','HALF5_not_fixed_lambda2_MP_proof','three_stress_and_cone_are_source_reported','cone_total_customer_mass1_not_W1','rational_two_fifths_only_feasible_no_exact_dual','old_blind_and_after_read_stages_preserved','no_new_blind_or_external_review']:ck(scope[k],'explicit-domain-and-status-'+k)
recs=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(recs)==5 and len(targets)==len(set(targets))==3 and {x['id'] for x in recs}=={x['id'] for x in rows},'five-primary-receipts-three-distinct-objects')
for a in recs:
 sr=next(x for x in rows if x['id']==a['id']);ck(a['owner']=='Boss4' and a['disposition']=='integrated' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-integrated-semantic-'+a['id']);ck(a['source_size']==sr['size'] and a['source_sha256']==sr['sha256'] and a['source_path']==sr['source_path'] and a['raw_evidence']==sr['path'],'receipt-raw-source-identity-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'specific-full-content-accounted-'+a['id']);ck('external stage only' in a['publication_status'] and 'not body-pushed' in a['delivery_status'],'semantic-versus-body-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==66,'sixty-six-human-mathematical-obligations');rels=j(W/'relation-review.json')['relations'];ck(len(rels)==8 and all(len(x['explanation'])>40 for x in rels),'eight-explained-stage-two-relations')
h=j(E/'intake-history/pre-claim-draft-boundary.json');ck(h['claim_status']=='awaiting-actual-parent-capture' and not h['primary_receipts_written'] and h['new_supplement_calls']==0,'preclaim-no-success-receipts-historical-boundary-preserved')
ids=[];links=[]
for rel in targets:
 p=S/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>6800 and not c0(p) and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'full-object-raw-C0-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));p2=S/q if (S/q).is_file() else R/q;ck(p2.is_file(),'resolve-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(p2)})
ck(len(set(ids))==3,'three-stable-distinct-ids');a,b,d=[(S/p).read_text() for p in targets]
for text,label in [('半群仍成立','SG-no-concavity-assumed'),('r≥n≥1','positive-parameter-domain'),('rs}{nt','conditional-coverer-bias'),('同一原身份','same-source-role-cocycle'),('每个J另选其最佳','different-query-not-aligned'),('不是新的真实SPE','erased-leaf-not-real-SPE')]:
 if label=='SG-no-concavity-assumed':ck('半群仍成立' in a or '半群仍' in a,'operator-'+label)
 elif label=='erased-leaf-not-real-SPE':ck('没让每份z_J成为新的真实SPE' in a,'operator-'+label)
 else:ck(text in a,'operator-'+label)
for text,label in [('d_m=M_m−u_m','nonBR-last-defect'),('α=1或3/2还含W','other-prices-not-free-normalization'),('严格种子的必要条件','necessary-not-sufficient'),('HALF5','five-proof-not-MP'),('有真实L_i≤M_i','lower-floor-monotonic-screen')]:
 if label=='lower-floor-monotonic-screen':ck('真实L_i≤M_i' in b,'screen-'+label)
 else:ck(text in b,'screen-'+label)
for text,label in [('五种重置','reset-domain-table'),('总客户质量1','cone-not-W-normalization'),('未精确重构LP对偶','no-exact-dual'),('首在误加','actual-old-failed-check-retained'),('0新执行','no-replay-old-KC'),('保存§1–8','before-author-read-stage')]:ck(text in d,'review-'+label)
# Closed scalar bookkeeping from old result and published bank formula only, no math program calls.
mu=[F(x) for x in rr['floors']];up=[F(x) for x in rr['target_profits']];ur=[F(x) for x in rr['BR_reset_profits']];ck(sum(mu)==34 and sum(up)==23 and sum(ur)==31 and mu[-1]-up[-1]==F(5,2),'same-old31-record-fixed-Mtot-and-last-defect')
oldF=[];newF=[]
for alpha in [F(1),F(3,2),F(2)]:
 oldF.append(2*sum(up)-31+alpha*sum(m-u for m,u in zip(mu[:-1],up[:-1])));newF.append(2*sum(ur)-31+alpha*sum(m-u for m,u in zip(mu[:-1],ur[:-1])))
ck(oldF==[F(47,2),F(111,4),F(32)] and newF==[F(34),F(71,2),F(37)] and 2*sum(mu)-31==37,'three-alpha-before-after-scalar-table-not-new-BI')
ck([F(3*m-2,2*m-1)-F(m,m-1) for m in [4,5,6]]==[F(2,21),F(7,36),F(14,55)],'old-bank-weak-root-floor-exact-four-five-six-substitution')
n=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(n['rows'])==len(nm['rows'])==5 and not nm['missing'] and n['source_bytes']==sum(x['size'] for x in n['rows'])==20388,'next-local-actual-five20388-not-done')
for x in n['rows']:
 p=Path(x['local_path']);ck(p.stat().st_size==x['size'] and sha(p)==x['sha256'] and x['actual_local_complete'] and x['not_primary_done_here'],'next-source-byte-complete-not-done-'+x['id'])
files=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file());ck(files==j(W/'copy-files.json') and WR+'/copy-files.json' in files,'exact-sorted-self-inclusive-copy-manifest');ck(all(not p.startswith('/') and '..' not in Path(p).parts for p in files),'safe-relative-copy-whitelist');ck(not any(c0(S/p) for p in files),'all-actual-C0-except-LF-TAB-CR');ck(not any(any(line.endswith((' ','\t')) for line in (S/p).read_text().splitlines()) for p in files),'no-trailing-whitespace-all-files')
for p in files:
 if p.endswith('.json'):json.loads((S/p).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'raw source/claim/receipts/old-success-reuse/metadata/links/C0 and closed scalar arithmetic only; no original/canonical/auxiliary math entry imported or executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'primary_bytes':30833,'objects':3,'integrated_receipts':5,'human_math_items':66,'explained_relations':8,'new_math_entry_calls':0,'original_source_function_or_canonical_calls':0,'LP_or_parameter_scans':0,'old_KC_attempts_reused':2,'old_KC_failure_reused':1,'old_KC_success_reused':1,'next_actual_local_bytes':20388,'C0_scope':'actual bytes except only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
