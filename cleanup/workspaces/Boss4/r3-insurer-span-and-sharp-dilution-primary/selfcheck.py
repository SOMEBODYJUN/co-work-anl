#!/usr/bin/env python3
"""Read-only raw evidence/claim/formal links/finite scalar identities; no source calls."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,posixpath

ROOT=Path('/workspace/scratch/37f0f9248cfc');REPO=ROOT/'boss4-research'
STAGE=ROOT/'boss4-next-cache/r3-insurer-span-and-sharp-dilution-primary'
ER='archives/customer-attraction/tools/evidence/insurer-span-and-sharp-dilution-primary'
WR='cleanup/workspaces/Boss4/r3-insurer-span-and-sharp-dilution-primary'
E=STAGE/ER;W=STAGE/WR
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def c0(p):return [b for b in p.read_bytes() if b<32 and b not in (9,10,13)]

source=j(E/'source-manifest.json');rows=source['rows']
ck(len(rows)==5 and sum(a['size'] for a in rows)==34889,'five-full-primary34889')
ck(source['method'].startswith('safe local raw'),'no-network-show-source-method')
lm=j(W/'local-source-export-manifest.json');ck(not lm['missing'] and {a['id'] for a in lm['rows']}=={a['id'] for a in rows},'full-safe-local-export-manifest')
inventory={a['id']:a for a in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
for a in rows:
 p=STAGE/a['path'];b=p.read_bytes()
 ck(len(b)==a['size'] and hashlib.sha256(b).hexdigest()==a['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+a['id'])
 ck(a['source_path'].endswith('.md') and a['full_primary_read'] and a['prior_HI_full_context_sameSHA_reuse'] and a['original_entry_calls']==0,'full-Markdown-primary-not-original-entry-'+a['id'])
 ck(inventory[a['id']]['sha256']==a['sha256'] and a['path']==ER+'/original/'+a['source_path'],'inventory-full-frozen-path-'+a['id'])
claim=j(W/'claim-evidence.json');gate=j(W/'primary-authorization-check.json')
ck(claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and claim['remote_tip']=='3c00fa1a343da10251bd91fc9745d8203894dda1','actual-pushed-synced3c00fa')
ck(len(claim['ids'])==10 and set(a['id'] for a in rows)<=set(claim['ids']) and gate['whole_capture_ids']==claim['ids'] and gate['whole_capture_size']==10,'five-subset-of-unprojected-whole-ten')
ck(gate['original_capture_unmodified_sha256']==sha(W/'claim-evidence.json') and sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-hq-claim.json'),'actual-whole-capture-unmodified')
for o in gate['current_owners']:
 ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'ownerSHA-at-primary-authorization-'+o['id'])

context=j(E/'context-manifest.json')
ck(context['context_only'] and context['primary_done_added']==context['entry_calls_here']==0 and len(context['rows'])==2,'two-full-padded-context-no-added-done-entry')
for a in context['rows']:
 p=STAGE/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_context_read'] and not a['additional_primary_done'],'context-sizeSHA-full-'+a['id'])
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==5,'five-distinct-related-formal-comparisons')
for a in comp:
 p=STAGE/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_related_read'],'comparison-complete-sizeSHA-'+a['name'])
 ck(a['published_not_inferred_from_local_presence'],'comparison-publication-not-inferred-'+a['name'])
missing=j(E/'unavailable-audit-source-manifest.json');ck(not missing['rows'] and len(missing['missing'])==5 and all('local blob absent' in a['reason'] for a in missing['missing']),'five-true-local-missing-audits-no-fallback')
ck(sha(E/'unavailable-audit-source-manifest.json')==sha(ROOT/'boss4-next-cache/submarkov-next-insurer-audits-local-inputs/local-export-manifest.json'),'unmodified-missing-audit-local-evidence')

scope=j(E/'scope.json')
ck(scope['original_entry_calls']==scope['source_function_calls']==scope['canonical_solver_calls']==scope['new_SPE_or_BI_enumerations']==scope['context_primary_done_added']==scope['network_or_shared_git_writes']==0,'actual-no-source-or-canonical-or-original-SPE-calls')
ck(scope['all_theme_intersection_not_maxima_only'] and scope['same_root_real_complete_suffix'] and not scope['root_optimality_required'] and scope['arbitrary_many_signed_independent_coordinates'] and scope['total_client_cost_not_half_dilution'],'exact-mathematical-domain-fields')
ck(not scope['general_half_proved'] and not scope['general_old_plan_R4_best_constant_claim'] and not scope['new_blind_review_or_external_review'] and not scope['historical_audit_counts_verified_by_new_entry'],'explicit-open-model-and-historical-evidence-boundaries')
ck(scope['historical_blind_insurer_comparisons_as_source_reported']==120552 and scope['historical_blind_joint_comparisons_as_source_reported']==22620 and scope['historical_sharp_instances_as_source_reported']==34 and scope['historical_sharp_root_pairs_as_source_reported']==750 and scope['historical_sharp_positive_pairs_as_source_reported']==90 and scope['historical_three_theme_strategy_count_as_source_reported']==81 and scope['historical_three_theme_cone_pairs_as_source_reported']==6561,'source-reported-finite-scopes-not-new-computations')

arith=j(E/'arithmetic-crosscheck.json');ck(arith['original_entry_calls']==arith['source_function_calls']==0 and 'not original source run' in arith['scope'] and len(arith['rows'])==5,'scalar-identities-not-source-BI-or-parameter-search')
for row in arith['rows']:
 m=row['m'];s=F(row['rational_s_pre_unit_cloning']);C2=F(row['two_theme_C_W_OPT']);C=F(row['padded_C_OPT']);Wactual=F(row['padded_actual_W']);D=F(row['padded_dilution']);delta=F(row['same_root_delta']);z=F(row['extra_uncovered_Z_mass'])
 ck(C2==(m+1)*s and C==(2*m-1)*s and Wactual==C2 and z==(m-2)*s and C-C2==z,'three-cost-objects-and-uncovered-Z-m'+str(m))
 ck(D==2*Wactual-C==3*delta==3*s and C>=(m+1)*delta and F(row['two_theme_dilution'])==C2,'two-distinct-sharp-costs-scalar-m'+str(m))
ck(arith['rows'][0]['m']==2 and F(arith['rows'][0]['extra_uncovered_Z_mass'])==0,'m2-no-Z-same-two-and-padded-construction')

receipts=j(W/'semantic-receipts.json');ck(len(receipts)==5 and {a['id'] for a in receipts}=={a['id'] for a in rows},'five-exact-primary-receipts')
targets=j(W/'target-paths.json');ck(len(targets)==3 and len(set(targets))==3,'three-distinct-formal-object-paths')
for a in receipts:
 s=next(x for x in rows if x['id']==a['id'])
 ck(a['disposition']=='integrated' and a['owner']=='Boss4' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-semantic-integrated-'+a['id'])
 ck(a['source_sha256']==s['sha256'] and a['source_size']==s['size'] and a['source_path']==s['source_path'] and a['raw_evidence']==s['path'],'receipt-exact-source-identity-'+a['id'])
 ck(all(len(a[k])>=70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'substantive-source-specific-receipt-'+a['id'])
 ck('external stage only' in a['publication_status'] and 'not publication' in a['delivery_status'],'semantic-versus-publication-'+a['id'])
human=(W/'mathematical-self-review.md').read_text();ck(human.count('- [x] ')==89,'eighty-nine-human-mathematical-obligations')
rels=j(W/'relation-review.json');ck(len(rels['relations'])==9 and all(len(r['explanation'])>30 for r in rels['relations']),'nine-explained-stage-two-relations')

links=[];stable=[]
for rel in targets:
 p=STAGE/rel;text=p.read_text();parts=text.split('---',2)
 ck(len(parts)==3 and not text.startswith('#'),'flat-MATEK-frontmatter-'+p.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:
  ck(re.search(r'^'+key+r': .+',parts[1],re.M) is not None,'metadata-'+key+'-'+p.name)
 stable.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1))
 ck(not c0(p) and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',text),'actual-canonical-C0-and-completeness-'+p.name)
 ck(p.stat().st_size>9000,'full-self-contained-substantive-body-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));found=STAGE/q if (STAGE/q).is_file() else REPO/q
  ck(found.is_file(),'resolved-formal-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(found)})
ck(len(set(stable))==3,'three-distinct-stable-ids')
span=(STAGE/targets[0]).read_text();sharp=(STAGE/targets[1]).read_text();review=(STAGE/targets[2]).read_text()
ck('共同资源上的四个工具' in span and '内部子主题的动态删除' in span and '同根跨度的全部计算' in span and 'C\\ge(m+1)\\Delta' in span,'span-all-proof-tools-and-total-client-lower-bound')
ck('k≥2：根花瓣被后继完整覆盖' in sharp and 'k=1：保留未被覆盖的B\\A' in sharp and '无正差时的基线' in sharp and '任意多个独立坐标、异号收益差' in sharp,'sharp-both-k-cases-baseline-signed-coordinates')
ck('第一份通过3s**构造**' in review and '后者是另一次' in review and '本批实际原入口' in review,'two-review-priors-not-retrospectively-conflated')
ck('同为2026-10-23不等于' in review and '没有新blind身份' in review and '源码/输入报告闭包' in review,'historical-reading-order-and-code-identity-boundaries')

nexts=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json')
ck(len(nexts['rows'])==len(nm['rows'])==5 and nexts['source_bytes']==sum(x['size'] for x in nm['rows'])==26914 and not nm['missing'],'next-five-real-complete26914')
for a in nexts['rows']:
 p=Path(a['local_path']);b=p.read_bytes();ck(len(b)==a['size'] and hashlib.sha256(b).hexdigest()==a['sha256'] and a['actual_local_complete'] and a['not_primary_done_here'],'next-real-bytes-not-done-'+a['id'])

files=sorted(p.relative_to(STAGE).as_posix() for p in STAGE.rglob('*') if p.is_file());manifest=j(W/'copy-files.json')
ck(manifest==files and WR+'/copy-files.json' in manifest,'exact-sorted-self-inclusive-copy-whitelist')
ck(all(not x.startswith('/') and '..' not in Path(x).parts for x in manifest),'safe-relative-copy-paths')
ck(not any(c0(STAGE/x) for x in files),'all-actual-staged-C0-bytes-except-LF-TAB-CR')
ck(not any(any(line.endswith((' ','\t')) for line in (STAGE/x).read_text().splitlines()) for x in files),'all-text-no-trailing-space-tab')
for x in files:
 if x.endswith('.json'):json.loads((STAGE/x).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'raw local size/SHA/blob/whole claim subset/receipts/metadata/links/exact analytic scalar identities/C0; no original or canonical source imported or executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'primary_source_bytes':34889,'formal_objects':3,'primary_receipts':5,'human_math_items':89,'explained_relations':9,'original_entry_calls':0,'source_function_calls':0,'canonical_solver_calls':0,'new_SPE_BI_enumerations':0,'source_reported_historical_audits_not_new_runs':True,'K_is_all_legal_themes_intersection':True,'signed_independent_coordinates':True,'context_primary_done_added':0,'next_real_local_candidate_bytes':26914,'C0_scope':'actual staged bytes excluding only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
