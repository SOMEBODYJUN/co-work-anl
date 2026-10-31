"""Structural delivery audit only; does not rerun the mathematical entry."""
from pathlib import Path
import ast,hashlib,json,re
WS=Path(__file__).resolve().parent
stage=WS.parents[3]
assert stage.name=='r3-repeated-last-prefix-and-partition-primary'
repo=stage.parent.parent/'boss4-research'
ev=stage/'archives/customer-attraction/tools/evidence/repeated-last-prefix-and-partition-primary'
out=WS/'self-check.json'
assert not out.exists(),'Do not rerun final structural audit without recording the reason'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((ev/'primary-manifest.json').read_text())
ids=set()
for x in primary['sources']:
 p=stage/x['saved_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
 ids.add(x['id'])
assert len(ids)==5 and sum(x['size'] for x in primary['sources'])==25157
dependency=json.loads((ev/'dependency-boundary.json').read_text())
for x in dependency['provided_comparison_sources']:
 p=stage/x['saved_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
receipt=WS/'claim-receipt.json'
observation=json.loads((WS/'claim-observation.json').read_text())
claim=json.loads(receipt.read_text())
assert sha(receipt)==observation['capture_sha256']
assert claim['status']=='pushed' and claim['actor']=='Boss4'
assert claim['local_sync']['status']=='synced'
assert set(claim['ids'])==ids
assert all(x['record']['owner']=='Boss4' for x in observation['local_working_tree_owners'])
semantic=json.loads((WS/'semantic-receipts.json').read_text())
assert len(semantic)==5 and {x['id'] for x in semantic}==ids
for x in semantic:
 assert x['disposition']=='integrated'
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(len(x[k])>50 for k in ['read_note','comparison_note','decision_note'])
 assert all((stage/p).is_file() for p in x['targets'])
proposal_dir=ev/'unapplied-corrections/pfr-opt-status'
proposal=json.loads((proposal_dir/'proposal.json').read_text())
assert sha(proposal_dir/'before.md')==proposal['original_sha256']
assert sha(proposal_dir/'proposed.md')==proposal['proposed_sha256']
assert not (stage/proposal['target_path']).exists(),'Old canonical target must not be in worker manifest'
assert (stage/proposal['publish_dependency']).is_file()
runtime=json.loads((ev/'runtime-record.json').read_text())
mathematics=json.loads((ev/'new-definition-check.json').read_text())
assert runtime['original_program_entry_runs']==0 and runtime['new_definition_entry_runs']==1 and runtime['optimizer_calls']==0
assert sha(ev/'new-definition-check.json')==runtime['output_sha256']
assert mathematics['status']=='pass' and len(mathematics['all_m_k_cases'])==5050
assert mathematics['fourteen_customer_point']['including_self_comparisons']==42
assert mathematics['fourteen_customer_point']['nonself_comparisons']==35
assert len(mathematics['fourteen_customer_point']['all_36_ordered_comparison_tuples'])==36
assert len(mathematics['fourteen_customer_point']['all_four_order_matching_checks'])==4
json_paths=sorted(stage.rglob('*.json'))
for p in json_paths:json.loads(p.read_text())
py_paths=sorted(stage.rglob('*.py'))
for p in py_paths:ast.parse(p.read_text(),filename=str(p))
# Raw originals/proposal snapshots preserve their source-context missing links.
# Only new canonical prose and newly authored guide links use live result paths.
md_paths=sorted((stage/'archives/customer-attraction/state').rglob('*.md'))+[ev/'README.md',WS/'HANDOFF.md',WS/'math-self-review.md',WS/'relation-review.md']
links=[]
for p in md_paths:
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if dest.startswith(('https:','http:','#','source:','mailto:')):continue
  dest=dest.split('#',1)[0].strip('<>')
  q=(p.parent/dest).resolve()
  if q.is_file():resolved='stage'
  elif q.is_relative_to(stage) and (repo/q.relative_to(stage)).is_file():resolved='existing-canonical'
  else:raise AssertionError((str(p),dest,str(q)))
  links.append({'from':str(p.relative_to(stage)),'to':dest,'resolved':resolved})
for p in (stage/'archives/customer-attraction/state').rglob('*.md'):
 t=p.read_text();assert t.startswith('---\n')
 for key in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert key in t[:2500],(p,key)
result={'status':'pass','audit_kind':'structural-only-not-new-mathematical-run','structural_audit_runs':1,'actual_primary_count':5,'primary_bytes':25157,'comparison_source_count':2,'comparison_source_bytes':10764,'primary_byte_sha256_blob_sha1_verified':True,'full_original_claim_preserved':True,'expected_actual_owner_verified':True,'semantic_receipt_count':5,'new_canonical_object_count':3,'all_stage_json_parsed':len(json_paths),'all_stage_python_ast_parsed_without_execution':len(py_paths),'new_canonical_and_guide_links_checked':links,'historical_raw_md_and_proposal_links':'Preserved in original source/target directory context; unprovided historical links not fabricated as live files.','old_pfr_target_excluded_from_stage':True,'proposal_original_and_proposed_hashes_verified':True,'old_status_correction':'Root canonical draft alreadyincorporates after fullread, sameEF publication; worker appliesnothing','math_entry_runs':1,'original_entry_runs':0,'optimizer_calls':0,'no_shared_git_network_auth_spawn':True,'unpaid_interfaces':['general sixplayer half; k1/2 cases','E_mix≤2actualSPE W or strongerE_* version','criterion boundarylambda andbestpossible repeatedtheme theorem'],'source_run_claims_not_upgraded':True}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','actual_primary_count','new_canonical_object_count','all_stage_json_parsed','all_stage_python_ast_parsed_without_execution','math_entry_runs','original_entry_runs']}))
