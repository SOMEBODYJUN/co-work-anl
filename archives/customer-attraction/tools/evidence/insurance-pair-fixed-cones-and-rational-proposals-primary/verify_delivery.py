"""Integrity and literal report transcription only; no Fraction/solver/LP/IC or original source execution."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-insurance-pair-fixed-cones-and-rational-proposals-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(E/'actual-source-manifest.json');rows=manifest['rows'];ids={x['id'] for x in rows}
assert len(rows)==3 and sum(x['size'] for x in rows)==4129
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==11 and ids<=set(claim['ids'])
assert claim['remote_tip']=='251ed6c535d46be83f3f15ae8c1f6348dec89bdb' and claim['local_sync']['status']=='synced'
assert manifest['raw_original_local_sync']==claim['local_sync']
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True and x['new_normal_show'] is True
 owner=read(E/'local-progress-at-read'/(x['id']+'.json'))
 assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
 cap=read(E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 assert cap['source']=={k:x[k] for k in ('blob','id','mode','path','sha256','size','sources')} and cap['output']==x['local_path']
com=read(E/'formal-comparison.json');assert len(com)==5
for x in com:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
md=read(E/'related-MD-manifest.json');assert len(md)==1
for x in md:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and p.read_bytes()==Path(x['actual_read_from']).read_bytes() and x['full_file_reviewed'] is True
 assert x['new_primary'] is False and x['new_done'] is False
deps=read(E/'related-runtime-source-manifest.json');assert len(deps)==6 and {x['path'] for x in deps}=={'customer_attraction/model.py','customer_attraction/exact.py','customer_attraction/certificate.py','customer_attraction/__init__.py','examples/customer_attraction/root_tax_failure.json','examples/customer_attraction/eight_cce_welfare_gap.json'}
assert sum(x['size'] for x in deps)==27024
for x in deps:
 p=S/x['snapshot'];b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['actual_read_from']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True
 assert x['new_primary'] is False and x['new_done'] is False
receipts=read(W/'semantic-receipts.json');assert len(receipts)==3 and {x['id'] for x in receipts}==ids
for x in receipts:
 assert x['disposition']=='retained' and all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
sc=read(E/'execution-and-domain-boundaries.json')
assert all(sc[k]==0 for k in ('current_original_entry_runs','current_imports','current_solver_runs','current_certificate_generation','current_LP_runs','current_IC_replays','current_parameter_scans','new_mathematical_implementation_runs'))
assert sc['historical_execution_manifest_present'] is False and sc['dual_optimality_certificate_present'] is False and sc['full_policy_maps_present_in_reports'] is False
assert sc['all_report_fields_transcribed'] is True and not (E/'runs').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
page=math[0].read_text();stored=read(E/'stored-reports-literal-transcription.json')
actual={x['id']:read(S/x['stage_path']) for x in rows[1:]};assert stored==actual
assert sum(len(r['weights']) for r in actual.values())==13
for x in rows[1:]:
 r=actual[x['id']];assert set(r)==set(sc['report_keys'])
 for k in ('float_objective','exact_objective','min_exact_ic','source'):assert str(r[k]) in page
 for k in ('high_path','low_path','comparison'):assert ','.join(map(str,r[k])) in page
 pcount=6 if r['source']=='root_tax_failure' else 4
 for mask,w in r['weights'].items():
  bitstring=','.join(str(i) for i in range(pcount) if int(mask)>>i&1)
  assert f"|{r['source']}|{mask}|{bitstring}|{w}|" in page
assert actual['cba82764e1c24456332c']['exact_objective']=='-1/5' and actual['de3c477c8761be7fba26']['exact_objective']=='-1/23'
# Data structure checks only, not regenerated strategies or mathematical feasibility.
inputs={x['path']:read(S/x['snapshot']) for x in deps if x['path'].endswith('.json')}
assert inputs['examples/customer_attraction/root_tax_failure.json']['players']==4
assert inputs['examples/customer_attraction/eight_cce_welfare_gap.json']['players']==3
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():assert (R/str(q.relative_to(S))).is_file(),(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result=dict(status='PASS',scope='primary/hash/blob/normal metadata/owner/claim, dependency source bytes, comparison snapshots, all literal reports/weights, receipts and links only; no mathematical evaluation',primary_files=3,primary_bytes=4129,new_normal_show_files=3,retained=3,duplicate=0,formal_math_files=1,comparison_snapshots=5,related_MD_files=1,related_runtime_sources=6,related_runtime_bytes=27024,report_files=2,report_fields_each=8,nonzero_weights_records=13,relations=8,source_state_updates=0,original_entry_runs=0,imports=0,solver_runs=0,certificate_generation=0,LP_runs=0,IC_replays=0,parameter_scans=0,new_mathematical_implementation_runs=0,links_checked=links)
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
