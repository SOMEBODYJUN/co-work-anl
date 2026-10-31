"""Structural verification only: the mathematical entry is never rerun here."""
from pathlib import Path
from fractions import Fraction as F
import ast,hashlib,json,re
WS=Path(__file__).resolve().parent;stage=WS.parents[3]
assert stage.name=='r3-security-cartesian-and-disjoint-primary'
repo=stage.parent.parent/'boss4-research'
ev=stage/'archives/customer-attraction/tools/evidence/security-cartesian-and-disjoint-primary'
out=WS/'self-check.json';assert not out.exists(),'Record reason before repeating structural audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((ev/'primary-manifest.json').read_text());ids={x['id'] for x in primary['sources']}
assert len(ids)==5 and primary['primary_bytes']==23155
for x in primary['sources']:
 p=stage/x['saved_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
obs=json.loads((WS/'claim-observation.json').read_text());claim=json.loads((WS/'claim-receipt.json').read_text())
assert sha(WS/'claim-receipt.json')==obs['capture_sha256']
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced'
assert set(claim['ids'])==ids and all(x['record']['owner']=='Boss4' for x in obs['local_working_tree_owners'])
receipt=json.loads((WS/'semantic-receipts.json').read_text())
assert len(receipt)==5 and {x['id'] for x in receipt}==ids
for x in receipt:
 assert x['disposition']=='integrated'
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(len(x[k])>50 for k in ['read_note','comparison_note','decision_note'])
 assert all((stage/p).is_file() for p in x['targets'])
runtime=json.loads((ev/'runtime-record.json').read_text());result=json.loads((ev/'new-product-and-security-check.json').read_text())
assert runtime['new_definition_entry_runs']==1 and runtime['original_entries']==0 and runtime['external_solver_calls']==0
assert runtime['exact_tiny_LP_values_by_explicit_vertex_plus_dual_enumeration']==4
assert sha(ev/runtime['entry'])==runtime['entry_sha256'] and sha(ev/runtime['output'])==runtime['output_sha256']
assert result['status']=='pass'
c=result['cartesian'];g=result['gadget_deletion_and_disjoint']
assert c['nodes']==273 and c['including_self_comparisons']==4368 and c['nonself_comparisons']==4095
assert len(c['all273_nodes_and4368_comparisons'])==273 and len(c['all273_policy_entries'])==273
assert c['G1']=='161/6' and c['G2']=='271/6' and c['g']=='55/3'
assert c['W']==134 and c['OPT']==144 and c['half_slack']==124 and F(c['joint_strong_aggregate_slack_lower'])==24
assert g['nodes']==43 and g['including_self_comparisons']==258 and g['nonself_comparisons']==215
assert len(g['two_copy_uniform_lower_all4368'])==4368 and g['two_copy_v6_exact']=='35/4'
assert g['fractional_violation']=='1/105'
binding=json.loads((ev/'source-version-binding.json').read_text())
assert {x['id'] for x in binding['sources']}==ids and len({x['path'] for x in binding['sources']})==5
assert len(result['source_md_hashes'])<5,'Known basename metadata limitation must stay explicit'
dependency=json.loads((ev/'dependency-boundary.json').read_text())
assert len(dependency['safe_local_export']['missing'])==7 and not dependency['safe_local_export']['rows']
jsons=sorted(stage.rglob('*.json'))
for p in jsons:json.loads(p.read_text())
pys=sorted(stage.rglob('*.py'))
for p in pys:ast.parse(p.read_text(),filename=str(p))
canonical=sorted((stage/'archives/customer-attraction/state').rglob('*.md'));assert len(canonical)==3
newmd=canonical+[ev/'README.md',WS/'HANDOFF.md',WS/'math-self-review.md',WS/'relation-review.md'];links=[]
for p in newmd:
 t=p.read_text()
 if p in canonical:
  assert t.startswith('---\n')
  for key in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert key in t[:3000]
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if dest.startswith(('https:','http:','#','source:','mailto:')):continue
  dest=dest.split('#',1)[0].strip('<>');q=(p.parent/dest).resolve()
  if q.is_file():where='stage'
  elif q.is_relative_to(stage) and (repo/q.relative_to(stage)).is_file():where='existing-canonical'
  else:raise AssertionError((str(p),dest))
  links.append({'from':str(p.relative_to(stage)),'to':dest,'resolved':where})
report={'status':'pass','structural_audit_runs':1,'mathematical_entry_not_executed_by_validator':True,'actual_primary_count':5,'primary_bytes':23155,'semantic_receipts':5,'all_integrated':True,'whole_claim_actual_owner_verified':True,'all_primary_size_sha256_blob_sha1_verified':True,'canonical_count':3,'all_stage_JSON_parsed':len(jsons),'all_Python_AST_parsed_without_execution':len(pys),'new_live_md_links':links,'archived_source_links':'retained sourcecontext; missinghistoricalprograms not fabricated','new_definition_entry_runs':1,'original_entries':0,'external_solver_calls':0,'tiny_exactLP_values_by_explicit_vertices_anddual':4,'known_output_basename_metadata_limitation':'full5pathbindings independentlypreserved; successfulcode notchanged/rerun','no_EF_ER_rerun':True,'own_Cartesian_strategy_not_missingauthorJSON':True,'sixplayerdisjointstrategy_not_newlycertified':True,'root_scan_not_newlycertified':True,'no_sharedGit_network_auth_spawn':True,'unpaid_interfaces':['generalstrongaggregateandPAIR','generalsixhalf','exactrationalcompilerseedwithstrictrootmargin','beyond3Cartesianmenu']}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','actual_primary_count','canonical_count','all_stage_JSON_parsed','all_Python_AST_parsed_without_execution','new_definition_entry_runs','original_entries','tiny_exactLP_values_by_explicit_vertices_anddual']}))
