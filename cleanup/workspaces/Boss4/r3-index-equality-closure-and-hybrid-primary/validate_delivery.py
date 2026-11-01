"""Structural audit only; no mathematical entry runs or old certificate audits."""
from pathlib import Path
import ast,hashlib,json,re
WS=Path(__file__).resolve().parent;stage=WS.parents[3]
assert stage.name=='r3-index-equality-closure-and-hybrid-primary'
repo=stage.parent.parent/'boss4-research';ev=stage/'archives/customer-attraction/tools/evidence/index-equality-closure-and-hybrid-primary'
out=WS/'self-check.json';assert not out.exists(),'Record reason before repeating structural audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((ev/'primary-manifest.json').read_text());ids={x['id'] for x in primary['sources']}
assert len(ids)==5 and primary['primary_bytes']==22913
for x in primary['sources']:
 p=stage/x['saved_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
claim=json.loads((WS/'claim-receipt.json').read_text());obs=json.loads((WS/'claim-observation.json').read_text())
assert sha(WS/'claim-receipt.json')==obs['capture_sha256']
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced'
assert len(claim['ids'])==22 and ids<=set(claim['ids'])
assert set(obs['claimed_primary_ids'])==ids and set(obs['all_actual_claim_ids'])==set(claim['ids'])
assert obs['no_projection_receipt_created'] is True and obs['full_original_multi_group_receipt_retained'] is True
assert all(x['record']['owner']=='Boss4' for x in obs['local_working_tree_owners'])
receipt=json.loads((WS/'semantic-receipts.json').read_text());assert len(receipt)==5 and {x['id'] for x in receipt}==ids
for x in receipt:
 assert x['disposition']=='integrated'
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(len(x[k])>50 for k in ['read_note','comparison_note','decision_note'])
 assert all((stage/p).is_file() for p in x['targets'])
runtime=json.loads((ev/'runtime-record.json').read_text());d=json.loads((ev/'new-index-pattern-and-hybrid-check.json').read_text())
assert runtime['new_definition_entry_runs']==1 and runtime['original_entries']==runtime['external_solver_calls']==runtime['old_math_reruns']==0
assert sha(ev/runtime['entry'])==runtime['entry_sha256'] and sha(ev/runtime['output'])==runtime['output_sha256']
assert d['status']=='pass' and all(d['source_comparison'].values())
assert len(d['terminal_rows'])==10 and sum(x['reused_ER_row'] for x in d['terminal_rows'])==1
assert d['new_terminal_row_count']==9 and d['new_terminal_literal_terms']==11520
assert len(d['pair_rows'])==220 and d['pair_atom_compact_literal_equalities']==14080 and d['literal_branch_query_triples']==176000
assert d['weak_violations']==24 and d['strong_violations']==38
c=d['hybrid_cases'][0]
assert (c['m'],c['k'],c['W'],c['OPT'])==(10,2,3963,8400)
assert c['actual_path_nodes']==10 and c['actual_path_comparisons_including_self']==200 and c['actual_path_comparisons_nonself']==190
assert c['terminal_nodes']==0 and c['terminal_histories_exhausted'] is False and c['full_SPE_claimed'] is False
assert c['missing_offpath_row']['slack']=='-735'
assert [x['terminal_nodes'] for x in d['hybrid_cases'][1:]]==[36,576]
assert [x['terminal_comparisons_including_self'] for x in d['hybrid_cases'][1:]]==[216,4608]
assert all(x['full_SPE_claimed'] is False for x in d['hybrid_cases'])
assert len(d['source_md_hashes_full_paths'])==5
for x in primary['sources']:assert d['source_md_hashes_full_paths'][x['path']]==x['sha256']
assert sha(ev/'comparison/five_player_indexed_bound.json')==d['input64_sha256']
dep=json.loads((ev/'dependency-boundary.json').read_text());assert len(dep['safe_local_export']['missing'])==11 and not dep['safe_local_export']['rows']
assert sha(ev/'comparison/reused-ER-AE-row.json')==dep['reused_ER_AE_row']['sha256']
jsons=sorted(stage.rglob('*.json'))
for p in jsons:json.loads(p.read_text())
pys=sorted(stage.rglob('*.py'))
for p in pys:ast.parse(p.read_text(),filename=str(p))
canonical=sorted((stage/'archives/customer-attraction/state').rglob('*.md'));assert len(canonical)==3
newmd=canonical+[ev/'README.md',WS/'HANDOFF.md',WS/'math-self-review.md',WS/'relation-review.md'];links=[]
for p in newmd:
 text=p.read_text()
 if p in canonical:
  assert text.startswith('---\n')
  for key in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert key in text[:3000]
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if dest.startswith(('https:','http:','#','source:','mailto:')):continue
  dest=dest.split('#',1)[0].strip('<>');q=(p.parent/dest).resolve()
  if q.is_file():where='stage'
  elif q.is_relative_to(stage) and (repo/q.relative_to(stage)).is_file():where='existing-canonical'
  else:raise AssertionError((str(p),dest))
  links.append({'from':str(p.relative_to(stage)),'to':dest,'resolved':where})
report={'status':'pass','structural_audit_runs':1,'mathematical_entry_not_run_by_validator':True,'actual_primary_count':5,'primary_bytes':22913,'all_integrated_receipts':5,'whole_claim_ids':22,'worker_subset_ids':5,'original_multigroup_claim_not_projected':True,'owner_sha_verified':True,'canonical_count':3,'all_stageJSON_parsed':len(jsons),'all_pythonAST_parsed_without_execution':len(pys),'live_newMD_links':links,'raw_links':'sourcecontextpreserved, missingoriginalsnotfabricated','new_definition_entry_runs':1,'original_entries':0,'external_solver_calls':0,'reused_ER_row_not_rerun':True,'m10_contract':'onlyactual200andmissingnegative, zeroexhaustedterminalnodes, notfullSPE','all_hybrid_fullSPE_flags_false':True,'42point_andrestricted_certificates_not_newlyverified':True,'no_R18_falsefullSPE_used_or_rerun':True,'no_sharedGit_network_auth_spawn':True,'unpaid_interfaces':['generalsixhalf','unrestrictedtypepricing','full-depthcommonpayment']}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','actual_primary_count','whole_claim_ids','canonical_count','all_stageJSON_parsed','all_pythonAST_parsed_without_execution','new_definition_entry_runs','original_entries']}))
