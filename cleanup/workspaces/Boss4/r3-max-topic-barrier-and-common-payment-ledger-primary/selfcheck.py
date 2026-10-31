#!/usr/bin/env python3
"""Read-only source/receipt/C0 checks and closed integer/Fraction bookkeeping; no original code imported."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');R=ROOT/'boss4-research';S=ROOT/'boss4-next-cache/r3-max-topic-barrier-and-common-payment-ledger-primary';ER='archives/customer-attraction/tools/evidence/max-topic-barrier-and-common-payment-ledger-primary';WR='cleanup/workspaces/Boss4/r3-max-topic-barrier-and-common-payment-ledger-primary';E=S/ER;W=S/WR;j=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(x,n):
 if not x:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(x<32 and x not in (9,10,13) for x in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json');inv={a['id']:a for a in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())};ck(len(rows)==5 and sum(a['size'] for a in rows)==18846 and not lm['missing'],'five-full-MD-primary18846')
for a in rows:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256']==inv[a['id']]['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-source-sizeSHAblob-'+a['id']);ck(a['full_primary_read'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md'),'whole-primary-MD-no-original-entry-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['remote_tip']=='3206da3a2eb241fc9bd77db7e935c7b281989f49','actual-LK-pushed-synced3206da');ck(sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-lk-claim.json')==g['original_capture_unmodified_sha256'],'exact-whole-unprojected-original-capture');ck(len(c['ids'])==g['whole_capture_size']==20 and c['ids']==g['whole_capture_ids'] and set(a['id'] for a in rows)<=set(c['ids']) and g['claim_subset_not_projected'],'own-five-intersect-whole20-not-projected')
for a in g['current_owners']:ck(a['owner']=='Boss4' and a['disposition']=='in-progress' and a['source_sha256']==next(x['sha256'] for x in rows if x['id']==a['id']),'actual-owner-sourceSHA-'+a['id'])
ctx=j(E/'context-manifest.json');ck(len(ctx['rows'])==2 and sum(x['size'] for x in ctx['rows'])==10566 and ctx['context_primary_done_added']==ctx['source_function_or_original_entry_calls']==0,'two-full-counter-context10566-no-extra-done')
for a in ctx['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'] and a['full_context_read'] and not a['additional_primary_done'],'context-whole-raw-identity-'+a['id'])
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==10,'ten-related-current-whole-objects')
for a in comp:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256']==sha(R/a['canonical_path']) and a['full_related_read'] and a['full_related_read_same_SHA_reused'] and a['publication_not_inferred_from_local_presence'],'comparison-whole-current-sameSHA-'+a['name'])
ck(comp[0]['size']==11233 and comp[0]['sha256']=='e66e762af835f21575d7799a16937aee608e87706f75bebb3994cec1427562b0','exact-prior-full-bank-proof-not-replayed')
sc=j(E/'scope.json');ck(sc['primary_sources']==5 and sc['primary_source_bytes']==18846 and sc['new_formal_objects']==2 and sc['human_math_items']==67 and sc['explained_relations']==8,'source-mathematics-scope-identity')
for k in ['original_entry_calls','source_function_calls','canonical_solver_imports_or_calls','LP_or_parameter_scans','new_independent_math_entries','context_primary_done_added','network_or_shared_git_writes']:ck(sc[k]==0,'zero-new-'+k)
for k in ['K_strengthening_zero_background_root_domain','K_true_all_inputs_m1_m2','K_refuted_every_m_ge3_by_prior_bank','K_counterexample_not_ROW_MG_SUMROW_or_half','all_big_equality_old_mechanism_analytic_reconstruction','same_SHA_prior_bank_controller_not_replayed','pure_query_safe_not_mixed_common_column','uniform_free_position_error_withdrawn_not_current','six_stable_R6_contracts_preserved','q_ell_potential_ranges_not_independent_wallets','counter_Cauchy_composition_dominated_by_direct_bound','root_kernel_counts_only_source_reported','combinatorial_count_agreement_not_actual_loop_certification','terminal_exact_six_not_float_probe_six','old_KC_two_attempts_not_current_run','old_five_route_failure_not_current_five_open','old_quick_search_not_new_browse_or_novelty_check','no_new_blind_external_review_or_novelty_claim']:ck(sc[k],'exact-math-history-boundary-'+k)
rec=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(rec)==5 and len(targets)==len(set(targets))==2 and {x['id'] for x in rec}=={x['id'] for x in rows},'five-final-receipts-two-distinct-objects')
for a in rec:
 sr=next(x for x in rows if x['id']==a['id']);ck(a['owner']=='Boss4' and a['disposition']=='integrated' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-integrated-'+a['id']);ck(a['source_sha256']==sr['sha256'] and a['source_size']==sr['size'] and a['source_path']==sr['source_path'] and a['raw_evidence']==sr['path'],'receipt-raw-source-identity-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'specific-source-unit-accounting-'+a['id']);ck('external stage only' in a['publication_status'] and 'not body-pushed' in a['delivery_status'],'semantic-integrated-not-body-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==67,'sixty-seven-human-source-math-obligations');rel=j(W/'relation-review.json')['relations'];ck(len(rel)==8 and all(len(x['explanation'])>40 for x in rel),'eight-explained-stage-two-relations');hist=j(E/'intake-history/pre-claim-draft-boundary.json');ck(not hist['primary_receipts_written'] and hist['claim_status']=='awaiting-actual-parent-capture' and hist['new_math_entry_calls']==0,'actual-preclaim-draft-no-success-receipt-preserved')
ids=[];links=[]
for rp in targets:
 p=S/rp;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>6000 and not c0(p) and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'self-contained-current-object-raw-C0-'+p.name)
 tab=[s for s in t.splitlines() if s.startswith('|')];ck(all(s.count('|')==4 for s in tab),'generated-three-column-tables-no-unescaped-math-bars-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rp),ref.split('#')[0]));p2=S/q if (S/q).is_file() else R/q;ck(p2.is_file(),'resolved-formal-link-'+q);links.append({'from':rp,'to':q,'resolved_at':str(p2)})
ck(len(set(ids))==2,'two-stable-distinct-math-ids');a,b=[(S/p).read_text() for p in targets]
for t,label in [('零初始背景','zero-background-domain'),('全部有序历史','full-SPE-not-terminal-array'),('m2成立','true-two-player-case'),('每个m≥3','all-larger-m-counterexamples'),('3+\\frac1{m-1}','root-ROW-MG-positive-margin'),('m+2>0','half-margin-positive'),('本源未重建','old71-not-new-replay')]:
 if label=='zero-background-domain':ck('零初始背景' in a or '零初始' in a or '零初始背景' in a,'K-'+label)
 else:ck(t in a,'K-'+label)
for t,label in [('R6-ERASURE-JOINT-v1','joint-stable-ID'),('R6-ERASURE-LOSS-POTENTIAL-v1','potential-stable-ID'),('R6-ERASURE-NESTING-v1','nesting-stable-ID'),('R6-RESET-FLOOR-PAY-NO-v1','floor-stable-ID'),('R6-TERMINAL-FULL-PAY-v1','terminal-stable-ID'),('R6-SIGNED-SEED-SCREEN-v1','screen-stable-ID'),('只属counter来源账局部符号','local-source-symbols-not-price-M'),('逐T分别挑L_T不能当一个共同L','pure-vs-mixture-quantifier'),('未在这五源提供','missing-original-first-draft-not-invented'),('exact audit的六证书','exact6-vs-float6'),('不把它反填','count-consistency-not-run'),('没有重新联网','historical-search-not-new-browse')]:ck(t in b,'ledger-'+label)
# Closed Fraction substitutions only, no CAG policy/tree or kernel code executed.
deltas=[]
for m in [3,4,5,6]:
 lhs=F(3*m-5)+F(3,m)-F(m*m,m-1);rhs=F(2*m*(m-2)**2-3,m*(m-1));ck(lhs==rhs and lhs>0,'K-closed-scalar-polynomial-substitution-m'+str(m));deltas.append(lhs)
ck(deltas==[F(1,2),F(29,12),F(87,20),F(63,10)] and F(3*5-5)+F(3,5)==F(53,5) and F(25,4)==F(5*5,4),'source-five-and-analytic-six-K-values-not-parameter-scan')
ck(all(F(m*m,m-1)-(m-2)==F(3)+F(1,m-1) for m in [3,4,5,6]),'positive-root-ROW-MG-margin-scalar-only')
ck(4*sum(r*r for r in range(1,10))==1140 and 4*sum(range(1,10))==180 and 4*sum(r*(r+1)//2 for r in range(1,10))==660 and 4*sum(r*2**(r-1) for r in range(1,10))==16388,'source-root-kernel-group-count-consistency-only-no-loop-or-PASS-recertification')
n=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(n['rows'])==len(nm['rows'])==5 and not nm['missing'] and n['source_bytes']==sum(x['size'] for x in n['rows'])==23140,'next-actual-local-five23140-not-done')
for x in n['rows']:
 p=Path(x['local_path']);ck(p.stat().st_size==x['size'] and sha(p)==x['sha256'] and x['actual_local_complete'] and x['not_primary_done_here'],'next-local-source-exact-not-primary-done-'+x['id'])
files=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file());ck(files==j(W/'copy-files.json') and WR+'/copy-files.json' in files,'exact-sorted-self-inclusive-copy-whitelist');ck(all(not p.startswith('/') and '..' not in Path(p).parts for p in files),'safe-relative-copy-paths');ck(not any(c0(S/p) for p in files),'all-actual-C0-bytes-except-LF-TAB-CR');ck(not any(any(s.endswith((' ','\t')) for s in (S/p).read_text().splitlines()) for p in files),'no-trailing-whitespace-all-files')
for p in files:
 if p.endswith('.json'):json.loads((S/p).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'raw/claim/receipts/history/metadata/links/C0 and closed Fraction/integer arithmetic only; no source math/controller/solver imported or executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'primary_bytes':18846,'new_objects':2,'integrated_receipts':5,'human_math_items':67,'explained_relations':8,'original_or_auxiliary_math_entry_calls':0,'source_function_or_canonical_calls':0,'LP_or_parameter_scans':0,'K_m1_m2_true_mge3_prior_bank_false':True,'K_not_ROW_MG_SUMROW_or_half_counterexample':True,'reported_kernel_group_counts_not_new_run':True,'next_actual_local_bytes':23140,'C0_scope':'actual bytes except only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
