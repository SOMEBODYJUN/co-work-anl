"""Structural final audit only; never executes any mathematical entry."""
from pathlib import Path
import ast,hashlib,json,re
WS=Path(__file__).resolve().parent;stage=WS.parents[3]
assert stage.name=='r3-rank-one-thinning-and-aligned-closure-primary'
repo=stage.parent.parent/'boss4-research';ev=stage/'archives/customer-attraction/tools/evidence/rank-one-thinning-and-aligned-closure-primary'
out=WS/'self-check.json';assert not out.exists(),'Record reason before repeating structural audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((ev/'primary-manifest.json').read_text());ids={x['id'] for x in primary['sources']}
assert len(ids)==5 and primary['primary_bytes']==38372
for x in primary['sources']:
 p=stage/x['saved_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
claim=json.loads((WS/'claim-receipt.json').read_text());observation=json.loads((WS/'claim-observation.json').read_text())
assert sha(WS/'claim-receipt.json')==observation['capture_sha256']
assert claim['actor']=='Boss4' and claim['status']=='pushed' and claim['local_sync']['status']=='synced' and set(claim['ids'])==ids
assert all(x['record']['owner']=='Boss4' for x in observation['local_working_tree_owners'])
pre=json.loads((WS/'preclaim-preparation-observation.json').read_text());assert pre['superseded_by']=='claim-observation.json'
assert not (WS/'preclaim-status.json').exists()
receipt=json.loads((WS/'semantic-receipts.json').read_text());assert len(receipt)==5 and {x['id'] for x in receipt}==ids
for x in receipt:
 assert x['disposition']=='integrated'
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(len(x[k])>50 for k in ['read_note','comparison_note','decision_note'])
 assert all((stage/p).is_file() for p in x['targets'])
runtime=json.loads((ev/'runtime-record.json').read_text());d=json.loads((ev/'new-thinning-definition-check.json').read_text())
assert runtime['new_definition_entry_runs']==1 and runtime['original_entries']==runtime['external_solver_calls']==0
assert runtime['claim_and_owner_before_new_execution'] is True
assert sha(ev/runtime['entry'])==runtime['entry_sha256'] and sha(ev/runtime['output'])==runtime['output_sha256']
assert d['status']=='pass' and d['nodes']==21 and d['including_self_comparisons']==84 and d['nonself_comparisons']==63
assert len(d['all_rows'])==21 and len(d['all64_terminal_coverages'])==64
assert d['W']==d['OPT']==13 and d['half_slack']==13
assert [x['coefficients'] for x in d['three_zero_integral_obstructions']]==[[0,-2,3],[-2,4,0],[1,0,-3]]
assert len(d['source_md_hashes_full_paths'])==5
for x in primary['sources']:assert d['source_md_hashes_full_paths'][x['path']]==x['sha256']
reuse=json.loads((ev/'sufficient-run-reuse.json').read_text());assert reuse['new_runs_for_reuse']==0
DJ=repo/reuse['rankone']['result_path'];assert sha(DJ)==reuse['rankone']['sha256']
assert reuse['rankone']['case']['constrained_ordered_nodes']==621
ER=Path(reuse['AE64']['mature_stage_result_path']);assert sha(ER)==reuse['AE64']['sha256']
dependency=json.loads((ev/'dependency-boundary.json').read_text());assert len(dependency['safe_local_export']['missing'])==9 and not dependency['safe_local_export']['rows']
jsons=sorted(stage.rglob('*.json'))
for p in jsons:json.loads(p.read_text())
pys=sorted(stage.rglob('*.py'))
for p in pys:ast.parse(p.read_text(),filename=str(p))
canonical=sorted((stage/'archives/customer-attraction/state').rglob('*.md'));assert len(canonical)==4
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
report={'status':'pass','structural_audit_runs':1,'mathematical_program_not_run_by_validator':True,'actual_primary_count':5,'primary_bytes':38372,'all_integrated_receipts':5,'whole_actual_claim_owner_verified':True,'preclaim_history_not_success_receipt':True,'all_primary_size_sha256_blob_sha1_verified':True,'canonical_count':4,'all_stage_JSON_parsed':len(jsons),'all_Python_AST_parsed_without_execution':len(pys),'live_new_md_links':links,'historical_raw_md_links':'Preserved sourcecontext, unprovidedprograms notfabricated','new_thinning_entry_runs':1,'original_entries':0,'external_solver_calls':0,'new_rank_orAE64_runs':0,'new38mass_orroot_coupling_oruniform_runs':0,'all5source_fullpath_bindings_verified':True,'no_sharedGit_network_auth_spawn':True,'not_certified':['fullnineplayerrankpolicySPE','38mass/alignednegative/root92/96/9770certificates','uniformgeneralinterface','generalsixhalf'],'analytic_only':['allmemptygraft','finiteTrootfamily','positivequadratureboundanduniformuniqueness','rankunboundedfamily','aligneduniversalrow']}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','actual_primary_count','canonical_count','all_stage_JSON_parsed','all_Python_AST_parsed_without_execution','new_thinning_entry_runs','original_entries']}))
