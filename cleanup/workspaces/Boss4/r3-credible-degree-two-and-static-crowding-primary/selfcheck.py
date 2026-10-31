#!/usr/bin/env python3
"""Read-only source/claim/receipts/links/C0 and closed-form scalar/count bookkeeping only."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib,json,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');R=ROOT/'boss4-research';S=ROOT/'boss4-next-cache/r3-credible-degree-two-and-static-crowding-primary';ER='archives/customer-attraction/tools/evidence/credible-degree-two-and-static-crowding-primary';WR='cleanup/workspaces/Boss4/r3-credible-degree-two-and-static-crowding-primary';E=S/ER;W=S/WR
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(b<32 and b not in (9,10,13) for b in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json');ck(len(rows)==5 and sum(a['size'] for a in rows)==30382 and not lm['missing'],'five-full-primary30382')
inv={a['id']:a for a in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for a in rows:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and hashlib.sha256(b).hexdigest()==a['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+a['id']);ck(a['full_primary_read'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md') and a['path']==ER+'/original/'+a['source_path'],'full-MD-primary-no-original-entry-'+a['id']);ck(inv[a['id']]['sha256']==a['sha256'],'inventory-sourceSHA-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['remote_tip']=='1a854689eecb8a10e0c2bbdd45857979d73b21b8','actual-pushed-synced1a8546')
ck(len(c['ids'])==10 and g['whole_capture_ids']==c['ids'] and g['whole_capture_size']==10 and set(a['id'] for a in rows)<=set(c['ids']) and g['claim_subset_not_projected'],'five-actual-subset-original10-unprojected');ck(g['original_capture_unmodified_sha256']==sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-jm-claim.json'),'whole-real-capture-bytes')
for o in g['current_owners']:ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'actual-primary-ownerSHA-'+o['id'])
context=j(E/'context-manifest.json');ck(len(context['rows'])==2 and context['context_primary_done_added']==context['original_entry_calls_here']==0,'two-full-old-context-no-new-done-run')
for a in context['rows']:
 p=S/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_context_read'] and a['already_done_by_other_source_disposition_not_changed'] and not a['additional_primary_done'],'full-context-sizeSHA-scope-'+a['id'])
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==3,'three-full-current-related-comparisons')
for a in comp:
 p=S/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_related_read'] and a['publication_not_inferred_from_local_presence'],'comparison-full-raw-'+a['name'])
scope=j(E/'scope.json');ck(scope['primary_sources']==5 and scope['primary_source_bytes']==30382 and scope['formal_objects']==3 and scope['all_primary_Markdown'],'primary-scope-identity')
ck(scope['original_entry_calls']==scope['source_function_calls']==scope['canonical_solver_calls']==scope['new_LP_or_parameter_scans']==scope['context_primary_done_added']==scope['network_or_shared_git_writes']==0,'actual-no-original-source-solver-LP-scan')
for k in ['root_equal_pure_theta_not_strict_counterexample','constructed_actual_W_equal_OPT_not_all_SPE_claim','one_one_tie_follows_second_group_code_already_correct','general_incidence_COV_not_same_scope_as_degree_two_opposite_group','nonuniform_menu_not_perturbed_strategy_SPE_claim','K5_true_SPE_vs_C5_uncredible_menu_separate','K5_Gamma_table_new_analytic_not_original_audit','author_full_vs_independent_nonrepeat_counts_not_added','six_provider_specialization_analytic_not_original_run','historical_audit_numbers_source_reported']:ck(scope[k],'explicit-math-and-audit-domain-'+k)
ck(scope['author_finite_parameter_max_q']==4 and scope['author_finite_parameter_max_m']==5 and not scope['general_degree_two_theta_or_half_proved'] and not scope['new_blind_or_external_review'],'finite-maxm5-vs-general-proof-no-half-or-new-blind')
recs=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(recs)==5 and len(targets)==len(set(targets))==3 and {a['id'] for a in recs}=={a['id'] for a in rows},'five-exact-receipts-three-distinct-objects')
for a in recs:
 s=next(x for x in rows if x['id']==a['id']);ck(a['owner']=='Boss4' and a['disposition']=='integrated' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-semantic-integrated-'+a['id']);ck(a['source_sha256']==s['sha256'] and a['source_size']==s['size'] and a['source_path']==s['source_path'] and a['raw_evidence']==s['path'],'receipt-source-exact-identity-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'substantive-unique-source-coverage-'+a['id']);ck('external stage only' in a['publication_status'] and 'not body-pushed' in a['delivery_status'],'semantic-versus-body-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==scope['human_math_items']==68,'sixty-eight-human-mathematical-source-obligations');rels=j(W/'relation-review.json')['relations'];ck(len(rels)==scope['explained_relations']==7 and all(len(a['explanation'])>30 for a in rels),'seven-explained-stage-two-relations')
ids=[];links=[]
for rel in targets:
 p=S/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>6500 and not c0(p) and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'actual-canonical-full-C0-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));p2=S/q if (S/q).is_file() else R/q;ck(p2.is_file(),'resolved-new-formal-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(p2)})
ck(len(set(ids))==3,'three-distinct-stable-ids')
a,b,d=[(S/p).read_text() for p in targets]
for s,label in [('构造只声称存在下述SPE','constructed-not-all-SPE-optimal'),('最近动作所在组','necessary-root-menu-tie'),('不是隐藏随机查询的minimax','pure-theta-not-hidden-security'),('m6','analytic-six-specialization')]:
 if label=='analytic-six-specialization':ck('当前六人可作纯解析代入q5' in a,'construct-unit-'+label)
 else:ck(s in a,'construct-unit-'+label)
for s,label in [('符号是K−c','signed-static-gap-direction'),('每一份','strict-quantifier-every-static-prefix'),('度二假设在这段承重','general-incidence-versus-opposite-group-domain'),('也没证明扰动后原完整策略还SPE','no-free-perturbed-policy'),('覆盖成本>q不能倒推u<θ','sufficient-cover-not-necessary-root-floor'),('此菜单非SPE','pure-C5-is-not-true-K5')]:ck(s in b,'static-unit-'+label)
for s,label in [('按**作者正文**','review-not-unread-proof-blind'),('不能把两个节点数相加','different-run-count-dimensions'),('最高q4/m5','finite-original-not-m6'),('非均匀静态菜单算术','nonuniform-algebra-not-SPE-audit')]:ck(s in d,'review-unit-'+label)
# Closed-form bookkeeping of source-reported cases, not history/SPE enumeration.
countrows=[]
for q,multiplicity in [(2,2),(3,3),(4,2)]:
 p=2*q;full=sum(p**ell for ell in range(q+1));fullmoves=p*full;nr=sum(factorial(p)//factorial(p-ell) for ell in range(q+1));nmoves=sum((factorial(p)//factorial(p-ell))*(p-ell) for ell in range(q+1));countrows.append((q,multiplicity,full,fullmoves,nr,nmoves))
ck([(a,c,d,e,f) for a,b,c,d,e,f in countrows]==[(2,21,84,17,40),(3,259,1554,157,516),(4,4681,37448,2081,8800)],'source-audit-size-formula-rows-not-replayed-nodes')
ck(sum(m*n for q,m,n,v,x,y in countrows)==10181 and sum(m*v for q,m,n,v,x,y in countrows)==79726 and sum(m*x for q,m,n,v,x,y in countrows)==4667 and sum(m*y for q,m,n,v,x,y in countrows)==19228,'source-two-distinct-audit-total-counts-not-new-IC')
q=5;aa=1;bb=2;N=q*q*bb+q*(q-1)*aa;WW=q*q*bb+F((q-1)*(q+2),2)*aa;L=F(q*bb,2)+(q-1)*aa;H=F(2*q-1,2)*bb+F(q-1,2)*aa;gap=aa*(q-1)*(q-2)//2
ck(N==70 and WW==64 and L==9 and H==11 and L+q*H==WW and L-H==-2 and gap==6,'six-provider-general-proof-scalar-substitution-not-original-run')
ck(F(11,6)-3==-F(7,6) and F(10,3)-3==F(1,3) and F(4,3)-3==-F(5,3),'K5-source-query-price-Gamma-arithmetic-not-new-SPE-run')
ck(1+5+25==31 and 31*5==155,'K5-source-node-count-arithmetic-not-new-audit')
n=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(n['rows'])==len(nm['rows'])==5 and not nm['missing'] and n['source_bytes']==sum(a['size'] for a in n['rows'])==15944,'next-five-actual-local15944-not-done')
for a in n['rows']:
 p=Path(a['local_path']);ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['actual_local_complete'] and a['not_primary_done_here'],'next-source-raw-not-done-'+a['id'])
files=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file());manifest=j(W/'copy-files.json');ck(files==manifest and WR+'/copy-files.json' in manifest,'exact-sorted-self-inclusive-copy-whitelist');ck(all(not p.startswith('/') and '..' not in Path(p).parts for p in files),'safe-relative-copy-paths');ck(not any(c0(S/p) for p in files),'all-actual-C0-bytes-except-LF-TAB-CR');ck(not any(any(line.endswith((' ','\t')) for line in (S/p).read_text().splitlines()) for p in files),'no-trailing-whitespace-all-files')
for p in files:
 if p.endswith('.json'):json.loads((S/p).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'raw/claim/receipts/metadata/links/C0 and closed-form scalar/audit-size bookkeeping only; no original/canonical math code imported or executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'primary_source_bytes':30382,'formal_objects':3,'primary_receipts':5,'human_math_items':68,'explained_relations':7,'original_entry_calls':0,'source_function_calls':0,'canonical_solver_or_LP_calls':0,'new_parameter_scans':0,'author_finite_max_m':5,'six_provider_values_are_analytic_not_original_run':True,'K5_Gamma_table_analytic_not_original_run':True,'context_primary_done_added':0,'next_actual_local_bytes':15944,'C0_scope':'actual bytes excluding only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
