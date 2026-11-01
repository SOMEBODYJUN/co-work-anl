"""Structural package verification only; mathematical entries are not run."""
from pathlib import Path
from fractions import Fraction
import ast,hashlib,json,re
WS=Path(__file__).resolve().parent
stage=WS.parents[3]
assert stage.name=='r3-terminal-menu-exclusion-and-envelope-primary'
repo=stage.parent.parent/'boss4-research'
ev=stage/'archives/customer-attraction/tools/evidence/terminal-menu-exclusion-and-envelope-primary'
output=WS/'self-check.json'
assert not output.exists(),'Record any reason before repeating final structural audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((ev/'primary-manifest.json').read_text())
ids={x['id'] for x in source['sources']}
assert len(ids)==5 and source['primary_bytes']==20018
for x in source['sources']:
 p=stage/x['saved_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
observation=json.loads((WS/'claim-observation.json').read_text())
claim=json.loads((WS/'claim-receipt.json').read_text())
assert sha(WS/'claim-receipt.json')==observation['capture_sha256']
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced'
assert set(claim['ids'])==ids and all(x['record']['owner']=='Boss4' for x in observation['local_working_tree_owners'])
receipts=json.loads((WS/'semantic-receipts.json').read_text())
assert len(receipts)==5 and {x['id'] for x in receipts}==ids
assert sum(x['disposition']=='integrated' for x in receipts)==3
assert sum(x['disposition']=='duplicate' for x in receipts)==2
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(len(x[k])>50 for k in ['read_note','comparison_note','decision_note'])
 for p in x['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
 if x['disposition']=='duplicate':
  p=x['targets'][0]
  assert not (stage/p).exists(),'Duplicate canonicalbody must not be rewritten'
  original=next(y for y in source['sources'] if y['id']==x['id'])
  assert original['path'] in (repo/p).read_text(),'Existingbody must already cite exactsource'
runtime=json.loads((ev/'runtime-record.json').read_text())
mathematics=json.loads((ev/'new-ae-menu-exclusion.json').read_text())
assert runtime['original_program_entry_runs']==0 and runtime['new_selected_definition_entry_runs']==1
assert runtime['optimizer_calls']==0 and runtime['new_envelope_LP_runs']==0 and runtime['new_prefix_runs']==0 and runtime['new_fourteen_point_runs']==0
assert sha(ev/'new-ae-menu-exclusion.json')==runtime['output_sha256']
assert mathematics['status']=='selected-necessary-row-violated'
assert mathematics['input_atoms']==64 and mathematics['expanded_offdiagonal_terms']==1280
assert len(mathematics['atom_records'])==64
assert Fraction(mathematics['necessary_row_slack'])<0
assert Fraction(mathematics['full_sum_row_slack'])>0 and Fraction(mathematics['diagonal_sum_row_slack'])>0
assert sha(ev/'comparison/five_player_indexed_bound.json')==mathematics['input_sha256']
EFpub=json.loads((ev/'EF-publication-observation.json').read_text())
assert EFpub['body_pushed']=='e19cb68758cc9d07ed419d3920a5390991a20bdc'
for x in EFpub['worker_verified_local_body_bytes_equal_mature_manifest']:
 assert sha(repo/x['path'])==x['sha256'] and (repo/x['path']).stat().st_size==x['size']
json_paths=sorted(stage.rglob('*.json'))
for p in json_paths:json.loads(p.read_text())
py_paths=sorted(stage.rglob('*.py'))
for p in py_paths:ast.parse(p.read_text(),filename=str(p))
canonical=sorted((stage/'archives/customer-attraction/state').rglob('*.md'))
assert len(canonical)==2
new_md=canonical+[ev/'README.md',WS/'HANDOFF.md',WS/'math-self-review.md',WS/'relation-review.md']
links=[]
for p in new_md:
 text=p.read_text()
 if p in canonical:
  assert text.startswith('---\n')
  for key in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert key in text[:2500]
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if dest.startswith(('https:','http:','#','source:','mailto:')):continue
  dest=dest.split('#',1)[0].strip('<>');q=(p.parent/dest).resolve()
  if q.is_file():where='stage'
  elif q.is_relative_to(stage) and (repo/q.relative_to(stage)).is_file():where='existing-canonical'
  else:raise AssertionError((str(p),dest))
  links.append({'from':str(p.relative_to(stage)),'to':dest,'resolved':where})
result={'status':'pass','structural_audit_runs':1,'mathematical_program_not_executed_by_this_validator':True,'actual_primary_count':5,'primary_bytes':20018,'dispositions':{'integrated':3,'duplicate':2},'whole_actual_claim_and_owner_verified':True,'primary_size_sha256_blob_sha1_verified':True,'new_canonical_count':2,'duplicate_canonical_targets_not_overwritten':True,'existing_targets_already_cite_duplicate_source_paths':True,'EF_actual_publication_report_and_current_bytes_verified':True,'all_stage_json_parsed':len(json_paths),'all_python_ast_parsed_without_running':len(py_paths),'live_new_md_links':links,'archived_source_links':'preserved historical source context, unprovided oldprogram links not fabricated','new_AE_selected_entry_runs':1,'original_entries':0,'new_EF_prefix_or_14_point_runs':0,'envelope_solver_runs':0,'optimizer_calls':0,'AE_fixed64_negative_and_full_diagonal_positive':True,'no_437_dual_reaudit':True,'no_enhanced_template_optimum_or_true_SPE_from_fixed_point':True,'no_network_auth_git_spawn':True,'unpaid_interfaces':['general6half','E_mix or E_* paid byactualSPE W','enhancedmenu template fulltype optimum/realizability']}
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','actual_primary_count','dispositions','new_canonical_count','all_stage_json_parsed','all_python_ast_parsed_without_running','new_AE_selected_entry_runs','original_entries']}))
