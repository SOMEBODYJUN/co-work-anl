#!/usr/bin/env python3
"""Local bytes, provenance, receipts and scalar bookkeeping; imports no original math code."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');R=ROOT/'boss4-research';S=ROOT/'boss4-next-cache/r3-ancestor-promise-reset-and-root-handoff-primary';ER='archives/customer-attraction/tools/evidence/ancestor-promise-reset-and-root-handoff-primary';WR='cleanup/workspaces/Boss4/r3-ancestor-promise-reset-and-root-handoff-primary';E=S/ER;W=S/WR
j=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(x,n):
 if not x:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(b<32 and b not in (9,10,13) for b in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json');inv={a['id']:a for a in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
ck(len(rows)==5 and sum(a['size'] for a in rows)==15944 and not lm['missing'],'five-full-primary15944')
for a in rows:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and sha(p)==a['sha256']==inv[a['id']]['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'original-sizeSHAblob-'+a['id']);ck(a['full_primary_read'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md') and a['path']==ER+'/original/'+a['source_path'],'full-MD-source-not-original-run-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced','actual-claim-pushed-synced-Boss4')
ck(re.fullmatch(r'[0-9a-f]{40}',c['remote_tip']) is not None and c['remote_tip']==g['remote_tip'],'actual-remote-claim-tip')
ck(sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-jy-claim.json')==g['original_capture_unmodified_sha256'],'exact-original-unprojected-capture-bytes')
ck(c['ids']==g['whole_capture_ids'] and len(c['ids'])==g['whole_capture_size'] and g['claim_subset_not_projected'] and set(a['id'] for a in rows)<=set(c['ids']),'own-five-subset-of-original-whole-claim')
for o in g['current_owners']:ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'actual-owner-sourceSHA-'+o['id'])
ctx=j(E/'context-manifest.json');ck(len(ctx['rows'])==1 and ctx['rows'][0]['id']=='8a2963e34481e30f669a' and ctx['rows'][0]['size']==7023 and ctx['context_primary_done_added']==ctx['source_function_or_original_calls']==0,'old-three-client-full-context-not-new-done-or-run')
for a in ctx['rows']:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'] and a['full_context_read'] and not a['additional_primary_done'],'exact-full-context-'+a['id'])
ck([x['id'] for x in ctx['missing_local_reference_ids']]==['2467dc33959693ee7ca0'],'missing-Ra5-code-not-falsely-certified')
for name,n in [('submarkov-next-ancestor-and-regret-audits-local-inputs',4),('submarkov-next-regret-report-local-inputs',2)]:
 m=j(E/(name+'.json'));ck(len(m['missing'])==n and not m['rows'] and 'no network/lazy fetch' in m['method'],'actual-local-missing-boundary-'+name)
comps=j(E/'comparison-manifest.json')['rows'];ck(len(comps)==6,'six-current-whole-comparisons')
for a in comps:ck((S/a['path']).stat().st_size==a['size'] and sha(S/a['path'])==a['sha256'] and a['full_related_read'] and a['publication_not_inferred_from_local_presence'],'actual-comparison-sizeSHA-'+a['name'])
scope=j(E/'scope.json');ck(scope['primary_sources']==5 and scope['primary_source_bytes']==15944 and scope['formal_objects']==2 and scope['all_primary_Markdown'],'scope-math-source-identity')
for k in ['original_entry_calls','source_function_calls','canonical_solver_calls','new_LP_or_parameter_scans','network_or_shared_git_writes','context_primary_done_added']:ck(scope[k]==0,'zero-new-'+k)
for k in ['restricted_query_uses_unrestricted_child_floors','three_customer_original_SPE_is_old','new_diagnostic_cap_floor_5over6_to_4over3','all_L_counterexample_only_global_fixed_K_heredity','fixed_tree_230_and_seven_inputs_source_reported','general_robust_or_overlap_not_proved','Mind_and_unrestricted_M_distinct','old_tail_gap_not_Mfull_counterexample_but_current_Mfull_refuted','original_entry_closure_missing_preserved','no_new_blind_or_external_review']:ck(scope[k],'preserved-quantifier-and-evidence-'+k)
recs=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(recs)==5 and len(targets)==len(set(targets))==2 and set(a['id'] for a in recs)==set(a['id'] for a in rows),'five-exact-primary-receipts-two-math-objects')
for a in recs:
 s=next(x for x in rows if x['id']==a['id']);ck(a['owner']=='Boss4' and a['disposition']=='integrated' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-integrated-semantic-'+a['id']);ck(a['source_path']==s['source_path'] and a['source_size']==s['size'] and a['source_sha256']==s['sha256'] and a['raw_evidence']==s['path'],'receipt-exact-source-identity-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'substantive-specific-receipt-'+a['id']);ck('external stage only' in a['publication_status'] and 'not body-pushed' in a['delivery_status'],'semantic-integrated-not-body-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==scope['human_math_items']==56,'fifty-six-human-source-mathematics-obligations');rels=j(W/'relation-review.json')['relations'];ck(len(rels)==scope['explained_relations']==8 and all(len(a['explanation'])>35 for a in rels),'eight-explained-stage-two-relations')
ids=[];links=[]
for rel in targets:
 p=S/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>9500 and not c0(p) and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'self-contained-canonical-actual-C0-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));p2=S/q if (S/q).is_file() else R/q;ck(p2.is_file(),'resolve-formal-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(p2)})
ck(len(set(ids))==2,'distinct-stable-formal-ids')
a,b=[(S/p).read_text() for p in targets]
for s,label in [('不受Π约束','unrestricted-sibling-floor'),('各有序孩子子树互不相交','exact-gluing-sufficiency'),('所选a本身亦有','included-selected-action-floor'),('全部13有序决策节点','old-full-three-client-SPE'),('4/3−5/6=1/2','exact-B-option-reset-release'),('整数m>max(2K,2)','all-m-fixed-K-quantifier'),('不否定固定m可另取依m界','not-fixed-m-impossibility'),('没有独立复核该代码或运行它','Ra5-source-reported-only'),('当前原入口、原函数和规范solver调用均0','missing-code-no-original-run')]:ck(s in a,'reset-math-domain-'+label)
for s,label in [('这里p为该固定实例合法主题数','finite-LP-support-p-defined'),('共230项','historical-230-scope'),('M_unres≤M_ind','product-menu-contract-not-added'),('每个极大主题大小S=','degree-two-repeat-bound-S-defined'),('七个固定输入','seven-not-client-cones'),('指定的','tail-query-existence-quantifier'),('尾列仅m−1人、少原根','tail-versus-full-current-status'),('旧population_exchange','prior-fixed-population-identity')]:ck(s in b,'resource-scope-'+label)
ck(F(4,3)-F(5,6)==F(1,2) and F(5,6)<1<F(4,3),'cap-diagnostic-scalar-only-not-original-SPE-audit')
ck(1+3+9==13 and 3*13==39,'historical-tree-size-arithmetic-not-node-replay')
ck(all(x<=2 for x in [F(7,4),F(3,2),F(33,23),F(9,8)]),'four-source-reported-optimum-scalar-inequalities-no-LP-run')
ck(F(6,2)==3 and F(6,6)==1 and 6<2*6 and 6+1==7,'all-L-six-substitution-not-parameter-scan')
ck(2-F(1,6)-F(1,15)==F(53,30) and F(53,30)>1+F(1,5),'existing-bank-six-menu-scalar-not-controller-run')
pr=j(W/'legacy-clarification-proposal.json');cp=next(x for x in comps if x['canonical_path']==pr['canonical_path']);text=(S/cp['path']).read_text();ck(pr['base_sha256']==cp['sha256'] and pr['base_size']==cp['size']==6691 and text.count(pr['exact_old_text'])==pr['occurrences']==1 and not pr['shared_page_modified'],'exact-old-SHA-single-paragraph-proposal-no-shared-mutation');ck('proposal-only' in pr['status'] and '不能先把祖先承诺施给全部旁枝' in pr['replacement_text'],'clarification-only-no-transfer-algebra-changed')
h=j(E/'intake-history/pre-claim-draft-boundary.json');ck(not h['primary_receipts_written'] and h['claim_status']=='awaiting-actual-parent-capture','real-preclaim-draft-boundary-preserved-not-rewritten')
n=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(n['rows'])==len(nm['rows'])==5 and not nm['missing'] and n['source_bytes']==sum(x['size'] for x in n['rows'])==23752,'next-actual-local-five23752-not-done')
for x in n['rows']:
 p=Path(x['local_path']);ck(p.stat().st_size==x['size'] and sha(p)==x['sha256'] and x['actual_local_complete'] and x['not_primary_done_here'],'next-local-identity-not-primary-done-'+x['id'])
files=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file());ck(files==j(W/'copy-files.json') and WR+'/copy-files.json' in files,'exact-sorted-self-inclusive-copy-whitelist');ck(all(not p.startswith('/') and '..' not in Path(p).parts for p in files),'safe-repository-relative-copy-paths');ck(not any(c0(S/p) for p in files),'all-staged-actual-bytes-C0-except-LF-TAB-CR');ck(not any(any(t.endswith((' ','\t')) for t in (S/p).read_text().splitlines()) for p in files),'no-trailing-whitespace-all-files')
for p in files:
 if p.endswith('.json'):json.loads((S/p).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'source/claim/receipts/metadata/links/rawC0 and scalar bookkeeping only; no original code or solver imported/executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'source_bytes':15944,'formal_objects':2,'final_integrated_receipts':5,'human_math_items':56,'relations':8,'original_entry_calls':0,'source_function_calls':0,'canonical_solver_or_LP_calls':0,'parameter_scans':0,'missing_referenced_code_or_reports':7,'historical_audits_source_reported_not_replayed':True,'context_primary_done_added':0,'next_actual_local_bytes':23752,'C0_scope':'actual bytes except only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
