"""Source/provenance and delivery checks only; no math module import or evaluation."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-residual-new-coverage-refund-and-background-security-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==4 and sum(x['size'] for x in rows)==12708
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==4 and ids==set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='e9fdad90273912439186b4abdce1507f8478c0a6'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True
 d=read(E/'local-progress-at-read'/(x['id']+'.json'));assert d['owner']=='Boss4' and d['source_sha256']==x['sha256']
 assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
comp=read(E/'formal-comparison.json');assert len(comp)==14
available={x['path'] for x in comp}
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
rr=read(W/'semantic-receipts.json');assert len(rr)==4 and {x['id'] for x in rr}==ids
assert sum(x['disposition']=='retained' for x in rr)==2 and sum(x['disposition']=='duplicate' for x in rr)==2
for x in rr:
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() or t in available for t in x['targets'])
scope=read(E/'execution-and-domain-boundaries.json')
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','current_LP_runs','current_RNG_replays','current_solver_runs','current_certificate_replays','new_mathematical_implementation_runs','current_parameter_scans'))
assert scope['historical_full_execution_manifest_or_stdout_present'] is False and scope['frozen_negative_JSON_report_present'] is False
assert not (E/'runs').exists() and read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==11
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==2
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.is_file():
   rel=str(q.relative_to(S));assert (R/rel).is_file() or rel in available,(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
p=W/'copy-files.json'
if p.exists():assert read(p)==sorted(str(q.relative_to(S)) for q in S.rglob('*') if q.is_file())
result={'status':'PASS','scope':'source hashes/blob, actual complete claim/owner, full-read comparison snapshots, receipt/relations and links only; no mathematical computation or replay','primary_files':4,'primary_bytes':12708,'receipts':4,'retained':2,'duplicate':2,'formal_math_files':2,'comparison_snapshots':14,'relations':11,'source_state_updates':0,'original_entry_runs':0,'imports':0,'LP_runs':0,'RNG_replays':0,'solver_runs':0,'certificate_replays':0,'new_mathematical_implementation_runs':0,'parameter_scans':0,'historical_report_fabrications':0,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
