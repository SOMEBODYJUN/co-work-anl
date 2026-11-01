#!/usr/bin/env python3
"""Read-only raw/claim/metadata/link/C0 and stated scalar arithmetic; no source/SPE calls."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');REPO=ROOT/'boss4-research';STAGE=ROOT/'boss4-next-cache/r3-coupled-and-assigned-profit-seats-primary';ER='archives/customer-attraction/tools/evidence/coupled-and-assigned-profit-seats-primary';WR='cleanup/workspaces/Boss4/r3-coupled-and-assigned-profit-seats-primary';E=STAGE/ER;W=STAGE/WR
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(b<32 and b not in (9,10,13) for b in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json');ck(len(rows)==5 and sum(a['size'] for a in rows)==30175 and not lm['missing'],'five-full-local-primary30175')
inv={a['id']:a for a in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
for a in rows:
 p=STAGE/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and hashlib.sha256(b).hexdigest()==a['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+a['id']);ck(a['full_primary_read'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md') and a['path']==ER+'/original/'+a['source_path'],'full-MD-primary-no-code-entry-'+a['id']);ck(inv[a['id']]['sha256']==a['sha256'],'inventory-sourceSHA-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['remote_tip']=='3037285ce2ccebd76f4c9800f0c675ca905d79c4','actual-pushed-synced3037285')
ck(set(c['ids'])=={a['id'] for a in rows} and g['whole_capture_ids']==c['ids'] and g['whole_capture_size']==5 and g['claim_subset_not_projected'],'original-exact-five-capture-not-projected');ck(g['original_capture_unmodified_sha256']==sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-ig-claim.json'),'whole-actual-capture-unmodified')
for o in g['current_owners']:ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'primary-authorization-ownerSHA-'+o['id'])
context=j(E/'context-manifest.json');ck(len(context['rows'])==2 and context['context_only'] and context['additional_primary_done']==context['original_entry_calls_here']==0,'two-context-no-new-done-entry')
for a in context['rows']:
 p=STAGE/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_context_read'] and not a['additional_primary_done'],'context-full-raw-'+a['id'])
inputrow=next(a for a in context['rows'] if a['id']=='44fd0b2a643f6b4774e0');inp=j(STAGE/inputrow['path']);ck(inputrow['size']==1486 and inputrow['sha256']=='8fa88f66e5ebf2bdc8239f61d2e0ee32b2c49786edc05a6308d30b5ba2304ccc','true124-input-raw-identity')
ck('actions' not in inp and 'strategy' not in inp and inp['instance']['players']==3 and inp['instance']['topics']==['0','1','2','3','4'] and len(inp['instance']['customers'])==11 and sum(a['multiplicity'] for a in inp['instance']['customers'])==124,'true-input-no-actions-eleven-types124')
ck(inp['path']==[0,4,2] and inp['welfare']==95 and inp['new']=='127/2' and inp['old_combined']=='184/3' and inp['gap']=='13/6','source-declared-strict-path-and-spectra')
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==5,'five-full-formal-comparisons')
for a in comp:
 p=STAGE/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_related_read'] and a['published_not_inferred_from_local_presence'],'comparison-full-bytes-'+a['name'])
scope=j(E/'scope.json');ck(scope['original_entry_calls']==scope['source_function_calls']==scope['canonical_solver_calls']==scope['new_SPE_BI_enumerations']==scope['new_static_F_E_scans']==scope['context_primary_done_added']==scope['network_or_shared_git_writes']==0,'actual-zero-original-source-solver-BI-static-scan')
for k in ['historical_audit_counts_are_source_reported','existing_124_audit_not_repeated','F_G_touch_contract_not_E_assignment_contract','Q_empty_F_G_direct_not_automatic_E_collapse','E_infinite_empty_domains_finite_order_statistic','analytic_review_blind_G_not_blind_F','analytic_review_did_not_recheck_finite_numbers','numerical_review_G_only_not_F_E','J2_general_mutual_domination_not_claimed','true_dynamic_J2_can_reproduce_E','all_maxima_old_J2_obstruction_applies']:ck(scope[k],'actual-scope-'+k)
ck(not scope['general_half_or_six_half_proved'] and not scope['new_blind_or_external_review'],'no-general-half-or-new-blind-external-claim')
receipts=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(receipts)==5 and len(targets)==len(set(targets))==3 and {a['id'] for a in receipts}=={a['id'] for a in rows},'three-objects-five-exact-receipts')
for a in receipts:
 r=next(x for x in rows if x['id']==a['id']);ck(a['disposition']=='integrated' and a['owner']=='Boss4' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-semantic-integrated-'+a['id']);ck(a['source_sha256']==r['sha256'] and a['source_size']==r['size'] and a['source_path']==r['source_path'] and a['raw_evidence']==r['path'],'receipt-exact-source-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'substantive-unique-content-destination-'+a['id']);ck('external stage only' in a['publication_status'] and 'does not imply published' in a['delivery_status'],'semantic-versus-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==scope['human_math_items']==62,'sixty-two-human-math-source-obligations');rels=j(W/'relation-review.json')['relations'];ck(len(rels)==scope['explained_relations']==8 and all(len(a['explanation'])>30 for a in rels),'eight-explained-stage-two-relations')
stable=[];links=[]
for rel in targets:
 p=STAGE/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(not c0(p) and p.stat().st_size>7500 and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'actual-canonical-complete-C0-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));found=STAGE/q if (STAGE/q).is_file() else REPO/q;ck(found.is_file(),'resolved-new-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(found)})
ck(len(set(stable))==3,'three-distinct-stable-ids')
a,b,d=[(STAGE/p).read_text() for p in targets]
for s,label in [('同一个冻结子树的残余归纳','frozen-actual-subtree-full-proof'),('无私有遗漏及末位的准确退化','precise-Q-empty-and-final-boundary'),('任意合法起点扩展','all-private-arbitrary-prefix-distinct-extension')]:ck(s in a,'math-body-'+label)
for s,label in [('+∞','empty-domain-infinity'),('Q全空时F/G退直接分母，不自动意味着E也退化','different-E-assignment-constraint'),('不能笼统断言E与原容器J2互相支配','container-versus-true-history-domain'),('J_true在起点至少Θ','dynamic-reproduces-fixed-capacity'),('899/60','old-all-maxima-general-obstruction')]:ck(s in b,'math-body-'+label)
for s,label in [('F明确是**读稿后核对**','original-G-blind-F-informed-order'),('第二独审明确没有计算精确F或Λ','finite-G-only-review'),('155含自身比较','weak-SPE-not-strict'),('源码6583不同于原menu6306','different-source-code-not-exactSHA-replay')]:ck(s in d,'review-body-'+label)
ck(F(15)+F(41,2)+28==F(127,2) and F(15)+F(55,3)+28==F(184,3) and F(127,2)-F(184,3)==F(13,6),'source-strict-G-sum-arithmetic-no-spectrum-enumeration')
ck(31*5==155 and 155-31==124 and 121+3==124 and 31+3==34,'source-reported-comparison-counts-not-new-IC')
ck(7*sum((F(1,k) for k in range(1,6)),F())-1==F(899,60) and F(15)-F(899,60)==F(1,60),'old-J2-m5k6-scalar-not-new-obstruction-audit')
nexts=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(nexts['rows'])==len(nm['rows'])==5 and nexts['source_bytes']==sum(a['size'] for a in nexts['rows'])==21398 and not nm['missing'],'next-real-local-five21398')
for a in nexts['rows']:
 p=Path(a['local_path']);ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['actual_local_complete'] and a['not_primary_done_here'],'next-actual-bytes-not-done-'+a['id'])
files=sorted(p.relative_to(STAGE).as_posix() for p in STAGE.rglob('*') if p.is_file());manifest=j(W/'copy-files.json');ck(files==manifest and WR+'/copy-files.json' in files,'exact-sorted-self-inclusive-copy-whitelist');ck(all(not x.startswith('/') and '..' not in Path(x).parts for x in files),'safe-relative-paths');ck(not any(c0(STAGE/x) for x in files),'all-actual-C0-bytes-except-LF-TAB-CR');ck(not any(any(line.endswith((' ','\t')) for line in (STAGE/x).read_text().splitlines()) for x in files),'no-trailing-whitespace-all-files')
for x in files:
 if x.endswith('.json'):json.loads((STAGE/x).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'raw source/context/claim/receipts/metadata/links/C0 and stated scalar arithmetic only; no source or solver imported/executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_sources':5,'primary_source_bytes':30175,'primary_receipts':5,'human_math_items':62,'explained_relations':8,'original_entry_calls':0,'source_function_calls':0,'canonical_solver_calls':0,'new_SPE_BI_or_F_E_scans':0,'context_primary_done_added':0,'analytic_review_not_finite_review':True,'finite_review_G_not_F_E':True,'E_not_automatic_Q_empty_collapse':True,'J2_general_mutual_domination_not_claimed':True,'next_real_local_bytes':21398,'C0_scope':'actual bytes excluding only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
