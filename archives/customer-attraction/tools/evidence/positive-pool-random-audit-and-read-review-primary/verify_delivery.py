"""Source/report/provenance/overlap packaging check only; no RNG or math module execution."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-positive-pool-random-audit-and-read-review-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
man=read(E/'actual-source-manifest.json');rows=man['rows'];ids={x['id'] for x in rows}
assert len(rows)==3 and sum(x['size'] for x in rows)==5466
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==6 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='5e23cd12d98c1b09dc35e1073fc82561e5cd5d8e'
for row in rows:
 p=S/row['stage_path'];b=p.read_bytes()
 assert len(b)==row['size'] and sha(p)==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
 assert Path(row['local_path']).read_bytes()==b
 progress=read(E/'local-progress-at-read'/(row['id']+'.json'))
 assert progress['owner']=='Boss4' and progress['source_sha256']==row['sha256']
 assert (E/'normal-show-captures'/Path(row['actual_normal_show_capture']).name).is_file()
report=read(S/next(x['stage_path'] for x in rows if x['id']=='cd7aeff7e276b39a59d4'))
assert report=={'status':'PASS','random_legal_leaf_instances':1800,'exact_arithmetic':'Fraction','local_sharpness_r':24,'scope':'definition-level finite verification; proof remains in markdown'}
code=(S/next(x['stage_path'] for x in rows if x['id']=='bbb9940d07f02b457779')).read_text()
assert 'Random(20261024)' in code and '__name__' not in code
rr=read(W/'semantic-receipts.json');assert len(rr)==3 and {x['id'] for x in rr}==ids
assert sum(x['disposition']=='duplicate' for x in rr)==1 and sum(x['disposition']=='retained' for x in rr)==2
for x in rr:
 assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(x[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
comp=read(E/'formal-comparison.json');assert len(comp)==5
for x in comp:
 p=S/x['snapshot'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'] and x['full_file_reviewed']
collision=read(E/'remote-vs-parallel-draft-comparison.json')
oldids=set(collision['old_ids_excluded_from_current_receipts']);assert len(oldids)==3 and not ids&oldids
assert len(collision['actual_remote_formal_objects'])==2 and len(collision['parallel_unpublished_drafts'])==2
for x in collision['actual_local_done_progress_read']:
 d=read(S/x['snapshot']);assert d['disposition']!='in-progress' and d['source_sha256']==x['source_sha256'] and d['full_file_reviewed'] is True
scope=read(E/'execution-and-domain-boundaries.json')
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','new_mathematical_implementation_runs','current_RNG_replays','current_parent_SPE_scan_replays','remote_formal_overwrites'))
assert scope['parallel_old_formal_objects_not_published'] is True
assert set(scope['old_remote_completed_ids_not_receipted'])==oldids
assert not (E/'runs').exists()
assert len(read(W/'relation-evidence.json'))==6 and read(W/'source-state-updates.json')==[]
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
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
result={'status':'PASS','scope':'source hashes/report fields, raw claim/owner, overlap evidence, snapshots, receipts and links only; no RNG/math execution','primary_files':3,'primary_bytes':5466,'receipts':3,'duplicates':1,'retained':2,'formal_math_files':1,'comparison_snapshots':5,'relations':6,'old_remote_completed_ids_excluded':sorted(oldids),'parallel_formal_pages_not_published':2,'source_state_updates':0,'original_entries':0,'imports':0,'RNG_replays':0,'new_mathematical_implementation_runs':0,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
