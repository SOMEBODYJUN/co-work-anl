"""Structural delivery/record check only; never runs the original math entry."""
from pathlib import Path
import json,hashlib,re,ast
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-seven-maxima-full-floor-route-obstruction-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==6812
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==4 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='5977796d3f7045df737a82c08daa0ba57c92c671'
for row in rows:
 p=S/row['stage_path'];b=p.read_bytes()
 assert len(b)==row['size'] and sha(p)==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
 assert Path(row['local_path']).read_bytes()==b
 pp=read(E/'local-progress-at-read'/(row['id']+'.json'))
 assert pp['owner']=='Boss4' and pp['source_sha256']==row['sha256']
 assert (E/'normal-show-captures'/Path(row['actual_normal_show_capture']).name).is_file()
rr=read(W/'semantic-receipts.json');assert len(rr)==2 and {x['id'] for x in rr}==ids
for x in rr:
 assert x['disposition']=='retained'
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
comp=read(E/'formal-comparison.json');assert len(comp)==5
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed']
run=E/'runs/one-original-main';meta=read(run/'run.json')
assert meta['exit_code']==0 and meta['original_main_entries']==1 and meta['direct_cli'] is False
assert meta['argv'][1:3]==['-I','-B'] and meta['stdin']=='DEVNULL'
assert meta['before']==meta['after'] and meta['original_sources_unchanged']
for p,fp in meta['after'].items():
 q=Path(p);assert q.stat().st_size==fp['bytes'] and sha(q)==fp['sha256']
assert (run/'stdout.txt').stat().st_size==meta['stdout_bytes']==257
assert (run/'stderr.txt').stat().st_size==meta['stderr_bytes']==0
assert sha(run/'audit_full_max_floor_obstruction.py')=='b092ff8fc66eda8d579a357b193e89e38208c8f0fb42111c852fdbc8f1e17c1d'
for x in meta['outputs']:
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
stdout=ast.literal_eval((run/'stdout.txt').read_text());assert stdout==meta['summary']
assert stdout['rows']==83 and stdout['columns_in_support']==18 and stdout['minimum_row_average']=='0' and stdout['target_average']=='-42280/9125787'
c=read(run/'captured-original-main-locals.json')
assert c['original_main_return_events']==1 and c['row_count']==83 and len(c['averages'])==83
assert len(c['support'])==18 and len(c['pairs'])==28 and c['objective']==stdout['target_average']
assert all(re.fullmatch(r'\d+(?:/\d+)?',x) for x in c['averages'])
assert c['averages'][48]=='82043/42587006'
scope=read(E/'execution-and-comparison-scope.json')
assert scope['original_main_entries']==1 and scope['direct_cli_entries']==0
assert all(scope[k]==0 for k in ('new_mathematical_implementation_runs','solver_runs','SPE_search_runs','old_five_route_replays'))
assert len(read(W/'relation-evidence.json'))==6 and read(W/'source-state-updates.json')==[]
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
formal=math[0].read_text()
assert '<!--' not in formal and '-{799778' in formal
assert all(value in formal for value in c['averages'])
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.exists():assert (R/q.relative_to(S)).is_file(),(str(p),target)
  links+=1
for x in read(E/'content-manifest.json'):
 p=S/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
copy=W/'copy-files.json'
if copy.exists():assert read(copy)==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result={'status':'PASS','scope':'structural, fingerprints, captured prior original-main fields, links; no math entry execution','primary_files':2,'primary_bytes':6812,'receipts':2,'retained':2,'duplicates':0,'formal_math_files':1,'comparison_snapshots':5,'relations':6,'source_state_updates':0,'original_main_entries_recorded':1,'direct_cli_entries':0,'new_mathematical_implementation_runs':0,'original_row_averages_preserved':83,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
