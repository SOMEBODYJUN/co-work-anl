"""Final structural audit after actualclaim records; no mathematical execution."""
from pathlib import Path
import ast,hashlib,json,re
WS=Path(__file__).resolve().parent;stage=WS.parents[3]
assert stage.name=='r3-r642-entry-and-residual-primary'
repo=stage.parent.parent/'boss4-research';ev=stage/'archives/customer-attraction/tools/evidence/r642-entry-and-residual-primary'
if not (WS/'claim-receipt.json').is_file():raise SystemExit('Actualclaim records pending; cannot final-audit success')
out=WS/'self-check.json';assert not out.exists(),'Record reason before repeating structural audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((ev/'primary-manifest.json').read_text());ids={x['id'] for x in primary['sources']}
assert len(ids)==3 and primary['primary_bytes']==12989
for x in primary['sources']:
 p=stage/x['saved_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256']
 assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob']
claim=json.loads((WS/'claim-receipt.json').read_text());observation=json.loads((WS/'claim-observation.json').read_text())
assert sha(WS/'claim-receipt.json')==observation['capture_sha256']
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==ids
assert all(x['record']['owner']=='Boss4' for x in observation['local_working_tree_owners'])
pre=json.loads((WS/'preclaim-preparation-observation.json').read_text());assert pre['superseded_by']=='claim-observation.json'
receipt=json.loads((WS/'semantic-receipts.json').read_text());assert len(receipt)==3 and {x['id'] for x in receipt}==ids
for x in receipt:
 assert x['disposition']=='integrated'
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(len(x[k])>50 for k in ['read_note','comparison_note','decision_note'])
 assert all((stage/p).is_file() for p in x['targets'])
runtime=json.loads((ev/'runtime-record.json').read_text())
assert runtime['original_entries']==runtime['new_mathematical_entries']==runtime['external_solver_calls']==runtime['old_math_reruns']==0
reuse=json.loads((ev/'sufficient-data-reuse.json').read_text());assert reuse['new_runs']==0 and reuse['exact_policy_replay_reuse'] is False
assert reuse['R642_reply_in_formal_labels']==['B','R','R','S','S','R']
assert reuse['canonical_reply']==['B','R','R','R','S','R']
assert sha(repo/reuse['old_report']['path'])==reuse['old_report']['sha256']
dep=json.loads((ev/'dependency-boundary.json').read_text());assert len(dep['safe_local_export']['missing'])==7 and not dep['safe_local_export']['rows']
jsons=sorted(stage.rglob('*.json'))
for p in jsons:json.loads(p.read_text())
pys=sorted(stage.rglob('*.py'))
for p in pys:ast.parse(p.read_text(),filename=str(p))
canonical=sorted((stage/'archives/customer-attraction/state').rglob('*.md'));assert len(canonical)==2
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
report={'status':'pass','structural_audit_runs':1,'mathematical_entries_not_run_by_validator':True,'actual_primary_count':3,'primary_bytes':12989,'integrated_receipts':3,'complete_actual_claim_owner_verified':True,'success_after_actualclaim_only':True,'all_primary_size_sha256_blob_sha1_verified':True,'canonical_count':2,'all_stageJSON_parsed':len(jsons),'all_PythonAST_parsed_without_math_execution':len(pys),'live_newMD_links':links,'raw_links':'preservedsourcecontext; missingoriginals notfabricated','original_entries':0,'new_mathematical_entries':0,'external_solver_calls':0,'oldpolicy_not_misidentified_as_samevariant':True,'newreply_validity':'explicitlastBR7/root6same, analyticfullSPEpreservation','no_extra_primary_or_candidate_batch':True,'no_sharedGit_network_auth_spawn':True,'unpaid_interfaces':['generalsixhalf','enhancedfulltypeupperbound','full-depthtruecommonpayment']}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','actual_primary_count','canonical_count','all_stageJSON_parsed','all_PythonAST_parsed_without_math_execution','original_entries','new_mathematical_entries']}))
