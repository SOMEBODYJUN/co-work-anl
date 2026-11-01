"""Source, claim, reading reuse and packaging only; no mathematical execution."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-general-ledger-and-deep-amount-source-closure-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==5 and sum(x['size'] for x in rows)==18218
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==21 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='e1384b14ee2d5360eb844c29a19d4cf538e64080'
for x in rows:
 p=S/x['stage_path'];b=p.read_bytes()
 assert len(b)==x['size'] and sha(p)==x['sha256'] and b==Path(x['local_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and x['full_file_reviewed'] is True
 assert p.suffix=='.md'
 d=read(E/'local-progress-at-read'/(x['id']+'.json'));assert d['owner']=='Boss4' and d['source_sha256']==x['sha256']
 assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
reuse=read(E/'prior-related-complete-reading-reused.json');assert len(reuse)==2
assert {x['id'] for x in reuse}=={'49d812c22c050d9a42b7','22b85da39da11d287947'}
for x in reuse:
 row=next(z for z in rows if z['id']==x['id']);p=Path(x['prior_full_read_snapshot'])
 assert p.stat().st_size==x['bytes']==row['size'] and sha(p)==x['sha256']==row['sha256']
 assert p.read_bytes()==(S/row['stage_path']).read_bytes()
 assert all(x[k] is True for k in ('complete_reading_reused','current_normal_show_is_new','no_prior_primary_done_claimed'))
comp=read(E/'formal-comparison.json');assert len(comp)==11;available={x['path'] for x in comp}
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed'] is True
rr=read(W/'semantic-receipts.json');assert len(rr)==5 and {x['id'] for x in rr}==ids
assert sum(x['disposition']=='retained' for x in rr)==1 and sum(x['disposition']=='duplicate' for x in rr)==4
for x in rr:
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() or t in available for t in x['targets'])
scope=read(E/'execution-and-domain-boundaries.json')
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','current_LP_runs','current_RNG_replays','current_solver_or_IC_replays','new_mathematical_implementation_runs','current_parameter_scans','current_web_requests'))
assert scope['current_new_normal_show_files']==5 and scope['complete_prior_related_readings_reused']==2
assert scope['old33802_report_not_read_or_replayed_in_this_scope'] is True and not (E/'runs').exists()
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
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
result={'status':'PASS','scope':'raw full transaction/owner/source hashes/blob, two prior full-reading byte identities, snapshots/receipts/links only; no mathematical program or scan','primary_files':5,'primary_bytes':18218,'new_normal_show_files':5,'prior_complete_related_readings_reused':2,'receipts':5,'retained':1,'duplicate':4,'formal_math_files':1,'comparison_snapshots':11,'relations':8,'source_state_updates':0,'original_entry_runs':0,'imports':0,'LP_runs':0,'RNG_replays':0,'solver_or_IC_replays':0,'new_mathematical_implementation_runs':0,'parameter_scans':0,'web_requests':0,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
