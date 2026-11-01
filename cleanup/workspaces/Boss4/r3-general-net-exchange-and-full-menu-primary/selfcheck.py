#!/usr/bin/env python3
"""Read-only raw/claim/history/receipts/metadata/links/C0; no original math source calls."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');REPO=ROOT/'boss4-research';S=ROOT/'boss4-next-cache/r3-general-net-exchange-and-full-menu-primary';ER='archives/customer-attraction/tools/evidence/general-net-exchange-and-full-menu-primary';WR='cleanup/workspaces/Boss4/r3-general-net-exchange-and-full-menu-primary';E=S/ER;W=S/WR
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(b<32 and b not in (9,10,13) for b in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json');ck(len(rows)==5 and sum(a['size'] for a in rows)==21398 and not lm['missing'],'five-full-primary21398')
inv={a['id']:a for a in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
for a in rows:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and hashlib.sha256(b).hexdigest()==a['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+a['id']);ck(a['full_source_read'] and a['full_primary_read'] and a['read_before_claim_then_sameSHA_primary_verified'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md') and a['path']==ER+'/original/'+a['source_path'],'true-pre-read-to-primary-sameSHA-'+a['id']);ck(inv[a['id']]['sha256']==a['sha256'],'inventory-sourceSHA-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['remote_tip']=='6ee0cfa438457fb1d930d333113c2295da2d1669','actual-pushed-synced6ee0cfa')
ck(len(c['ids'])==15 and g['whole_capture_ids']==c['ids'] and g['whole_capture_size']==15 and set(a['id'] for a in rows)<=set(c['ids']) and g['claim_subset_not_projected'],'five-subset-original15-unprojected');ck(g['original_capture_unmodified_sha256']==sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-io-claim.json'),'full-actual-capture-unmodified')
for o in g['current_owners']:ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'actual-owner-sourceSHA-'+o['id'])
tr=j(E/'authorization-transition.json');ck(len(tr['history'])==7 and tr['original_draft_boundary_preserved_not_rewritten'] and tr['actual_IO_claim_remote_tip']==c['remote_tip'] and tr['actual_IO_claim_status']=='pushed' and tr['actual_IO_local_sync']=='synced' and tr['this_agent_network_or_shared_git_writes']==0 and tr['math_body_published_or_done_not_inferred_from_claim'],'true-authorization-transition-not-retrospective-success')
for a in tr['history']:
 p=S/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['unchanged_bytes'],'original-draft-history-raw-'+p.name)
old=j(E/'intake-history/draft-authorization-boundary.json');notes=j(E/'intake-history/draft-source-review-notes.json');ck(old['status']=='draft-only-not-actualclaimed' and not old['primary_done_claimed'] and not old['successful_semantic_receipts_written'] and notes['not_a_semantic_receipt'],'old-blocked-not-claimed-notes-preserved-honestly')
context=j(E/'context-manifest.json');ck(len(context['rows'])==2 and context['additional_primary_done']==context['original_entry_calls_here']==0,'two-full-context-no-extra-done-entry')
for a in context['rows']:
 p=S/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_context_read'] and not a['additional_primary_done'],'context-full-raw-'+a['id'])
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==7,'seven-full-related-comparisons')
for a in comp:
 p=S/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_related_read'] and a['published_not_inferred_from_local_presence'],'comparison-full-byte-'+a['name'])
scope=j(E/'scope.json');ck(scope['actual_primary_claimed'] and scope['successful_cleanup_receipts_written'] and scope['prior_blocked_draft_preserved_unchanged'] and scope['formal_objects']==3,'current-final-semantic-claim-scope')
ck(scope['original_entry_calls']==scope['source_function_calls']==scope['canonical_solver_calls']==scope['new_LP_or_parameter_scans']==scope['context_primary_done_added']==scope['network_or_shared_git_writes']==0,'actual-zero-source-original-solver-LP-scan')
for k in ['FTA_not_refuted_by_individual_Mfull_failure','Mpath_defined_as_pooled_actual_full_columns','same_p_quadratic_not_automatically_preserved_by_quotient','net_exchange_not_gross_omission','static_price_and_rook_counterexamples_not_SPE','historical_audit_numbers_source_reported']:ck(scope[k],'actual-scope-'+k)
ck(not scope['new_blind_or_external_review'] and not scope['general_half_or_six_half_proved'],'no-new-blind-or-general-half-claim')
receipts=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(receipts)==5 and len(targets)==len(set(targets))==3 and {a['id'] for a in receipts}=={a['id'] for a in rows},'five-exact-receipts-three-objects')
for a in receipts:
 r=next(x for x in rows if x['id']==a['id']);ck(a['disposition']=='integrated' and a['owner']=='Boss4' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-semantic-integrated-'+a['id']);ck(a['source_sha256']==r['sha256'] and a['source_size']==r['size'] and a['source_path']==r['source_path'] and a['raw_evidence']==r['path'],'receipt-exact-source-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets) and '本README未claim' not in a['read_note'],'substantive-source-coverage-no-stale-gate-'+a['id']);ck('external stage only' in a['publication_status'] and 'not body-pushed' in a['delivery_status'],'semantic-versus-body-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==scope['human_math_items']==56,'fifty-six-human-mathematical-obligations');rels=j(W/'relation-review.json')['relations'];ck(len(rels)==scope['explained_relations']==7 and all(len(a['explanation'])>30 for a in rels),'seven-explained-stage-two-relations')
ids=[];links=[]
for rel in targets:
 p=S/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>5000 and not c0(p) and 'intake-draft' not in parts[1] and '本批未实际claim' not in t and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'actual-canonical-full-C0-current-scope-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));roots=[S,REPO,ROOT/'boss4-next-cache/r3-coupled-and-assigned-profit-seats-primary'];p2=next((r/q for r in roots if (r/q).is_file()),None);ck(p2 is not None,'resolved-current-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(p2)})
ck(len(set(ids))==3,'three-distinct-stable-ids')
a,b,d=[(S/p).read_text() for p in targets]
for s,label in [('C^+-D=T_{tail}-H','complete-tail-signed-identity'),('C^+-u=T_{tail}-H-e','actual-IC-slack-retained'),('M_{path}(\\sigma)','pooled-full-actual-menu-definition'),('它不自动保某个原二次FTA坏p','quotient-free-menu-not-quadratic-witness')]:ck(s in a,'math-unit-'+label)
for s,label in [('lost','net-swap-loss'),('p_i(d_x)','random-comparison-indices'),('L_i-L_{i-1}','exact-net-increment-credit'),('尚未','cumulative-payment-not-proved')]:
 if label=='cumulative-payment-not-proved':ck('未证' in b,'math-unit-'+label)
 else:ck(s in b,'math-unit-'+label)
for s,label in [('45个不同非空主题','ten-customer-complete-catalog'),('B(v)=10(1-v/2)_+','fractional-price-exact-proof'),('3/2>1+1/q','rook-own-leaf-corrected-deviation'),('这些静态失败','not-half-counterexample')]:ck(s in d,'math-unit-'+label)
ck(3*F(141,10)-F(6879+5349+5349,400)==-F(657,400),'source381-three-row-sum-only-no-IC-replay')
ck(F(36)-21==15 and F(9)+30*(F(1,4)-F(1,9))==F(79,6) and F(79,6)-15==-F(11,6),'source61-local-potential-arithmetic-no-controller-run')
ck(10*(1-F(3,2)/2)==F(5,2)==4-F(3,2) and 10*(1-F(1,2))==5>4 and 6<=2*4,'static-price-compression-exact-values-not-SPE-enumeration')
n=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(n['rows'])==len(nm['rows'])==5 and not nm['missing'] and n['source_bytes']==sum(x['size'] for x in n['rows'])==8709,'next-five-real-local8709-not-primary-done')
for a in n['rows']:
 p=Path(a['local_path']);ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['actual_local_complete'] and a['not_claimed_or_primary_done_here'],'next-actual-raw-not-done-'+a['id'])
files=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file());manifest=j(W/'copy-files.json');ck(files==manifest and WR+'/copy-files.json' in manifest,'exact-sorted-self-inclusive-copy-whitelist');ck(all(not x.startswith('/') and '..' not in Path(x).parts for x in files),'safe-relative-copy-paths');ck(not any(c0(S/x) for x in files),'all-actual-C0-bytes-except-LF-TAB-CR');ck(not any(any(line.endswith((' ','\t')) for line in (S/x).read_text().splitlines()) for x in files),'no-trailing-whitespace-all-files')
for x in files:
 if x.endswith('.json'):json.loads((S/x).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'raw size/SHA/blob/authentic whole claim/history transition/receipts/metadata/links/C0 and stated scalar arithmetic only; no source or solver execution','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'primary_source_bytes':21398,'formal_objects':3,'primary_receipts':5,'human_math_items':56,'explained_relations':7,'original_entry_calls':0,'source_function_calls':0,'canonical_solver_or_LP_calls':0,'prior_unclaimed_blocked_draft_history_preserved_files':7,'prior_boundary_not_rewritten_as_success':True,'Mpath_pooled_actual_full_columns_not_individual_Mfull':True,'static_compression_examples_not_SPE_counterexamples':True,'context_primary_done_added':0,'next_real_local_bytes':8709,'C0_scope':'actual bytes excluding only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
