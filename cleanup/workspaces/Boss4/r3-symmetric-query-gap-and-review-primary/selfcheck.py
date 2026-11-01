#!/usr/bin/env python3
"""Read-only byte/claim/receipt/metadata/link/C0 and written scalar arithmetic, no sources executed."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,posixpath
ROOT=Path('/workspace/scratch/37f0f9248cfc');R=ROOT/'boss4-research';S=ROOT/'boss4-next-cache/r3-symmetric-query-gap-and-review-primary';ER='archives/customer-attraction/tools/evidence/symmetric-query-gap-and-review-primary';WR='cleanup/workspaces/Boss4/r3-symmetric-query-gap-and-review-primary';E=S/ER;W=S/WR
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def c0(p):return any(b<32 and b not in (9,10,13) for b in p.read_bytes())
rows=j(E/'source-manifest.json')['rows'];lm=j(W/'local-source-export-manifest.json');ck(len(rows)==5 and sum(a['size'] for a in rows)==8709 and not lm['missing'],'five-full-local-primary8709')
inv={a['id']:a for a in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for a in rows:
 p=S/a['path'];b=p.read_bytes();ck(len(b)==a['size'] and hashlib.sha256(b).hexdigest()==a['sha256'] and hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==a['blob'],'raw-sizeSHAblob-'+a['id']);ck(a['full_primary_read'] and a['original_entry_calls']==0 and a['source_path'].endswith('.md') and a['path']==ER+'/original/'+a['source_path'],'full-MD-original-not-run-'+a['id']);ck(inv[a['id']]['sha256']==a['sha256'],'inventory-sourceSHA-'+a['id'])
c=j(W/'claim-evidence.json');g=j(W/'primary-authorization-check.json');ck(c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['remote_tip']=='5217f2ec948fa2f33905d49ce7ba205b5ab4f830','actual-pushed-synced5217f2')
ck(len(c['ids'])==12 and g['whole_capture_ids']==c['ids'] and g['whole_capture_size']==12 and set(a['id'] for a in rows)<=set(c['ids']) and g['claim_subset_not_projected'],'actual-five-subset-whole12-unprojected');ck(g['original_capture_unmodified_sha256']==sha(W/'claim-evidence.json')==sha(ROOT/'boss4-r3-next-ja-claim.json'),'whole-original-capture-bytes')
for o in g['current_owners']:ck(o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==next(a['sha256'] for a in rows if a['id']==o['id']),'actual-primary-authorization-ownerSHA-'+o['id'])
comp=j(E/'comparison-manifest.json')['rows'];ck(len(comp)==5,'five-full-comparison-pages')
for a in comp:
 p=S/a['path'];ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['full_related_read'] and a['publication_not_inferred_from_local_presence'],'comparison-raw-full-'+a['name'])
scope=j(E/'scope.json');ck(scope['primary_sources']==5 and scope['primary_source_bytes']==8709 and scope['formal_objects']==2 and scope['all_primary_Markdown'],'source-scope-five-MD-two-formal-objects');ck(scope['original_entry_calls']==scope['source_function_calls']==scope['canonical_solver_calls']==scope['new_LP_or_parameter_scans']==scope['next_primary_done_added']==scope['network_or_shared_git_writes']==0,'zero-original-source-solver-LP-scan')
for k in ['original_review_P_R_not_PW_B','original_review_not_assumed_statement_first_blind','new_informed_one_reply_E_is_negative_BR_slacks','last_two_E_nonpositive_not_general_earlier_debt_bound','existing_71_family_directional_arithmetic_not_new_game','one_direction_false_not_symmetric_PW_refuted','five_component_counts_are_complete_coefficient_domains']:ck(scope[k],'explicit-math-review-scope-'+k)
ck(not scope['general_PW_FTA_or_six_half_proved'] and not scope['new_blind_or_external_review'],'general-budget-open-no-new-blind-external')
recs=j(W/'semantic-receipts.json');targets=j(W/'target-paths.json');ck(len(recs)==5 and len(targets)==len(set(targets))==2 and {a['id'] for a in recs}=={a['id'] for a in rows},'five-exact-receipts-two-distinct-targets')
for a in recs:
 s=next(x for x in rows if x['id']==a['id']);ck(a['disposition']=='integrated' and a['owner']=='Boss4' and a['full_file_reviewed'] and a['related_material_checked'] and a['unique_content_accounted_for'],'final-semantic-integrated-'+a['id']);ck(a['source_sha256']==s['sha256'] and a['source_size']==s['size'] and a['source_path']==s['source_path'] and a['raw_evidence']==s['path'],'receipt-source-identity-'+a['id']);ck(all(len(a[k])>70 for k in ['read_note','comparison_note','decision_note']) and set(a['targets'])<=set(targets),'substantive-full-source-destination-'+a['id']);ck('external stage only' in a['publication_status'] and 'not body-pushed' in a['delivery_status'],'semantic-versus-publication-'+a['id'])
ck((W/'mathematical-self-review.md').read_text().count('- [x] ')==scope['human_math_items']==44,'forty-four-human-math-obligations');rels=j(W/'relation-review.json')['relations'];ck(len(rels)==scope['explained_relations']==6 and all(len(a['explanation'])>30 for a in rels),'six-explained-stage-two-relations')
links=[];ids=[]
for rel in targets:
 p=S/rel;t=p.read_text();parts=t.split('---',2);ck(len(parts)==3 and not t.startswith('#'),'flat-MATEK-'+p.name)
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck(re.search(r'^'+k+r': .+',parts[1],re.M) is not None,'metadata-'+k+'-'+p.name)
 ids.append(re.search(r'^id: (.+)$',parts[1],re.M).group(1));ck(p.stat().st_size>6500 and not c0(p) and not re.search(r'\bTODO\b|\bTBD\b|待填|占位',t),'actual-canonical-full-C0-'+p.name)
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in ref or ref.startswith('#'):continue
  q=posixpath.normpath(posixpath.join(posixpath.dirname(rel),ref.split('#')[0]));roots=[S,R,ROOT/'boss4-next-cache/r3-general-net-exchange-and-full-menu-primary'];p2=next((r/q for r in roots if (r/q).is_file()),None);ck(p2 is not None,'resolved-new-formal-link-'+q);links.append({'from':rel,'to':q,'resolved_at':str(p2)})
ck(len(set(ids))==2,'two-distinct-stable-ids')
a,b=[(S/p).read_text() for p in targets]
for s,label in [('四种会员位只直接核R','outside-customers-cancel-after-substitution'),('e_i(empty)=u_i','empty-action-IC-not-removed'),('E_i(A,T)=-','one-reply-negative-BR-slacks'),('末位则E=0','final-position-boundary'),('反向21','explicit-71-opposite-direction'),('未证明问号PW预算','identity-not-universal-payment')]:ck(s in a,'formal-unit-'+label)
for s,label in [('没有声明“未读主稿先盲证”','no-invented-blindness'),('没有有限实例搜索','original-review-no-search'),('36组件/47872','source-five-coefficient-identity'),('7497','relaxation-not-SPE'),('五人零背景定理不当有背景五人suffix或六人结论','no-five-to-six-background-migration')]:ck(s in b,'review-unit-'+label)
# Literal scalar substitutions of an existing analytic family, not a scan/SPE replay.
k=3;aa=6*k-2;bb=7*k-2;ww=aa+bb;forward=(bb-F(1,2))+bb;reverse=(aa-k)+F(aa,2)
ck(ww==35 and forward==F(75,2) and reverse==21 and forward>ww,'existing71-one-direction-false-explicit-pair')
ck(forward+reverse==F(117,2) and 2*ww-forward-reverse==F(23,2),'existing71-symmetric-positive-slack-scalar')
ck(F(1,2)+(bb-F(aa,2))==F(23,2) and bb-F(aa,2)==4*k-1,'existing71-root-BR-and-final-IC-credit')
ck(3+14+8+5+3+2+1==36,'known-local-component-count-not-verifier-run')
n=j(W/'next-candidates.json');nm=j(W/'next-local-export-manifest.json');ck(len(n['rows'])==len(nm['rows'])==5 and not nm['missing'] and n['source_bytes']==sum(a['size'] for a in n['rows'])==30382,'next-five-actual-local30382-not-done')
for a in n['rows']:
 p=Path(a['local_path']);ck(p.stat().st_size==a['size'] and sha(p)==a['sha256'] and a['actual_local_complete'] and a['not_primary_done_here'],'next-raw-exists-not-primarydone-'+a['id'])
files=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file());manifest=j(W/'copy-files.json');ck(files==manifest and WR+'/copy-files.json' in manifest,'exact-sorted-self-inclusive-copy-whitelist');ck(all(not p.startswith('/') and '..' not in Path(p).parts for p in files),'safe-relative-copy-paths');ck(not any(c0(S/p) for p in files),'all-actual-C0-bytes-except-LF-TAB-CR');ck(not any(any(line.endswith((' ','\t')) for line in (S/p).read_text().splitlines()) for p in files),'no-trailing-whitespace-all-files')
for p in files:
 if p.endswith('.json'):json.loads((S/p).read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
ck(True,'strict-finite-JSON-all-staged')
out={'status':'pass','scope':'raw source/claim/receipt/metadata/link/C0 and existing analytic-family scalar substitutions only; no original/canonical code execution','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'primary_sources':5,'primary_source_bytes':8709,'formal_objects':2,'primary_receipts':5,'human_math_items':44,'explained_relations':6,'original_entry_calls':0,'source_function_calls':0,'canonical_solver_or_LP_calls':0,'new_parameter_scans':0,'last_two_E_nonpositive_known_BR_connection':True,'original_review_not_PW_budget_certification':True,'existing71_forward':str(forward),'existing71_reverse':str(reverse),'existing71_symmetric_slack':str(2*ww-forward-reverse),'next_actual_local_bytes':30382,'next_primary_done_added':0,'C0_scope':'actual bytes excluding only LF/TAB/CR'}
(W/'selfcheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','formal_links']},ensure_ascii=False))
