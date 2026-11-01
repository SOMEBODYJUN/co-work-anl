#!/usr/bin/env python3
"""Read-only raw bytes/claim/metadata/links/finite exact identities; no math source calls."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');REPO=ROOT/'boss4-research';STAGE=ROOT/'boss4-next-cache/r3-effective-insurer-margin-and-status-primary'
ER='archives/customer-attraction/tools/evidence/effective-insurer-margin-and-status-primary';WR='cleanup/workspaces/Boss4/r3-effective-insurer-margin-and-status-primary';E=STAGE/ER;W=STAGE/WR
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def c0(p):return [b for b in p.read_bytes() if b<32 and b not in (9,10,13)]
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json')
ck(len(rows)==5 and sum(a['size'] for a in rows)==26914 and not lm['missing'],'five-full-local-primary26914')
ck({a['id'] for a in rows}=={a['id'] for a in lm['rows']},'five-exact-local-raw-ids')
inventory={a['id']:a for a in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
for a in rows:
 p=STAGE/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and hashlib.sha256(b).hexdigest()==a['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+a['id'])
 ck(a['full_primary_read'] and a['source_path'].endswith('.md') and a['original_entry_calls']==0 and a['path']==ER+'/original/'+a['source_path'],'full-MD-primary-no-original-entry-'+a['id'])
 ck(inventory[a['id']]['sha256']==a['sha256'],'inventory-sourceSHA-'+a['id'])
claim=j(W/'claim-evidence.json');gate=j(W/'primary-authorization-check.json')
ck(claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and claim['remote_tip']=='19b6528ed861ab38c02dbdc0d0efbad4f4cf61da','actual-pushed-synced19b6528')
ck(len(claim['ids'])==17 and gate['whole_capture_ids']==claim['ids'] and gate['whole_capture_size']==17 and set(a['id'] for a in rows)<=set(claim['ids']),'five-actual-subset-of-whole17')
ck(gate['claim_subset_not_projected'] and gate['original_capture_unmodified_sha256']==sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-hy-claim.json'),'whole-real-capture-preserved-unprojected')
for o in gate['current_owners']:
 ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'authorization-ownerSHA-'+o['id'])
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==14,'fourteen-full-related-comparison-pages')
for a in comp:
 p=STAGE/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_related_read'],'comparison-raw-full-'+a['name'])
 ck(a['publication_not_inferred_from_local_presence'],'comparison-preserves-published-boundary-'+a['name'])
scope=j(E/'scope.json')
ck(scope['primary_sources']==5 and scope['primary_source_bytes']==26914 and scope['formal_objects']==3 and scope['all_primary_Markdown'],'scope-source-identity')
ck(scope['original_entry_calls']==scope['source_function_calls']==scope['canonical_solver_calls']==scope['new_SPE_BI_enumerations']==scope['new_audit_originals']==scope['next_primary_done_added']==scope['network_or_shared_git_writes']==0,'actual-zero-original-source-solver-BI-calls')
ck(scope['historical_audit_counts_are_source_reported'] and scope['claims_dependencies_not_all_recertified'] and not scope['new_blind_or_external_review'],'history-and-claims-not-new-audit-certification')
ck(scope['independent_M_additive_only_with_matching_suffix_menu'] and scope['unrestricted_product_M_not_claimed_additive'] and scope['unrestricted_M_le_independent_M'],'restricted-versus-unrestricted-product-floor-domain')
ck(not scope['general_overlap_three_margin_bound_proved'] and not scope['general_half_or_six_half_proved'] and scope['five_half_known_from_uploaded_proof_not_new_here'],'known-five-versus-open-six-and-strong-insurer-candidate')

targets=j(W/'target-paths.json');recs=j(W/'semantic-receipts.json')
ck(len(targets)==3 and len(set(targets))==3 and len(recs)==5 and {a['id'] for a in recs}=={a['id'] for a in rows},'three-objects-five-exact-primary-receipts')
for a in recs:
 s=next(x for x in rows if x['id']==a['id'])
 ck(a['owner']=='Boss4' and a['disposition']=='integrated' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-integrated-substantive-'+a['id'])
 ck(a['source_sha256']==s['sha256'] and a['source_size']==s['size'] and a['source_path']==s['source_path'] and a['raw_evidence']==s['path'],'receipt-exact-raw-source-'+a['id'])
 ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'unique-full-content-destinations-'+a['id'])
 ck('external stage only' in a['publication_status'] and 'does not assert published' in a['delivery_status'],'semantic-ready-versus-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==scope['human_math_items']==99,'ninety-nine-mathematical-and-source-obligations')
relations=j(W/'relation-review.json')['relations'];ck(len(relations)==scope['explained_relations']==11 and all(len(a['explanation'])>30 for a in relations),'eleven-explained-semantic-relations')
links=[];ids=[]
for rel in targets:
 p=STAGE/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>9000 and not c0(p),'actual-canonical-substantive-C0-'+p.name)
 ck(not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'no-placeholder-'+p.name)
 for a in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in a or a.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),a.split('#')[0]));roots=[STAGE,REPO,ROOT/'boss4-next-cache/r3-insurer-span-and-sharp-dilution-primary'];found=next((r/q for r in roots if (r/q).is_file()),None);ck(found is not None,'resolved-new-formal-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(found)})
ck(len(set(ids))==3,'three-distinct-stable-ids')
effective=(STAGE/targets[0]).read_text();assets=(STAGE/targets[1]).read_text();failed=(STAGE/targets[2]).read_text()
for s,label in [
 ('M恰为全部完整根纯SPE的最低首人收益','menu-floor-min-root-SPE'),
 ('指定H可补成完整根SPE，当且仅当h≥M','specified-leaf-iff-root-threshold'),
 ('M_{unres}\\le M_{ind}','unrestricted-floor-no-greater-than-restricted'),
 ('D≥3e_ind不推出D≥3e_unres','no-independent-contract-substituted-for-coupled'),
 ('两名玩家的一般目录','two-player-general-BR-reconstruction'),
 ('任意人数的调和后继保底','all-m-harmonic-denominator-chain')]:ck(s in effective,'body-'+label)
for s,label in [('CA-PREFIX-COUPLED-SEAT-BUDGET','prefix-F-G-identity'),('DEG2-CREDIBLE-NEG-FLUX','degree-two-negative-flux'),('STATIC-CROWDING-DOMINATION','static-crowding-sufficient-only'),('POPULATION-DELETION-ALL','all-population-deletion'),('SECURITY-OPT-REAL-TAIL-GAP','specified-optimal-query-tail-gap'),('ROBUST-ROOT-ONLY-3-EQUIV','old-plan-half-equivalence'),('11744','padded-source-finite-audit'),('51403','disjoint-source-finite-audit'),('53正整数','five-uploaded-proof-scope')]:ck(s in assets,'asset-full-unit-'+label)
for s,label in [('2.260825','old-two-path-mechanism'),('635','all-p-not-selfconsistent'),('817','bad-query-not-optimal'),('22428','true-Markov-welfare-separation'),('11>28/3','unreset-final-floor-failure'),('5/6抬成4/3','ancestor-unconditional-commitment'),('2k^2-41k-33','P-pool-exact-tax-counterfamily'),('H(1)','single-query-not-maximum')]:ck(s in failed,'failure-full-unit-'+label)

# Exact arithmetic already stated in the analytic text; no instance/SPE enumeration.
ck(F(271,6)<2*F(161,6) and 2*F(161,6)==F(161,3),'existing-product-root-floor-strict-nonadditivity-scalar')
ck(2*134-144==124 and F(146,3)<2*F(161,6),'existing-product-welfare-is-half-safe-and-root-below-independent-floor')
ck(F(19,14)>F(4,3) and F(59,36)>F(4,3),'existing-bank-free-and-full-menu-values-not-root-payoff')
ck(F(2*22*22-41*22-33,2*(22+1))>0 and F(2*21*21-41*21-33,2*(21+1))<0,'source-P-pool-threshold-arithmetic-not-controller-run')
ck(3*F(2,1)/2==3 and 2*(2+1)-3==3,'two-player-three-dilution-attainment-arithmetic-only')

nexts=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(nexts['rows'])==len(nm['rows'])==5 and not nm['missing'] and sum(a['size'] for a in nexts['rows'])==nexts['source_bytes']==30175,'next-real-local-five30175-not-primary-done')
for a in nexts['rows']:
 p=Path(a['local_path']);ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['actual_local_complete'] and a['not_primary_done_here'],'next-real-raw-not-done-'+a['id'])
files=sorted(p.relative_to(STAGE).as_posix() for p in STAGE.rglob('*') if p.is_file());manifest=j(W/'copy-files.json')
ck(manifest==files and WR+'/copy-files.json' in files,'exact-sorted-self-inclusive-copy-whitelist')
ck(all(not x.startswith('/') and '..' not in Path(x).parts for x in files),'safe-relative-copy-paths')
ck(not any(c0(STAGE/x) for x in files),'all-actual-C0-bytes-except-LF-TAB-CR')
ck(not any(any(line.endswith((' ','\t')) for line in (STAGE/x).read_text().splitlines()) for x in files),'no-trailing-whitespace-all-files')
for x in files:
 if x.endswith('.json'):json.loads((STAGE/x).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'all-strict-finite-JSON')
out={'status':'pass','scope':'read-only raw source/claim/receipts/metadata/links/explicit analytic scalar identities/C0; no source imported/executed','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_sources':5,'primary_source_bytes':26914,'primary_receipts':5,'human_math_items':99,'explained_relations':11,'original_entry_calls':0,'source_function_calls':0,'canonical_solver_calls':0,'new_SPE_BI_enumerations':0,'historical_audit_counts_only_source_reported':True,'M_ind_not_unrestricted_M':True,'new_blind_or_external_review':False,'next_primary_done_added':0,'next_actual_local_bytes':30175,'C0_scope':'actual staged bytes excluding only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
