"""Structural source/provenance/link checks only; imports no mathematical code."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-terminal-amount-cap-and-audit-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(p,row):
 b=p.read_bytes();assert len(b)==row['size'] and sha(p)==row['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==2 and sum(x['size'] for x in rows)==9700
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==6 and ids<=set(claim['ids'])
assert claim['remote_tip']=='cb753bdeca667ca9f908cf99dff5a6e99b0bdc24'
assert claim['local_sync']['status']=='needs-attention' and man['raw_original_local_sync']['status']=='needs-attention'
proof=read(E/'claim-sync-preservation-independent-proof.json')
assert proof['receipt']=='boss4-resume-next6sc-claim' and proof['stash']=='363773c81987c4c2842d52866176ab5667631691'
assert proof['untracked_count']==2 and proof['missing']==proof['different']==[]
assert len(proof['tracked'])==2 and all(x['same'] is True for x in proof['tracked'])
assert proof['unmerged']=='' and proof['stash_kept'] is True
for row in rows:
 p=S/row['stage_path'];verify(p,row);assert Path(row['local_path']).read_bytes()==p.read_bytes()
 progress=read(E/'local-progress-at-read'/(row['id']+'.json'))
 assert progress['owner']=='Boss4' and progress['source_sha256']==row['sha256']
 assert (E/'normal-show-captures'/Path(row['actual_normal_show_capture']).name).is_file()
related=read(E/'required-related-manifest.json');assert len(related)==1
row=related[0];assert row['id']=='44ac5a996de190a8da48' and row['size']==6880
assert row['primary'] is False and row['new_receipt'] is False and row['new_done'] is False
verify(S/row['stage_path'],row);assert (S/row['stage_path']).read_bytes()==Path(row['local_path']).read_bytes()
assert row['sha256']=='8a9519bb7e9682adafbbdca3cb622fe8212607c17f2905c8a92513a2c8e19c67'
rr=read(W/'semantic-receipts.json');assert len(rr)==2 and {x['id'] for x in rr}==ids
for x in rr:
 assert x['disposition']=='retained'
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
comp=read(E/'formal-comparison.json');assert len(comp)==3
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed']
scope=read(E/'execution-and-source-boundaries.json')
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','new_mathematical_implementation_runs','new_solver_runs','new_SPE_scan_runs'))
assert scope['historical_output_not_acquired']['id']=='34c68a75254ba1675fc7'
assert not list(S.rglob('amount_cap_existing.json')) and not (E/'runs').exists()
assert len(read(W/'relation-evidence.json'))==6 and read(W/'source-state-updates.json')==[]
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==2
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
result={'status':'PASS','scope':'source fingerprints, raw needs-attention claim plus independent preservation proof, receipts, comparisons, links and manifest only; no math run','primary_files':2,'primary_bytes':9700,'required_related_files':1,'required_related_bytes':6880,'receipts':2,'retained':2,'duplicates':0,'formal_math_files':2,'comparison_snapshots':3,'relations':6,'source_state_updates':0,'original_entry_runs':0,'imports':0,'new_mathematical_implementation_runs':0,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
