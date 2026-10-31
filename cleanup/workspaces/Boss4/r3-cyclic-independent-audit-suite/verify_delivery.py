"""Identity, frozen-record structure and delivery validation; no original audit main is run."""
from pathlib import Path
import ast,hashlib,json,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/cyclic-independent-audit-suite');ws=Path('cleanup/workspaces/Boss4/r3-cyclic-independent-audit-suite')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(ev/'manifest.json');allentries=m['originals']+m['comparisons'];by={x['id']:x for x in allentries}
for r in allentries:
 p=stage/r['evidence_path'];assert p.stat().st_size==r['size'];assert sha(p)==r['sha256']
 if p.suffix=='.py':ast.parse(p.read_text())
for p in stage.rglob('*.json'):json.loads(p.read_text())
for r in read(ev/'related-formal-material.json'):assert sha(repo/r['path'])==r['sha256']
bind=read(ev/'run-binding.json');assert bind['new_original_program_runs']==0
for r in bind['bindings']:
 a=read(r['frozen_record_path']);assert a['source_sha256']==r['primary_sha256'];assert r['historical_exit_code'] is None and not r['new_run_performed']
cy=read(by['be4729e9171c5d987eba']['evidence_path']);assert cy['reviewed_source_sha256']==by['84632fae4a437ba5f4cd']['sha256'];assert cy['independent_frozen_menu_comparisons']==9000 and cy['positive_comparisons']==3032
assert [r['positive_comparisons'] for r in cy['per_machine_count']]==[340,1008,1684]
mi=read(by['b675256af1948262aa9a']['evidence_path']);assert mi['explicit_menu_equivalence']['random_explicit_menus']==3000 and mi['explicit_menu_equivalence']['menus_with_strict_machine_simple_cycle']==1028
pad=read(by['3e853e2f77d938aaf6cc']['evidence_path']);assert len(pad['cases'])==63;count=0
for k,r in zip(range(2,65),pad['cases']):
 assert (r['pads'],r['machines'],r['jobs'])==(8*k,8*k+3,8*k+6)
 z=r['explicit_job_to_slot_injection'];assert len(z)==r['jobs'];assert [x[0] for x in z]==list(range(r['jobs']));assert len({tuple(x[1:]) for x in z})==len(z);count+=len(z)
assert count==17010
con=pad['cases'][0]['concrete_instance'];i=read(by['c5a89ad13c28b4244ab2']['evidence_path']);c=read(by['6dd7e1109bd9fa0671e8']['evidence_path']);assert all(con[k]==v for k,v in i.items());assert all(con[k]==v for k,v in c.items() if k not in ['input_file','claim','explicit_job_to_slot_injection']);assert c['explicit_job_to_slot_injection']==pad['cases'][0]['explicit_job_to_slot_injection']
batch=read(by['aab22aac4dec0c04d05d']['evidence_path']);assert 'status' not in batch
for r in batch['fanout']:
 k=r['k'];g=r['integer_gray'];assert g['assignments']==2**(4*k+2) and g['min_lex_distance']==k+1 and g['min_makespan_distance']==k+3
 assert {a:b for a,b in r['compressed'].items() if a!='compressed_types'}==g
 if k<=3:assert r['independent_fraction']==g
for r in batch['compressed_large']:
 k=r['k'];assert r['compressed']['assignments']==2**(4*k+2) and r['compressed']['compressed_types']==4*(2*k+1)**2
ident=read(by['69ee0bf3ef1f323dad3d']['evidence_path']);d=ident['dependencies_sha256'];assert d['tests/audits/unrelated_machines/rounding_and_gap.py']==by['e57947bc795251d373c3']['sha256'];assert d['tests/audits/unrelated_machines/cyclic_batch_repair.py']==by['84632fae4a437ba5f4cd']['sha256']
assert d['research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md']=='8bbc487e1d4d4f69a0755e92e7f1f803217d63dd52b774a3a6f4eb42a7847f9c'!=by['7ff5e8374a6b9826845c']['sha256']
assert sum(r['independent_assignments'] for r in ident['cases'])==19699 and all(r['optimizer_iterations']==0 for r in ident['cases'])
find=read(ev/'comparison-findings.json')['metadata_erratum_suggestion'];assert sha(repo/find['old_manifest_path'])==find['old_manifest_sha256']==sha(stage/find['snapshot']);om=read(find['snapshot']);rr=next(x for x in om['source_refs'] if x['id']==find['record_id']);assert rr['sha256']==find['old_record_sha256_field']!=find['actual_frozen_json_sha256']
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==5 and {r['id'] for r in receipts}=={r['id'] for r in m['originals']}
for r in receipts:
 assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(r[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for p in r['targets']:assert (stage/p).is_file() or (repo/p).is_file()
broken=[];md=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in md:
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',dest):continue
  local=(p.parent/dest.split('#',1)[0]).resolve()
  try:rel=local.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),dest]);continue
  if not local.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),dest])
assert not broken,broken
report={'status':'passed','primary_sources':5,'new_formal_objects':3,'new_original_program_runs':0,'checks':['17 original/comparison/dependency records size and SHA match inventory','All copied JSON parses; all Python originals AST parse without execution','5 old run bindings source hashes match; old exit codes unknown, no invented status for batch','cyclic frozen dependency SHA and all counts match','complete padding 63 records/17010 injection entries checked; k2 full concrete fields match both original split fixtures','support Fraction/Gray/compressed frozen fields agree where actually executed; large types distinguished from weighted count','identical-work executable dependency SHA matches and proof document mismatch explicitly preserved','5 receipt target coverage complete','new Markdown links resolve','all 5 existing related formal pages and old metadata snapshot remain unchanged'], 'old_document_hash_mismatch_is_expected':True}
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=sorted({str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}|{str(ws/'copy-files.json')});(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
report['file_count']=len(files);report['file_identities_excluding_self']=[{'path':p,'size':(stage/p).stat().st_size,'sha256':sha(stage/p)} for p in files if p!=str(ws/'validation.json')]
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}
print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'new_original_program_runs':0,'new_formal_objects':3},ensure_ascii=False))
