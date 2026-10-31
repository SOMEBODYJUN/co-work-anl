"""Local structural/identity check. Does not execute the three mathematical programs."""
from pathlib import Path
import ast,hashlib,json,re,sys
stage=Path(__file__).resolve().parents[4]
repo=stage.parent.parent/'boss4-research'
ev=Path('archives/unrelated-machines/tools/evidence/cyclic-resource-distortion')
ws=Path('cleanup/workspaces/Boss4/r3-cyclic-resource-distortion')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(ev/'manifest.json'); checked=[]
for group in ['originals','comparisons','dependencies','historical_replay_records']:
 for r in m[group]:
  p=stage/r['evidence_path'];assert p.stat().st_size==r['size'];assert sha(p)==r['sha256'];checked.append(r['evidence_path'])
for r in read(ev/'related-formal-material.json'):
 assert sha(repo/r['repository_path'])==r['sha256']
 if 'snapshot_path' in r:assert sha(stage/r['snapshot_path'])==r['sha256']
for p in stage.rglob('*.json'):json.loads(p.read_text())
for r in m['originals']:
 if r['path'].endswith('.py'):ast.parse((stage/r['evidence_path']).read_text())
cy=read(ev/'comparisons/cyclic_batch_repair_audit.json');rf=read(ev/'comparisons/resource_distortion_flat_menu_audit.json');ri=read(ev/'comparisons/resource_distortion_independent_audit.json');old=read(ev/'historical-replay-records/replay-results.json')
assert cy['source_sha256']==m['originals'][1]['sha256'];assert cy['actual_padded_fork_optimizer']['input_sha256']==m['dependencies'][0]['sha256']
assert (cy['explicit_menu_comparisons'],cy['random_optimizer_cases'],cy['boundary_cases'],cy['invalid_cases'])==(720,86,3,6)
assert 'exit_code' not in cy
assert rf['source_sha256']==m['originals'][3]['sha256']==old['legacy_resource_flat_menu_replay_for_comparison']['source_sha256'];assert rf['cases']==945
assert ri['script_sha256']==m['originals'][4]['sha256']==old['resource_independent_audit']['script_sha256']
assert ri['counts']==old['resource_independent_audit']['counts']=={'instances':1301,'original_schedules':1328275,'santa_allocations':20798}
assert ri['approximate_allocations_decoded']==old['resource_independent_audit']['approximate_allocations_decoded']=={'41/10':10770,'7':10770}
assert old['resource_independent_audit']['exit_code']==old['legacy_resource_flat_menu_replay_for_comparison']['exit_code']==0
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==5;assert {r['id'] for r in receipts}=={r['id'] for r in m['originals']}
for r in receipts:
 assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(r[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for p in r['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
broken=[];newmd=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in newmd:
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',dest):continue
  target=dest.split('#',1)[0];local=(p.parent/target).resolve()
  try:rel=local.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),dest]);continue
  if not local.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),dest])
assert not broken,broken
findings=read(ev/'comparison-findings.json')
c2=findings['findings'][0]
assert c2['exact_old_text'] in (stage/c2['existing_page']['snapshot_path']).read_text()
assert read(ev/'historical-run-reuse.json')['new_mathematical_program_runs']==0
report={'status':'passed','checks':['all 5 primary originals, 5 comparison originals, 2 actual dependencies and 2 old replay records byte/hash checked','8 existing formal comparison objects remain unchanged; 2 complete snapshots match','all JSON parses; original three Python programs AST-parse only, no mathematical execution','cyclic exact code/fixture hashes and finite fields match old historical run witness; no old exit_code invented','two resource program hashes and all historical replay count fields match, both old exit0 explicit','5 semantic receipts complete and targets present','5 new formal objects and all new explanatory Markdown links resolve against stage plus existing repository','old C2 actual quote preserved; only minimal suggestion, existing pages untouched','new primary program executions=0; no network, Git, claim, done, or spawn'], 'primary_ids':[r['id'] for r in m['originals']], 'new_formal_objects':len(list((stage/'archives/unrelated-machines/state').rglob('*.md'))),'new_mathematical_program_runs':0,'identity_checked_paths':checked,'copied_files':[]}
# Exact inventory includes its own copy list and this validation file; SHA manifest omits only itself.
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p.name!='copy-files.json')+[str(ws/'copy-files.json')]
files=sorted(files);(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
report['copied_files']=files
report['file_count']=len(files)
report['file_identities_excluding_self']=[{'path':s,'size':(stage/s).stat().st_size,'sha256':sha(stage/s)} for s in files if s!=str(ws/'validation.json')]
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}
print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'primary_sources':5,'new_formal_objects':report['new_formal_objects'],'new_mathematical_program_runs':0},ensure_ascii=False))
